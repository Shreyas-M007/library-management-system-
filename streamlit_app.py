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
        with open("books.txt", "r") as file:
            for line in file:
                parts = line.strip().split(" , ")
                if len(parts) == 2:
                    books[parts[0]] = int(parts[1])
    except:
        books = {"Project Hail Mary": 6, "Hamlet": 10, "Interstellar": 5 , "Dune": 7}
    return books

# save books to file
def save_books(books):
    with open("books.txt", "w") as file:
        for book, qty in books.items():
            file.write(f"{book} , {qty}\n")

# load borrowed books from file
def load_borrowed():
    borrowed = {}
    try:
        with open("borrowed_books.txt", "r") as file:
            for line in file:
                parts = line.strip().split(" , ")
                if len(parts) == 2:
                    borrowed[parts[0]] = parts[1]
    except:
        borrowed = {}
    return borrowed

# save borrowed books to file
def save_borrowed(borrowed):
    with open("borrowed_books.txt", "w") as file:
        for book, user in borrowed.items():
            file.write(f"{book} , {user}\n")

# fix book name so typing "harry potter" still works
def fix_name(text):
    return text.strip().title()

# search for a book without caring about uppercase or lowercase
def find_book(text, dictionary):
    name = fix_name(text)
    if name in dictionary:
        return name
    return None

# session state setup
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

# inject dark mode css
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
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#3b82f6,#2563eb) !important;
    color: white !important; border-radius: 10px !important; font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# draw a dynamic book card
def show_card(book_name, badge_text, color):
    style = "background:rgba(16,185,129,0.2);color:#10b981;border:1px solid rgba(16,185,129,0.4);" if color == "green" else "background:rgba(59,130,246,0.2);color:#3b82f6;border:1px solid rgba(59,130,246,0.4);"
    st.markdown(f"""<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);
    border-radius:12px;padding:16px 20px;display:flex;justify-content:space-between;
    align-items:center;margin-bottom:10px;">
    <span style="font-weight:700;color:#f8fafc;font-size:1.05rem;">{book_name}</span>
    <span style="padding:6px 14px;border-radius:20px;font-size:0.85rem;font-weight:600;{style}">{badge_text}</span>
    </div>""", unsafe_allow_html=True)

# ---- LOGIN PAGE ----
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>📚 Library Management System</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["👤 Borrower Login", "🛡️ Librarian Login"])
        with tab1:
            user_id = st.text_input("Borrower ID")
            user_usn = st.text_input("USN")
            user_pass = st.text_input("Password ", type="password")
            if st.button("Login as Borrower", use_container_width=True):
                if user_id in BORROWERS and BORROWERS[user_id] == user_pass and BORROWER_USN[user_id] == user_usn:
                    st.session_state.logged_in, st.session_state.role, st.session_state.username = True, "borrower", user_id
                    st.rerun()
                else:
                    st.error("Wrong credentials!")
        with tab2:
            lib_id = st.text_input("Librarian ID")
            lib_pass = st.text_input("Password", type="password", key="lib_pass")
            if st.button("Login as Librarian", use_container_width=True):
                if lib_id in LIBRARIANS and LIBRARIANS[lib_id] == lib_pass:
                    st.session_state.logged_in, st.session_state.role, st.session_state.username = True, "librarian", lib_id
                    st.rerun()
                else:
                    st.error("Wrong credentials!")

# ---- LIBRARIAN DASHBOARD ----
elif st.session_state.role == "librarian":
    with st.sidebar:
        st.markdown(f"### 🛡️ {st.session_state.username}")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<h1>🛡️ Librarian Dashboard</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])
    with col1:
        with st.container(border=True):
            st.subheader("📦 Library Inventory")
            for book, qty in st.session_state.books.items():
                show_card(book, f"{qty} Copies", "green")
    with col2:
        with st.container(border=True):
            st.subheader("➕ Add Books")
            add_name = st.text_input("Book Name")
            add_qty = st.number_input("Quantity", min_value=1, value=1, key="add_q")
            if st.button("Add to Inventory"):
                book = fix_name(add_name)
                if book:
                    st.session_state.books[book] = st.session_state.books.get(book, 0) + add_qty
                    save_books(st.session_state.books)
                    st.rerun()

        with st.container(border=True):
            st.subheader("➖ Remove Books")
            rem_name = st.text_input("Remove Book Name")
            rem_qty = st.number_input("Quantity", min_value=1, value=1, key="rem_q")
            if st.button("Remove"):
                found = find_book(rem_name, st.session_state.books)
                if found:
                    st.session_state.books[found] -= rem_qty
                    if st.session_state.books[found] <= 0: del st.session_state.books[found]
                    save_books(st.session_state.books)
                    st.rerun()

# ---- BORROWER DASHBOARD ----
else:
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("<h1>📖 Borrower Portal</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("📚 Available Books")
            for book, qty in st.session_state.books.items():
                show_card(book, f"{qty} Left", "green")
        with st.container(border=True):
            st.subheader("➕ Borrow")
            b_name = st.text_input("Book to Borrow")
            if st.button("Borrow"):
                found = find_book(b_name, st.session_state.books)
                if found:
                    st.session_state.books[found] -= 1
                    if st.session_state.books[found] == 0: del st.session_state.books[found]
                    st.session_state.borrowed[found] = st.session_state.username
                    save_books(st.session_state.books)
                    save_borrowed(st.session_state.borrowed)
                    st.rerun()
    with col2:
        with st.container(border=True):
            st.subheader("📋 Currently Borrowed")
            for b, u in st.session_state.borrowed.items():
                show_card(b, f"By {u}", "blue")
        with st.container(border=True):
            st.subheader("↩️ Return")
            r_name = st.text_input("Book to Return")
            if st.button("Return"):
                found = find_book(r_name, st.session_state.borrowed)
                if found and st.session_state.borrowed[found] == st.session_state.username:
                    del st.session_state.borrowed[found]
                    st.session_state.books[found] = st.session_state.books.get(found, 0) + 1
                    save_books(st.session_state.books)
                    save_borrowed(st.session_state.borrowed)
                    st.rerun()
