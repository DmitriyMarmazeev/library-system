from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# Author schemas
class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)

class AuthorResponse(AuthorBase):
    id: int
    books_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

# Genre schemas
class GenreBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class GenreCreate(GenreBase):
    pass

class GenreUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)

class GenreResponse(GenreBase):
    id: int
    books_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

# Book schemas
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1400, le=datetime.now().year)
    description: Optional[str] = None
    publisher: Optional[str] = Field(None, max_length=100)
    pages: Optional[int] = Field(None, ge=1, le=10000)

class BookCreate(BookBase):
    author_ids: List[int] = Field(default_factory=list)
    genre_ids: List[int] = Field(default_factory=list)
    
    @validator('isbn')
    def validate_isbn(cls, v):
        if v and len(v) not in [10, 13]:
            raise ValueError('ISBN must be either 10 or 13 characters long')
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, max_length=20)
    publication_year: Optional[int] = Field(None, ge=1400, le=datetime.now().year)
    description: Optional[str] = None
    publisher: Optional[str] = Field(None, max_length=100)
    pages: Optional[int] = Field(None, ge=1, le=10000)
    author_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None

class BookResponse(BookBase):
    id: int
    authors: List[AuthorResponse] = []
    genres: List[GenreResponse] = []
    total_copies: Optional[int] = 0
    available_copies: Optional[int] = 0
    
    class Config:
        from_attributes = True

class BookListResponse(BaseModel):
    id: int
    title: str
    authors: List[str]
    publication_year: Optional[int]
    available_copies: int
    
    class Config:
        from_attributes = True

# Search schemas
class BookSearchParams(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_from: Optional[int] = Field(None, ge=1400)
    year_to: Optional[int] = Field(None, le=datetime.now().year)
    isbn: Optional[str] = None
    
    @validator('year_to')
    def validate_years(cls, v, values):
        if v and values.get('year_from') and v < values['year_from']:
            raise ValueError('year_to must be greater than or equal to year_from')
        return v