from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextOption
from PySide6.QtGui import QTextCursor

class LogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.logs = []
        self.max_logs = 100
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)

        title = QLabel("MAVLink Logs")
        title.setStyleSheet("""
            color: #ffffff;
            font-weight: bold;
            font-size: 14px;
        """)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedSize(60, 25)
        self.clear_btn.clicked.connect(self.clear_logs)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background: #2d2d2d;
                border: 1px solid #444;
                border-radius: 4px;
                color: #ddd;
                padding: 2px;
            }
            QPushButton:hover {
                background: #3d3d3d;
                border: 1px solid #555;
            }
        """)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.clear_btn)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.log_text.setLineWrapMode(QTextEdit.NoWrap)
        self.log_text.setWordWrapMode(QTextOption.NoWrap)
        self.log_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.log_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.log_text.setStyleSheet("""
            QTextEdit {
                background: #0a0a0a;
                border: 1px solid #333;
                border-radius: 8px;
                color: #e0e0e0;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                padding: 8px;
            }
        """)

        layout.addWidget(header)
        layout.addWidget(self.log_text)

    def add_log(self, text):
        from datetime import datetime

        clean_text = " ".join(text.splitlines())

        if self.logs and (
            clean_text.startswith("_") or
            not clean_text.startswith(("PreArm:", "AP:", "EKF", "GPS", "RC", "IMU"))
        ):
            self.logs[-1] += clean_text
        else:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.logs.append(f"[{timestamp}] {clean_text}")

        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]

        self.log_text.setPlainText("\n".join(self.logs))

        sb = self.log_text.verticalScrollBar()
        sb.setValue(sb.maximum())


    def clear_logs(self):
        self.logs.clear()
        self.log_text.clear()
