from sqlalchemy import Column, Integer, String
from database_conn import Base

# Basic class to store books in the database
class Book(Base):
    __tablename__ = "book"

    record_id = Column(Integer, primary_key=True, index=True)
    isbn_10 = Column(String, unique=True, index=True)
    isbn_13 = Column(String, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    summary = Column(String)
    cover_url = Column(String)

    def __toJson__(self):
        return {
            'isbn': self.isbn, 
            'title': self.title, 
            'author': self.author, 
            'summary': self.summary,  
            'cover_url': self.cover_url
        }
