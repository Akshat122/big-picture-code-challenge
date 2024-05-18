import requests

# A function to validate isbn_10 and isbn_13 
def validate_isbn(isbn: str) -> bool:
    # https://www.instructables.com/How-to-verify-a-ISBN/

    if len(isbn) == 10:
        return isbn.isdigit() and sum((i + 1) * int(num) for i, num in enumerate(isbn)) % 11 == 0
    elif len(isbn) == 13:
        return isbn.isdigit() and sum((1 if i % 2 == 0 else 3) * int(num) for i, num in enumerate(isbn)) % 10 == 0
    return False

# A function to get the book details from OpenLibrary
def fetch_book_details(isbn: str):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    response = requests.get(url)

    # Checking the response code 
    if response.status_code != 200:
        return None
    # checking if the response is not empty from the API
    res_data = response.json().get(f"ISBN:{isbn}", {})
    if not res_data:
        return None

    # Extract ISBNs from the response data 
    isbn_10, isbn_13= "",""

    # Setting the ISBN according to its length 
    if len(isbn) == 10:
        isbn_10 = isbn
    elif len(isbn)== 13:
        isbn_13 = isbn

    # Setting the ISBN from the response from the API 
    if "identifiers" in res_data:
        if "isbn_10" in res_data["identifiers"] and isbn_10 == "":
            isbn_10 = res_data["identifiers"]["isbn_10"][0]
        if "isbn_13" in res_data["identifiers"] and isbn_13 == "":
            isbn_13 = res_data["identifiers"]["isbn_13"][0]


    # Creating json of new book to store in the database
    return {
        "title": res_data.get("title", ""), # Title of the book
        "author": ", ".join(author["name"] for author in res_data.get("authors", [])), # Joining all the author's names 
        "summary": "", # Unable to find a way to get summary from API
        "cover_url": res_data.get("cover", {}).get("small", ""), # Getting the cover URL
        "isbn_10": isbn_10,
        "isbn_13": isbn_13,
    }


