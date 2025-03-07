import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QPalette, QColor
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QSlider, QLabel
from PySide6.QtGui import (QGuiApplication)
from gyroscope import Cube

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Test')

        self.label1 = QLabel("Yaw: 0")
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "yaw"))
        self.slider1.setRange(0,360)
        
        self.label2 = QLabel("Pitch: 0")
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "pitch"))
        self.slider2.setRange(0,360)

        self.label3 = QLabel("Roll: 0")
        self.slider3 = QSlider(Qt.Horizontal)
        self.slider3.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "roll"))
        self.slider3.setRange(0,360)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.cube = Cube()
        self.container = QWidget.createWindowContainer(self.cube)
        self.container.setFixedSize(200, 200)

        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)

        self.layout.addWidget(self.container)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.slider2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.slider3)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def update_label_and_rotation(self, value: int, axis: str):
        if axis == "yaw":
            self.label1.setText(f"Yaw: {value}")
            self.cube.update_rotation(value, self.slider2.value(), self.slider3.value())
        elif axis == "pitch":
            self.label2.setText(f"Pitch: {value}")
            self.cube.update_rotation(self.slider1.value(), value, self.slider3.value())
        elif axis == "roll":
            self.label3.setText(f"Roll: {value}")
            self.cube.update_rotation(self.slider1.value(), self.slider2.value(), value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
