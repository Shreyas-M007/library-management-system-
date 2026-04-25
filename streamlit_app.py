import streamlit as st

st.set_page_config(page_title="Library Management", layout="wide")

# passwords
LIBRARIANS = {"Admin":"1234", "Shreyas": "0007"}
BORROWERS = {"Shivam": "1111", "Shivram": "2222","Shreyas": "2007"}

# university roll numbers (USN) for each borrower
BORROWER_USN = {"Shivam": "1BM25AI154", "Shivram": "1BM25AI155","Shreyas": "1BM25AI157"}

# load books from file
def load_books():
    books = {}
    try:
        file = open("books.txt", "r")
        for line in file:
            parts = line.strip().split(" , ")
            if len(parts) == 2:
                books[parts[0]] = int(parts[1])
        file.close()
    except:
        books = {"Project Hail mary": 6, "Hamlet": 10, "Interstellar": 5 , "Dune": 7}
    return books

# save books to file
def save_books(books):
    file = open("books.txt", "w")
    for book in books:
        file.write(book + " , " + str(books[book]) + "\n")
    file.close()

# load borrowed books from file
def load_borrowed():
    borrowed = {}
    try:
        file = open("borrowed_books.txt", "r")
        for line in file:
            parts = line.strip().split(" , ")
            if len(parts) == 2:
                borrowed[parts[0]] = parts[1]
        file.close()
    except:
        borrowed = {}
    return borrowed

# save borrowed books to file
def save_borrowed(borrowed):
    file = open("borrowed_books.txt", "w")
    for book in borrowed:
        file.write(book + " , " + borrowed[book] + "\n")
    file.close()

# fix book name so typing "harry potter" still works
def fix_name(text):
    return text.strip().title()

# search for a book without caring about uppercase or lowercase
def find_book(text, dictionary):
    name = fix_name(text)
    if name in dictionary:
        return name
    return None

# session state setup (so data is not lost on button click)
if "books" not in st.session_state:
    st.session_state.books = load_books()
if "borrowed" not in st.session_state:
    st.session_state.borrowed = load_borrowed()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "username" not in st.session_state:
    st.session_state.username = ""

