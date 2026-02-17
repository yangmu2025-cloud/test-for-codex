import os
import pandas as pd
from typing import List
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from database.models import Paper


class ExcelExporter:
    """Exporter for Excel format."""

    def __init__(self, output_path: str):
        """
        Initialize Excel exporter.

        Args:
            output_path: Path to output Excel file
        """
        self.output_path = output_path

    def export(self, papers: List[Paper]):
        """
        Export papers to Excel file.

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
                'ID': paper.id,
                'Title': paper.title,
                'Authors': ', '.join([author.name for author in paper.authors]),
                'Abstract': paper.abstract,
                'Keywords': ', '.join([keyword.keyword for keyword in paper.keywords]),
                'Publish Date': paper.publish_date.strftime('%Y-%m-%d') if paper.publish_date else '',
                'Source': paper.source,
                'Source ID': paper.source_id,
                'PDF URL': paper.pdf_url,
                'PDF Path': paper.pdf_path,
                'Citation Count': paper.citation_count,
                'Created At': paper.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Create DataFrame
        df = pd.DataFrame(data)

        # Export to Excel with formatting
        with pd.ExcelWriter(self.output_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Papers')

            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Papers']

            # Format header
            for cell in worksheet[1]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center', vertical='center')

            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass

                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        print(f"Exported {len(papers)} papers to {self.output_path}")

    def export_csv(self, papers: List[Paper], csv_path: str):
        """
        Export papers to CSV file.

        Args:
            papers: List of Paper objects
            csv_path: Path to output CSV file
        """
        # Create output directory if not exists
        output_dir = os.path.dirname(csv_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Convert papers to list of dictionaries
        data = []
        for paper in papers:
            data.append({
                'ID': paper.id,
                'Title': paper.title,
                'Authors': ', '.join([author.name for author in paper.authors]),
                'Abstract': paper.abstract,
                'Keywords': ', '.join([keyword.keyword for keyword in paper.keywords]),
                'Publish Date': paper.publish_date.strftime('%Y-%m-%d') if paper.publish_date else '',
                'Source': paper.source,
                'Source ID': paper.source_id,
                'PDF URL': paper.pdf_url,
                'PDF Path': paper.pdf_path,
                'Citation Count': paper.citation_count,
                'Created At': paper.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Create DataFrame and export to CSV
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')

        print(f"Exported {len(papers)} papers to {csv_path}")
