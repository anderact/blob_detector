import cv2
import numpy as np
import argparse
import time

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Blob Detector with Tracing Lines")
parser.add_argument("video_path", type=str, help="Path to the video file")
args = parser.parse_args()

# Initialize the video capture with the provided video file path
cap = cv2.VideoCapture(args.video_path)
if not cap.isOpened():
    print(f"Error: Could not open video file {args.video_path}")
    exit()

# Create a window for the sliders
cv2.namedWindow("Blob Detector with Tracing")

# Initialize parameters with default values
params = cv2.SimpleBlobDetector_Params()

# Global variables to store trackbar values
min_area = 500
max_area = 5000
min_circularity = 50
max_circularity = 100  # Add max_circularity
min_convexity = 87
max_convexity = 100  # Add max_convexity
min_inertia_ratio = 10
max_inertia_ratio = 100  # Add max_inertia_ratio
loop_video = 1
min_movement_threshold = 10  # Default minimum movement threshold (in pixels)
min_movement_threshold_small = 2  # Default threshold for extremely small movements (in pixels)
alpha = 100  # Default alpha value (0 = fully transparent, 100 = fully opaque)

# Function to validate and update parameters
def update_min_area(value):
    global min_area
    min_area = max(1, min(value, max_area))  # Ensure min_area is between 1 and max_area
    cv2.setTrackbarPos("Min Area", "Blob Detector with Tracing", min_area)
    params.minArea = min_area

def update_max_area(value):
    global max_area
    max_area = max(min_area, min(value, 10000))  # Ensure max_area is between min_area and 10000
    cv2.setTrackbarPos("Max Area", "Blob Detector with Tracing", max_area)
    params.maxArea = max_area

def update_min_circularity(value):
    global min_circularity
    min_circularity = max(0, min(value, max_circularity))  # Ensure min_circularity is between 0 and max_circularity
    cv2.setTrackbarPos("Min Circularity", "Blob Detector with Tracing", min_circularity)
    params.minCircularity = min_circularity / 100  # Scale to 0.0-1.0

def update_max_circularity(value):
    global max_circularity
    max_circularity = max(min_circularity, min(value, 100))  # Ensure max_circularity is between min_circularity and 100
    cv2.setTrackbarPos("Max Circularity", "Blob Detector with Tracing", max_circularity)
    params.maxCircularity = max_circularity / 100  # Scale to 0.0-1.0

def update_min_convexity(value):
    global min_convexity
    min_convexity = max(0, min(value, max_convexity))  # Ensure min_convexity is between 0 and max_convexity
    cv2.setTrackbarPos("Min Convexity", "Blob Detector with Tracing", min_convexity)
    params.minConvexity = min_convexity / 100  # Scale to 0.0-1.0

def update_max_convexity(value):
    global max_convexity
    max_convexity = max(min_convexity, min(value, 100))  # Ensure max_convexity is between min_convexity and 100
    cv2.setTrackbarPos("Max Convexity", "Blob Detector with Tracing", max_convexity)
    params.maxConvexity = max_convexity / 100  # Scale to 0.0-1.0

def update_min_inertia_ratio(value):
    global min_inertia_ratio
    min_inertia_ratio = max(0, min(value, max_inertia_ratio))  # Ensure min_inertia_ratio is between 0 and max_inertia_ratio
    cv2.setTrackbarPos("Min Inertia Ratio", "Blob Detector with Tracing", min_inertia_ratio)
    params.minInertiaRatio = min_inertia_ratio / 100  # Scale to 0.0-1.0

def update_max_inertia_ratio(value):
    global max_inertia_ratio
    max_inertia_ratio = max(min_inertia_ratio, min(value, 100))  # Ensure max_inertia_ratio is between min_inertia_ratio and 100
    cv2.setTrackbarPos("Max Inertia Ratio", "Blob Detector with Tracing", max_inertia_ratio)
    params.maxInertiaRatio = max_inertia_ratio / 100  # Scale to 0.0-1.0

def update_loop_video(value):
    global loop_video
    loop_video = max(0, min(value, 1))  # Ensure loop_video is either 0 or 1
    cv2.setTrackbarPos("Loop Video", "Blob Detector with Tracing", loop_video)

def update_min_movement_threshold(value):
    global min_movement_threshold
    min_movement_threshold = max(1, min(value, 50))  # Ensure min_movement_threshold is between 1 and 50
    cv2.setTrackbarPos("Min Movement", "Blob Detector with Tracing", min_movement_threshold)

def update_min_movement_threshold_small(value):
    global min_movement_threshold_small
    min_movement_threshold_small = max(1, min(value, 10))  # Ensure min_movement_threshold_small is between 1 and 10
    cv2.setTrackbarPos("Min Small Movement", "Blob Detector with Tracing", min_movement_threshold_small)

def update_alpha(value):
    global alpha
    alpha = max(0, min(value, 100))  # Ensure alpha is between 0 and 100
    cv2.setTrackbarPos("Alpha", "Blob Detector with Tracing", alpha)

