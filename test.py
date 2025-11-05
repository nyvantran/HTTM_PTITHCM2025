from repository.drowsy_video_repo import get_unlabeled_drowsy_videos_by_user, get_all_drowsy_videos_by_user
from repository.frame_repo import get_frames_by_video
import datetime

# data = get_frames_by_video(video_id=114)
# data = [dict(frame)["imageURL"] for frame in data]
#
# print(data)

# data = get_all_drowsy_videos_by_user(user_id=2)
# print(data)
day1 = datetime.datetime.fromisoformat("20251104_145740")
day2 = datetime.datetime.fromisoformat("20251104_145744")
diff = day2 - day1
print(diff.seconds)  # Output: 1
