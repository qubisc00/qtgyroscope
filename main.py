import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from CircleWidget import *
from BodyOrientationWidget import *
from DebugToolbox import *
from SpectrogramWidget import App
from GyrosMonitorWidget import * 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Test')

        # Layouts
        self.gyroGraphLayout = QHBoxLayout()
        self.gyroLayout = QVBoxLayout()
        self.gyroSpectogramLayout = QHBoxLayout()
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.circleWidget = CircleWidget()

        self.yawGyroWidget = BodyOrientationWidget("Yaw Orientation")
        self.rollGyroWidget = BodyOrientationWidget("Roll Orientation")
        self.pitchGyroWidget = BodyOrientationWidget("Pitch Orientation")
        self.gyrosWidget = GyrosMonitorWidget("Gyros")
        self.gyroGraphLayout.addWidget(self.gyrosWidget)
        self.gyroGraphLayout.addWidget(self.yawGyroWidget)
        self.gyroGraphLayout.addWidget(self.rollGyroWidget)
        self.gyroGraphLayout.addWidget(self.pitchGyroWidget)

        if __debug__:
            self.toolbox = DebugToolbox()
            self.toolbox.show()

            self.toolbox.slider1.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "yaw"))
            self.toolbox.slider1.valueChanged.connect(lambda value: self.circleWidget.set_angle(value))
            self.toolbox.slider1.valueChanged.connect(lambda value: self.yawGyroWidget.set_angle(value))
            self.toolbox.slider1.valueChanged.connect(lambda value: self.gyrosWidget.set_yaw_angle(value))

            self.toolbox.slider2.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "pitch"))
            self.toolbox.slider2.valueChanged.connect(lambda value: self.pitchGyroWidget.set_angle(value))
            self.toolbox.slider2.valueChanged.connect(lambda value: self.gyrosWidget.set_pitch_angle(value))

            self.toolbox.slider3.valueChanged.connect(lambda value: self.update_label_and_rotation(value, "roll"))
            self.toolbox.slider3.valueChanged.connect(lambda value: self.rollGyroWidget.set_angle(value))
            self.toolbox.slider3.valueChanged.connect(lambda value: self.gyrosWidget.set_roll_angle(value))

        # ============ Spectogram and Gyroscope Layout ============
        self.openglWidget = App()
        self.gyroSpectogramLayout.addWidget(self.openglWidget)
        self.gyroLayout.addWidget(self.circleWidget)
        self.gyroSpectogramLayout.addLayout(self.gyroLayout)
        # =========================================================

        self.layout.addLayout(self.gyroGraphLayout)
        self.layout.addLayout(self.gyroSpectogramLayout)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    # For debug purposes
    def update_label_and_rotation(self, value: int, axis: str):
        if axis == "yaw":
            if __debug__:
                self.toolbox.label1.setText(f"Yaw: {value}")
        elif axis == "pitch":
            if __debug__:
                self.toolbox.label2.setText(f"Pitch: {value}")
        elif axis == "roll":
            if __debug__:
                self.toolbox.label3.setText(f"Roll: {value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())