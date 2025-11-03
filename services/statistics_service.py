from db.db import get_connection
from datetime import datetime

def get_daily_drowsy_frequency(user_id, days=7):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
            SUBSTR(DrowsyVideo.startTime, 1, 8) AS raw_date,
            COUNT(*) AS count
        FROM DrowsyVideo
        JOIN Session ON DrowsyVideo.sessionID = Session.ID
        WHERE Session.userID = ?
        AND raw_date >= strftime('%Y%m%d', datetime('now', ?))
        GROUP BY raw_date
        ORDER BY raw_date ASC
    """

    cursor.execute(query, (user_id, f'-{days} days'))
    rows = cursor.fetchall()

    # Chuyển "20251031" → "2025-10-31"
    result = [
        {'date': f"{r[0][:4]}-{r[0][4:6]}-{r[0][6:8]}", 'count': r[1]}
        for r in rows
    ]
    return result

def get_hourly_drowsy_frequency(user_id: int):
    """
    Trả về tần suất buồn ngủ theo từng giờ trong 24h qua.
    
    Returns:
        List[dict]: [
            { 'hour': '2025-10-31 13:00', 'count': 3 },
            ...
        ]
    """
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT 
                SUBSTR(DrowsyVideo.startTime, 1, 8) || SUBSTR(DrowsyVideo.startTime, 9, 3) AS raw_time,
                SUBSTR(DrowsyVideo.startTime, 1, 8) || ' ' || SUBSTR(DrowsyVideo.startTime, 10, 2) AS hour_key,
                COUNT(*) AS count
            FROM DrowsyVideo
            JOIN Session ON DrowsyVideo.sessionID = Session.ID
            WHERE Session.userID = ?
              AND DrowsyVideo.startTime >= strftime('%Y%m%d_%H%M%S', datetime('now', '-24 hours'))
            GROUP BY hour_key
            ORDER BY hour_key ASC
        """, (user_id,))

        rows = cursor.fetchall()

        # format kết quả cho dễ đọc
        results = []
        for hour_key, count in [(r[1], r[2]) for r in rows]:
            # hour_key = '20251031 21' → '2025-10-31 21:00'
            formatted_hour = f"{hour_key[:4]}-{hour_key[4:6]}-{hour_key[6:8]} {hour_key[9:]}:00"
            results.append({'hour': formatted_hour, 'count': count})
        return results

def get_daily_detail_statistics(user_id: int, days: int = 7):
    """
    Trả về thống kê chi tiết theo ngày:
      - Số video cảnh báo (model detect)
      - Số video người dùng xác nhận (bất kỳ label != NULL)
      - Tổng thời gian lái trong ngày
    """
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT 
                SUBSTR(DrowsyVideo.startTime, 1, 8) AS raw_date,
                COUNT(DrowsyVideo.ID) AS alert_count,
                SUM(CASE WHEN DrowsyVideo.userChoiceLabel IS NOT NULL THEN 1 ELSE 0 END) AS confirmed_count,
                MIN(Session.startTime) AS session_start,
                MAX(Session.endTime) AS session_end
            FROM DrowsyVideo
            JOIN Session ON DrowsyVideo.sessionID = Session.ID
            WHERE Session.userID = ?
              AND DrowsyVideo.startTime >= strftime('%Y%m%d_%H%M%S', datetime('now', ?))
            GROUP BY raw_date
            ORDER BY raw_date DESC
        """, (user_id, f'-{days} days'))

        rows = cursor.fetchall()

        results = []
        for raw_date, alert_count, confirmed_count, start, end in rows:
            # format ngày: 20251027 → 27/10/2025
            date_fmt = f"{raw_date[6:8]}/{raw_date[4:6]}/{raw_date[:4]}"

            # Tính tổng thời gian lái xe (end - start)
            drive_time = "--"
            if start and end:
                try:
                    s = datetime.strptime(start, "%Y%m%d_%H%M%S")
                    e = datetime.strptime(end, "%Y%m%d_%H%M%S")
                    delta = e - s
                    hours, remainder = divmod(delta.seconds, 3600)
                    minutes = remainder // 60
                    drive_time = f"{hours}h {minutes}m"
                except Exception:
                    pass

            results.append({
                "date": date_fmt,
                "alert_count": alert_count or 0,
                "confirmed_count": confirmed_count or 0,
                "driving_time": drive_time
            })

        return results
