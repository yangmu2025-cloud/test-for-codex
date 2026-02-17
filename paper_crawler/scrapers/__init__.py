"""Scraper modules for paper crawler."""

from .base_scraper import BaseScraper
from .arxiv_scraper import ArxivScraper
from .scholar_scraper import ScholarScraper
from .ieee_scraper import IEEEScraper

__all__ = ['BaseScraper', 'ArxivScraper', 'ScholarScraper', 'IEEEScraper']
