from repository.drowsy_video_repo import get_drowsy_video_by_start_time
from repository.frame_repo import get_high_confidence_frames, insert_frame_to_dataset
from repository.dataset_repo import get_active_dataset, create_dataset, is_dataset_full

def process_drowsy_video_by_start_time(start_time: str, user_id: int, threshold: float = 0.7):
    """
    1. Tìm video bằng startTime
    2. Lấy frame có confidenceScore > threshold
    3. Thêm vào dataset hiện tại của user
    4. Nếu dataset đầy thì tạo dataset mới
    """
    video = get_drowsy_video_by_start_time(start_time)
    if not video:
        print(f"❌ Không tìm thấy video với startTime = {start_time}")
        return

    video_id = video["ID"]
    print("video id", video_id)
    frames = get_high_confidence_frames(video_id, threshold)

    if not frames:
        print(f"❗Không có frame nào đạt ngưỡng {threshold} trong video {video_id}.")
        return

    dataset = get_active_dataset(user_id)
    if not dataset:
        dataset_id = create_dataset(user_id, frame_limit=1000)
        print(f"🆕 Tạo dataset mới ID={dataset_id} cho user {user_id}.")
    else:
        dataset_id = dataset["ID"]

    for frame in frames:
        if is_dataset_full(dataset_id):
            dataset_id = create_dataset(user_id, frame_limit=1000)
            print(f"📦 Dataset đầy, tạo dataset mới ID={dataset_id}.")
        insert_frame_to_dataset(frame, dataset_id)

    print(f"✅ Đã xử lý {len(frames)} frame từ video startTime={start_time} cho user {user_id}.")
