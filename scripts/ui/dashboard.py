from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from .joystick import JoystickWidget
from .map_widget import MapWidget
from .camera_widget import CameraWidget
from .log_widget import LogWidget
from .map_overlay import MapOverlay


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone UI")
        self.setStyleSheet("background-color:#1e1e1e;")

        main = QHBoxLayout(self)
        main.setContentsMargins(10,10,10,10)
        main.setSpacing(12)

        left_col = QVBoxLayout()
        left_col.setSpacing(12)

        self.video = CameraWidget()
        self.video.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.log_widget = LogWidget()

        left_col.addWidget(self.video, stretch=2)
        left_col.addWidget(self.log_widget, stretch=1)

        main.addLayout(left_col, stretch=7)

        right = QVBoxLayout()
        right.setSpacing(12)

        self.telemetry = QLabel("Waiting for MAVLink…")
        self.telemetry.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.telemetry.setStyleSheet("""
            background:#111;
            border-radius:14px;
            padding:14px;
            color:white;
            font-size:14px;
        """)
        right.addWidget(self.telemetry, stretch=2)

        self.map_container = QWidget()
        self.map_container.setStyleSheet("background: transparent;")
        map_layout = QVBoxLayout(self.map_container)
        map_layout.setContentsMargins(0, 0, 0, 0)

        self.map = MapWidget()
        self.map.setMinimumHeight(250)
        map_layout.addWidget(self.map)

        self.map_overlay = MapOverlay(self.map_container, self.map)

        right.addWidget(self.map_container, stretch=3)

        joys = QWidget()
        joys.setStyleSheet("background:#111; border-radius:14px;")
        joy_layout = QHBoxLayout(joys)
        joy_layout.setContentsMargins(20,20,20,20)
        joy_layout.setSpacing(20)
        joy_layout.setAlignment(Qt.AlignCenter)

        self.left_joy = JoystickWidget()
        self.right_joy = JoystickWidget()
        self.left_joy.setFixedSize(200,200)
        self.right_joy.setFixedSize(200,200)

        joy_layout.addWidget(self.left_joy)
        joy_layout.addWidget(self.right_joy)

        right.addWidget(joys, stretch=1)

        main.addLayout(right, stretch=3)

    def update_telem(self, text):
        self.telemetry.setText(text)

    def add_log(self, text):
        self.log_widget.add_log(text)
