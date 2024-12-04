import sqlite3

def connect_to_sqlite(db_path):
    try:
        connection = sqlite3.connect(db_path)
        print("Kết nối SQLite thành công!")
        return connection
    
    except sqlite3.Error as error:
        print(f"Lỗi kết nối SQLite: {error}")
        return None
connect_to_sqlite('expense_tracker.db')