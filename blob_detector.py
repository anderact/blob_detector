import cv2
import numpy as np
import random
import string
from gui import BlobDetectorGUI
from video_export import VideoExporter

class BlobDetector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video file {video_path}")
        else:
            print(f"Video file {video_path} loaded successfully.")

        # Display video information
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        print(f"Video Resolution: {self.frame_width}x{self.frame_height}")
        print(f"Total Frames: {self.total_frames}")
        print(f"Frame Rate: {self.fps} FPS")

        self.params = cv2.SimpleBlobDetector_Params()
        self.previous_blobs = []
        self.paused = False  # Pause state
        self.exporting = False  # Export state
        self.frame_delay = 1  # Delay between frames in milliseconds

    def detect_blobs(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detector = cv2.SimpleBlobDetector_create(self.params)
        keypoints = detector.detect(gray)
        return keypoints

    def get_text_for_blob(self, x, y, text_mode):
        if text_mode == 0:  # Coordinates
            return f"({x}, {y})"
        elif text_mode == 1:  # Random Symbols
            return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))
        elif text_mode == 2:  # Custom Text
            return "Blob"  # Replace with self.gui.custom_text if you want dynamic custom text
        return ""

    def draw_blobs(self, frame, keypoints, show_text, text_mode, show_blobs):
        blob_overlay = np.zeros_like(frame)
        current_blobs = []
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            size = int(kp.size)
            half_size = size // 2
            if show_blobs:
                cv2.rectangle(blob_overlay, (x - half_size, y - half_size),
                              (x + half_size, y + half_size), (255, 255, 255), 2)
            if show_text:
                text = self.get_text_for_blob(x, y, text_mode)
                cv2.putText(blob_overlay, text, (x + 5, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            current_blobs.append((x, y))  # Store blob center
        return blob_overlay, current_blobs

    def draw_tracing_lines(self, blob_overlay, previous_blobs, current_blobs, show_lines):
        if show_lines:
            for prev_blob in previous_blobs:
                for curr_blob in current_blobs:
                    # Draw line between blob centers
                    cv2.line(blob_overlay, prev_blob, curr_blob, (255, 255, 255), 2)
        return blob_overlay

    def process_frame(self, frame, alpha_video, max_blobs, show_text, text_mode, show_blobs, show_lines):
        keypoints = self.detect_blobs(frame)
        # Sort keypoints by size and keep only the top N blobs
        keypoints = sorted(keypoints, key=lambda kp: kp.size, reverse=True)[:max_blobs]
        blob_overlay, current_blobs = self.draw_blobs(frame, keypoints, show_text, text_mode, show_blobs)
        blob_overlay = self.draw_tracing_lines(blob_overlay, self.previous_blobs, current_blobs, show_lines)
        self.previous_blobs = current_blobs

        # Apply alpha to the video frame
        alpha_value = alpha_video / 100.0
        transparent_frame = cv2.addWeighted(frame, alpha_value, np.zeros_like(frame), 1 - alpha_value, 0)

        # Combine the transparent video frame and the blob overlay
        final_frame = cv2.add(transparent_frame, blob_overlay)
        return final_frame, blob_overlay

    def export_video(self, gui, verbose=True):
        # Pause the video and rewind to the beginning
        self.paused = True
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Initialize the exporter
        exporter = VideoExporter(self.video_path, verbose=verbose)
        exporter.initialize()

        frame_count = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break  # End of video

            final_frame, blob_overlay = self.process_frame(
                frame, gui.alpha_video, gui.max_blobs, gui.show_text, gui.text_mode, gui.show_blobs, gui.show_lines
            )
            exporter.write_frames(final_frame, blob_overlay, frame_count)
            frame_count += 1

        exporter.release()
        print(f"Export completed. Total frames processed: {frame_count}")

    def run(self, gui, verbose=True):
        frame_count = 0
        while True:
            if not self.paused and not self.exporting:
                ret, frame = self.cap.read()
                if not ret:
                    if gui.loop_video:
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        ret, frame = self.cap.read()
                    else:
                        cv2.putText(frame, "Video Ended. Press 'q' to quit.", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        cv2.imshow("Blob Detector with Tracing", frame)
                        if cv2.waitKey(self.frame_delay) & 0xFF == ord('q'):
                            break
                        continue

                final_frame, blob_overlay = self.process_frame(
                    frame, gui.alpha_video, gui.max_blobs, gui.show_text, gui.text_mode, gui.show_blobs, gui.show_lines
                )
                cv2.imshow("Blob Detector with Tracing", final_frame)
                frame_count += 1

            key = cv2.waitKey(self.frame_delay) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('e'):
                self.exporting = True
                self.export_video(gui, verbose=verbose)
                self.exporting = False
            elif key == ord('p'):
                self.paused = not self.paused
                print("Video paused." if self.paused else "Video resumed.")
            elif key == ord('+'):  # Increase speed (reduce delay)
                self.frame_delay = max(1, self.frame_delay - 10)
                print(f"Frame delay: {self.frame_delay} ms")
            elif key == ord('-'):  # Decrease speed (increase delay)
                self.frame_delay += 10
                print(f"Frame delay: {self.frame_delay} ms")

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Blob Detector with Tracing Lines")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    parser.add_argument("--no-verbose", action="store_true", help="Disable verbose output during export")
    args = parser.parse_args()

    detector = BlobDetector(args.video_path)
    gui = BlobDetectorGUI(detector)
    detector.run(gui, verbose=not args.no_verbose)