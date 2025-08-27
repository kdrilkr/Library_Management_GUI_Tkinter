#PACKAGES
import tkinter as tk

from tkinter import messagebox as msg
import functions
import os
import json
#BOOK LIST PATH
PATH = "Library_Management_GUI/data/books.json"
def only_int(input):
    return input.isdigit() or input == "" 
root = tk.Tk()
vcmd = (root.register(only_int), "%P")
root.geometry("300x240")
root.title("LMS")
#LABELS AND ENTRIES
mainlabel = tk.Label(root, text="Library Management System")
mainlabel.place(x=80, y=8,relx=0.22,anchor="center")

BookNameLabel= tk.Label(root, text="Book Name:")
BookNameLabel.place(x=40, y=30, relx=0.052,anchor="center")

BookNameEntry = tk.Entry(root, bd=1.5)
BookNameEntry.place(x=110,y=30, relx=0.15,anchor="center")

AuthorLabel= tk.Label(root, text="Author: ")
AuthorLabel.place(x=65, y=60, relx=0.013,anchor="center")

AuthorEntry = tk.Entry(root, bd=1.5)
AuthorEntry.place(x=110,y=60, relx=0.15,anchor="center")

ISBNLabel= tk.Label(root, text="ISBN: ")
ISBNLabel.place(x=77, y=90, relx=0,anchor="center")

ISBNEntry = tk.Entry(root, bd=1.5, validate="key", validatecommand=vcmd)
ISBNEntry.place(x=110,y=90, relx=0.15,anchor="center")

def NewBook():
    name = BookNameEntry.get().strip()
    author = AuthorEntry.get().strip()
    isbn = ISBNEntry.get().strip()

    if name == "" or author == "" or isbn == "":
        msg.showwarning("Warning", "You missed 1 or more parameters!")
        return

    newbook = {
        "ISBN": isbn,
        "NAME": name,
        "AUTHOR": author,
        "STOCK": 1,
        "STATUS": "Available"
    }

    from functions import AddBook
    new_stock = AddBook(newbook)

    if new_stock !=1 :
        msg.showinfo("Information", f"Book already exists. Stock increased to {new_stock}.")

    BookNameEntry.delete(0, tk.END)
    AuthorEntry.delete(0, tk.END)
    ISBNEntry.delete(0, tk.END)

def ShowBooks():
    # Eğer pencere zaten açıksa yeniden çiz
    if hasattr(ShowBooks, "window") and ShowBooks.window.winfo_exists():
        window = ShowBooks.window
        for widget in window.winfo_children():
            widget.destroy()
    else:
        window = tk.Toplevel()
        ShowBooks.window = window
        window.title("Book List")
        window.geometry("775x600")

    # --- Scroll destekli yapı ---
    container = tk.Frame(window)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Scroll ayarı: içerik büyüdükçe scrollbar aktif olsun
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", on_frame_configure)
    # --- Bitti ---

    from functions import ReadBook, DecreaseStock
    cont_dict = ReadBook()

    labels = ["BOOK'S NAME", "AUTHOR", "ISBN", "STOCK", "ACTIONS"]
    for i, mainlabels in enumerate(labels):
        tk.Label(frame, text=mainlabels, font=("Times New Roman", 10, "bold"),borderwidth=1, relief="solid", width=20).grid(row=0, column=i, sticky="nsew")

    def shorten(text, max_len=20):
        return text if len(text) <= max_len else text[:max_len-3] + "..."

    def delete_action(isbn):
        DecreaseStock(isbn)
        ShowBooks()   # tabloyu yenile

    for line, (isbn, book) in enumerate(cont_dict.items(), start=1):
        tk.Label(frame, text=shorten(book["NAME"], 20), borderwidth=1, relief="solid",width=20, padx=5, pady=5, anchor="w").grid(row=line, column=0, sticky="nsew")
        tk.Label(frame, text=shorten(book["AUTHOR"], 20), borderwidth=1, relief="solid",width=20, padx=5, pady=5, anchor="w").grid(row=line, column=1, sticky="nsew")
        tk.Label(frame, text=shorten(isbn, 15), borderwidth=1, relief="solid",width=20, padx=5, pady=5, anchor="w").grid(row=line, column=2, sticky="nsew")
        tk.Label(frame, text=book["STOCK"], borderwidth=1, relief="solid",width=20, padx=5, pady=5, anchor="center").grid(row=line, column=3, sticky="nsew")

        tk.Button(frame, text="Sil", width=10, command=lambda i=isbn: delete_action(i))\
            .grid(row=line, column=4, padx=5, pady=5)

#ADD BOOK BUTTON / BOOK LIST BUTTON
AddButton = tk.Button(root,command=NewBook, text="Add Book")
AddButton.place(x=70,y=150, relx=0.08,anchor="center")
BookListButton = tk.Button(root, command=ShowBooks, text="Book List")
BookListButton.place(x=170,y=150, relx=0.08,anchor="center")
#WARNING IN MAIN WINDOW
warninglabel = tk.Label(root, text="Warning: Please only use English charachters!")
warninglabel.place(x=80, y=115,relx=0.22,anchor="center")

root.resizable(False, False)
root.mainloop()
