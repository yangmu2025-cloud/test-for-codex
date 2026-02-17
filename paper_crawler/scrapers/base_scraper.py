from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time
import random
from fake_useragent import UserAgent


class BaseScraper(ABC):
    """Base class for all paper scrapers."""

    def __init__(self, config: dict):
        """
        Initialize scraper.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.delay_min = config.get('scraper', {}).get('delay_min', 2)
        self.delay_max = config.get('scraper', {}).get('delay_max', 5)
        self.max_retries = config.get('scraper', {}).get('max_retries', 3)
        self.timeout = config.get('scraper', {}).get('timeout', 30)
        self.download_pdf = config.get('scraper', {}).get('download_pdf', True)
        self.max_results = config.get('scraper', {}).get('max_results', 50)
        self.ua = UserAgent()

    def random_delay(self):
        """Add random delay between requests to avoid rate limiting."""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)

    def get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers with random user agent.

        Returns:
            Headers dictionary
        """
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    @abstractmethod
    def search_by_title(self, title: str) -> List[Dict[str, Any]]:
        """
        Search papers by title.

        Args:
            title: Paper title to search

        Returns:
            List of paper data dictionaries
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the name of the paper source.

        Returns:
            Source name (e.g., 'arXiv', 'Google Scholar')
        """
        pass

    def normalize_paper_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize paper data to standard format.

        Args:
            raw_data: Raw paper data from source

        Returns:
            Normalized paper data dictionary
        """
        return {
            'title': raw_data.get('title', ''),
            'authors': raw_data.get('authors', []),
            'abstract': raw_data.get('abstract', ''),
            'keywords': raw_data.get('keywords', []),
            'publish_date': raw_data.get('publish_date'),
            'source': self.get_source_name(),
            'source_id': raw_data.get('source_id', ''),
            'pdf_url': raw_data.get('pdf_url', ''),
            'pdf_path': raw_data.get('pdf_path', ''),
            'citation_count': raw_data.get('citation_count', 0)
        }
