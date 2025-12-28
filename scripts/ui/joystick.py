from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt, QRectF

class JoystickWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.x = 0.0
        self.y = 0.0
        self.setMinimumSize(200, 200)

    def update_stick(self, x, y):
        self.x = max(-1.0, min(1.0, float(x)))
        self.y = max(-1.0, min(1.0, float(y)))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        r = min(w, h) * 0.45

        p.setPen(Qt.NoPen)

        p.setBrush(QColor(35, 35, 35))
        p.drawEllipse(QRectF(w/2 - r, h/2 - r, r*2, r*2))

        p.setBrush(QColor(60, 60, 60))
        p.drawEllipse(QRectF(w/2 - r*0.7, h/2 - r*0.7, r*1.4, r*1.4))

        sr = r * 0.25
        sx = w/2 + (self.x * r * 0.6) - sr
        sy = h/2 - (self.y * r * 0.6) - sr

        p.setBrush(QColor(0, 150, 255))
        p.drawEllipse(QRectF(sx, sy, sr*2, sr*2))
