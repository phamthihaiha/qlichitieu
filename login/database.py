import sqlite3

class DatabaseManager:
    def __init__(self, db_path='expense_tracker.db'):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        # Open connection 
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Create User table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hash_password TEXT NOT NULL,
                expense REAL DEFAULT 0
            )
            ''')

            # Create Categories table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES User (id)
            )
            ''')

            # Create Expense table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                note TEXT,
                user_id INTEGER,
                category_id INTEGER,
                description TEXT,
                date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES User (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
            ''')

            # Commit changes
            conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred while creating tables: {e}")

        finally:
            # Always close the connection
            cursor.close()
            conn.close()

# Create an instance of the DatabaseManager
database_manager = DatabaseManager('expense_tracker.db')