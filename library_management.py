# Import the flask library
from flask import Flask, render_template, request, redirect

# Make our app
app = Flask(__name__)


# --- Hardcoded Passwords (Beginner logic using Dictionaries) ---
# NOTE: these must all stay lowercase inside the python code!
LIBRARIANS = {
    "admin": "1234",
    "Shreyas": "0007"
}

BORROWERS = {
    "user": "0000",
    "Shivam": "1111",
    "Shivram": "2222"
}


# --- Beginner Friendly Python Storage Logic ---
def load_books():
    # Try to open the file if it exists
    working_dictionary = {}
    try:
        with open("books.txt", "r") as file:
            for line in file:
                clean_line = line.replace("\n", "")
                parts = clean_line.split(" , ")
                if len(parts) == 2:
                    # Keep book names pretty Using Title Case when loading!
                    book_name = parts[0].title()
                    quantity = int(parts[1])
                    working_dictionary[book_name] = quantity
                
        return working_dictionary
    except:
        # If the file is not there, start with some default books and quantities
        return {"Harry Potter": 3, "Atomic Habits": 2, "Python Crash Course": 1}


def save_books():
    # Write all the books to the text file safely
    with open("books.txt", "w") as file:
        for book_name, quantity in books.items():
            # Combine them with a comma and write them to the file
            file.write(book_name + " , " + str(quantity) + "\n")


def load_borrowed():
    working_dictionary = {}
    # Try to open the file if it exists
    try:
        with open("borrowed_books.txt", "r") as file:
            for line in file:
                clean_line = line.replace("\n", "")
                parts = clean_line.split(" , ")
                if len(parts) == 2:
                    book_name = parts[0].title()
                    person_name = parts[1].title()
                    working_dictionary[book_name] = person_name
                
        return working_dictionary
    except:
        return {}


def save_borrowed():
    # Write all borrowed books back to the text file safely
    with open("borrowed_books.txt", "w") as file:
        for book_name, person_name in borrowed_books.items():
            file.write(book_name + " , " + person_name + "\n")


# 1. Start the memory variables by using the load functions
books = load_books()
borrowed_books = load_borrowed()


# The main home page
@app.route("/")
def home():
    # Show the HTML file and give it our lists and dictionaries
    return render_template("index.html", available_books=books, borrowed=borrowed_books)


# Route to add a book
@app.route("/add", methods=["POST"])
def add_book():
    # .title() makes "harry POtter" -> "Harry Potter" (Case Insensitive!)
    new_book = request.form.get("book_name", "").strip().title()
    
    # .lower() makes "ADMIN" -> "admin" (Case Insensitive Login!)
    lib_id = request.form.get("librarian_id", "").strip().lower()
    lib_pass = request.form.get("password", "").strip().lower()
    
    is_allowed = False
    if lib_id in LIBRARIANS:
        if LIBRARIANS[lib_id] == lib_pass:
            is_allowed = True
            
    if is_allowed == True:
        if new_book != "":
            if new_book in books:
                books[new_book] = books[new_book] + 1
            else:
                books[new_book] = 1
                
            save_books() 
        
    return redirect("/")


# Route to borrow a book
@app.route("/borrow", methods=["POST"])
def borrow_book():
    book_to_borrow = request.form.get("book_name", "").strip().title()
    person_who_wants_it = request.form.get("person_name", "").strip().title()
    borrow_id = request.form.get("borrower_id", "").strip().lower()
    borrow_pass = request.form.get("password", "").strip().lower()
    
    is_allowed = False
    if borrow_id in BORROWERS:
        if BORROWERS[borrow_id] == borrow_pass:
            is_allowed = True
            
    if is_allowed == True:
        if book_to_borrow in books:
            if person_who_wants_it != "":
                books[book_to_borrow] = books[book_to_borrow] - 1
                
                if books[book_to_borrow] == 0:
                    books.pop(book_to_borrow)
                    
                borrowed_books[book_to_borrow] = person_who_wants_it
                save_books()
                save_borrowed()
                return redirect("/")
        else:
            return render_template("index.html", available_books=books, borrowed=borrowed_books, error_msg="Valid book only!")
        
    return redirect("/")


# Route to return a book
@app.route("/return_book", methods=["POST"])
def return_book():
    book_to_return = request.form.get("book_name", "").strip().title()
    
    if book_to_return in borrowed_books:
        borrowed_books.pop(book_to_return)
        
        if book_to_return in books:
            books[book_to_return] = books[book_to_return] + 1
        else:
            books[book_to_return] = 1
            
        save_books()
        save_borrowed()
        return redirect("/")
    else:
        return render_template("index.html", available_books=books, borrowed=borrowed_books, error_msg="Valid book only!")


# Route to completely remove/delete a book permanently
@app.route("/remove", methods=["POST"])
def remove_book():
    book_to_remove = request.form.get("book_name", "").strip().title()
    lib_id = request.form.get("librarian_id", "").strip().lower()
    lib_pass = request.form.get("password", "").strip().lower()
    
    is_allowed = False
    if lib_id in LIBRARIANS:
        if LIBRARIANS[lib_id] == lib_pass:
            is_allowed = True
            
    if is_allowed == True:
        if book_to_remove in books:
            books.pop(book_to_remove)
            save_books()
            
    return redirect("/")


# This tricky line is REQUIRED by servers like PythonAnywhere to avoid crashing!
if __name__ == "__main__":
    app.run(debug=True, port=8080)
