from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor
import math

class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0  # Initial angle in degrees
        self.setMinimumSize(200, 200)

    def set_angle(self, angle):
        self.angle = angle
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define circle properties
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 3
        
        # Draw circle
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(center, radius, radius)
        
        # Calculate dot position
        radians = math.radians(self.angle - 90)
        dot_x = center.x() + radius * math.cos(radians)
        dot_y = center.y() + radius * math.sin(radians)
        
        # Draw dot
        painter.setPen(QPen(Qt.red))
        painter.setBrush(QColor(Qt.red))
        painter.drawEllipse(QPointF(dot_x, dot_y), 5, 5)