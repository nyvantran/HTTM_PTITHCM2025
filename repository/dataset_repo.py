from db.db import get_connection

def create_dataset(userID, frameLimit, status="SPENDING"):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO Dataset (userID, frameLimit, status)
            VALUES (?, ?, ?)
        """, (userID, frameLimit, status))
        conn.commit()

def get_datasets_by_user(userID):
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM Dataset WHERE userID = ?", (userID,))
        return [dict(row) for row in cur.fetchall()]

def update_dataset_status(dataset_id, new_status):
    with get_connection() as conn:
        conn.execute("UPDATE Dataset SET status = ? WHERE ID = ?", (new_status, dataset_id))
        conn.commit()
