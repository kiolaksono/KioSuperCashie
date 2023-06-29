import sqlite3

def create_connection():
    conn = sqlite3.connect('tokoshop.db')
    return conn