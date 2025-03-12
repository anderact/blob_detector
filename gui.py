import cv2

class BlobDetectorGUI:
    def __init__(self, detector):
        self.detector = detector
        self.min_area = 500
        self.max_area = 5000
        self.min_circularity = 50
        self.max_circularity = 100
        self.min_convexity = 87
        self.max_convexity = 100
        self.min_inertia_ratio = 10
        self.max_inertia_ratio = 100
        self.loop_video = 1
        self.min_movement_threshold = 10
        self.min_movement_threshold_small = 2
        self.alpha = 100
        self.setup_trackbars()

    def setup_trackbars(self):
        cv2.namedWindow("Blob Detector with Tracing")
        cv2.createTrackbar("Min Area", "Blob Detector with Tracing", self.min_area, 5000, self.update_min_area)
        cv2.createTrackbar("Max Area", "Blob Detector with Tracing", self.max_area, 10000, self.update_max_area)
        cv2.createTrackbar("Min Circularity", "Blob Detector with Tracing", self.min_circularity, 100, self.update_min_circularity)
        cv2.createTrackbar("Max Circularity", "Blob Detector with Tracing", self.max_circularity, 100, self.update_max_circularity)
        cv2.createTrackbar("Min Convexity", "Blob Detector with Tracing", self.min_convexity, 100, self.update_min_convexity)
        cv2.createTrackbar("Max Convexity", "Blob Detector with Tracing", self.max_convexity, 100, self.update_max_convexity)
        cv2.createTrackbar("Min Inertia Ratio", "Blob Detector with Tracing", self.min_inertia_ratio, 100, self.update_min_inertia_ratio)
        cv2.createTrackbar("Max Inertia Ratio", "Blob Detector with Tracing", self.max_inertia_ratio, 100, self.update_max_inertia_ratio)
        cv2.createTrackbar("Loop Video", "Blob Detector with Tracing", self.loop_video, 1, self.update_loop_video)
        cv2.createTrackbar("Min Movement", "Blob Detector with Tracing", self.min_movement_threshold, 50, self.update_min_movement_threshold)
        cv2.createTrackbar("Min Small Movement", "Blob Detector with Tracing", self.min_movement_threshold_small, 10, self.update_min_movement_threshold_small)
        cv2.createTrackbar("Alpha", "Blob Detector with Tracing", self.alpha, 100, self.update_alpha)

    def update_min_area(self, value):
        self.min_area = max(1, min(value, self.max_area))
        cv2.setTrackbarPos("Min Area", "Blob Detector with Tracing", self.min_area)
        self.detector.params.minArea = self.min_area

    def update_max_area(self, value):
        self.max_area = max(self.min_area, min(value, 10000))
        cv2.setTrackbarPos("Max Area", "Blob Detector with Tracing", self.max_area)
        self.detector.params.maxArea = self.max_area

    def update_min_circularity(self, value):
        self.min_circularity = max(0, min(value, self.max_circularity))
        cv2.setTrackbarPos("Min Circularity", "Blob Detector with Tracing", self.min_circularity)
        self.detector.params.minCircularity = self.min_circularity / 100

    def update_max_circularity(self, value):
        self.max_circularity = max(self.min_circularity, min(value, 100))
        cv2.setTrackbarPos("Max Circularity", "Blob Detector with Tracing", self.max_circularity)
        self.detector.params.maxCircularity = self.max_circularity / 100

    def update_min_convexity(self, value):
        self.min_convexity = max(0, min(value, self.max_convexity))
        cv2.setTrackbarPos("Min Convexity", "Blob Detector with Tracing", self.min_convexity)
        self.detector.params.minConvexity = self.min_convexity / 100

    def update_max_convexity(self, value):
        self.max_convexity = max(self.min_convexity, min(value, 100))
        cv2.setTrackbarPos("Max Convexity", "Blob Detector with Tracing", self.max_convexity)
        self.detector.params.maxConvexity = self.max_convexity / 100

    def update_min_inertia_ratio(self, value):
        self.min_inertia_ratio = max(0, min(value, self.max_inertia_ratio))
        cv2.setTrackbarPos("Min Inertia Ratio", "Blob Detector with Tracing", self.min_inertia_ratio)
        self.detector.params.minInertiaRatio = self.min_inertia_ratio / 100

    def update_max_inertia_ratio(self, value):
        self.max_inertia_ratio = max(self.min_inertia_ratio, min(value, 100))
        cv2.setTrackbarPos("Max Inertia Ratio", "Blob Detector with Tracing", self.max_inertia_ratio)
        self.detector.params.maxInertiaRatio = self.max_inertia_ratio / 100

    def update_loop_video(self, value):
        self.loop_video = max(0, min(value, 1))
        cv2.setTrackbarPos("Loop Video", "Blob Detector with Tracing", self.loop_video)

    def update_min_movement_threshold(self, value):
        self.min_movement_threshold = max(1, min(value, 50))
        cv2.setTrackbarPos("Min Movement", "Blob Detector with Tracing", self.min_movement_threshold)

    def update_min_movement_threshold_small(self, value):
        self.min_movement_threshold_small = max(1, min(value, 10))
        cv2.setTrackbarPos("Min Small Movement", "Blob Detector with Tracing", self.min_movement_threshold_small)

    def update_alpha(self, value):
        self.alpha = max(0, min(value, 100))
        cv2.setTrackbarPos("Alpha", "Blob Detector with Tracing", self.alpha)