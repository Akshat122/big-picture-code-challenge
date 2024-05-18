from pydantic import BaseModel

# Schema for creating a new book entry in the database.
class Create_Book(BaseModel):
    title: str
    author: str
    summary: str
    cover_url: str
    isbn_10 : str
    isbn_13 : str

# Schema for representing a book fetched from the database.
class Fetch_Book(BaseModel):
    record_id: int
    title: str
    author: str
    summary: str
    cover_url: str
    isbn_10 : str
    isbn_13 : str

# Schema for searching a book 
class Book_Search(BaseModel):
    isbn: str
