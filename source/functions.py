import json
import os

PATH = "Library_Management_GUI/data/books.json"

def ReadBook():
    if not os.path.exists(PATH) or os.path.getsize(PATH) == 0:
        return {}
    try:
        with open(PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, json.decoder.JSONDecodeError):
        return {}

def WriteBook(books_dict):
    with open(PATH, "w") as f:
        json.dump(books_dict, f, indent=4, ensure_ascii=False)

def AddBook(new_book):
    books = ReadBook()
    isbn = new_book["ISBN"]
    
    if isbn in books:
        # increase stock
        books[isbn]["STOCK"] += 1
    else:
        # add new book
        books[isbn] = {
            "NAME": new_book["NAME"],
            "AUTHOR": new_book["AUTHOR"],
            "STOCK": new_book["STOCK"],
            "STATUS": new_book["STATUS"]
        }
    WriteBook(books)
    return books[isbn]["STOCK"]

def DecreaseStock(isbn):
    books = ReadBook()
    if isbn in books:
        if books[isbn]["STOCK"] > 1:
            books[isbn]["STOCK"] -= 1
        else:
            del books[isbn]  # if stock is 1 delete book
        WriteBook(books)
        return True
    return False
