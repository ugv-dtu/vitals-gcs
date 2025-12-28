from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession, QMediaDevices, QVideoSink
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Camera Feed")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            background:#2a2a2a;
            border-radius:16px;
            color:#aaa;
            font-size:16px;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.label)

        self.video_sink = QVideoSink()
        self.video_sink.videoFrameChanged.connect(self.on_frame)

        devices = QMediaDevices.videoInputs()
        if not devices:
            self.label.setText("No camera found")
            return

        self.camera = QCamera(devices[0])

        self.capture = QMediaCaptureSession()
        self.capture.setCamera(self.camera)
        self.capture.setVideoSink(self.video_sink)

        self.camera.start()

    def on_frame(self, frame):
        if not frame.isValid():
            return

        image = frame.toImage()
        if image.isNull():
            return

        image = image.mirrored(True, False)

        pixmap = QPixmap.fromImage(image)

        self.label.setPixmap(
            pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def resizeEvent(self, event):
        if self.label.pixmap():
            self.label.setPixmap(
                self.label.pixmap().scaled(
                    self.label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        super().resizeEvent(event)

    def closeEvent(self, event):
        if self.camera.isActive():
            self.camera.stop()
        event.accept()