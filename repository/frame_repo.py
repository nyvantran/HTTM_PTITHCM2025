from db.db import get_connection
from datetime import datetime

def insert_frame(drowsy_video_id: int, confidence: float, prediction: bool, image_path: str, dataset_id: int = None):
    """Insert a frame into the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Frame (drowsyVideoID, confidenceScore, modelPrediction, imageURL, datasetID, createdAt)
            VALUES (?, ?, ?, ?, NULL, ?)
        """, (drowsy_video_id, confidence, prediction, image_path, dataset_id, datetime.now().isoformat()))
        conn.commit()
        return cursor.lastrowid

def get_frames_by_video(video_id: int):
    """Retrieve all frames for a given video."""
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT ID, confidenceScore, modelPrediction, imageURL, createdAt
            FROM Frame
            WHERE drowsyVideoID = ?
            ORDER BY createdAt ASC
        """, (video_id,))
        return cursor.fetchall()

def delete_frames_by_video(video_id: int):
    """Delete all frames for a given video."""
    with get_connection() as conn:
        conn.execute("DELETE FROM Frame WHERE drowsyVideoID = ?", (video_id,))
        conn.commit()