import cv2
import os
from datetime import datetime

class VideoExporter:
    def __init__(self, video_path, verbose=True):  # Set verbose=True by default
        self.video_path = video_path
        self.output_dir = os.path.dirname(os.path.abspath(video_path))
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_path_with_blobs = os.path.join(self.output_dir, f"output_with_blobs_{self.timestamp}.mp4")
        self.output_path_blobs_only = os.path.join(self.output_dir, f"output_blobs_only_{self.timestamp}.mp4")
        self.out_with_blobs = None
        self.out_blobs_only = None
        self.verbose = verbose

    def initialize(self):
        cap = cv2.VideoCapture(self.video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.release()

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out_with_blobs = cv2.VideoWriter(self.output_path_with_blobs, fourcc, fps, (frame_width, frame_height))
        self.out_blobs_only = cv2.VideoWriter(self.output_path_blobs_only, fourcc, fps, (frame_width, frame_height))

        if self.verbose:
            print(f"Initialized video exporters:")
            print(f"  - Output with blobs: {self.output_path_with_blobs}")
            print(f"  - Output blobs only: {self.output_path_blobs_only}")

    def write_frames(self, frame_with_blobs, blob_overlay, frame_count):
        if self.out_with_blobs is not None:
            self.out_with_blobs.write(frame_with_blobs)
        if self.out_blobs_only is not None:
            self.out_blobs_only.write(blob_overlay)

        if self.verbose and frame_count % 10 == 0:  # Print progress every 10 frames
            print(f"Processed frame {frame_count}")

    def release(self):
        if self.out_with_blobs is not None:
            self.out_with_blobs.release()
        if self.out_blobs_only is not None:
            self.out_blobs_only.release()

        if self.verbose:
            print(f"Export completed:")
            print(f"  - Output with blobs: {self.output_path_with_blobs}")
            print(f"  - Output blobs only: {self.output_path_blobs_only}")