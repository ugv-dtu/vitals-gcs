from PySide6.QtWidgets import (
    QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QToolButton
)
from PySide6.QtCore import Qt

class MapOverlay(QWidget):
    def __init__(self, container, map_widget):
        super().__init__(container)
        self.container = container
        self.map = map_widget
        self.expanded = False

        self.setFixedWidth(220)
        self.setStyleSheet("""
            QWidget {
                background: rgba(15,15,15,210);
                border-radius: 10px;
            }
            QLineEdit {
                background:#222;
                color:white;
                border:1px solid #444;
                border-radius:4px;
                padding:4px;
            }
            QPushButton {
                background:#2a82da;
                color:white;
                border-radius:6px;
                padding:6px;
            }
            QToolButton {
                color: black;
                font-weight: bold;
                font-size: 24px;
                background: transparent;
                padding: 6px;
                border: none;
                text-align: right;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)

        self.toggle = QToolButton()
        self.toggle.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.toggle.setLayoutDirection(Qt.RightToLeft)
        self.toggle.setText("📍")
        self.toggle.clicked.connect(self.toggle_panel)
        self.layout.addWidget(self.toggle)

        self.panel = QWidget()
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(6)

        self.lat = QLineEdit()
        self.lat.setPlaceholderText("Latitude")

        self.lon = QLineEdit()
        self.lon.setPlaceholderText("Longitude")

        self.label = QLineEdit()
        self.label.setPlaceholderText("Label (optional)")

        add_btn = QPushButton("Add Marker")
        add_btn.clicked.connect(self.add_marker)

        clear_btn = QPushButton("Clear Path")
        clear_btn.clicked.connect(self.clear_path)

        panel_layout.addWidget(self.lat)
        panel_layout.addWidget(self.lon)
        panel_layout.addWidget(self.label)
        panel_layout.addWidget(add_btn)
        panel_layout.addWidget(clear_btn)

        self.panel.setVisible(False)
        self.layout.addWidget(self.panel)

        self.adjust_size()
        self.reposition()

    def toggle_panel(self):
        self.expanded = not self.expanded
        self.panel.setVisible(self.expanded)
        self.adjust_size()
        self.reposition()

    def adjust_size(self):
        self.setFixedHeight(50 if not self.expanded else 240)

    def reposition(self):
        self.move(
            self.container.width() - self.width() - 12,
            self.container.height() - self.height() - 12
        )
        self.raise_()

    def resizeEvent(self, event):
        self.reposition()
        super().resizeEvent(event)

    def add_marker(self):
        try:
            lat = float(self.lat.text())
            lon = float(self.lon.text())
            label = self.label.text() or "Waypoint"
            self.map.add_marker(lat, lon, label)
        except ValueError:
            pass

    def clear_path(self):
        self.map.clear_path()
