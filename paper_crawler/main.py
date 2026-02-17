#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Crawler - A tool for crawling academic papers from multiple sources.

Usage:
    python main.py --title "machine learning" --sources arxiv scholar ieee
    python main.py --title "deep learning" --sources all --export excel json
"""

import argparse
import sys
import os
from tqdm import tqdm

# Fix Windows encoding issue
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from utils import config, setup_logger
from database import DatabaseManager
from scrapers import ArxivScraper, ScholarScraper, IEEEScraper
from exporters import ExcelExporter, JSONExporter


def main():
    """Main entry point for paper crawler."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Paper Crawler - Crawl academic papers from multiple sources'
    )
    parser.add_argument(
        '--title',
        type=str,
        required=True,
        help='Paper title to search for'
    )
    parser.add_argument(
        '--sources',
        nargs='+',
        choices=['arxiv', 'scholar', 'ieee', 'all'],
        default=['all'],
        help='Sources to search (arxiv, scholar, ieee, or all)'
    )
    parser.add_argument(
        '--export',
        nargs='+',
        choices=['excel', 'json', 'csv'],
        default=['excel'],
        help='Export formats (excel, json, csv)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=None,
        help='Maximum number of results per source'
    )
    parser.add_argument(
        '--skip-pdf',
        action='store_true',
        help='Skip PDF download'
    )

    args = parser.parse_args()

    # Load configuration
    try:
        from utils.config import Config
        cfg = Config(args.config)
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {args.config}")
        sys.exit(1)

    # Setup logger
    log_file = cfg.get('logging.file', 'logs/crawler.log')
    log_level = cfg.get('logging.level', 'INFO')
    logger = setup_logger('paper_crawler', log_file, log_level)

    logger.info("=" * 80)
    logger.info("Starting Paper Crawler")
    logger.info(f"Search title: {args.title}")
    logger.info(f"Sources: {args.sources}")
    logger.info("=" * 80)

    # Initialize database
    try:
        db_url = cfg.get_database_url()
        db_manager = DatabaseManager(db_url)
        logger.info(f"Database initialized: {db_url}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)

    # Override max_results if specified
    if args.max_results:
        cfg.config['scraper']['max_results'] = args.max_results

    # Override download_pdf if skip-pdf is specified
    if args.skip_pdf:
        cfg.config['scraper']['download_pdf'] = False

    # Determine which sources to use
    sources = args.sources
    if 'all' in sources:
        sources = ['arxiv', 'scholar', 'ieee']

    # Initialize scrapers
    scrapers = []
    if 'arxiv' in sources:
        scrapers.append(('arXiv', ArxivScraper(cfg.config, logger)))
    if 'scholar' in sources:
        scrapers.append(('Google Scholar', ScholarScraper(cfg.config, logger)))
    if 'ieee' in sources:
        scrapers.append(('IEEE Xplore', IEEEScraper(cfg.config, logger)))

    # Crawl papers from each source
    all_papers = []
    for source_name, scraper in scrapers:
        logger.info(f"\n--- Searching {source_name} ---")
        print(f"\n🔍 Searching {source_name}...")

        try:
            papers = scraper.search_by_title(args.title)

            # Save to database
            session = db_manager.get_session()
            for paper_data in tqdm(papers, desc=f"Saving {source_name} papers"):
                try:
                    db_manager.add_paper(session, paper_data)
                except Exception as e:
                    logger.error(f"Error saving paper: {e}")

            session.close()

            logger.info(f"Successfully crawled {len(papers)} papers from {source_name}")
            print(f"✓ Found {len(papers)} papers from {source_name}")

        except Exception as e:
            logger.error(f"Error crawling {source_name}: {e}")
            print(f"✗ Error crawling {source_name}: {e}")

    # Get all papers from database
    session = db_manager.get_session()
    all_papers = db_manager.get_papers(session)
    session.close()

    total_count = len(all_papers)
    logger.info(f"\nTotal papers in database: {total_count}")
    print(f"\n📊 Total papers in database: {total_count}")

    # Export papers
    if total_count > 0:
        print(f"\n💾 Exporting papers...")

        if 'excel' in args.export:
            excel_path = cfg.get('export.excel_path', 'output/papers.xlsx')
            exporter = ExcelExporter(excel_path)
            exporter.export(all_papers)
            logger.info(f"Exported to Excel: {excel_path}")
            print(f"✓ Exported to Excel: {excel_path}")

        if 'csv' in args.export:
            csv_path = cfg.get('export.csv_path', 'output/papers.csv')
            exporter = ExcelExporter(csv_path)
            exporter.export_csv(all_papers, csv_path)
            logger.info(f"Exported to CSV: {csv_path}")
            print(f"✓ Exported to CSV: {csv_path}")

        if 'json' in args.export:
            json_path = cfg.get('export.json_path', 'output/papers.json')
            exporter = JSONExporter(json_path)
            exporter.export(all_papers)
            logger.info(f"Exported to JSON: {json_path}")
            print(f"✓ Exported to JSON: {json_path}")

    logger.info("\n" + "=" * 80)
    logger.info("Paper Crawler finished successfully")
    logger.info("=" * 80)
    print("\n✅ Crawling completed!")


if __name__ == '__main__':
    main()
