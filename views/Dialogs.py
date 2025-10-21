from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QTextOption
from utils.sound_manager import get_sound_manager


class DrowsinessAlertDialog(QDialog):
    """Dialog cảnh báo buồn ngủ với âm thanh"""

    def __init__(self, parent=None, id=None):
        super().__init__(parent)
        self.setWindowTitle("⚠️ CẢNH BÁO BUỒN NGỦ")
        self.setModal(True)
        self.setFixedSize(500, 300)
        self.crurrent_id = id
        # Sound manager
        self.sound_manager = None
        self.sound_started = False

        self.init_ui()

        # Phát âm thanh sau khi UI đã sẵn sàng
        QTimer.singleShot(100, self.start_sound)

        # Auto close sau 10 giây
        self.auto_close_timer = QTimer()
        self.auto_close_timer.timeout.connect(self.auto_reject)
        self.auto_close_timer.start(3000)

    def start_sound(self):
        """Bắt đầu phát âm thanh"""
        try:
            self.sound_manager = get_sound_manager()
            self.sound_manager.play_alert(loop=True)
            self.sound_started = True
        except Exception as e:
            print(f"⚠️ Không thể phát âm thanh: {e}")

    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Warning icon
        warning_label = QLabel("⚠️")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("font-size: 70px;")

        # Title
        title_label = QLabel("PHÁT HIỆN DẤU HIỆU BUỒN NGỦ!")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet("color: #e67e22;")

        # Message
        message_label = QLabel("Bạn có đang buồn ngủ không?")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setFont(QFont('Arial', 13))
        message_label.setStyleSheet("color: #2c3e50;")

        # Sound indicator
        self.sound_label = QLabel("🔊 Âm thanh cảnh báo đang phát...")
        self.sound_label.setAlignment(Qt.AlignCenter)
        self.sound_label.setFont(QFont('Arial', 9))
        self.sound_label.setStyleSheet("""
            QLabel {
                color: #e67e22;
                font-style: italic;
                background-color: #fff3cd;
                padding: 5px;
                border-radius: 3px;
            }
        """)

        # Buttons
        button_layout = QHBoxLayout()

        yes_button = QPushButton("Có, tôi buồn ngủ")
        yes_button.setMinimumHeight(45)
        yes_button.setFont(QFont('Arial', 11, QFont.Bold))
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
        yes_button.clicked.connect(self.accept_and_stop_sound)

        no_button = QPushButton("Không, tôi tỉnh táo")
        no_button.setMinimumHeight(45)
        no_button.setFont(QFont('Arial', 11, QFont.Bold))
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
        no_button.clicked.connect(self.reject_and_stop_sound)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        # Add to main layout
        layout.addWidget(warning_label)
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addWidget(self.sound_label)
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

        # Blinking effect
        self.blink_timer = QTimer()
        self.blink_state = True
        self.blink_timer.timeout.connect(self.blink_sound_label)
        self.blink_timer.start(500)

    def blink_sound_label(self):
        """Nhấp nháy label âm thanh"""
        if self.blink_state:
            self.sound_label.setStyleSheet("""
                QLabel {
                    color: #e67e22;
                    font-style: italic;
                    background-color: #fff3cd;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)
        else:
            self.sound_label.setStyleSheet("""
                QLabel {
                    color: #c0392b;
                    font-style: italic;
                    background-color: #f8d7da;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)
        self.blink_state = not self.blink_state

    def accept_and_stop_sound(self):
        """Xác nhận và dừng âm thanh"""
        self.stop_sound()
        self.accept()

    def reject_and_stop_sound(self):
        """Từ chối và dừng âm thanh"""
        self.stop_sound()
        self.reject()

    def auto_reject(self):
        """Tự động từ chối khi timeout"""
        self.stop_sound()
        self.reject()

    def stop_sound(self):
        """Dừng âm thanh"""
        try:
            if self.sound_manager and self.sound_started:
                self.sound_manager.stop_alert()
                self.sound_started = False
        except Exception as e:
            print(f"⚠️ Lỗi dừng âm thanh: {e}")

        try:
            self.auto_close_timer.stop()
            self.blink_timer.stop()
        except:
            pass

    def closeEvent(self, event):
        """Xử lý khi đóng dialog"""
        self.stop_sound()
        event.accept()


class RestAlertDialog(QDialog):
    """Dialog cảnh báo nghỉ ngơi với line spacing tốt hơn"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🚨 CẢNH BÁO NGHIÊM TRỌNG")
        self.setModal(True)
        self.setFixedSize(550, 400)  # Tăng chiều cao một chút

        # Sound manager
        self.sound_manager = None
        self.sound_started = False

        self.init_ui()

        # Phát âm thanh sau khi UI sẵn sàng
        QTimer.singleShot(100, self.start_sound)

    def start_sound(self):
        """Bắt đầu phát âm thanh"""
        try:
            self.sound_manager = get_sound_manager()
            self.sound_manager.play_alert(loop=True)
            self.sound_started = True
        except Exception as e:
            print(f"⚠️ Không thể phát âm thanh: {e}")

    def init_ui(self):
        """Khởi tạo giao diện"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Warning icon
        warning_label = QLabel("🚨")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("font-size: 90px; margin: 0px;")

        # Title
        self.title_label = QLabel("NGUY HIỂM!")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Arial', 22, QFont.Bold))
        self.title_label.setStyleSheet("color: #e74c3c; margin: 5px 0px;")

        # Message container với HTML để kiểm soát line height
        message_text = """
        <div style='text-align: center; line-height: 1.8;'>
            <p style='margin: 8px 0; font-size: 14px; color: #2c3e50;'>
                <b>Bạn đã xác nhận buồn ngủ 3 lần liên tiếp!</b>
            </p>
            <p style='margin: 8px 0; font-size: 13px; color: #34495e;'>
                Việc tiếp tục lái xe rất nguy hiểm.
            </p>
            <p style='margin: 8px 0; font-size: 13px; color: #34495e;'>
                Vui lòng dừng lại và nghỉ ngơi!
            </p>
        </div>
        """

        message_label = QLabel(message_text)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        message_label.setTextFormat(Qt.RichText)
        message_label.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 15px;
            }
        """)

        # Sound indicator
        self.sound_label = QLabel("🚨 ÂM THANH CẢNH BÁO KHẨN CẤP 🚨")
        self.sound_label.setAlignment(Qt.AlignCenter)
        self.sound_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.sound_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #e74c3c;
                padding: 10px;
                border-radius: 5px;
                margin: 5px 0px;
            }
        """)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        stop_button = QPushButton("🛑 Dừng lại nghỉ ngơi")
        stop_button.setMinimumHeight(55)
        stop_button.setFont(QFont('Arial', 12, QFont.Bold))
        stop_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        stop_button.clicked.connect(self.accept_and_stop_sound)

        continue_button = QPushButton("⚠️ Tiếp tục\n(Nguy hiểm)")
        continue_button.setMinimumHeight(55)
        continue_button.setFont(QFont('Arial', 10))
        continue_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7a7b;
            }
        """)
        continue_button.clicked.connect(self.reject_and_stop_sound)

        button_layout.addWidget(stop_button, 65)
        button_layout.addWidget(continue_button, 35)

        # Add to layout
        layout.addWidget(warning_label)
        layout.addWidget(self.title_label)
        layout.addSpacing(5)
        layout.addWidget(message_label)
        layout.addSpacing(5)
        layout.addWidget(self.sound_label)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Style
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border: 4px solid #e74c3c;
                border-radius: 10px;
            }
        """)

        # Blinking timers
        self.title_blink_timer = QTimer()
        self.title_blink_state = True
        self.title_blink_timer.timeout.connect(self.blink_title)
        self.title_blink_timer.start(500)

        self.sound_blink_timer = QTimer()
        self.sound_blink_state = True
        self.sound_blink_timer.timeout.connect(self.blink_sound_label)
        self.sound_blink_timer.start(300)

    def blink_title(self):
        """Nhấp nháy tiêu đề"""
        if self.title_blink_state:
            self.title_label.setStyleSheet("color: #e74c3c; margin: 5px 0px;")
        else:
            self.title_label.setStyleSheet("color: #c0392b; margin: 5px 0px;")
        self.title_blink_state = not self.title_blink_state

    def blink_sound_label(self):
        """Nhấp nháy label âm thanh"""
        if self.sound_blink_state:
            self.sound_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background-color: #e74c3c;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px 0px;
                }
            """)
        else:
            self.sound_label.setStyleSheet("""
                QLabel {
                    color: white;
                    background-color: #c0392b;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px 0px;
                }
            """)
        self.sound_blink_state = not self.sound_blink_state

    def accept_and_stop_sound(self):
        """Xác nhận và dừng âm thanh"""
        self.stop_sound()
        self.accept()

    def reject_and_stop_sound(self):
        """Từ chối và dừng âm thanh"""
        self.stop_sound()
        self.reject()

    def stop_sound(self):
        """Dừng âm thanh"""
        try:
            if self.sound_manager and self.sound_started:
                self.sound_manager.stop_alert()
                self.sound_started = False
        except Exception as e:
            print(f"⚠️ Lỗi dừng âm thanh: {e}")

        try:
            self.title_blink_timer.stop()
            self.sound_blink_timer.stop()
        except:
            pass

    def closeEvent(self, event):
        """Xử lý khi đóng dialog"""
        self.stop_sound()
        event.accept()
