import cv2

class BlobDetectorGUI:
    def __init__(self, detector):
        self.detector = detector
        self.min_area = 500
        self.max_area = 5000
        self.min_convexity = 87
        self.max_convexity = 100
        self.alpha_video = 100  # Alpha for video
        self.max_blobs = 10     # Maximum number of blobs to render
        self.show_text = 1      # Show text (1 = On, 0 = Off)
        self.loop_video = 1     # Loop video (1 = On, 0 = Off)
        self.text_mode = 0      # 0 = Coordinates, 1 = Random Symbols, 2 = Custom Text
        self.show_blobs = 1     # Show blobs (1 = On, 0 = Off)
        self.show_lines = 1     # Show tracing lines (1 = On, 0 = Off)
        self.custom_text = "Blob"  # Default custom text
        self.setup_trackbars()

    def setup_trackbars(self):
        cv2.namedWindow("Blob Detector with Tracing")
        cv2.createTrackbar("Min Area", "Blob Detector with Tracing", self.min_area, 5000, self.update_min_area)
        cv2.createTrackbar("Max Area", "Blob Detector with Tracing", self.max_area, 10000, self.update_max_area)
        cv2.createTrackbar("Min Convexity", "Blob Detector with Tracing", self.min_convexity, 100, self.update_min_convexity)
        cv2.createTrackbar("Max Convexity", "Blob Detector with Tracing", self.max_convexity, 100, self.update_max_convexity)
        cv2.createTrackbar("Alpha Video", "Blob Detector with Tracing", self.alpha_video, 100, self.update_alpha_video)
        cv2.createTrackbar("Max Blobs", "Blob Detector with Tracing", self.max_blobs, 50, self.update_max_blobs)
        cv2.createTrackbar("Show Text", "Blob Detector with Tracing", self.show_text, 1, self.update_show_text)
        cv2.createTrackbar("Loop Video", "Blob Detector with Tracing", self.loop_video, 1, self.update_loop_video)
        cv2.createTrackbar("Text Mode", "Blob Detector with Tracing", self.text_mode, 2, self.update_text_mode)
        cv2.createTrackbar("Show Blobs", "Blob Detector with Tracing", self.show_blobs, 1, self.update_show_blobs)
        cv2.createTrackbar("Show Lines", "Blob Detector with Tracing", self.show_lines, 1, self.update_show_lines)

    # Update methods for trackbars
    def update_min_area(self, value):
        self.min_area = max(1, min(value, self.max_area))
        cv2.setTrackbarPos("Min Area", "Blob Detector with Tracing", self.min_area)
        self.detector.params.minArea = self.min_area

    def update_max_area(self, value):
        self.max_area = max(self.min_area, min(value, 10000))
        cv2.setTrackbarPos("Max Area", "Blob Detector with Tracing", self.max_area)
        self.detector.params.maxArea = self.max_area

    def update_min_convexity(self, value):
        self.min_convexity = max(0, min(value, self.max_convexity))
        cv2.setTrackbarPos("Min Convexity", "Blob Detector with Tracing", self.min_convexity)
        self.detector.params.minConvexity = self.min_convexity / 100

    def update_max_convexity(self, value):
        self.max_convexity = max(self.min_convexity, min(value, 100))
        cv2.setTrackbarPos("Max Convexity", "Blob Detector with Tracing", self.max_convexity)
        self.detector.params.maxConvexity = self.max_convexity / 100

    def update_alpha_video(self, value):
        self.alpha_video = max(0, min(value, 100))
        cv2.setTrackbarPos("Alpha Video", "Blob Detector with Tracing", self.alpha_video)

    def update_max_blobs(self, value):
        self.max_blobs = max(1, min(value, 50))
        cv2.setTrackbarPos("Max Blobs", "Blob Detector with Tracing", self.max_blobs)

    def update_show_text(self, value):
        self.show_text = max(0, min(value, 1))
        cv2.setTrackbarPos("Show Text", "Blob Detector with Tracing", self.show_text)

    def update_loop_video(self, value):
        self.loop_video = max(0, min(value, 1))
        cv2.setTrackbarPos("Loop Video", "Blob Detector with Tracing", self.loop_video)

    def update_text_mode(self, value):
        self.text_mode = max(0, min(value, 2))
        cv2.setTrackbarPos("Text Mode", "Blob Detector with Tracing", self.text_mode)

    def update_show_blobs(self, value):
        self.show_blobs = max(0, min(value, 1))
        cv2.setTrackbarPos("Show Blobs", "Blob Detector with Tracing", self.show_blobs)

    def update_show_lines(self, value):
        self.show_lines = max(0, min(value, 1))
        cv2.setTrackbarPos("Show Lines", "Blob Detector with Tracing", self.show_lines)