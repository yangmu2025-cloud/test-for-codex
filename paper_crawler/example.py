#!/usr/bin/env python3
"""
Example usage of the Paper Crawler.

This script demonstrates how to use the paper crawler programmatically.
"""

from utils import config, setup_logger
from database import DatabaseManager
from scrapers import ArxivScraper
from exporters import ExcelExporter, JSONExporter


def example_arxiv_search():
    """Example: Search arXiv for papers."""

    # Setup logger
    logger = setup_logger('example')

    # Initialize database
    db_url = config.get_database_url()
    db_manager = DatabaseManager(db_url)

    # Initialize arXiv scraper
    scraper = ArxivScraper(config.config, logger)

    # Search for papers
    title = "transformer neural network"
    logger.info(f"Searching for: {title}")
    papers = scraper.search_by_title(title)

    # Save to database
    session = db_manager.get_session()
    for paper_data in papers:
        db_manager.add_paper(session, paper_data)
    session.close()

    logger.info(f"Saved {len(papers)} papers to database")

    # Export to Excel
    session = db_manager.get_session()
    all_papers = db_manager.get_papers(session)
    session.close()

    excel_exporter = ExcelExporter('output/example_papers.xlsx')
    excel_exporter.export(all_papers)

    logger.info(f"Exported {len(all_papers)} papers to Excel")


def example_database_query():
    """Example: Query papers from database."""

    logger = setup_logger('example')

    # Initialize database
    db_url = config.get_database_url()
    db_manager = DatabaseManager(db_url)

    # Get all papers
    session = db_manager.get_session()
    all_papers = db_manager.get_papers(session)

    logger.info(f"Total papers in database: {len(all_papers)}")

    # Search by title
    search_results = db_manager.search_papers_by_title(session, 'transformer')
    logger.info(f"Papers with 'transformer' in title: {len(search_results)}")

    # Print first 5 papers
    for paper in all_papers[:5]:
        print(f"\nTitle: {paper.title}")
        print(f"Authors: {', '.join([a.name for a in paper.authors])}")
        print(f"Source: {paper.source}")
        print(f"Published: {paper.publish_date}")

    session.close()


if __name__ == '__main__':
    # Run example
    print("Example 1: Search arXiv and save to database")
    example_arxiv_search()

    print("\n" + "="*80 + "\n")

    print("Example 2: Query papers from database")
    example_database_query()
