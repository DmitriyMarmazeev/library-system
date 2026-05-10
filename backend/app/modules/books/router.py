from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional

from app.modules.books.schemas import (
    BookResponse, BookCreate, BookUpdate, BookSearchParams,
    AuthorResponse, AuthorCreate, AuthorUpdate,
    GenreResponse, GenreCreate, GenreUpdate
)
from app.modules.books.service import BookService
from app.modules.books.dependencies import get_book_service
from app.modules.auth.dependencies import require_roles
from app.modules.users.models import User

router = APIRouter()

# Общие блоки ответов
AUTH_RESPONSES = {
    401: {"description": "Not authenticated"},
    403: {"description": "Forbidden – insufficient permissions"},
}
VALIDATION_RESPONSE = {
    422: {"description": "Validation Error"}
}


# ----------------------------------------------------------------
# Book endpoints
# ----------------------------------------------------------------

@router.get(
    "/",
    response_model=List[BookResponse],
    responses={
        200: {"description": "List of books"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_all_books(
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: BookService = Depends(get_book_service)
):
    """Get all books (authenticated users)"""
    return service.get_all_books(skip, limit)


@router.get(
    "/search",
    response_model=List[BookResponse],
    responses={
        200: {"description": "Search results"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    year_from: Optional[int] = Query(None, ge=1400),
    year_to: Optional[int] = Query(None),
    isbn: Optional[str] = Query(None),
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: BookService = Depends(get_book_service)
):
    """Search books by various criteria"""
    params = BookSearchParams(
        title=title,
        author=author,
        genre=genre,
        year_from=year_from,
        year_to=year_to,
        isbn=isbn
    )
    return service.search_books(params, skip, limit)


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    responses={
        200: {"description": "Book details"},
        404: {"description": "Book not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_book_by_id(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    """Get book by ID"""
    return service.get_book_by_id(book_id)


# ----------------------------------------------------------------
# Author endpoints
# ----------------------------------------------------------------

@router.get(
    "/authors/all",
    response_model=List[AuthorResponse],
    responses={
        200: {"description": "List of all authors"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_all_authors(
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: BookService = Depends(get_book_service)
):
    """Get all authors"""
    return service.get_all_authors(skip, limit)


@router.get(
    "/authors/search",
    response_model=List[AuthorResponse],
    responses={
        200: {"description": "Author search results"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def search_authors(
    q: str = Query(..., min_length=1),
    service: BookService = Depends(get_book_service)
):
    """Search authors by name"""
    return service.search_authors(q)


@router.get(
    "/authors/{author_id}",
    response_model=AuthorResponse,
    responses={
        200: {"description": "Author details"},
        404: {"description": "Author not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_author_by_id(
    author_id: int,
    service: BookService = Depends(get_book_service)
):
    """Get author by ID"""
    return service.get_author_by_id(author_id)


# ----------------------------------------------------------------
# Genre endpoints
# ----------------------------------------------------------------

@router.get(
    "/genres/all",
    response_model=List[GenreResponse],
    responses={
        200: {"description": "List of all genres"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_all_genres(
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: BookService = Depends(get_book_service)
):
    """Get all genres"""
    return service.get_all_genres(skip, limit)


@router.get(
    "/genres/search",
    response_model=List[GenreResponse],
    responses={
        200: {"description": "Genre search results"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def search_genres(
    q: str = Query(..., min_length=1),
    service: BookService = Depends(get_book_service)
):
    """Search genres by name"""
    return service.search_genres(q)


@router.get(
    "/genres/{genre_id}",
    response_model=GenreResponse,
    responses={
        200: {"description": "Genre details"},
        404: {"description": "Genre not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_genre_by_id(
    genre_id: int,
    service: BookService = Depends(get_book_service)
):
    """Get genre by ID"""
    return service.get_genre_by_id(genre_id)


# ----------------------------------------------------------------
# Protected endpoints (librarian and admin only)
# ----------------------------------------------------------------

@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Book created"},
        400: {"description": "Bad request – invalid input or business rule violation"},
        404: {"description": "Related resource not found (e.g., author)"},
        409: {"description": "Conflict – book already exists"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def create_book(
    book_data: BookCreate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: BookService = Depends(get_book_service)
):
    """Create a new book (librarian and admin only)"""
    return service.create_book(book_data)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    responses={
        200: {"description": "Book updated"},
        400: {"description": "Bad request – business rule violation (e.g., duplicate ISBN)"},
        404: {"description": "Book not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: BookService = Depends(get_book_service)
):
    """Update book (librarian and admin only)"""
    return service.update_book(book_id, book_data)


@router.delete(
    "/{book_id}",
    responses={
        200: {"description": "Book deleted successfully"},
        404: {"description": "Book not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def delete_book(
    book_id: int,
    current_user: User = Depends(require_roles(["admin"])),
    service: BookService = Depends(get_book_service)
):
    """Delete book (admin only)"""
    return service.delete_book(book_id)


@router.post(
    "/authors",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Author created"},
        400: {"description": "Bad request – duplicate name or other violation"},
        409: {"description": "Conflict – author already exists"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def create_author(
    author_data: AuthorCreate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: BookService = Depends(get_book_service)
):
    """Create a new author (librarian and admin only)"""
    return service.create_author(author_data)


@router.put(
    "/authors/{author_id}",
    response_model=AuthorResponse,
    responses={
        200: {"description": "Author updated"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        404: {"description": "Author not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: BookService = Depends(get_book_service)
):
    """Update author (librarian and admin only)"""
    return service.update_author(author_id, author_data)


@router.delete(
    "/authors/{author_id}",
    responses={
        200: {"description": "Author deleted successfully"},
        400: {"description": "Bad request – cannot delete author with existing books"},
        404: {"description": "Author not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def delete_author(
    author_id: int,
    current_user: User = Depends(require_roles(["admin"])),
    service: BookService = Depends(get_book_service)
):
    """Delete author (admin only)"""
    return service.delete_author(author_id)


@router.post(
    "/genres",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Genre created"},
        400: {"description": "Bad request – duplicate name or other violation"},
        409: {"description": "Conflict – genre already exists"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def create_genre(
    genre_data: GenreCreate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: BookService = Depends(get_book_service)
):
    """Create a new genre (librarian and admin only)"""
    return service.create_genre(genre_data)


@router.put(
    "/genres/{genre_id}",
    response_model=GenreResponse,
    responses={
        200: {"description": "Genre updated"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        404: {"description": "Genre not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def update_genre(
    genre_id: int,
    genre_data: GenreUpdate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: BookService = Depends(get_book_service)
):
    """Update genre (librarian and admin only)"""
    return service.update_genre(genre_id, genre_data)


@router.delete(
    "/genres/{genre_id}",
    responses={
        200: {"description": "Genre deleted successfully"},
        400: {"description": "Bad request – cannot delete genre with existing books"},
        404: {"description": "Genre not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def delete_genre(
    genre_id: int,
    current_user: User = Depends(require_roles(["admin"])),
    service: BookService = Depends(get_book_service)
):
    """Delete genre (admin only)"""
    return service.delete_genre(genre_id)