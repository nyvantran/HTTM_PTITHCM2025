from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QMovie


class DrowsinessAlertDialog(QDialog):
    """Dialog cảnh báo buồn ngủ"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚠️ CẢNH BÁO BUỒN NGỦ")
        self.setModal(True)
        self.setFixedSize(500, 300)
        self.init_ui()

        # Auto close sau 10 giây (coi như không buồn ngủ)
        self.timer = QTimer()
        self.timer.timeout.connect(self.reject)
        self.timer.start(10000)

    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Warning icon và text
        warning_label = QLabel("⚠️")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("font-size: 80px;")

        title_label = QLabel("PHÁT HIỆN DẤU HIỆU BUỒN NGỦ!")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        title_label.setStyleSheet("color: #e67e22;")

        message_label = QLabel("Bạn có đang buồn ngủ không?")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setFont(QFont('Arial', 14))
        message_label.setStyleSheet("color: #2c3e50;")

        # Buttons
        button_layout = QHBoxLayout()

        yes_button = QPushButton("Có, tôi buồn ngủ")
        yes_button.setMinimumHeight(50)
        yes_button.setFont(QFont('Arial', 12, QFont.Bold))
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        yes_button.clicked.connect(self.accept)

        no_button = QPushButton("Không, tôi tỉnh táo")
        no_button.setMinimumHeight(50)
        no_button.setFont(QFont('Arial', 12, QFont.Bold))
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        no_button.clicked.connect(self.reject)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        # Add to main layout
        layout.addWidget(warning_label)
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Style dialog
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 3px solid #e67e22;
                border-radius: 10px;
            }
        """)


class RestAlertDialog(QDialog):
    """Dialog cảnh báo cần nghỉ ngơi"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🚨 CẢNH BÁO NGHIÊM TRỌNG")
        self.setModal(True)
        self.setFixedSize(550, 350)
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Warning icon
        warning_label = QLabel("🚨")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("font-size: 100px;")

        # Title
        title_label = QLabel("NGUY HIỂM!")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet("color: #e74c3c;")

        # Message
        message_label = QLabel("Bạn đã xác nhận buồn ngủ 3 lần liên tiếp!\n\n"
                               "Việc tiếp tục lái xe rất nguy hiểm.\n"
                               "Vui lòng dừng lại và nghỉ ngơi!")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setFont(QFont('Arial', 13))
        message_label.setStyleSheet("color: #2c3e50; line-height: 1.5;")

        # Buttons
        button_layout = QHBoxLayout()

        stop_button = QPushButton("🛑 Dừng lại nghỉ ngơi")
        stop_button.setMinimumHeight(55)
        stop_button.setFont(QFont('Arial', 13, QFont.Bold))
        stop_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        stop_button.clicked.connect(self.accept)

        continue_button = QPushButton("⚠️ Tiếp tục lái (Không khuyến khích)")
        continue_button.setMinimumHeight(55)
        continue_button.setFont(QFont('Arial', 11))
        continue_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        continue_button.clicked.connect(self.reject)

        button_layout.addWidget(stop_button, 60)
        button_layout.addWidget(continue_button, 40)

        # Add to main layout
        layout.addWidget(warning_label)
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Style dialog
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 4px solid #e74c3c;
                border-radius: 10px;
            }
        """)

        # Blinking effect for title
        self.blink_timer = QTimer()
        self.blink_state = True
        self.title_label_ref = title_label
        self.blink_timer.timeout.connect(self.blink_title)
        self.blink_timer.start(500)

    def blink_title(self):
        """Nhấp nháy tiêu đề"""
        if self.blink_state:
            self.title_label_ref.setStyleSheet("color: #e74c3c;")
        else:
            self.title_label_ref.setStyleSheet("color: #c0392b;")
        self.blink_state = not self.blink_state