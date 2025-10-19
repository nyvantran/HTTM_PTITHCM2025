from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon
from utils.database import UserDatabase


class RegisterView(QWidget):
    """View đăng ký tài khoản"""

    # Signal phát ra khi đăng ký thành công
    register_success = pyqtSignal()
    back_to_login = pyqtSignal()

    def __init__(self, db: UserDatabase):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Frame chứa form đăng ký
        register_frame = QFrame()
        register_frame.setMaximumWidth(600)
        register_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 5px;
            }
        """)

        form_layout = QVBoxLayout(register_frame)

        # Tiêu đề
        title_label = QLabel("📝 ĐĂNG KÝ TÀI KHOẢN")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")

        subtitle_label = QLabel("Tạo tài khoản mới")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont('Arial', 12))
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")

        # Input style
        input_style = """
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
                min-height: 35px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """

        # Họ tên
        fullname_label = QLabel("Họ và tên: *")
        fullname_label.setFont(QFont('Arial', 10))
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Nhập họ và tên đầy đủ")
        self.fullname_input.setStyleSheet(input_style)

        # Username
        username_label = QLabel("Tên đăng nhập: *")
        username_label.setFont(QFont('Arial', 10))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ít nhất 3 ký tự")
        self.username_input.setStyleSheet(input_style)

        # Email
        email_label = QLabel("Email:")
        email_label.setFont(QFont('Arial', 10))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email@example.com (không bắt buộc)")
        self.email_input.setStyleSheet(input_style)

        # Phone
        phone_label = QLabel("Số điện thoại:")
        phone_label.setFont(QFont('Arial', 10))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("0123456789 (không bắt buộc)")
        self.phone_input.setStyleSheet(input_style)

        # Password
        password_label = QLabel("Mật khẩu: *")
        password_label.setFont(QFont('Arial', 10))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ít nhất 6 ký tự")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)

        # Confirm Password
        confirm_password_label = QLabel("Xác nhận mật khẩu: *")
        confirm_password_label.setFont(QFont('Arial', 10))
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Nhập lại mật khẩu")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(input_style)

        # Required field note
        note_label = QLabel("* Trường bắt buộc")
        note_label.setFont(QFont('Arial', 9))
        note_label.setStyleSheet("color: #e74c3c; font-style: italic;")

        # Buttons
        button_layout = QHBoxLayout()

        # Back button
        back_button = QPushButton("← Quay lại")
        back_button.setMinimumHeight(45)
        back_button.setFont(QFont('Arial', 11))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        back_button.clicked.connect(self.handle_back)

        # Register button
        self.register_button = QPushButton("Đăng ký")
        self.register_button.setMinimumHeight(45)
        self.register_button.setFont(QFont('Arial', 12, QFont.Bold))
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.register_button.clicked.connect(self.handle_register)

        button_layout.addWidget(back_button, 35)
        button_layout.addWidget(self.register_button, 65)

        # Thêm các widget vào layout
        form_layout.addWidget(title_label)
        form_layout.addWidget(subtitle_label)
        form_layout.addSpacing(15)

        form_layout.addWidget(fullname_label)
        form_layout.addWidget(self.fullname_input)
        form_layout.addSpacing(10)

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(10)

        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addSpacing(10)

        form_layout.addWidget(phone_label)
        form_layout.addWidget(self.phone_input)
        form_layout.addSpacing(10)

        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(10)

        form_layout.addWidget(confirm_password_label)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addSpacing(5)

        form_layout.addWidget(note_label)
        form_layout.addSpacing(15)

        form_layout.addLayout(button_layout)

        layout.addWidget(register_frame)

        # Set background
        self.setStyleSheet("QWidget { background-color: #ecf0f1; }")
        self.setLayout(layout)

        # Enter để register
        self.confirm_password_input.returnPressed.connect(self.handle_register)

    def handle_register(self):
        """Xử lý đăng ký"""
        # Lấy dữ liệu
        full_name = self.fullname_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Validation cơ bản
        if not full_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập họ tên!")
            self.fullname_input.setFocus()
            return

        if not username:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên đăng nhập!")
            self.username_input.setFocus()
            return

        if not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mật khẩu!")
            self.password_input.setFocus()
            return

        # Kiểm tra mật khẩu khớp
        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            self.confirm_password_input.setFocus()
            self.confirm_password_input.selectAll()
            return

        # Kiểm tra email format (nếu có)
        if email and '@' not in email:
            QMessageBox.warning(self, "Lỗi", "Email không hợp lệ!")
            self.email_input.setFocus()
            return

        # Đăng ký
        try:
            success = self.db.register_user(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone
            )

            if success:
                QMessageBox.information(
                    self,
                    "Thành công",
                    f"✅ Đăng ký thành công!\n\n"
                    f"Tài khoản: {username}\n"
                    f"Họ tên: {full_name}\n\n"
                    f"Vui lòng đăng nhập để tiếp tục."
                )
                self.clear_form()
                self.register_success.emit()

        except ValueError as e:
            QMessageBox.warning(self, "Lỗi", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra:\n{str(e)}")

    def handle_back(self):
        """Quay lại màn hình đăng nhập"""
        self.clear_form()
        self.back_to_login.emit()

    def clear_form(self):
        """Xóa form"""
        self.fullname_input.clear()
        self.username_input.clear()
        self.email_input.clear()
        self.phone_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
