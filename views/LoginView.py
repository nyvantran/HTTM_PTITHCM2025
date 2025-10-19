from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor
from utils.database import UserDatabase


class LoginView(QWidget):
    """View đăng nhập"""

    # Signal phát ra khi đăng nhập thành công
    login_success = pyqtSignal(dict)  # Truyền user_info
    register_clicked = pyqtSignal()

    def __init__(self, db: UserDatabase):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Frame chứa form đăng nhập
        login_frame = QFrame()
        login_frame.setMaximumWidth(500)
        login_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        form_layout = QVBoxLayout(login_frame)

        # Logo/Tiêu đề
        title_label = QLabel("🚗 HỆ THỐNG CẢNH BÁO")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        subtitle_label = QLabel("Giám sát buồn ngủ khi lái xe")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont('Arial', 12))
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")

        # Username field
        username_label = QLabel("Tên đăng nhập:")
        username_label.setFont(QFont('Arial', 10))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập tên đăng nhập")
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

        # Password field
        password_label = QLabel("Mật khẩu:")
        password_label.setFont(QFont('Arial', 10))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhập mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

        # Login button
        self.login_button = QPushButton("Đăng nhập")
        self.login_button.setMinimumHeight(45)
        self.login_button.setFont(QFont('Arial', 12, QFont.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)

        # Register link
        register_layout = QHBoxLayout()
        register_text = QLabel("Chưa có tài khoản?")
        register_text.setFont(QFont('Arial', 10))
        register_text.setStyleSheet("color: #7f8c8d;")

        self.register_link = QLabel('<a href="#" style="color: #3498db; text-decoration: none;">Đăng ký ngay</a>')
        self.register_link.setFont(QFont('Arial', 10, QFont.Bold))
        self.register_link.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_link.linkActivated.connect(self.handle_register_click)

        register_layout.addStretch()
        register_layout.addWidget(register_text)
        register_layout.addWidget(self.register_link)
        register_layout.addStretch()

        # Demo account info
        # demo_info = QLabel("💡 Đăng nhập nhanh: admin / admin")
        # demo_info.setAlignment(Qt.AlignCenter)
        # demo_info.setFont(QFont('Arial', 9))
        # demo_info.setStyleSheet("""
        #     QLabel {
        #         color: #27ae60;
        #         font-style: italic;
        #         background-color: #d5f4e6;
        #         border-radius: 3px;
        #         padding: 8px;
        #         border: 1px solid #27ae60;
        #     }
        # """)

        # Thêm các widget vào layout
        form_layout.addWidget(title_label)
        form_layout.addWidget(subtitle_label)
        form_layout.addSpacing(20)
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(15)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(25)
        form_layout.addWidget(self.login_button)
        form_layout.addSpacing(15)
        form_layout.addLayout(register_layout)
        form_layout.addSpacing(10)
        # form_layout.addWidget(demo_info)

        layout.addWidget(login_frame)

        # Set background cho toàn bộ view
        self.setStyleSheet("QWidget { background-color: #ecf0f1; }")
        self.setLayout(layout)

        # Enter để login
        self.password_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        """Xử lý đăng nhập"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Validation
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Kiểm tra đăng nhập mặc định admin/admin
        if username == "admin" and password == "admin":
            user_info = {
                'id': 0,
                'username': 'admin',
                'full_name': 'Administrator',
                'email': 'admin@system.local',
                'phone': '',
                'created_at': 'Default Account'
            }
            self.login_success.emit(user_info)
            self.clear_form()
            return

        # Kiểm tra đăng nhập với database
        success, user_info = self.db.login_user(username, password)

        if success:
            self.login_success.emit(user_info)
            self.clear_form()
        else:
            QMessageBox.warning(
                self,
                "Lỗi",
                "Tên đăng nhập hoặc mật khẩu không đúng!\n\n"
                "💡 Tip: Dùng admin/admin để đăng nhập nhanh"
            )

    def handle_register_click(self):
        """Xử lý khi click vào link đăng ký"""
        self.clear_form()
        self.register_clicked.emit()

    def clear_form(self):
        """Xóa form sau khi đăng nhập"""
        self.username_input.clear()
        self.password_input.clear()