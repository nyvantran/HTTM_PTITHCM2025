from repository.drowsy_video_repo import get_unlabeled_drowsy_videos_by_user

videos = get_unlabeled_drowsy_videos_by_user(0)
for v in videos:
    print(v)

