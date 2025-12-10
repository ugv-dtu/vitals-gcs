from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
import pygame


class JoystickWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.setMinimumSize(200, 200)

    def update_stick(self, x, y):
        self.x = max(-1, min(1, x))
        self.y = max(-1, min(1, y))
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        r = min(w, h) * 0.45

        p.setBrush(QColor(35, 35, 35))
        p.setPen(Qt.NoPen)
        p.drawEllipse(QRectF(w/2 - r, h/2 - r, r*2, r*2))

        p.setBrush(QColor(60, 60, 60))
        p.drawEllipse(QRectF(w/2 - r*0.7, h/2 - r*0.7, r*1.4, r*1.4))

        sr = r * 0.25
        sx = w/2 + (self.x * r * 0.6) - sr
        sy = h/2 - (self.y * r * 0.6) - sr

        p.setBrush(QColor(0, 150, 255))
        p.drawEllipse(QRectF(sx, sy, sr*2, sr*2))


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drone UI")
        self.setStyleSheet("background-color: rgba(0,0,0,120);")

        main = QHBoxLayout(self)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(12)

        video = QLabel("Video Feed Here")
        video.setAlignment(Qt.AlignCenter)
        video.setStyleSheet("""
            background-color: #222;
            border-radius: 20px;
            color: white;
            font-size: 18px;
        """)
        video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main.addWidget(video, stretch=7)

        right_col = QVBoxLayout()
        right_col.setSpacing(12)

        telem = QLabel(
            "GPS: 34.0522 N, 118.2437 W\n"
            "Altitude: 150 m\n"
            "Humidity: 40%\n"
            "Gas: CH4 0.1%, CO2 400ppm\n"
        )
        telem.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        telem.setStyleSheet("""
            background-color: #111;
            border-radius: 16px;
            padding: 16px;
            color: white;
            font-size: 14px;
        """)

        joys = QWidget()
        joys.setStyleSheet("background-color: #111; border-radius: 20px;")
        joy_layout = QHBoxLayout(joys)
        joy_layout.setContentsMargins(30, 20, 30, 20)
        joy_layout.setSpacing(30)
        joy_layout.setAlignment(Qt.AlignCenter)

        self.left_joy = JoystickWidget()
        self.right_joy = JoystickWidget()
        self.left_joy.setFixedSize(230, 230)
        self.right_joy.setFixedSize(230, 230)

        joy_layout.addWidget(self.left_joy)
        joy_layout.addWidget(self.right_joy)

        right_col.addWidget(telem, stretch=3)
        right_col.addWidget(joys, stretch=1)

        main.addLayout(right_col, stretch=1)


class ControllerReader(QObject):
    updated = Signal(float, float, float, float)

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.joystick.init()
        self.js = pygame.joystick.Joystick(0) if pygame.joystick.get_count() else None
        if self.js:
            self.js.init()
        self.timer = QTimer()
        self.timer.timeout.connect(self.read)
        self.timer.start(20)

    def read(self):
        if not self.js:
            return
        pygame.event.pump()
        lx = self.js.get_axis(0)
        ly = -self.js.get_axis(1)
        rx = self.js.get_axis(3)
        ry = -self.js.get_axis(4)
        self.updated.emit(lx, ly, rx, ry)


app = QApplication(sys.argv)
win = Dashboard()
win.resize(1600, 900)
win.show()

controller = ControllerReader()
controller.updated.connect(
    lambda lx, ly, rx, ry: (
        win.left_joy.update_stick(lx, ly),
        win.right_joy.update_stick(rx, ry)
    )
)

sys.exit(app.exec())
