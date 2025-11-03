from services.statistics_service import get_daily_drowsy_frequency, get_hourly_drowsy_frequency, \
    get_daily_detail_statistics

user_id = 0

# 1️⃣ 7 ngày qua
daily_stats = get_daily_drowsy_frequency(user_id, days=14)
detail = get_daily_detail_statistics(user_id=0, days=14)

# 2️⃣ Từng giờ trong 24h qua
hourly_stats = get_hourly_drowsy_frequency(user_id)

print("thống kế theo ngày:", daily_stats)
print("chi tiết theo ngày", detail)
print("24h qua:", hourly_stats)
from services.frame_selection_service import process_drowsy_video_by_start_time

# Giả sử muốn xử lý video có startTime = 20251031_215548 của user 40
process_drowsy_video_by_start_time(start_time="20251103_092810", user_id=0)
