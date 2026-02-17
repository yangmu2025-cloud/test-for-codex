from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Paper(Base):
    """Paper model for storing paper information."""

    __tablename__ = 'papers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    abstract = Column(Text)
    publish_date = Column(DateTime)
    source = Column(String(50))  # arXiv, Google Scholar, IEEE
    source_id = Column(String(200))  # Original ID from source
    pdf_url = Column(String(500))
    pdf_path = Column(String(500))  # Local PDF file path
    citation_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    authors = relationship('Author', secondary='paper_authors', back_populates='papers')
    keywords = relationship('Keyword', secondary='paper_keywords', back_populates='papers')

    def __repr__(self):
        return f"<Paper(id={self.id}, title='{self.title[:50]}...')>"


class Author(Base):
    """Author model for storing author information."""

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    affiliation = Column(String(300))
    email = Column(String(200))

    # Relationships
    papers = relationship('Paper', secondary='paper_authors', back_populates='authors')

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"


class Keyword(Base):
    """Keyword model for storing keywords."""

    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(100), nullable=False, unique=True)

    # Relationships
    papers = relationship('Paper', secondary='paper_keywords', back_populates='keywords')

    def __repr__(self):
        return f"<Keyword(id={self.id}, keyword='{self.keyword}')>"


class PaperAuthor(Base):
    """Association table for Paper and Author many-to-many relationship."""

    __tablename__ = 'paper_authors'

    paper_id = Column(Integer, ForeignKey('papers.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), primary_key=True)
    author_order = Column(Integer)  # Order of author in paper


class PaperKeyword(Base):
    """Association table for Paper and Keyword many-to-many relationship."""

    __tablename__ = 'paper_keywords'

    paper_id = Column(Integer, ForeignKey('papers.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), primary_key=True)
