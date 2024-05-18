# Book Management API

This is a RESTful API for managing books. It allows users to fetch book details by ISBN, save book details to the library, and list all books stored in the library.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- OpenLibrary API

## Features

### ISBN Validation

The backend validates an ISBN number using a custom function.

### Fetch Book Details

The backend fetches book details like author, title, summary, and cover URL from the OpenLibrary API. Both ISBN_10 and ISBN_13 can be used to find a book. 

### Endpoints

#### 1. Fetch Book Details by ISBN

- **Endpoint**: `GET /isbn/<isbn>`
- **Description**: Returns book details including author, title, summary, and cover URL from OpenLibrary API and store it in the database.
- **Request Parameters**: `isbn` (ISBN_10 or ISBN_13 number can be used )
- **Response**: JSON with book details

#### 2. Save Book Details to Library

- **Endpoint**: `POST /books`
- **Description**: Fetch the book details from OpenLibrary and then saves book details in the database.
- **Request Body**: JSON with `isbn` (ISBN_10 or ISBN_13 number can be used )
- **Response**: JSON with saved book details

#### 3. List All Books in Library

- **Endpoint**: `GET /books`
- **Description**: Returns a list of all books stored in the library database.
- **Response**: JSON array with book details

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/your_username/book-management-api.git
```
2. Create a virtual environment
```bash
python3 -m venv env
```
3. activate the environment
```bash
source env/bin/activate
```
4. Installing the requirements
```bash
pip install -r requirements.txt
```
5. To run the application 
```bash
uvicorn BookApp:app --reload
```

## Change the database

To change the database update the string `DATABASE_URI` in `database_conn.py`. To use my database set `DATABASE_URI = "sqlite:///.books_database.db"`

## Known edge failure cases

When adding a book to the database using the ISBN-13 number, the OpenLibrary API might not provide information about the ISBN-10 number. If a subsequent attempt is made to add another book with a missing ISBN-10 number, the application will crash with a 500 error. This occurs because the `isbn_10` column in the database has a unique constraint, and storing multiple entries with "" value in this column violates the uniqueness constraint.

solutions : Don't store the book in the database until both ISBN number are available. use multiple APIs to get the missing ISBN.

ISBN_13 : 9781612681139 
Book: Rich Dad Poor Dad

ISBN_13 : 9781785042188
Book : Surrounded by Idiots