from db.db import get_connection
from datetime import datetime

def create_drowsy_video(session_id: int, start_time: datetime):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DrowsyVideo (sessionID, startTime, isLabel)
            VALUES (?, ?, 0)
        """, (session_id, start_time.isoformat()))
        conn.commit()
        return cursor.lastrowid

def end_drowsy_video(video_id: int, end_time: datetime, user_label: bool = None, user_choice_label: str = None):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE DrowsyVideo
            SET endTime = ?, userChoiceLabel = ?, isLabel = ?
            WHERE ID = ?
        """, (end_time.isoformat(), user_choice_label, 1 if user_label is not None else 0, video_id))
        conn.commit()

def get_unlabeled_videos():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT ID, sessionID, startTime, endTime
            FROM DrowsyVideo
            WHERE isLabel = 0
        """)
        return cursor.fetchall()