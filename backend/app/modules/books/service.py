from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.modules.books.repository import BookRepository, AuthorRepository, GenreRepository
from app.modules.books.schemas import BookCreate, BookUpdate, AuthorCreate, AuthorUpdate, GenreCreate, GenreUpdate, BookSearchParams

class BookService:
    def __init__(self, db: Session):
        self.db = db
        self.book_repo = BookRepository(db)
        self.author_repo = AuthorRepository(db)
        self.genre_repo = GenreRepository(db)
    
    # Book methods
    def get_book_by_id(self, book_id: int):
        book = self.book_repo.get_by_id_with_relations(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        # Add copy counts
        book_dict = book.__dict__
        book_dict['total_copies'] = self.book_repo.get_total_copies_count(book_id)
        book_dict['available_copies'] = self.book_repo.get_available_copies_count(book_id)
        
        return book
    
    def get_all_books(self, skip: int = 0, limit: int = 100):
        books = self.book_repo.get_all_with_counts(skip, limit)
        
        # Add copy counts to each book
        for book in books:
            book.total_copies = self.book_repo.get_total_copies_count(book.id)
            book.available_copies = self.book_repo.get_available_copies_count(book.id)
        
        return books
    
    def create_book(self, book_data: BookCreate):
        # Check if book with same ISBN exists
        if book_data.isbn:
            existing = self.book_repo.get_by_isbn(book_data.isbn)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book with this ISBN already exists"
                )
        
        # Create book
        book_dict = book_data.dict(exclude={'author_ids', 'genre_ids'})
        book = self.book_repo.create(book_dict)
        
        # Add authors
        if book_data.author_ids:
            authors = self.author_repo.get_all()
            author_dict = {a.id: a for a in authors}
            for author_id in book_data.author_ids:
                if author_id in author_dict:
                    book.authors.append(author_dict[author_id])
        
        # Add genres
        if book_data.genre_ids:
            genres = self.genre_repo.get_all()
            genre_dict = {g.id: g for g in genres}
            for genre_id in book_data.genre_ids:
                if genre_id in genre_dict:
                    book.genres.append(genre_dict[genre_id])
        
        self.db.commit()
        self.db.refresh(book)
        
        return book
    
    def update_book(self, book_id: int, book_data: BookUpdate):
        book = self.get_book_by_id(book_id)
        
        # Check ISBN uniqueness if changed
        if book_data.isbn and book_data.isbn != book.isbn:
            existing = self.book_repo.get_by_isbn(book_data.isbn)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book with this ISBN already exists"
                )
        
        # Update basic fields
        update_dict = book_data.dict(exclude={'author_ids', 'genre_ids'}, exclude_unset=True)
        updated_book = self.book_repo.update(book_id, update_dict)
        
        # Update authors if provided
        if book_data.author_ids is not None:
            book.authors = []
            authors = self.author_repo.get_all()
            author_dict = {a.id: a for a in authors}
            for author_id in book_data.author_ids:
                if author_id in author_dict:
                    book.authors.append(author_dict[author_id])
        
        # Update genres if provided
        if book_data.genre_ids is not None:
            book.genres = []
            genres = self.genre_repo.get_all()
            genre_dict = {g.id: g for g in genres}
            for genre_id in book_data.genre_ids:
                if genre_id in genre_dict:
                    book.genres.append(genre_dict[genre_id])
        
        self.db.commit()
        self.db.refresh(book)
        
        return book
    
    def delete_book(self, book_id: int):
        book = self.get_book_by_id(book_id)
        
        # Check if book has copies
        if book.copies:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete book with existing copies"
            )
        
        deleted = self.book_repo.delete(book_id)
        return {"message": "Book deleted successfully"}
    
    def search_books(self, params: BookSearchParams, skip: int = 0, limit: int = 100):
        search_dict = params.dict(exclude_none=True)
        books = self.book_repo.search(search_dict, skip, limit)
        
        # Add copy counts
        for book in books:
            book.total_copies = self.book_repo.get_total_copies_count(book.id)
            book.available_copies = self.book_repo.get_available_copies_count(book.id)
        
        return books
    
    # Author methods
    def get_author_by_id(self, author_id: int):
        author = self.author_repo.get_by_id(author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )
        author.books_count = self.author_repo.get_books_count(author_id)
        return author
    
    def get_all_authors(self, skip: int = 0, limit: int = 100):
        authors = self.author_repo.get_all(skip, limit)
        for author in authors:
            author.books_count = self.author_repo.get_books_count(author.id)
        return authors
    
    def create_author(self, author_data: AuthorCreate):
        # Check if author exists
        existing = self.author_repo.get_by_name(
            author_data.first_name, 
            author_data.last_name
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author with this name already exists"
            )
        
        return self.author_repo.create(author_data.dict())
    
    def update_author(self, author_id: int, author_data: AuthorUpdate):
        author = self.get_author_by_id(author_id)
        update_dict = author_data.dict(exclude_unset=True)
        return self.author_repo.update(author_id, update_dict)
    
    def delete_author(self, author_id: int):
        author = self.get_author_by_id(author_id)
        
        # Check if author has books
        if author.books:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete author with existing books"
            )
        
        deleted = self.author_repo.delete(author_id)
        return {"message": "Author deleted successfully"}
    
    def search_authors(self, query: str):
        return self.author_repo.search(query)
    
    # Genre methods
    def get_genre_by_id(self, genre_id: int):
        genre = self.genre_repo.get_by_id(genre_id)
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found"
            )
        genre.books_count = self.genre_repo.get_books_count(genre_id)
        return genre
    
    def get_all_genres(self, skip: int = 0, limit: int = 100):
        genres = self.genre_repo.get_all(skip, limit)
        for genre in genres:
            genre.books_count = self.genre_repo.get_books_count(genre.id)
        return genres
    
    def create_genre(self, genre_data: GenreCreate):
        # Check if genre exists
        existing = self.genre_repo.get_by_name(genre_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Genre with this name already exists"
            )
        
        return self.genre_repo.create(genre_data.dict())
    
    def update_genre(self, genre_id: int, genre_data: GenreUpdate):
        genre = self.get_genre_by_id(genre_id)
        
        # Check name uniqueness if changed
        if genre_data.name and genre_data.name != genre.name:
            existing = self.genre_repo.get_by_name(genre_data.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Genre with this name already exists"
                )
        
        update_dict = genre_data.dict(exclude_unset=True)
        return self.genre_repo.update(genre_id, update_dict)
    
    def delete_genre(self, genre_id: int):
        genre = self.get_genre_by_id(genre_id)
        
        # Check if genre has books
        if genre.books:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete genre with existing books"
            )
        
        deleted = self.genre_repo.delete(genre_id)
        return {"message": "Genre deleted successfully"}
    
    def search_genres(self, query: str):
        return self.genre_repo.search(query)