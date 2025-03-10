import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

plt.rcParams["font.size"] = 7
plt.style.use('dark_background')

class GyroMonitorWidget(QWidget):
    def __init__(self, title=None):
        super().__init__()

        self.angle = 0
        self.max_value = -np.inf
        self.min_value = np.inf

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setFixedSize(400, 200)

        # Create Matplotlib figure
        self.fig, self.ax = plt.subplots()
        self.fig.set_tight_layout(True)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas)

        # Initialize data
        self.x_data = np.linspace(-10, 0, 11)  # Time from -10s to 0s
        self.y_data = np.zeros_like(self.x_data)  # Placeholder for gyro angles
        self.line, = self.ax.plot(self.x_data, self.y_data, marker='', linestyle='-', color='green')

        # Formatting
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("deg (°)")
        self.ax.set_ylim(-190, 190)  # Set y-axis limits
        self.ax.set_yticks(np.linspace(190, -190, 5))  # Set y-axis ticks from 180 to -180 in 20 steps
        self.ax.grid(False)

        # Store the background for blitting
        self.background = None
        self.canvas.mpl_connect('draw_event', self.on_draw)

        # Set up FuncAnimation
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=1000, blit=True)

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

    def set_angle(self, angle=None):
        if angle is not None:
            self.angle = angle

    def update_plot(self, frame):
        self.y_data = np.roll(self.y_data, -1)
        self.y_data[-1] = self.angle

        # Update max and min values
        self.max_value = max(self.max_value, self.angle)
        self.min_value = min(self.min_value, self.angle)

        # Update plot
        self.line.set_ydata(self.y_data)

        # Blit only the updated part
        if self.background is not None:
            self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.line)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()  # Use draw_idle instead of draw

        return self.line,  # Return the updated line for blitting
