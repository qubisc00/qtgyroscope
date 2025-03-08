import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from GyroscopeWidget import *
from CircleWidget import *
from GyroMonitorWidget import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Test')

        self.gyroGraphLayout = QHBoxLayout()
        self.gyroLayout = QHBoxLayout()

        self.circleWidget = CircleWidget()
        self.yawGyroWidget = GyroMonitorWidget("Yaw Orientation")
        self.rollGyroWidget = GyroMonitorWidget("Roll Orientation")
        self.pitchGyroWidget = GyroMonitorWidget("Pitch Orientation")

        self.gyroGraphLayout.addWidget(self.yawGyroWidget)
        self.gyroGraphLayout.addWidget(self.rollGyroWidget)
        self.gyroGraphLayout.addWidget(self.pitchGyroWidget)

        self.label1 = QLabel("Yaw: 0")
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "yaw"))
        self.slider1.valueChanged.connect(lambda value: self.circleWidget.set_angle(value))
        self.slider1.valueChanged.connect(lambda value: self.yawGyroWidget.set_angle(value))
        self.slider1.setRange(-180,180)
        self.slider1.setValue(0)
        
        self.label2 = QLabel("Pitch: 0")
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "pitch"))
        self.slider2.valueChanged.connect(lambda value: self.pitchGyroWidget.set_angle(value))
        self.slider2.setRange(-180,180)
        self.slider2.setValue(0)

        self.label3 = QLabel("Roll: 0")
        self.slider3 = QSlider(Qt.Horizontal)
        self.slider3.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "roll"))
        self.slider3.valueChanged.connect(lambda value: self.rollGyroWidget.set_angle(value))
        self.slider3.setRange(-180,180)
        self.slider3.setValue(0)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.cubeGryro = GyroscopeWidget()
        self.cubeGyroContainer = QWidget.createWindowContainer(self.cubeGryro)
        self.cubeGyroContainer.setFixedSize(200, 200)

        self.cubeGyroContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cubeGyroContainer.setFocusPolicy(Qt.StrongFocus)

        self.gyroLayout.addWidget(self.circleWidget)
        self.gyroLayout.addWidget(self.cubeGyroContainer)

        self.layout.addLayout(self.gyroGraphLayout)
        self.layout.addLayout(self.gyroLayout)
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
            self.cubeGryro.update_rotation(value, self.slider2.value(), self.slider3.value())
        elif axis == "pitch":
            self.label2.setText(f"Pitch: {value}")
            self.cubeGryro.update_rotation(self.slider1.value(), value, self.slider3.value())
        elif axis == "roll":
            self.label3.setText(f"Roll: {value}")
            self.cubeGryro.update_rotation(self.slider1.value(), self.slider2.value(), value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
