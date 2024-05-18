from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import database_model, schema, database_crud, database_conn, utils

# Creating tables for all the models defined in the database
database_model.Base.metadata.create_all(bind=database_conn.engine)

# Initializing FastAPI 
app = FastAPI()

# Connection to database
def connect_to_database():
    db = database_conn.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books", response_model=list[schema.Fetch_Book])
def get_all_books(db: Session = Depends(connect_to_database)):

    # Get all the books from the database
    return database_crud.get_books(db)

@app.get("/isbn/{isbn}", response_model=schema.Fetch_Book)
def get_book_details(isbn: str, db: Session = Depends(connect_to_database)):
    if not utils.validate_isbn(isbn):
        raise HTTPException(status_code=400, detail="Invalid ISBN.")
    
    # Check if the book already exists in the database
    book_search = database_crud.get_book_by_any_isbn(db, isbn)
    if book_search:
        return book_search
    
    # Fetch book details from the external API
    book_details = utils.fetch_book_details(isbn)
    if not book_details:
        raise HTTPException(status_code=404, detail="Book not found with the ISBN number.")
    
    # Save the book details to the database
    return database_crud.create_book(db, schema.Create_Book(**book_details))

@app.post("/books", response_model=schema.Fetch_Book)
def create_book(book: schema.Book_Search, db: Session = Depends(connect_to_database)):

    # Check if the ISBN number is valid or not 
    if not utils.validate_isbn(book.isbn):
        raise HTTPException(status_code=400, detail="Invalid ISBN.")
    
    # Check if the book already exists in the database by any of its ISBNs
    book_search = database_crud.get_book_by_any_isbn(db, book.isbn)
    if book_search:
        return book_search
    
    # Fetch book details from the Open Library API
    book_details = utils.fetch_book_details(book.isbn)
    if not book_details:
        raise HTTPException(status_code=404, detail="Book not found with the ISBN number.")
    
    # save the book in the database and return it as response 
    return database_crud.create_book(db, schema.Create_Book(**book_details))


