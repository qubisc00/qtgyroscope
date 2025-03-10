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
        self.max_value = 0

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
        self.set_y_limit()
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("deg (°)")
        self.ax.set_title(title)
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

        self.set_y_limit()

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

    def set_y_limit(self):
        # Get the min and max values of the current data
        y_min, y_max = self.y_data.min(), self.y_data.max()

        # Ensure a minimum range (start with small zoom)
        min_range = 10  # Minimum vertical range (e.g., from -5 to 5 initially)
        buffer = 10  # Additional padding around the data

        # Calculate new limits with buffer
        bottom_limit = y_min - buffer
        upper_limit = y_max + buffer

        # Ensure the range is at least `min_range`
        if upper_limit - bottom_limit < min_range:
            center = (y_max + y_min) / 2  # Find the center of the data
            bottom_limit = center - min_range / 2
            upper_limit = center + min_range / 2

        # Apply the new limits
        self.ax.set_ylim(bottom_limit, upper_limit)

        # Let Matplotlib determine smart tick locations
        self.ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10, integer=True))

