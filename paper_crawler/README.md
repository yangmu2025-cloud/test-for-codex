# Paper Crawler

A Python-based tool for crawling academic papers from multiple sources including arXiv, Google Scholar, and IEEE Xplore.

## Features

- **Multi-source Support**: Crawl papers from arXiv, Google Scholar, and IEEE Xplore
- **Title-based Search**: Search papers by title across multiple sources
- **Comprehensive Data Extraction**: Extract title, authors, abstract, keywords, PDF links, citation counts, and publication dates
- **Multiple Export Formats**: Export to Excel, JSON, CSV, and database (SQLite/MySQL/PostgreSQL)
- **PDF Download**: Automatically download PDF files (arXiv)
- **Anti-scraping Protection**: Built-in delays and user-agent rotation
- **Flexible Configuration**: YAML-based configuration file

## Installation

1. Clone or download this repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the tool by editing `config.yaml`

## Configuration

Edit `config.yaml` to customize:

- **Database**: Choose between SQLite, MySQL, or PostgreSQL
- **Export paths**: Set output file paths
- **Scraper settings**: Adjust delays, max results, PDF download, etc.
- **Logging**: Configure log level and file path

## Usage

### Basic Usage

Search for papers by title:

```bash
python main.py --title "machine learning"
```

### Specify Sources

Search specific sources:

```bash
# Search only arXiv
python main.py --title "deep learning" --sources arxiv

# Search arXiv and Google Scholar
python main.py --title "neural networks" --sources arxiv scholar

# Search all sources (default)
python main.py --title "artificial intelligence" --sources all
```

### Export Formats

Choose export formats:

```bash
# Export to Excel only
python main.py --title "computer vision" --export excel

# Export to multiple formats
python main.py --title "natural language processing" --export excel json csv
```

### Limit Results

Limit the number of results per source:

```bash
python main.py --title "machine learning" --max-results 20
```

### Custom Configuration

Use a custom configuration file:

```bash
python main.py --title "machine learning" --config my_config.yaml
```

## Command Line Arguments

- `--title`: **Required**. Paper title to search for
- `--sources`: Sources to search (arxiv, scholar, ieee, or all). Default: all
- `--export`: Export formats (excel, json, csv). Default: excel
- `--config`: Path to configuration file. Default: config.yaml
- `--max-results`: Maximum number of results per source

## Output

### Database

Papers are stored in a relational database with the following structure:

- **papers**: Paper information
- **authors**: Author information
- **keywords**: Keywords/tags
- **paper_authors**: Paper-author relationships
- **paper_keywords**: Paper-keyword relationships

### Export Files

By default, files are exported to the `output/` directory:

- `papers.xlsx`: Excel file with all papers
- `papers.json`: JSON file with structured data
- `papers.csv`: CSV file for data analysis
- `pdfs/`: Directory containing downloaded PDF files

## Project Structure

```
paper_crawler/
├── scrapers/           # Scraper implementations
│   ├── base_scraper.py
│   ├── arxiv_scraper.py
│   ├── scholar_scraper.py
│   └── ieee_scraper.py
├── database/           # Database models and manager
│   ├── models.py
│   └── db_manager.py
├── exporters/          # Export functionality
│   ├── excel_exporter.py
│   └── json_exporter.py
├── utils/              # Utility functions
│   ├── config.py
│   └── logger.py
├── main.py             # Main entry point
├── requirements.txt    # Python dependencies
├── config.yaml         # Configuration file
└── README.md           # This file
```

## Notes

### Google Scholar

- Google Scholar has anti-scraping measures
- The tool includes delays and user-agent rotation
- May require longer wait times between requests
- PDF downloads not supported (requires authentication)

### IEEE Xplore

- PDF downloads require authentication/subscription
- The tool extracts PDF URLs but doesn't download files
- Some papers may require IEEE membership to access

### arXiv

- Most reliable source with official API
- Supports PDF downloads
- No authentication required
- Recommended for open-access papers

## Troubleshooting

### Database Connection Error

- Check database configuration in `config.yaml`
- For SQLite: Ensure the directory exists
- For MySQL/PostgreSQL: Verify credentials and connection

### Scraper Timeout

- Increase timeout value in `config.yaml`
- Check internet connection
- Some sources may be temporarily unavailable

### PDF Download Failed

- Check disk space
- Verify PDF directory permissions
- arXiv is the only source that supports automatic PDF downloads

## License

This tool is for educational and research purposes only. Please respect the terms of service of the paper sources you crawl.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
