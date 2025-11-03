from datetime import datetime
from repository import frame_repo, drowsy_video_repo, dataset_repo
from db.db import get_connection

MAX_DATASET_SIZE = 5000
CONFIDENCE_THRESHOLD = 0.8
COOLDOWN_SEC = 5

class MonitoringService:
    def __init__(self, user_id: int, session_id: int):
        self.user_id = user_id
        self.session_id = session_id
        self.current_video_id = None
        self.start_time = None
        self.last_violation_end = None
        self.current_frames = []  # Buffer frames until confirmation

        # Initialize dataset
        self.dataset = dataset_repo.get_active_dataset(user_id)
        if not self.dataset:
            self.dataset_id = dataset_repo.create_dataset(user_id, MAX_DATASET_SIZE)
        else:
            self.dataset_id = self.dataset[0]  # dataset["ID"]

    def start_violation(self):
        """Start a new drowsy video when drowsy ratio ≥ 0.7 for ≥ 3 seconds."""
        now = datetime.now()

        # Check cooldown
        if self.last_violation_end and (now - self.last_violation_end).total_seconds() < COOLDOWN_SEC:
            return None

        self.start_time = now
        self.current_video_id = drowsy_video_repo.create_drowsy_video(self.session_id, now)
        self.current_frames = []
        return self.current_video_id

    def end_violation(self, user_label: bool = None, user_choice_label: str = None):
        """End the drowsy video and save frames if confirmed."""
        if not self.current_video_id:
            return

        end_time = datetime.now()
        drowsy_video_repo.end_drowsy_video(self.current_video_id, end_time, user_label, user_choice_label)

        # Save frames for confirmed drowsy videos
        if user_label:
            for frame_path, confidence, predicted_drowsy in self.current_frames:
                if confidence >= CONFIDENCE_THRESHOLD:
                    frame_repo.insert_frame(
                        self.current_video_id, confidence, predicted_drowsy, frame_path, self.dataset_id
                    )

            # Check if dataset is full
            if dataset_repo.count_dataset_frames(self.dataset_id) >= MAX_DATASET_SIZE:
                dataset_repo.mark_dataset_used(self.dataset_id)
                self.dataset_id = dataset_repo.create_dataset(self.user_id, MAX_DATASET_SIZE)

        self.last_violation_end = end_time
        self.current_video_id = None
        self.start_time = None
        self.current_frames = []

    def save_frame(self, frame_path: str, confidence: float, predicted_drowsy: bool):
        """Buffer frame until user confirmation."""
        if not self.current_video_id:
            return None
        self.current_frames.append((frame_path, confidence, predicted_drowsy))
        return len(self.current_frames)