from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, joinedload
from .models import Base, Paper, Author, Keyword, PaperAuthor, PaperKeyword


class DatabaseManager:
    """Database manager for handling database operations."""

    def __init__(self, database_url: str):
        """
        Initialize database manager.

        Args:
            database_url: SQLAlchemy database URL
        """
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy session
        """
        return self.SessionLocal()

    def add_paper(self, session: Session, paper_data: dict) -> Paper:
        """
        Add a paper to the database.

        Args:
            session: Database session
            paper_data: Paper information dictionary

        Returns:
            Created Paper object
        """
        # Check if paper already exists
        existing_paper = session.query(Paper).filter_by(
            source=paper_data.get('source'),
            source_id=paper_data.get('source_id')
        ).first()

        if existing_paper:
            return existing_paper

        # Create paper
        paper = Paper(
            title=paper_data.get('title'),
            abstract=paper_data.get('abstract'),
            publish_date=paper_data.get('publish_date'),
            source=paper_data.get('source'),
            source_id=paper_data.get('source_id'),
            pdf_url=paper_data.get('pdf_url'),
            pdf_path=paper_data.get('pdf_path'),
            citation_count=paper_data.get('citation_count', 0)
        )

        # Add authors (avoid duplicates)
        for idx, author_name in enumerate(paper_data.get('authors', [])):
            author = session.query(Author).filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name)
                session.add(author)
                session.flush()  # Ensure author has an ID

            # Check if author is already associated with this paper
            if author not in paper.authors:
                paper.authors.append(author)

        # Add keywords (avoid duplicates)
        for keyword_text in paper_data.get('keywords', []):
            keyword = session.query(Keyword).filter_by(keyword=keyword_text).first()
            if not keyword:
                keyword = Keyword(keyword=keyword_text)
                session.add(keyword)
                session.flush()

            # Check if keyword is already associated with this paper
            if keyword not in paper.keywords:
                paper.keywords.append(keyword)

        session.add(paper)
        session.commit()
        session.refresh(paper)

        return paper

    def get_papers(self, session: Session, source: Optional[str] = None) -> List[Paper]:
        """
        Get papers from database with eager loading of relationships.

        Args:
            session: Database session
            source: Filter by source (optional)

        Returns:
            List of Paper objects
        """
        query = session.query(Paper).options(
            joinedload(Paper.authors),
            joinedload(Paper.keywords)
        )
        if source:
            query = query.filter_by(source=source)

        return query.all()

    def search_papers_by_title(self, session: Session, title: str) -> List[Paper]:
        """
        Search papers by title.

        Args:
            session: Database session
            title: Title to search for

        Returns:
            List of Paper objects
        """
        return session.query(Paper).filter(Paper.title.ilike(f'%{title}%')).all()

    def get_paper_count(self, session: Session) -> int:
        """
        Get total paper count.

        Args:
            session: Database session

        Returns:
            Total number of papers
        """
        return session.query(Paper).count()
