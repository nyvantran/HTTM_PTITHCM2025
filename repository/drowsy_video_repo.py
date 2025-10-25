from db.db import get_connection
from datetime import datetime


def create_drowsy_video(session_id: int, start_time: datetime, end_time: datetime):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO DrowsyVideo (sessionID, startTime, isLabel, endTime)
                       VALUES (?, ?, 0, ?)
                       """, (session_id, start_time.format(), end_time))
        conn.commit()
        return cursor.lastrowid


def end_drowsy_video(end_time: datetime, user_label: bool = None, user_choice_label: str = None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE DrowsyVideo
                       SET userChoiceLabel = ?,
                           isLabel         = ?
                       WHERE endTime = ?
                       """, (user_choice_label, user_label, end_time))
        conn.commit()


def get_unlabeled_videos():
    with get_connection() as conn:
        cursor = conn.execute("""
                              SELECT ID, sessionID, startTime, endTime
                              FROM DrowsyVideo
                              WHERE isLabel = 0
                              """)
        return cursor.fetchall()
