import sqlite3
import hashlib
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Tạo kết nối database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Tạo bảng users nếu chưa tồn tại
def init_database():
    conn = get_db_connection()
    
    # Tạo bảng users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    

# Mã hóa mật khẩu
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Mô hình dữ liệu
class UserLogin(BaseModel):
    username: str
    password: str

# Khởi tạo database
init_database()

# API Đăng nhập
@app.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Truy vấn người dùng
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", 
        (user.username, hash_password(user.password))
    )
    
    # Kiểm tra tài khoản
    existing_user = cursor.fetchone()
    conn.close()
    
    # Xác thực
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không đúng"
        )
    
    return {"message": "Đăng nhập thành công"}

# API Đăng ký
@app.post("/register")
def register(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Thêm người dùng mới
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", 
            (user.username, hash_password(user.password))
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã tồn tại"
        )
    finally:
        conn.close()
    
    return {"message": "Đăng ký thành công"}

# Hàm thêm người dùng mặc định (để test)
def add_default_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Thêm user mặc định nếu chưa tồn tại
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
        ('admin', hash_password('admin@123'))
    )
    
    conn.commit()
    conn.close()

# Chạy ứng dụng
if __name__ == "_main_":
    # Thêm user mặc định
    add_default_user()
    # Chạy server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)