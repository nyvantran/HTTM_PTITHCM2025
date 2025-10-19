import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path


class UserDatabase:
    """Class quản lý database người dùng"""

    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.conn = None
        self._init_database()

    def _init_database(self):
        """Khởi tạo database"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()

        # Bảng users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                created_at TEXT NOT NULL,
                last_login TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')

        # Bảng driving_sessions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS driving_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration INTEGER,
                total_alerts INTEGER DEFAULT 0,
                confirmed_drowsy INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        self.conn.commit()

        # KHÔNG tạo admin mặc định nữa
        # Admin sẽ được xử lý ở login_view.py

    def _hash_password(self, password):
        """Mã hóa mật khẩu bằng SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password, full_name, email='', phone=''):
        """
        Đăng ký user mới
        Returns: True nếu thành công
        Raises: ValueError nếu có lỗi
        """
        # Validation
        if not username or len(username) < 3:
            raise ValueError("Tên đăng nhập phải có ít nhất 3 ký tự!")

        if not password or len(password) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự!")

        if not full_name:
            raise ValueError("Vui lòng nhập họ tên!")

        # Không cho phép đăng ký username "admin"
        if username.lower() == "admin":
            raise ValueError("Tên đăng nhập 'admin' đã được hệ thống sử dụng!\nVui lòng chọn tên khác.")

        # Kiểm tra username đã tồn tại
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            raise ValueError(f"Tên đăng nhập '{username}' đã tồn tại!")

        # Kiểm tra email đã tồn tại (nếu có)
        if email:
            cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            if cursor.fetchone():
                raise ValueError(f"Email '{email}' đã được sử dụng!")

        # Thêm user mới
        hashed_password = self._hash_password(password)
        created_at = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO users (username, password, full_name, email, phone, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, hashed_password, full_name, email, phone, created_at))

        self.conn.commit()
        return True

    def login_user(self, username, password):
        """
        Đăng nhập
        Returns: (success, user_info_dict) hoặc (False, None)
        """
        cursor = self.conn.cursor()
        hashed_password = self._hash_password(password)

        cursor.execute('''
            SELECT id, username, full_name, email, phone, created_at, is_active
            FROM users
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))

        result = cursor.fetchone()

        if result:
            # Kiểm tra tài khoản có active không
            if not result[6]:  # is_active
                return False, None

            # Cập nhật last_login
            cursor.execute('''
                UPDATE users
                SET last_login = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), result[0]))
            self.conn.commit()

            # Trả về thông tin user
            user_info = {
                'id': result[0],
                'username': result[1],
                'full_name': result[2],
                'email': result[3],
                'phone': result[4],
                'created_at': result[5]
            }
            return True, user_info

        return False, None

    def get_user_by_username(self, username):
        """Lấy thông tin user theo username"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, username, full_name, email, phone, created_at, last_login
            FROM users
            WHERE username = ?
        ''', (username,))

        result = cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'username': result[1],
                'full_name': result[2],
                'email': result[3],
                'phone': result[4],
                'created_at': result[5],
                'last_login': result[6]
            }
        return None

    def update_user(self, user_id, **kwargs):
        """Cập nhật thông tin user"""
        allowed_fields = ['full_name', 'email', 'phone', 'password']
        updates = []
        values = []

        for key, value in kwargs.items():
            if key in allowed_fields:
                if key == 'password':
                    value = self._hash_password(value)
                updates.append(f"{key} = ?")
                values.append(value)

        if not updates:
            return False

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"

        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()

        return True

    def get_all_users(self):
        """Lấy danh sách tất cả users"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, username, full_name, email, phone, created_at, last_login, is_active
            FROM users
            ORDER BY created_at DESC
        ''')

        results = cursor.fetchall()
        users = []
        for row in results:
            users.append({
                'id': row[0],
                'username': row[1],
                'full_name': row[2],
                'email': row[3],
                'phone': row[4],
                'created_at': row[5],
                'last_login': row[6],
                'is_active': row[7]
            })
        return users

    def delete_user(self, user_id):
        """Xóa user"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        return True

    def start_driving_session(self, user_id):
        """Bắt đầu phiên lái xe"""
        # Chỉ lưu session cho user từ database (id > 0)
        if user_id == 0:  # Admin mặc định
            return 0

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO driving_sessions (user_id, start_time)
            VALUES (?, ?)
        ''', (user_id, datetime.now().isoformat()))
        self.conn.commit()
        return cursor.lastrowid

    def end_driving_session(self, session_id, total_alerts=0, confirmed_drowsy=0):
        """Kết thúc phiên lái xe"""
        if session_id == 0:  # Admin mặc định
            return True

        cursor = self.conn.cursor()

        # Lấy start_time
        cursor.execute('SELECT start_time FROM driving_sessions WHERE id = ?', (session_id,))
        result = cursor.fetchone()
        if not result:
            return False

        start_time = datetime.fromisoformat(result[0])
        end_time = datetime.now()
        duration = int((end_time - start_time).total_seconds())

        cursor.execute('''
            UPDATE driving_sessions
            SET end_time = ?, duration = ?, total_alerts = ?, confirmed_drowsy = ?
            WHERE id = ?
        ''', (end_time.isoformat(), duration, total_alerts, confirmed_drowsy, session_id))

        self.conn.commit()
        return True

    def get_user_sessions(self, user_id, limit=10):
        """Lấy lịch sử phiên lái xe của user"""
        if user_id == 0:  # Admin mặc định
            return []

        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, start_time, end_time, duration, total_alerts, confirmed_drowsy
            FROM driving_sessions
            WHERE user_id = ?
            ORDER BY start_time DESC
            LIMIT ?
        ''', (user_id, limit))

        results = cursor.fetchall()
        sessions = []
        for row in results:
            sessions.append({
                'id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'duration': row[3],
                'total_alerts': row[4],
                'confirmed_drowsy': row[5]
            })
        return sessions

    def close(self):
        """Đóng kết nối database"""
        if self.conn:
            self.conn.close()