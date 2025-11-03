from db.db import get_connection
from datetime import datetime
import sqlite3

def insert_drowsy_video(session_id: int, start_time: datetime, end_time: datetime = None):
    # Định dạng ngày tháng là YYYY-MM-DDTHH:MM:SS
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO DrowsyVideo (sessionID, startTime, endTime, userChoiceLabel)
                VALUES (?, ?, ?, NULL)
            """, (
                session_id,
                start_time.isoformat(),
                end_time.isoformat() if end_time else None
            ))
            conn.commit()
            return cursor.lastrowid

    except sqlite3.Error as e:
        print(f"❌ Database error when inserting DrowsyVideo: {e}")
        if 'conn' in locals():
            conn.rollback()
        return None

    except Exception as e:
        print(f"⚠️ Unexpected error in insert_drowsy_video: {e}")
        if 'conn' in locals():
            conn.rollback()
        return None

def update_user_choice_by_start_time(start_time: str, user_choice: bool):
    """
    Cập nhật trường userChoiceLabel trong bảng DrowsyVideo
    dựa vào giá trị startTime.

    Args:
        start_time (str): thời gian bắt đầu video (ISO 8601, ví dụ '2025-10-22T20:46:52')
        user_choice (bool): nhãn người dùng xác nhận (True/False)
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE DrowsyVideo
                SET userChoiceLabel = ?
                WHERE startTime = ?
            """, (user_choice, start_time))
            conn.commit()

            if cursor.rowcount == 0:
                print(f"⚠️ Không có bản ghi nào có startTime = {start_time}")
            else:
                print(f"✅ Đã cập nhật {cursor.rowcount} bản ghi userChoiceLabel = {user_choice}")
            return cursor.rowcount

    except sqlite3.Error as e:
        print(f"❌ Lỗi database khi cập nhật userChoiceLabel: {e}")
        if 'conn' in locals():
            conn.rollback()
        return 0

def create_drowsy_video(session_id: int, start_time: datetime, end_time: datetime):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO DrowsyVideo (sessionID, startTime, isLabel, endTime)
                       VALUES (?, ?, 0, ?)
                       """, (session_id, start_time.format(), end_time))
        conn.commit()
        return cursor.lastrowid
    
def get_drowsy_video_by_start_time(start_time: str):
    """
    Truy vấn video theo startTime (định dạng 'YYYYMMDD_HHMMSS')
    """
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT ID, sessionID, startTime, endTime, userChoiceLabel
            FROM DrowsyVideo
            WHERE startTime = ?
        """, (start_time,))
        return cursor.fetchone()

