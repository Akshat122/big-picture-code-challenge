from sqlalchemy.orm import Session
from database_model import Book
from schema import Create_Book
from sqlalchemy import or_

# Function to search the database if the book already exist.
def get_book_by_any_isbn(db: Session, isbn: str):
    return db.query(Book).filter(
        or_(Book.isbn_10 == isbn, Book.isbn_13 == isbn)
    ).first()

# Function to create new book entry in the database
def create_book(db: Session, book: Create_Book):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Function to get all the books from the database
def get_books(db: Session):
    return db.query(Book).all()
