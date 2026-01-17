import cv2
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("FPV Camera")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            background:#2a2a2a;
            border-radius:16px;
            color:#aaa;
            font-size:16px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        # Open FPV camera directly via V4L2
        self.cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        if not self.cap.isOpened():
            self.label.setText("FPV camera not found")
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # ~30 FPS

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Convert BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        h, w, ch = frame.shape
        image = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(
            pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
