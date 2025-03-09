import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from GyroscopeWidget import *
from CircleWidget import *
from GyroMonitorWidget import *
from DebugToolbox import *
from SpectrogramWidget import App

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Test')

        self.gyroGraphLayout = QHBoxLayout()
        self.gyroLayout = QVBoxLayout()
        self.gyroSpectogramLayout = QHBoxLayout()

        self.circleWidget = CircleWidget()

        self.yawGyroWidget = GyroMonitorWidget("Yaw Orientation")
        self.rollGyroWidget = GyroMonitorWidget("Roll Orientation")
        self.pitchGyroWidget = GyroMonitorWidget("Pitch Orientation")

        self.gyroGraphLayout.addWidget(self.yawGyroWidget)
        self.gyroGraphLayout.addWidget(self.rollGyroWidget)
        self.gyroGraphLayout.addWidget(self.pitchGyroWidget)

        if __debug__:
            self.toolbox = DebugToolbox()
            self.toolbox.show()

            self.toolbox.slider1.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "yaw"))
            self.toolbox.slider1.valueChanged.connect(lambda value: self.circleWidget.set_angle(value))
            self.toolbox.slider1.valueChanged.connect(lambda value: self.yawGyroWidget.set_angle(value))

            self.toolbox.slider2.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "pitch"))
            self.toolbox.slider2.valueChanged.connect(lambda value: self.pitchGyroWidget.set_angle(value))

            self.toolbox.slider3.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "roll"))
            self.toolbox.slider3.valueChanged.connect(lambda value: self.rollGyroWidget.set_angle(value))

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # Spectogram and Gyroscope Layout
        self.openglWidget = App()
        self.gyroSpectogramLayout.addWidget(self.openglWidget)

        self.cubeGryro = GyroscopeWidget()
        self.cubeGyroContainer = QWidget.createWindowContainer(self.cubeGryro)
        self.cubeGyroContainer.setFixedSize(200, 200)
        self.cubeGyroContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cubeGyroContainer.setFocusPolicy(Qt.StrongFocus)
        self.gyroLayout.addWidget(self.circleWidget)
        self.gyroLayout.addWidget(self.cubeGyroContainer)

        self.gyroSpectogramLayout.addLayout(self.gyroLayout)

        self.layout.addLayout(self.gyroGraphLayout)
        self.layout.addLayout(self.gyroSpectogramLayout)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def update_label_and_rotation(self, value: int, axis: str):
        if axis == "yaw":
            if __debug__:
                self.toolbox.label1.setText(f"Yaw: {value}")
                self.cubeGryro.update_rotation(value, self.toolbox.slider2.value(), self.toolbox.slider3.value())
        elif axis == "pitch":
            if __debug__:
                self.toolbox.label2.setText(f"Pitch: {value}")
                self.cubeGryro.update_rotation(self.toolbox.slider1.value(), value, self.toolbox.slider3.value())
        elif axis == "roll":
            if __debug__:
                self.toolbox.label3.setText(f"Roll: {value}")
                self.cubeGryro.update_rotation(self.toolbox.slider1.value(), self.toolbox.slider2.value(), value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
