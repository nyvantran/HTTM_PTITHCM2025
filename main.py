import sys
import os

# Suppress deprecation warnings
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set environment variable để tắt OpenCV warnings
os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'

from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from views.LoginView import LoginView
from views.register_view import RegisterView
from views.DashboardView import DashboardView
from utils.database import UserDatabase
from utils.sound_manager import cleanup_sound_manager
from db.schema import create_tables


class MainWindow(QMainWindow):
    """Main Window để quản lý các view"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống cảnh báo buồn ngủ")

        # Giảm kích thước và cho phép resize
        self.setGeometry(100, 50, 1000, 650)
        self.setMinimumSize(900, 600)

        # Khởi tạo database
        self.db = UserDatabase()

        # Current user info
        self.current_user = None

        # Tạo stacked widget để chứa các view
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Khởi tạo các view
        self.init_views()

        # Hiển thị màn hình đăng nhập đầu tiên
        self.show_login()
        create_tables()

    def init_views(self):
        """Khởi tạo tất cả các view"""
        # Login View
        self.login_view = LoginView()
        self.login_view.login_success.connect(self.show_dashboard)
        self.login_view.register_clicked.connect(self.show_register)

        # Register View
        self.register_view = RegisterView()
        self.register_view.register_success.connect(self.show_login)
        self.register_view.back_to_login.connect(self.show_login)

        # Dashboard View
        self.dashboard_view = DashboardView()
        self.dashboard_view.set_database(self.db)
        self.dashboard_view.logout_signal.connect(self.show_login)

        # Thêm các view vào stacked widget
        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.addWidget(self.register_view)
        self.stacked_widget.addWidget(self.dashboard_view)

    def show_login(self):
        """Chuyển sang màn hình đăng nhập"""
        self.stacked_widget.setCurrentWidget(self.login_view)
        self.setWindowTitle("Đăng nhập - Hệ thống cảnh báo buồn ngủ")
        self.current_user = None

    def show_register(self):
        """Chuyển sang màn hình đăng ký"""
        self.stacked_widget.setCurrentWidget(self.register_view)
        self.setWindowTitle("Đăng ký tài khoản - Hệ thống cảnh báo buồn ngủ")

    def show_dashboard(self, user_info):
        """Chuyển sang màn hình dashboard"""
        self.current_user = user_info
        self.dashboard_view.set_user_info(user_info)
        self.stacked_widget.setCurrentWidget(self.dashboard_view)
        self.setWindowTitle(f"Dashboard - {user_info['full_name']} (@{user_info['username']})")

    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng"""
        print("\n🔄 Đang đóng ứng dụng...")

        try:
            # Dừng camera nếu đang chạy
            if hasattr(self.dashboard_view, 'camera_thread') and self.dashboard_view.camera_thread:
                print("📹 Đang dừng camera...")
                self.dashboard_view.stop_monitoring()

            # Cleanup sound manager
            print("🔇 Đang dừng âm thanh...")
            cleanup_sound_manager()

            # Đóng database
            print("💾 Đang đóng database...")
            self.db.close()

            print("✅ Ứng dụng đã đóng an toàn\n")

        except Exception as e:
            print(f"⚠️ Lỗi khi đóng: {e}")

        event.accept()


def main():
    # Tạo application
    app = QApplication(sys.argv)

    # Thiết lập style
    app.setStyle('Fusion')

    print("=" * 60)
    print("🚀 HỆ THỐNG CẢNH BÁO BUỒN NGỦ")
    print("=" * 60)
    print()

    # Tạo và hiển thị window
    window = MainWindow()
    window.show()

    # Chạy event loop
    exit_code = app.exec_()

    # Cleanup trước khi thoát
    print("\n" + "=" * 60)
    cleanup_sound_manager()
    print("=" * 60)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()