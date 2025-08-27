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
        # Mevcut kitabın stokunu 1 artır
        books[isbn]["STOCK"] += 1
    else:
        # Yeni kitap ekle
        books[isbn] = {
            "NAME": new_book["NAME"],
            "AUTHOR": new_book["AUTHOR"],
            "STOCK": new_book["STOCK"],
            "STATUS": new_book["STATUS"]
        }

    WriteBook(books)
    return books[isbn]["STOCK"]  # stok değerini geri döndürebiliriz


def DeleteBook(isbn):
    books = ReadBook()
    if isbn in books:
        del books[isbn]
        WriteBook(books)
        return True
    return False

def DecreaseStock(isbn):
    books = ReadBook()
    if isbn in books:
        if books[isbn]["STOCK"] > 1:
            books[isbn]["STOCK"] -= 1
        else:
            del books[isbn]  # stok 1 ise kitabı tamamen sil
        WriteBook(books)
        return True
    return False
