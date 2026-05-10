from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from typing import Optional, List
from app.modules.books.models import Book, Author, Genre, book_authors, book_genres
from app.modules.copies.models import Copy, CopyStatus
import re

def sanitize_search_query(query: str) -> str:
        # Удаляем управляющие символы (0x00-0x1F, 0x7F-0x9F)
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', query)
        # Экранируем символы `%` и `_`, чтобы не нарушить LIKE
        sanitized = sanitized.replace('%', '\\%').replace('_', '\\_')
        # Обрезаем до 200 символов
        return sanitized[:200]

class BookRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def sanitize_search_query(query: str) -> str:
        # Удаляем управляющие символы (0x00-0x1F, 0x7F-0x9F)
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', query)
        # Экранируем символы `%` и `_`, чтобы не нарушить LIKE
        sanitized = sanitized.replace('%', '\\%').replace('_', '\\_')
        # Обрезаем до 200 символов
        return sanitized[:200]
    
    # Book methods
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()
    
    def get_by_id_with_relations(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book)\
            .options(joinedload(Book.authors), joinedload(Book.genres))\
            .filter(Book.id == book_id)\
            .first()
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.db.query(Book).filter(Book.isbn == isbn).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return self.db.query(Book).offset(skip).limit(limit).all()
    
    def get_all_with_counts(self, skip: int = 0, limit: int = 100) -> List[Book]:
        return self.db.query(Book)\
            .options(joinedload(Book.authors), joinedload(Book.genres))\
            .offset(skip).limit(limit).all()
    
    def create(self, book_data: dict) -> Book:
        book = Book(**book_data)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def update(self, book_id: int, book_data: dict) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if book:
            for key, value in book_data.items():
                if value is not None:
                    setattr(book, key, value)
            self.db.commit()
            self.db.refresh(book)
        return book
    
    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
    
    def search(self, params: dict, skip: int = 0, limit: int = 100) -> List[Book]:
        query = self.db.query(Book).distinct()
        
        if params.get('title'):
            safe_q = sanitize_search_query(params['title'])
            search_term = f"%{safe_q}%"
            query = query.filter(Book.title.ilike(search_term))
        
        if params.get('isbn'):
            safe_q = sanitize_search_query(params['isbn'])
            search_term = f"%{safe_q}%"
            query = query.filter(Book.isbn.ilike(search_term))
        
        if params.get('year_from'):
            query = query.filter(Book.publication_year >= params['year_from'])
        
        if params.get('year_to'):
            query = query.filter(Book.publication_year <= params['year_to'])
        
        if params.get('author'):
            safe_q = sanitize_search_query(params['author'])
            search_term = f"%{safe_q}%"
            query = query.join(book_authors).join(Author).filter(
                or_(
                    Author.first_name.ilike(search_term),
                    Author.last_name.ilike(search_term)
                )
            )
        
        if params.get('genre'):
            safe_q = sanitize_search_query(params['genre'])
            search_term = f"%{safe_q}%"
            query = query.join(book_genres).join(Genre).filter(
                Genre.name.ilike(search_term)
            )
        
        return query.offset(skip).limit(limit).all()
    
    def get_available_copies_count(self, book_id: int) -> int:
        return self.db.query(Copy)\
            .filter(Copy.book_id == book_id)\
            .filter(Copy.status == CopyStatus.AVAILABLE)\
            .count()
    
    def get_total_copies_count(self, book_id: int) -> int:
        return self.db.query(Copy).filter(Copy.book_id == book_id).count()

class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def sanitize_search_query(query: str) -> str:
        # Удаляем управляющие символы (0x00-0x1F, 0x7F-0x9F)
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', query)
        # Экранируем символы `%` и `_`, чтобы не нарушить LIKE
        sanitized = sanitized.replace('%', '\\%').replace('_', '\\_')
        # Обрезаем до 200 символов
        return sanitized[:200]
    
    def get_by_id(self, author_id: int) -> Optional[Author]:
        return self.db.query(Author).filter(Author.id == author_id, Author.is_deleted == False).first()
    
    def get_by_name(self, first_name: str, last_name: str) -> Optional[Author]:
        return self.db.query(Author)\
            .filter(Author.first_name == first_name)\
            .filter(Author.last_name == last_name)\
            .first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Author]:
        return self.db.query(Author).filter(Author.is_deleted == False).offset(skip).limit(limit).all()
    
    def create(self, author_data: dict) -> Author:
        author = Author(**author_data)
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author
    
    def update(self, author_id: int, author_data: dict) -> Optional[Author]:
        author = self.get_by_id(author_id)
        if author:
            for key, value in author_data.items():
                if value is not None:
                    setattr(author, key, value)
            self.db.commit()
            self.db.refresh(author)
        return author
    
    def delete(self, author_id: int) -> bool:
        author = self.get_by_id(author_id)
        if author:
            author.is_deleted = True
            self.db.delete(author)
            self.db.commit()
            return True
        return False
    
    def search(self, query: str) -> List[Author]:
        safe_q = sanitize_search_query(query)
        search_term = f"%{safe_q}%"
        return self.db.query(Author).filter(Author.is_deleted == False,
            or_(
                Author.first_name.ilike(search_term),
                Author.last_name.ilike(search_term)
            )
        ).limit(20).all()
    
    def get_books_count(self, author_id: int) -> int:
        author = self.get_by_id(author_id)
        if author:
            return len(author.books)
        return 0

class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def sanitize_search_query(query: str) -> str:
        # Удаляем управляющие символы (0x00-0x1F, 0x7F-0x9F)
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', query)
        # Экранируем символы `%` и `_`, чтобы не нарушить LIKE
        sanitized = sanitized.replace('%', '\\%').replace('_', '\\_')
        # Обрезаем до 200 символов
        return sanitized[:200]
    
    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.id == genre_id, Genre.is_deleted == False).first()
    
    def get_by_name(self, name: str) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.name == name).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Genre]:
        return self.db.query(Genre).filter(Genre.is_deleted == False).offset(skip).limit(limit).all()
    
    def create(self, genre_data: dict) -> Genre:
        genre = Genre(**genre_data)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre
    
    def update(self, genre_id: int, genre_data: dict) -> Optional[Genre]:
        genre = self.get_by_id(genre_id)
        if genre:
            for key, value in genre_data.items():
                if value is not None:
                    setattr(genre, key, value)
            self.db.commit()
            self.db.refresh(genre)
        return genre
    
    def delete(self, genre_id: int) -> bool:
        genre = self.get_by_id(genre_id)
        if genre:
            Genre.is_deleted = True
            self.db.delete(genre)
            self.db.commit()
            return True
        return False
    
    def search(self, query: str) -> List[Genre]:
        safe_q = sanitize_search_query(query)
        search_term = f"%{safe_q}%"
        return self.db.query(Genre).filter(Genre.is_deleted == False,
            Genre.name.ilike(search_term)
        ).limit(20).all()
    
    def get_books_count(self, genre_id: int) -> int:
        genre = self.get_by_id(genre_id)
        if genre:
            return len(genre.books)
        return 0