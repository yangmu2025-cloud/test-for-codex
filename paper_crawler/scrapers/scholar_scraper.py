import logging
import os
from typing import List, Dict, Any
from datetime import datetime
from scholarly import scholarly, ProxyGenerator
from .base_scraper import BaseScraper


class ScholarScraper(BaseScraper):
    """Scraper for Google Scholar papers."""

    def __init__(self, config: dict, logger: logging.Logger = None):
        """
        Initialize Google Scholar scraper.

        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        super().__init__(config)
        self.logger = logger or logging.getLogger(__name__)
        self.pdf_dir = config.get('export', {}).get('pdf_dir', 'output/pdfs')

    def get_source_name(self) -> str:
        """Get source name."""
        return 'Google Scholar'

    def search_by_title(self, title: str) -> List[Dict[str, Any]]:
        """
        Search papers by title on Google Scholar.

        Args:
            title: Paper title to search

        Returns:
            List of paper data dictionaries
        """
        self.logger.info(f"Searching Google Scholar for: {title}")

        try:
            # Search for papers
            search_query = scholarly.search_pubs(title)

            papers = []
            count = 0

            for result in search_query:
                if count >= self.max_results:
                    break

                try:
                    # Fill in paper details
                    paper_filled = scholarly.fill(result)
                    paper_data = self._extract_paper_data(paper_filled)
                    papers.append(paper_data)
                    self.logger.info(f"Found paper: {paper_data['title']}")

                    count += 1
                    self.random_delay()

                except Exception as e:
                    self.logger.error(f"Error extracting paper data: {e}")
                    continue

            self.logger.info(f"Found {len(papers)} papers on Google Scholar")
            return papers

        except Exception as e:
            self.logger.error(f"Error searching Google Scholar: {e}")
            return []

    def _extract_paper_data(self, result: dict) -> Dict[str, Any]:
        """
        Extract paper data from Google Scholar result.

        Args:
            result: Google Scholar search result

        Returns:
            Paper data dictionary
        """
        # Extract authors
        authors = []
        if 'author' in result.get('bib', {}):
            authors = [author for author in result['bib']['author']]

        # Extract keywords (not directly available in Google Scholar)
        keywords = []

        # Extract publication year and convert to datetime
        publish_date = None
        if 'pub_year' in result.get('bib', {}):
            try:
                year = int(result['bib']['pub_year'])
                publish_date = datetime(year, 1, 1)
            except (ValueError, TypeError):
                pass

        # Get PDF URL if available
        pdf_url = result.get('eprint_url', '')

        # Get citation count
        citation_count = result.get('num_citations', 0)

        # Normalize data
        raw_data = {
            'title': result.get('bib', {}).get('title', ''),
            'authors': authors,
            'abstract': result.get('bib', {}).get('abstract', ''),
            'keywords': keywords,
            'publish_date': publish_date,
            'source_id': result.get('pub_url', ''),
            'pdf_url': pdf_url,
            'pdf_path': '',  # PDF download not implemented for Google Scholar
            'citation_count': citation_count
        }

        return self.normalize_paper_data(raw_data)
