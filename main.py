import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from views.LoginView import LoginView
from views.register_view import RegisterView
from views.DashboardView import DashboardView
from utils.database import UserDatabase


class MainWindow(QMainWindow):
    """Main Window để quản lý các view"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống cảnh báo buồn ngủ")
        # self.setGeometry(100, 100, 1200, 300)
        self.setGeometry(100, 50, 1000, 650)  # Giảm từ 1200x700
        self.setMinimumSize(900, 600)  # Kích thước tối thiểu
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

    def init_views(self):
        """Khởi tạo tất cả các view"""
        # Login View
        self.login_view = LoginView(self.db)
        self.login_view.login_success.connect(self.show_dashboard)
        self.login_view.register_clicked.connect(self.show_register)

        # Register View
        self.register_view = RegisterView(self.db)
        self.register_view.register_success.connect(self.show_login)
        self.register_view.back_to_login.connect(self.show_login)

        # Dashboard View
        self.dashboard_view = DashboardView()
        self.dashboard_view.set_database(self.db)  # Pass database reference
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
        print("🔄 Đang đóng ứng dụng...")

        # Dừng camera nếu đang chạy
        if hasattr(self.dashboard_view, 'camera_thread') and self.dashboard_view.camera_thread:
            print("📹 Đang dừng camera...")
            self.dashboard_view.stop_monitoring()

        # Đóng database
        print("💾 Đang đóng database...")
        self.db.close()

        print("✅ Ứng dụng đã đóng an toàn")
        event.accept()


def main():
    app = QApplication(sys.argv)

    # Thiết lập style cho app
    app.setStyle('Fusion')

    # Suppress PyQt5 deprecation warnings
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    print("🚀 Khởi động ứng dụng...")
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
