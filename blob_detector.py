import cv2
import numpy as np
from gui import BlobDetectorGUI
from video_export import VideoExporter

class BlobDetector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Error: Could not open video file {video_path}")

        self.params = cv2.SimpleBlobDetector_Params()
        self.previous_blobs = []
        self.blob_timers = {}

    def detect_blobs(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detector = cv2.SimpleBlobDetector_create(self.params)
        keypoints = detector.detect(gray)
        return keypoints

    def draw_blobs(self, frame, keypoints):
        blob_overlay = np.zeros_like(frame)
        current_blobs = []
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            size = int(kp.size)
            half_size = size // 2
            cv2.rectangle(blob_overlay, (x - half_size, y - half_size),
                          (x + half_size, y + half_size), (255, 255, 255), 2)
            vertices = [
                (x - half_size, y - half_size),
                (x + half_size, y - half_size),
                (x + half_size, y + half_size),
                (x - half_size, y + half_size)
            ]
            current_blobs.append(vertices)
        return blob_overlay, current_blobs

    def draw_tracing_lines(self, blob_overlay, previous_blobs, current_blobs, min_movement_threshold, min_movement_threshold_small):
        for prev_blob in previous_blobs:
            for curr_blob in current_blobs:
                movement = np.linalg.norm(np.array(prev_blob[0]) - np.array(curr_blob[0]))
                if movement >= min_movement_threshold and movement >= min_movement_threshold_small:
                    for i in range(4):
                        cv2.line(blob_overlay, prev_blob[i], curr_blob[i], (255, 255, 255), 1)
                        cv2.putText(blob_overlay, f"({prev_blob[i][0]}, {prev_blob[i][1]})",
                                    (prev_blob[i][0] + 5, prev_blob[i][1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.4, (255, 255, 255), 1)
                        cv2.putText(blob_overlay, f"({curr_blob[i][0]}, {curr_blob[i][1]})",
                                    (curr_blob[i][0] + 5, curr_blob[i][1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.4, (255, 255, 255), 1)
        return blob_overlay

    def process_frame(self, frame, alpha, min_movement_threshold, min_movement_threshold_small):
        keypoints = self.detect_blobs(frame)
        blob_overlay, current_blobs = self.draw_blobs(frame, keypoints)
        blob_overlay = self.draw_tracing_lines(blob_overlay, self.previous_blobs, current_blobs, min_movement_threshold, min_movement_threshold_small)
        self.previous_blobs = current_blobs

        # Apply alpha to the video frame
        alpha_value = alpha / 100.0
        transparent_frame = cv2.addWeighted(frame, alpha_value, np.zeros_like(frame), 1 - alpha_value, 0)

        # Combine the transparent video frame and the blob overlay
        final_frame = cv2.add(transparent_frame, blob_overlay)
        return final_frame, blob_overlay

    def run(self, gui, export_video=False):
        if export_video:
            exporter = VideoExporter(self.video_path)
            exporter.initialize()

        while True:
            ret, frame = self.cap.read()
            if not ret:
                if gui.loop_video:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()
                else:
                    cv2.putText(frame, "Video Ended. Press 'q' to quit.", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.imshow("Blob Detector with Tracing", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    continue

            final_frame, blob_overlay = self.process_frame(frame, gui.alpha, gui.min_movement_threshold, gui.min_movement_threshold_small)

            if export_video:
                exporter.write_frames(final_frame, blob_overlay)

            cv2.imshow("Blob Detector with Tracing", final_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('e'):  # Export video on 'e' key press
                exporter = VideoExporter(self.video_path)
                exporter.initialize()
                exporter.write_frames(final_frame, blob_overlay)
                print("Exporting video... Press 'q' to stop.")

        if export_video:
            exporter.release()
            print(f"Videos saved to {exporter.output_path_with_blobs} and {exporter.output_path_blobs_only}")

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Blob Detector with Tracing Lines")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    args = parser.parse_args()

    detector = BlobDetector(args.video_path)
    gui = BlobDetectorGUI(detector)
    detector.run(gui)