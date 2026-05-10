from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

# Association table for many-to-many relationship between books and authors
book_authors = Table(
    'book_authors',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True)
)

# Association table for many-to-many relationship between books and genres
book_genres = Table(
    'book_genres',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    isbn = Column(String(20), unique=True, index=True, nullable=True)
    publication_year = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    publisher = Column(String(100), nullable=True)
    pages = Column(Integer, nullable=True)
    
    # Relationships
    authors = relationship("Author", secondary=book_authors, back_populates="books")
    genres = relationship("Genre", secondary=book_genres, back_populates="books")
    copies = relationship("Copy", back_populates="book")

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    books = relationship("Book", secondary=book_authors, back_populates="authors")

class Genre(Base):
    __tablename__ = 'genres'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    books = relationship("Book", secondary=book_genres, back_populates="genres")