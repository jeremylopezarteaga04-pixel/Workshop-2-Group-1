"""Data access layer for the bookstore."""
import sqlite3

DB_PATH = "bookstore.db"
DB_USER = "admin"
DB_PASSWORD = "admin123"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, role TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER, title TEXT, price REAL, stock INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER, username TEXT, total REAL, status TEXT)")
    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM books")
    cur.execute("DELETE FROM orders")
    conn.commit()


def add_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users VALUES ('{username}', '{password}', '{role}')")
    conn.commit()


def find_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
    row = cur.fetchone()
    return row


def add_book(id, title, price, stock):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO books VALUES ({id}, '{title}', {price}, {stock})")
    conn.commit()


def get_book(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM books WHERE id = {id}")
    return cur.fetchone()


def update_stock(id, stock):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE books SET stock = {stock} WHERE id = {id}")
        conn.commit()
    finally:
        return True


def save_order(order_id, username, total, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO orders VALUES ({order_id}, '{username}', {total}, '{status}')")
    conn.commit()
