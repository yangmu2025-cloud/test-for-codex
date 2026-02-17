import os
import json
from typing import List
from database.models import Paper


class JSONExporter:
    """Exporter for JSON format."""

    def __init__(self, output_path: str):
        """
        Initialize JSON exporter.

        Args:
            output_path: Path to output JSON file
        """
        self.output_path = output_path

    def export(self, papers: List[Paper]):
        """
        Export papers to JSON file.

        Args:
            papers: List of Paper objects
        """
        # Create output directory if not exists
        output_dir = os.path.dirname(self.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Convert papers to list of dictionaries
        data = []
        for paper in papers:
            data.append({
                'id': paper.id,
                'title': paper.title,
                'authors': [
                    {
                        'name': author.name,
                        'affiliation': author.affiliation,
                        'email': author.email
                    }
                    for author in paper.authors
                ],
                'abstract': paper.abstract,
                'keywords': [keyword.keyword for keyword in paper.keywords],
                'publish_date': paper.publish_date.isoformat() if paper.publish_date else None,
                'source': paper.source,
                'source_id': paper.source_id,
                'pdf_url': paper.pdf_url,
                'pdf_path': paper.pdf_path,
                'citation_count': paper.citation_count,
                'created_at': paper.created_at.isoformat(),
                'updated_at': paper.updated_at.isoformat()
            })

        # Write to JSON file
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Exported {len(papers)} papers to {self.output_path}")
