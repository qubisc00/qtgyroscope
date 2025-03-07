# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 QtDataVisualization example"""

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication, QSizePolicy, QMainWindow, QWidget, QVBoxLayout
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DCore import Qt3DCore
from PySide6.QtGui import (QGuiApplication, QVector3D)

class Cube(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super().__init__()

        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 5))
        self.camera().setViewCenter(QVector3D(0, 0, 0))

        # For camera controls
        self.createScene()
        # self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        # self.camController.setLinearSpeed(50)
        # self.camController.setLookSpeed(180)
        # self.camController.setCamera(self.camera())

        self.setRootEntity(self.rootEntity)

    def createScene(self):
        # Root entity
        self.rootEntity = Qt3DCore.QEntity()

        # Material
        self.material = Qt3DExtras.QPhongMaterial(self.rootEntity)

        # Cube
        self.cubeEntity = Qt3DCore.QEntity(self.rootEntity)
        self.cubeMesh = Qt3DExtras.QCuboidMesh()

        self.cubeTransform = Qt3DCore.QTransform()
        self.cubeTransform.setScale(2)

        self.cubeEntity.addComponent(self.cubeMesh)
        self.cubeEntity.addComponent(self.cubeTransform)
        self.cubeEntity.addComponent(self.material)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Test')

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.bars = Cube()
        self.container = QWidget.createWindowContainer(self.bars)
        geometry = QGuiApplication.primaryScreen().geometry()
        self.container.setFixedSize(200, 200)

        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        # self.setCentralWidget(self.container)

        layout.addWidget(self.container)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())