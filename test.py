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
