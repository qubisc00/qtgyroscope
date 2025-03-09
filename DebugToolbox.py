from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PySide6.QtCore import Qt

class DebugToolbox(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label1 = QLabel("Yaw: 0")
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setRange(-180,180)
        self.slider1.setValue(0)

        self.label2 = QLabel("Pitch: 0")
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setRange(-180,180)
        self.slider2.setValue(0)

        self.label3 = QLabel("Roll: 0")
        self.slider3 = QSlider(Qt.Horizontal)
        self.slider3.setRange(-180,180)
        self.slider3.setValue(0)

        layout.addWidget(self.label1)
        layout.addWidget(self.slider1)

        layout.addWidget(self.label2)
        layout.addWidget(self.slider2)

        layout.addWidget(self.label3)
        layout.addWidget(self.slider3)

        self.setLayout(layout)
