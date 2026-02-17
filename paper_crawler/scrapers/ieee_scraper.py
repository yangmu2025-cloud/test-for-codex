import logging
import requests
from typing import List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper


class IEEEScraper(BaseScraper):
    """Scraper for IEEE Xplore papers."""

    def __init__(self, config: dict, logger: logging.Logger = None):
        """
        Initialize IEEE scraper.

        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        super().__init__(config)
        self.logger = logger or logging.getLogger(__name__)
        self.base_url = "https://ieeexplore.ieee.org"
        self.search_url = f"{self.base_url}/rest/search"

    def get_source_name(self) -> str:
        """Get source name."""
        return 'IEEE Xplore'

    def search_by_title(self, title: str) -> List[Dict[str, Any]]:
        """
        Search papers by title on IEEE Xplore.

        Args:
            title: Paper title to search

        Returns:
            List of paper data dictionaries
        """
        self.logger.info(f"Searching IEEE Xplore for: {title}")

        try:
            # Prepare search query
            params = {
                'queryText': title,
                'highlight': 'true',
                'returnFacets': ['ALL'],
                'returnType': 'SEARCH',
                'matchPubs': 'true',
                'rowsPerPage': min(self.max_results, 100)
            }

            headers = self.get_headers()
            headers['Content-Type'] = 'application/json'

            # Send search request
            response = requests.post(
                self.search_url,
                json=params,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code != 200:
                self.logger.error(f"IEEE search failed with status code: {response.status_code}")
                return []

            data = response.json()
            papers = []

            # Extract papers from response
            if 'records' in data:
                for record in data['records'][:self.max_results]:
                    try:
                        paper_data = self._extract_paper_data(record)
                        papers.append(paper_data)
                        self.logger.info(f"Found paper: {paper_data['title']}")
                        self.random_delay()
                    except Exception as e:
                        self.logger.error(f"Error extracting paper data: {e}")
                        continue

            self.logger.info(f"Found {len(papers)} papers on IEEE Xplore")
            return papers

        except Exception as e:
            self.logger.error(f"Error searching IEEE Xplore: {e}")
            return []

    def _extract_paper_data(self, record: dict) -> Dict[str, Any]:
        """
        Extract paper data from IEEE record.

        Args:
            record: IEEE search result record

        Returns:
            Paper data dictionary
        """
        # Extract authors
        authors = []
        if 'authors' in record:
            authors = [author.get('normalizedName', author.get('preferredName', ''))
                      for author in record['authors']]

        # Extract keywords
        keywords = []
        if 'indexTerms' in record:
            for key in ['IEEE Terms', 'Author Keywords', 'INSPEC Controlled Terms']:
                if key in record['indexTerms']:
                    keywords.extend([term.get('term', '') for term in record['indexTerms'][key]])

        # Extract publication date
        publish_date = None
        if 'publicationDate' in record:
            try:
                date_str = record['publicationDate']
                publish_date = datetime.strptime(date_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                # Try alternative format
                if 'publicationYear' in record:
                    try:
                        year = int(record['publicationYear'])
                        publish_date = datetime(year, 1, 1)
                    except (ValueError, TypeError):
                        pass

        # Get PDF URL
        pdf_url = ''
        if 'pdfUrl' in record:
            pdf_url = self.base_url + record['pdfUrl']

        # Get document number as source ID
        source_id = record.get('articleNumber', record.get('documentLink', ''))

        # Normalize data
        raw_data = {
            'title': record.get('articleTitle', ''),
            'authors': authors,
            'abstract': record.get('abstract', ''),
            'keywords': keywords,
            'publish_date': publish_date,
            'source_id': source_id,
            'pdf_url': pdf_url,
            'pdf_path': '',  # PDF download requires authentication
            'citation_count': record.get('citationCount', 0)
        }

        return self.normalize_paper_data(raw_data)
