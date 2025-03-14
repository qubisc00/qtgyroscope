import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

plt.rcParams["font.size"] = 7
plt.style.use('dark_background')

class GyrosMonitorWidget(QWidget):
    def __init__(self, title=None):
        super().__init__()

        self.yaw_angle = 0
        self.pitch_angle = 0
        self.roll_angle = 0
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
        self.yaw_data = np.zeros_like(self.x_data)  # Placeholder for yaw angles
        self.pitch_data = np.zeros_like(self.x_data)  # Placeholder for pitch angles
        self.roll_data = np.zeros_like(self.x_data)  # Placeholder for roll angles

        # Create lines for yaw, pitch, and roll
        self.yaw_line, = self.ax.plot(self.x_data, self.yaw_data, marker='', linestyle='-', color='green', label='Yaw')
        self.pitch_line, = self.ax.plot(self.x_data, self.pitch_data, marker='', linestyle='-', color='blue', label='Pitch')
        self.roll_line, = self.ax.plot(self.x_data, self.roll_data, marker='', linestyle='-', color='red', label='Roll')

        # Formatting
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("deg (°)")
        self.ax.set_ylim(-190, 190)  # Set y-axis limits
        self.ax.set_yticks(np.linspace(190, -190, 5))  # Set y-axis ticks from 180 to -180 in 20 steps
        self.ax.grid(False)
        self.ax.legend()
        
        self.ax.set_title(title)

        # Store the background for blitting
        self.background = None
        self.canvas.mpl_connect('draw_event', self.on_draw)

        # Set up FuncAnimation
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=1000, blit=True)

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)

    def set_yaw_angle(self, yaw=None):
        if yaw is not None:
            self.yaw_angle = yaw
            
    def set_pitch_angle(self, pitch=None):
        if pitch is not None:
            self.pitch_angle = pitch
            
    def set_roll_angle(self, roll=None):
        if roll is not None:
            self.roll_angle = roll

    def update_plot(self, frame):
        self.yaw_data = np.roll(self.yaw_data, -1)
        self.yaw_data[-1] = self.yaw_angle

        self.pitch_data = np.roll(self.pitch_data, -1)
        self.pitch_data[-1] = self.pitch_angle

        self.roll_data = np.roll(self.roll_data, -1)
        self.roll_data[-1] = self.roll_angle

        # Update max and min values
        self.max_value = max(self.max_value, self.yaw_angle, self.pitch_angle, self.roll_angle)
        self.min_value = min(self.min_value, self.yaw_angle, self.pitch_angle, self.roll_angle)

        # Update plot
        self.yaw_line.set_ydata(self.yaw_data)
        self.pitch_line.set_ydata(self.pitch_data)
        self.roll_line.set_ydata(self.roll_data)

        # Blit only the updated part
        if self.background is not None:
            self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.yaw_line)
            self.ax.draw_artist(self.pitch_line)
            self.ax.draw_artist(self.roll_line)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()  # Use draw_idle instead of draw

        return self.yaw_line, self.pitch_line, self.roll_line  # Return the updated lines for blitting