# Add trackbars to the window
cv2.createTrackbar("Min Area", "Blob Detector with Tracing", min_area, 5000, update_min_area)
cv2.createTrackbar("Max Area", "Blob Detector with Tracing", max_area, 10000, update_max_area)
cv2.createTrackbar("Min Circularity", "Blob Detector with Tracing", min_circularity, 100, update_min_circularity)
cv2.createTrackbar("Max Circularity", "Blob Detector with Tracing", max_circularity, 100, update_max_circularity)
cv2.createTrackbar("Min Convexity", "Blob Detector with Tracing", min_convexity, 100, update_min_convexity)
cv2.createTrackbar("Max Convexity", "Blob Detector with Tracing", max_convexity, 100, update_max_convexity)
cv2.createTrackbar("Min Inertia Ratio", "Blob Detector with Tracing", min_inertia_ratio, 100, update_min_inertia_ratio)
cv2.createTrackbar("Max Inertia Ratio", "Blob Detector with Tracing", max_inertia_ratio, 100, update_max_inertia_ratio)
cv2.createTrackbar("Loop Video", "Blob Detector with Tracing", loop_video, 1, update_loop_video)  # 1 = Loop, 0 = Stop
cv2.createTrackbar("Min Movement", "Blob Detector with Tracing", min_movement_threshold, 50, update_min_movement_threshold)
cv2.createTrackbar("Min Small Movement", "Blob Detector with Tracing", min_movement_threshold_small, 10, update_min_movement_threshold_small)
cv2.createTrackbar("Alpha", "Blob Detector with Tracing", alpha, 100, update_alpha)  # Alpha control (0 = transparent, 100 = opaque)

# Print tooltips to the terminal
print("=== Tooltips ===")
print("Min Area: Minimum size (in pixels) of blobs to detect.")
print("Max Area: Maximum size (in pixels) of blobs to detect.")
print("Min Circularity: Minimum circularity of blobs (0.0 = any shape, 1.0 = perfect circle).")
print("Max Circularity: Maximum circularity of blobs (0.0 = any shape, 1.0 = perfect circle).")
print("Min Convexity: Minimum convexity of blobs (0.0 = any shape, 1.0 = perfectly convex).")
print("Max Convexity: Maximum convexity of blobs (0.0 = any shape, 1.0 = perfectly convex).")
print("Min Inertia Ratio: Minimum elongation of blobs (0.0 = highly elongated, 1.0 = no elongation).")
print("Max Inertia Ratio: Maximum elongation of blobs (0.0 = highly elongated, 1.0 = no elongation).")
print("Loop Video: Loop the video when it ends (1 = On, 0 = Off).")
print("Min Movement: Minimum movement (in pixels) required to consider a blob as 'moving'.")
print("Min Small Movement: Minimum movement (in pixels) to filter out extremely small movements.")
print("Alpha: Transparency of the video (0 = fully transparent, 100 = fully opaque).")
print("================")

# Store previous blob positions for tracing lines
previous_blobs = []
blob_timers = {}  # Dictionary to store timers for each blob

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If the video reaches the end, handle looping or stopping
    if not ret:
        if loop_video:
            # Loop the video by resetting to the first frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
        else:
            # Stop the video and wait for user input
            cv2.putText(frame, "Video Ended. Press 'q' to quit.", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Blob Detector with Tracing", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Update detector with current parameters
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs
    keypoints = detector.detect(gray)

    # Create a transparent version of the video frame
    alpha_value = alpha / 100.0  # Scale alpha to 0.0-1.0
    transparent_frame = cv2.addWeighted(frame, alpha_value, np.zeros_like(frame), 1 - alpha_value, 0)

    # Draw detected blobs as white rectangles on a separate overlay
    blob_overlay = np.zeros_like(frame)  # Create a blank overlay for blobs
    current_blobs = []
    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        size = int(kp.size)
        half_size = size // 2

        # Draw rectangle on the overlay
        cv2.rectangle(blob_overlay, (x - half_size, y - half_size),
                      (x + half_size, y + half_size), (255, 255, 255), 2)

        # Store rectangle vertices for drawing lines and coordinates
        vertices = [
            (x - half_size, y - half_size),
            (x + half_size, y - half_size),
            (x + half_size, y + half_size),
            (x - half_size, y + half_size)
        ]
        current_blobs.append(vertices)

    # Draw tracing lines between previous and current blobs on the overlay
    for prev_blob in previous_blobs:
        for curr_blob in current_blobs:
            # Calculate the distance between corresponding vertices
            movement = np.linalg.norm(np.array(prev_blob[0]) - np.array(curr_blob[0]))
            if movement >= min_movement_threshold and movement >= min_movement_threshold_small:
                for i in range(4):  # Draw lines between corresponding vertices
                    cv2.line(blob_overlay, prev_blob[i], curr_blob[i], (255, 255, 255), 1)

                    # Add coordinates text to the vertices
                    cv2.putText(blob_overlay, f"({prev_blob[i][0]}, {prev_blob[i][1]})",
                                (prev_blob[i][0] + 5, prev_blob[i][1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.4, (255, 255, 255), 1)
                    cv2.putText(blob_overlay, f"({curr_blob[i][0]}, {curr_blob[i][1]})",
                                (curr_blob[i][0] + 5, curr_blob[i][1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.4, (255, 255, 255), 1)

    # Update previous blobs
    previous_blobs = current_blobs

    # Combine the transparent video frame and the blob overlay
    final_frame = cv2.add(transparent_frame, blob_overlay)

    # Display the final frame
    cv2.imshow("Blob Detector with Tracing", final_frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()