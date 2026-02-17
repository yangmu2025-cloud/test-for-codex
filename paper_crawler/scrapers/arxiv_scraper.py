import arxiv
import os
import logging
from typing import List, Dict, Any
from datetime import datetime
from .base_scraper import BaseScraper


class ArxivScraper(BaseScraper):
    """Scraper for arXiv papers."""

    def __init__(self, config: dict, logger: logging.Logger = None):
        """
        Initialize arXiv scraper.

        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        super().__init__(config)
        self.logger = logger or logging.getLogger(__name__)
        self.pdf_dir = config.get('export', {}).get('pdf_dir', 'output/pdfs')

    def get_source_name(self) -> str:
        """Get source name."""
        return 'arXiv'

    def search_by_title(self, title: str) -> List[Dict[str, Any]]:
        """
        Search papers by title on arXiv.

        Args:
            title: Paper title to search

        Returns:
            List of paper data dictionaries
        """
        self.logger.info(f"Searching arXiv for: {title}")

        try:
            # Create search query - search in title and abstract for better coverage
            search = arxiv.Search(
                query=f'all:{title}',
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            papers = []
            for result in search.results():
                try:
                    paper_data = self._extract_paper_data(result)
                    papers.append(paper_data)
                    self.logger.info(f"Found paper: {paper_data['title']}")
                    self.random_delay()
                except Exception as e:
                    self.logger.error(f"Error extracting paper data: {e}")
                    continue

            self.logger.info(f"Found {len(papers)} papers on arXiv")
            return papers

        except Exception as e:
            self.logger.error(f"Error searching arXiv: {e}")
            return []

    def _extract_paper_data(self, result: arxiv.Result) -> Dict[str, Any]:
        """
        Extract paper data from arXiv result.

        Args:
            result: arXiv search result

        Returns:
            Paper data dictionary
        """
        # Extract authors
        authors = [author.name for author in result.authors]

        # Extract keywords (arXiv categories as keywords)
        keywords = result.categories

        # Download PDF if enabled
        pdf_path = ''
        if self.download_pdf:
            pdf_path = self._download_pdf(result)

        # Normalize data
        raw_data = {
            'title': result.title,
            'authors': authors,
            'abstract': result.summary,
            'keywords': keywords,
            'publish_date': result.published,
            'source_id': result.entry_id.split('/')[-1],
            'pdf_url': result.pdf_url,
            'pdf_path': pdf_path,
            'citation_count': 0  # arXiv doesn't provide citation count directly
        }

        return self.normalize_paper_data(raw_data)

    def _download_pdf(self, result: arxiv.Result) -> str:
        """
        Download PDF file.

        Args:
            result: arXiv search result

        Returns:
            Local PDF file path
        """
        try:
            # Create PDF directory if not exists
            if not os.path.exists(self.pdf_dir):
                os.makedirs(self.pdf_dir)

            # Generate filename
            source_id = result.entry_id.split('/')[-1]
            filename = f"arxiv_{source_id}.pdf"
            filepath = os.path.join(self.pdf_dir, filename)

            # Download PDF
            if not os.path.exists(filepath):
                self.logger.info(f"Downloading PDF: {filename}")
                result.download_pdf(dirpath=self.pdf_dir, filename=filename)
            else:
                self.logger.info(f"PDF already exists: {filename}")

            return filepath

        except Exception as e:
            self.logger.error(f"Error downloading PDF: {e}")
            return ''
