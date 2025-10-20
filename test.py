import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer


def _play_alert_sound():
    """Phát âm thanh cảnh báo bằng QMediaPlayer"""
    try:
        sound_path = os.path.join(os.path.dirname(__file__), 'assets', 'alert.mp3')
        abs_path = os.path.abspath(sound_path)  # QUrl hoạt động tốt nhất với đường dẫn tuyệt đối

        if not os.path.exists(abs_path):
            print(f"File not found: {abs_path}")
            return

        print(f"Playing: {abs_path}")

        # 1. Tạo một QApplication (BẮT BUỘC để có event loop)
        # Kiểm tra xem app đã tồn tại chưa (nếu đây là 1 phần của app lớn)
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # 2. Tạo QMediaPlayer
        player = QMediaPlayer()

        # 3. Tạo hàm để thoát app khi chơi xong
        def handle_status_changed(status):
            if status == QMediaPlayer.EndOfMedia:
                print("Playback finished.")
                app.quit()  # Thoát khỏi event loop
            elif status == QMediaPlayer.Error:
                print("Error playing media:", player.errorString())
                app.quit()

        player.mediaStatusChanged.connect(handle_status_changed)

        # 4. Thiết lập file và chơi
        url = QUrl.fromLocalFile(abs_path)
        player.setMedia(QMediaContent(url))
        player.play()

        # 5. Chạy event loop (để giữ cho chương trình sống)
        # Chương trình sẽ bị kẹt ở dòng này cho đến khi app.quit() được gọi
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Error playing sound: {e}")


if __name__ == "__main__":
    _play_alert_sound()
