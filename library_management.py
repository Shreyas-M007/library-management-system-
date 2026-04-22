# Import the flask library
from flask import Flask, render_template, request, redirect

# Make our app
app = Flask(__name__)


# --- Hardcoded Passwords (Beginner logic using Dictionaries) ---
LIBRARIANS = {
    "admin": "1234",
    "shreyas": "boss123"
}

BORROWERS = {
    "user": "0000",
    "john": "apple123",
    "mary": "books456"
}


# --- Beginner Friendly Python Storage Logic ---
def load_books():
    # Try to open the file if it exists
    working_dictionary = {}
    try:
        with open("books.txt", "r") as file:
            for line in file:
                # Remove the hidden enter key press
                clean_line = line.replace("\n", "")
                
                # Split the line by the comma we used when saving
                parts = clean_line.split(" , ")
                
                # Error check: make sure the line split perfectly into 2 pieces!
                if len(parts) == 2:
                    book_name = parts[0]
                    quantity = int(parts[1])
                    # Put it in our dictionary
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
                # Remove the hidden enter key press
                clean_line = line.replace("\n", "")
                
                # Split the line by the comma we used when saving
                parts = clean_line.split(" , ")
                
                # Error check: make sure the line split perfectly into 2 pieces!
                if len(parts) == 2:
                    book_name = parts[0]
                    person_name = parts[1]
                    # Put it in our dictionary
                    working_dictionary[book_name] = person_name
                
        return working_dictionary
    except:
        # If the file is not there, return an empty dictionary
        return {}


def save_borrowed():
    # Write all borrowed books back to the text file safely
    with open("borrowed_books.txt", "w") as file:
        for book_name, person_name in borrowed_books.items():
            # Combine them with a comma and write them to the file
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
    # Get the input safely (use default "" if failing) to prevent Server Crashes
    new_book = request.form.get("book_name", "").strip()
    lib_id = request.form.get("librarian_id", "").strip()
    lib_pass = request.form.get("password", "").strip()
    
    # Beginner-friendly safe checking logic
    is_allowed = False
    if lib_id in LIBRARIANS:
        if LIBRARIANS[lib_id] == lib_pass:
            is_allowed = True
            
    # If the password is correct, save the book
    if is_allowed == True:
        if new_book != "":
            # If the book is already in our dictionary, add +1 to the copies
            if new_book in books:
                books[new_book] = books[new_book] + 1
            # If it's a completely new book, start tracking it at 1 copy
            else:
                books[new_book] = 1
                
            save_books() 
        
    return redirect("/")


# Route to borrow a book
@app.route("/borrow", methods=["POST"])
def borrow_book():
    # Safely get all inputs so we never get a NoneType crash error
    book_to_borrow = request.form.get("book_name", "").strip()
    person_who_wants_it = request.form.get("person_name", "").strip()
    borrow_id = request.form.get("borrower_id", "").strip()
    borrow_pass = request.form.get("password", "").strip()
    
    # Beginner-friendly safe checking logic
    is_allowed = False
    if borrow_id in BORROWERS:
        if BORROWERS[borrow_id] == borrow_pass:
            is_allowed = True
            
    # If the password is correct, process the book
    if is_allowed == True:
        if book_to_borrow in books:
            if person_who_wants_it != "":
                # Subtract 1 copy from the inventory
                books[book_to_borrow] = books[book_to_borrow] - 1
                
                # If there are officially 0 copies left, remove it from the list completely
                if books[book_to_borrow] == 0:
                    books.pop(book_to_borrow)
                    
                # Put it in the borrowed dictionary
                borrowed_books[book_to_borrow] = person_who_wants_it
                save_books()
                save_borrowed()
                return redirect("/")
        else:
            # If the book does not exist, send a beginner error to the frontend!
            return render_template("index.html", available_books=books, borrowed=borrowed_books, error_msg="Valid book only!")
        
    return redirect("/")


# Route to return a book
@app.route("/return_book", methods=["POST"])
def return_book():
    book_to_return = request.form.get("book_name", "").strip()
    
    # Make sure the book is actually borrowed
    if book_to_return in borrowed_books:
        # Remove it from the borrower tracking
        borrowed_books.pop(book_to_return)
        
        # Add a copy back to the inventory
        if book_to_return in books:
            books[book_to_return] = books[book_to_return] + 1
        else:
            books[book_to_return] = 1
            
        save_books()
        save_borrowed()
        return redirect("/")
    else:
        # Send an error if it doesn't exist
        return render_template("index.html", available_books=books, borrowed=borrowed_books, error_msg="Valid book only!")


# Route to completely remove/delete a book permanently
@app.route("/remove", methods=["POST"])
def remove_book():
    book_to_remove = request.form.get("book_name", "").strip()
    lib_id = request.form.get("librarian_id", "").strip()
    lib_pass = request.form.get("password", "").strip()
    
    # Beginner-friendly safe checking logic
    is_allowed = False
    if lib_id in LIBRARIANS:
        if LIBRARIANS[lib_id] == lib_pass:
            is_allowed = True
            
    # If the librarian is logged in correctly, totally wipe the book from inventory
    if is_allowed == True:
        if book_to_remove in books:
            books.pop(book_to_remove)
            save_books()
            
    return redirect("/")


# This tricky line is REQUIRED by servers like PythonAnywhere to avoid crashing!
if __name__ == "__main__":
    app.run(debug=True, port=8080)
