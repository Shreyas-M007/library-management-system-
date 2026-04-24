# Import the flask library
from flask import Flask, render_template, request, redirect, session, url_for

# Make our app
app = Flask(__name__)
app.secret_key = 'super_secret_library_key'

# --- Hardcoded Passwords (Beginner logic using Dictionaries) ---
LIBRARIANS = {
    "admin": "1234",
    "shreyas": "0007"
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


# The main home page for borrowers
@app.route("/")
def home():
    # Show the HTML file and give it our lists and dictionaries
    return render_template("index.html", available_books=books, borrowed=borrowed_books)


# Librarian Login Page
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        lib_id = request.form.get("librarian_id", "").strip()
        lib_pass = request.form.get("password", "").strip()
        
        if lib_id in LIBRARIANS and LIBRARIANS[lib_id] == lib_pass:
            session['admin'] = True
            session['admin_id'] = lib_id
            return redirect("/admin_dashboard")
        else:
            return render_template("admin_login.html", error_msg="Invalid librarian credentials!")
            
    return render_template("admin_login.html")


# Librarian Dashboard
@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get('admin'):
        return redirect("/admin_login")
    return render_template("admin_dashboard.html", available_books=books, admin_id=session.get('admin_id'))


# Logout for Librarian
@app.route("/logout")
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect("/")


# Route to add a book (Admin only)
@app.route("/add", methods=["POST"])
def add_book():
    if not session.get('admin'):
        return redirect("/admin_login")
        
    new_book = request.form.get("book_name", "").strip().title()
    try:
        qty = int(request.form.get("quantity", 1))
        if qty <= 0: qty = 1
    except:
        qty = 1
    
    if new_book != "":
        if new_book in books:
            books[new_book] = books[new_book] + qty
        else:
            books[new_book] = qty
        save_books() 
        
    return redirect("/admin_dashboard")


# Route to remove a book completely or subtract quantity (Admin only)
@app.route("/remove", methods=["POST"])
def remove_book():
    if not session.get('admin'):
        return redirect("/admin_login")
        
    book_to_remove = request.form.get("book_name", "").strip().title()
    try:
        qty = int(request.form.get("quantity", 1))
        if qty <= 0: qty = 1
    except:
        qty = 1
    
    if book_to_remove in books:
        books[book_to_remove] = books[book_to_remove] - qty
        if books[book_to_remove] <= 0:
            books.pop(book_to_remove)
        save_books()
            
    return redirect("/admin_dashboard")


# Route to borrow a book
@app.route("/borrow", methods=["POST"])
def borrow_book():
    book_to_borrow = request.form.get("book_name", "").strip().title()
    person_who_wants_it = request.form.get("person_name", "").strip()
    borrow_id = request.form.get("borrower_id", "").strip()
    borrow_pass = request.form.get("password", "").strip()
    
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
    else:
        return render_template("index.html", available_books=books, borrowed=borrowed_books, error_msg="Invalid borrower credentials!")
        
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
        return render_template("index.html", available_books=books, borrowed=borrowed_books, error_msg="Book is not borrowed!")


# This tricky line is REQUIRED by servers like PythonAnywhere to avoid crashing!
if __name__ == "__main__":
    app.run(debug=True, port=8080)
