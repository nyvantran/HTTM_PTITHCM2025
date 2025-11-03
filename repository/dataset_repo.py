from db.db import get_connection
from datetime import datetime

def create_dataset(user_id: int, frame_limit: int, expires_at: datetime = None):
    """Create a new dataset for a user."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Dataset (userID, frameLimit, status, expiresAt, createdAt)
            VALUES (?, ?, 'SPENDING', ?, ?)
        """, (user_id, frame_limit, expires_at.isoformat() if expires_at else None, datetime.now().isoformat()))
        conn.commit()
        return cursor.lastrowid

def get_active_dataset(user_id: int):
    """Retrieve the active dataset for a user."""
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT ID, userID, frameLimit, status, expiresAt, createdAt
            FROM Dataset
            WHERE userID = ? AND status = 'SPENDING'
            ORDER BY createdAt DESC LIMIT 1
        """, (user_id,))
        return cursor.fetchone()

def mark_dataset_used(dataset_id: int):
    """Mark a dataset as used."""
    with get_connection() as conn:
        conn.execute("""
            UPDATE Dataset SET status = 'USED' WHERE ID = ?
        """, (dataset_id,))
        conn.commit()

def count_dataset_frames(dataset_id: int):
    """Count the number of frames in a dataset."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM Frame WHERE datasetID = ?", (dataset_id,))
        return cursor.fetchone()[0]

def get_dataset_limit(dataset_id: int):
    with get_connection() as conn:
        cursor = conn.execute("SELECT frameLimit FROM Dataset WHERE ID = ?", (dataset_id,))
        row = cursor.fetchone()
        return row["frameLimit"] if row else None

def is_dataset_full(dataset_id: int):
    """Kiểm tra dataset có đầy chưa."""
    limit = get_dataset_limit(dataset_id)
    if not limit:
        return False
    count = count_dataset_frames(dataset_id)
    return count >= limit
