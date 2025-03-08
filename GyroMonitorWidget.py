import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

plt.rcParams["font.size"] = 7

class GyroMonitorWidget(QWidget):
    def __init__(self, title=None):
        super().__init__()

        self.angle = 0
        self.max_value = 0

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setFixedSize(400,200)

        # Create Matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.fig.set_tight_layout(True)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas)

        # Initialize data
        self.x_data = np.linspace(-10, 0, 11)  # Time from -10s to 0s
        self.y_data = np.zeros_like(self.x_data)  # Placeholder for gyro angles
        self.line, = self.ax.plot(self.x_data, self.y_data, marker='', linestyle='-')

        # Formatting
        # self.ax.set_xlim(-10, 0)
        self.set_y_limit()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("deg (°)")
        self.ax.set_title(title)
        self.ax.grid(True)

        # Timer for updating data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  # Update every second

    def set_angle(self, angle=None):
        if angle is not None:
            self.angle = angle

    def update_plot(self):
        self.y_data = np.roll(self.y_data, -1)
        self.y_data[-1] = self.angle

        self.set_y_limit()

        # Update plot
        self.line.set_ydata(self.y_data)
        self.canvas.draw()

    def set_y_limit(self):
        # Calculate the upper and lower limits
        upper_limit = int(abs(self.y_data.max())) + 5
        bottom_limit = int(self.y_data.min()) - 5

        # Ensure that the limit doesn't exceed 180
        if upper_limit > 180:
            upper_limit = 180
        if bottom_limit < -180:
            bottom_limit = -180

        # Set the y-axis limits
        self.ax.set_ylim(bottom_limit, upper_limit)

        # Calculate the total range
        total_range = upper_limit - bottom_limit

        # Calculate a dynamic step size based on the mean limit and range
        step_size = round(total_range / 6)  # Try for about 6 ticks (this can be adjusted)

        # Optionally, ensure the step size is a reasonable value (e.g., multiple of 5, 10, etc.)
        if step_size < 5:
            step_size = 5  # Avoid very small step sizes
        elif step_size % 5 != 0:
            step_size = (step_size // 5) * 5  # Round to the nearest multiple of 5

        # Set y-ticks with the calculated step size
        self.ax.set_yticks(range(bottom_limit, upper_limit + 1, step_size))