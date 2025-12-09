from abc import ABC, abstractmethod
from bisect import bisect_left, insort
from collections import defaultdict
from dataclasses import dataclass
from typing import List
import os


# ==============================
# ✅ Core Data Model
# ==============================

@dataclass(order=True)
class Video:
    start_time: int
    end_time: int
    camera_id: str
    file_path: str


# ==============================
# ✅ Video Source Interface
# ==============================

class VideoSource(ABC):
    @abstractmethod
    def fetch_all_videos(self) -> List[Video]:
        pass


# ==============================
# ✅ File System Video Source
# ==============================

class FileSystemVideoSource(VideoSource):

    def __init__(self, base_directory: str):
        self.base_directory = base_directory

    def fetch_all_videos(self) -> List[Video]:
        videos = []

        for file_name in os.listdir(self.base_directory):
            if not file_name.endswith(".mp4"):
                continue

            try:
                camera_id, start_ts, end_ts = file_name.replace(".mp4", "").split("_")
                video = Video(
                    camera_id=camera_id,
                    start_time=int(start_ts),
                    end_time=int(end_ts),
                    file_path=os.path.join(self.base_directory, file_name)
                )
                videos.append(video)

            except ValueError:
                print(f"Skipping invalid file: {file_name}")

        return videos


# ==============================
# ✅ S3 Video Source (Mock)
# ==============================

class S3VideoSource(VideoSource):

    def fetch_all_videos(self) -> List[Video]:
        # In real world → fetch using boto3
        return [
            Video("camera-A123", 1658648000, 1658650000, "s3://bucket/video1.mp4"),
            Video("camera-A123", 1658650100, 1658651000, "s3://bucket/video2.mp4"),
        ]


# ==============================
# ✅ Video Manager (Main Engine)
# ==============================

class VideoManager:

    def __init__(self):
        # camera_id → sorted list of videos (by start_time)
        self.camera_index = defaultdict(list)

    def add_video(self, video: Video):
        # Insert while maintaining sorted order
        insort(self.camera_index[video.camera_id], video)

    def load_from_source(self, source: VideoSource):
        videos = source.fetch_all_videos()
        for video in videos:
            self.add_video(video)

    def get_videos(self, camera_id: str, start_range: int, end_range: int) -> List[Video]:
        """
        Returns all videos for a camera overlapping time range
        """
        if camera_id not in self.camera_index:
            return []

        videos = self.camera_index[camera_id]

        # Binary search for first possible overlap
        i = bisect_left(videos, Video(start_range, 0, camera_id, ""))

        result = []

        while i < len(videos):
            video = videos[i]

            # Stop if video starts after range
            if video.start_time > end_range:
                break

            # Overlapping check
            if video.end_time >= start_range:
                result.append(video)

            i += 1

        return result


# ==============================
# ✅ Demo Usage
# ==============================

if __name__ == "__main__":

    manager = VideoManager()

    # Load from File System
    fs_source = FileSystemVideoSource("videos/")
    # manager.load_from_source(fs_source)

    # Load from S3
    s3_source = S3VideoSource()
    manager.load_from_source(s3_source)

    # Manual Add
    manager.add_video(Video("camera-A123", 1658648399, 1658655599, "/videos/v1.mp4"))
    manager.add_video(Video("camera-A123", 1658656000, 1658659000, "/videos/v2.mp4"))

    # Query videos between time range
    start_time = 1658656000  # 12 PM
    end_time = 1658659000    # 1 PM

    results = manager.get_videos("camera-A123", start_time, end_time)
    print(results)

    for v in results:
        print(v)