# inject dark mode css styling from python
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #312e81, #000);
    background-size: 400% 400%;
    animation: bg 15s ease infinite;
}
@keyframes bg { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#3b82f6,#2563eb) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(59,130,246,0.5) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover { transform: translateY(-2px) !important; }
div[data-testid="stButton"] > button[kind="secondary"] {
    background: rgba(255,255,255,0.08) !important; color: #f8fafc !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important; font-weight: 600 !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover { background: rgba(255,255,255,0.15) !important; transform: translateY(-2px) !important; }
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {
    background: rgba(15,23,42,0.7) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important; color: #f8fafc !important;
}
div[data-testid="stTextInput"] input:focus, div[data-testid="stNumberInput"] input:focus {
    border-color: #3b82f6 !important; box-shadow: 0 0 15px rgba(59,130,246,0.3) !important;
}
div[data-testid="stTextInput"] label, div[data-testid="stNumberInput"] label { color: #94a3b8 !important; font-weight: 600 !important; }
section[data-testid="stSidebar"] { background: rgba(15,23,42,0.85) !important; border-right: 1px solid rgba(255,255,255,0.1) !important; }
h1, h2, h3 { color: #f8fafc !important; }
p, span, label { color: #cbd5e1 !important; }
div[data-testid="stMetricValue"] { color: #3b82f6 !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)
def show_card(book_name, badge_text, color):
    if color == "green":
        style = "background:rgba(16,185,129,0.2);color:#10b981;border:1px solid rgba(16,185,129,0.4);"
    else:
        style = "background:rgba(59,130,246,0.2);color:#3b82f6;border:1px solid rgba(59,130,246,0.4);"
    st.markdown(f"""<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);border-radius:12px;padding:16px 20px;display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
    <span style="font-weight:700;color:#f8fafc;">{book_name}</span>
    <span style="padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:600;{style}">{badge_text}</span>
    </div>""", unsafe_allow_html=True)



# ---- LOGIN PAGE ----
if st.session_state.logged_in == False:

    st.markdown("<h1 style='text-align:center;'>📚 Library Management System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#94a3b8;'>Sign in to continue</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            tab1, tab2 = st.tabs(["👤 Borrower Login", "🛡️ Librarian Login"])

            with tab1:
                with st.form("borrower_form"):
                    user_id = st.text_input("Borrower ID")
                    user_usn = st.text_input("USN (University Roll Number)")
                    user_pass = st.text_input("Password", type="password")
                    if st.form_submit_button("Login as Borrower", use_container_width=True):
                        if user_id in BORROWERS and BORROWERS[user_id] == user_pass and BORROWER_USN[user_id] == user_usn:
                            st.session_state.logged_in = True
                            st.session_state.role = "borrower"
                            st.session_state.username = user_id
                            st.rerun()
                        else:
                            st.error("Wrong ID, USN, or Password!")

            with tab2:
                with st.form("librarian_form"):
                    lib_id = st.text_input("Librarian ID")
                    lib_pass = st.text_input("Password", type="password")
                    if st.form_submit_button("Login as Librarian", use_container_width=True):
                        if lib_id in LIBRARIANS and LIBRARIANS[lib_id] == lib_pass:
                            st.session_state.logged_in = True
                            st.session_state.role = "librarian"
                            st.session_state.username = lib_id
                            st.rerun()
                        else:
                            st.error("Wrong ID or Password!")

# ---- LIBRARIAN DASHBOARD ----
elif st.session_state.role == "librarian":

    with st.sidebar:
        st.markdown("<h3>🛡️ " + st.session_state.username + "</h3>", unsafe_allow_html=True)
        st.divider()
        st.metric("Total Copies", sum(st.session_state.books.values()))
        st.metric("Unique Titles", len(st.session_state.books))
        st.metric("Borrowed", len(st.session_state.borrowed))
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.role = ""
            st.rerun()

    st.markdown("<h1>🛡️ Librarian Dashboard</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([1.5, 1])

    with col1:
        with st.container(border=True):
            st.subheader("📦 Library Inventory")
            for book, qty in st.session_state.books.items():
                st.write(f"**{book}**: {qty} copies")

    with col2:
        with st.container(border=True):
            st.subheader("➕ Add Books")
            with st.form("add_form"):
                add_name = st.text_input("Book Name")
                add_qty = st.number_input("Quantity", min_value=1, value=1)
                if st.form_submit_button("Add to Inventory", use_container_width=True):
                    book = fix_name(add_name)
                    if book == "":
                        st.error("Please enter a book name!")
                    else:
                        found = find_book(add_name, st.session_state.books)
                        if found:
                            st.session_state.books[found] = st.session_state.books[found] + add_qty
                        else:
                            st.session_state.books[book] = add_qty
                        save_books(st.session_state.books)
                        st.success("Added " + str(add_qty) + " copies of " + book + "!")
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("➖ Remove Books")
            with st.form("rem_form"):
                rem_name = st.text_input("Book Name")
                rem_qty = st.number_input("Quantity", min_value=1, value=1)
                if st.form_submit_button("Remove from Inventory", use_container_width=True):
                    found = find_book(rem_name, st.session_state.books)
                    if found:
                        st.session_state.books[found] = st.session_state.books[found] - rem_qty
                        if st.session_state.books[found] <= 0:
                            del st.session_state.books[found]
                        save_books(st.session_state.books)
                        st.success("Removed copies of " + found + "!")
                        st.rerun()
                    else:
                        st.error(fix_name(rem_name) + " not found!")

# ---- BORROWER DASHBOARD ----
else:

    with st.sidebar:
        st.markdown("<h3>👤 " + st.session_state.username + "</h3>", unsafe_allow_html=True)
        st.divider()
        st.metric("Available Copies", sum(st.session_state.books.values()))
        st.metric("Books Borrowed", len(st.session_state.borrowed))
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.role = ""
            st.rerun()

    st.markdown("<h1>📖 Borrower Portal</h1>", unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("📚 Available Books")
            for book, qty in st.session_state.books.items():
                st.write(f"**{book}**: {qty} copies left")

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("➕ Borrow a Book")
            with st.form("borrow_form"):
                borrow_name = st.text_input("Book Name (any case)")
                if st.form_submit_button("Borrow Book", use_container_width=True):
                    found = find_book(borrow_name, st.session_state.books)
                    if found:
                        st.session_state.books[found] = st.session_state.books[found] - 1
                        if st.session_state.books[found] <= 0:
                            del st.session_state.books[found]
                        st.session_state.borrowed[found] = st.session_state.username
                        save_books(st.session_state.books)
                        save_borrowed(st.session_state.borrowed)
                        st.success("You borrowed " + found + "!")
                        st.rerun()
                    else:
                        st.error(fix_name(borrow_name) + " not found!")

    with col2:
        with st.container(border=True):
            st.subheader("📋 Currently Borrowed")
            for book, person in st.session_state.borrowed.items():
                st.write(f"**{book}**: Borrowed by {person}")

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("↩️ Return a Book")
            with st.form("return_form"):
                return_name = st.text_input("Book Name (any case)")
                if st.form_submit_button("Return Book", use_container_width=True):
                    found = find_book(return_name, st.session_state.borrowed)
                    if found:
                        if st.session_state.borrowed[found] == st.session_state.username:
                            del st.session_state.borrowed[found]
                            if found in st.session_state.books:
                                st.session_state.books[found] = st.session_state.books[found] + 1
                            else:
                                st.session_state.books[found] = 1
                            save_books(st.session_state.books)
                            save_borrowed(st.session_state.borrowed)
                            st.success("You returned " + found + "!")
                            st.rerun()
                        else:
                            st.error("You didn't borrow this book!")
                    else:
                        st.error(fix_name(return_name) + " is not borrowed!")
