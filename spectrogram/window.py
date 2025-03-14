from spectrogram import config
import moderngl
import time

from PySide6.QtCore import QTimer
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget

class Window(QOpenGLWidget):

	frame_rate = 61

	def __init__(self):
		super().__init__()

		self.setFixedSize(
				config.WINDOW_WIDTH,
				config.WINDOW_HEIGHT)

		fmt = QSurfaceFormat()
		fmt.setVersion(3, 3)
		fmt.setProfile(QSurfaceFormat.CoreProfile)
		fmt.setDefaultFormat(fmt)
		fmt.setSamples(4)
		self.setFormat(fmt)

		self.t = None

		self.timer = QTimer()
		self.timer.timeout.connect(self.update)
		self.timer.start(int(1000 / self.frame_rate))

	#-------------------
	#	Opengl Logic
	#-------------------
	
	def initializeGL(self):
		self.ctx = moderngl.create_context(require=330)
		self.ctx.clear(0.0, 0.0, 0.0)
		self.ctx.enable(moderngl.BLEND)
		self.ctx.multisample = True
		self.init()

	def resizeGL(self, w, h):
		self.size(w, h)

	def paintGL(self):
		now = time.time()
		dt = now - self.t if self.t else 1.0 / self.frame_rate
		self.t = now
		self.draw(dt)