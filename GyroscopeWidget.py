from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DCore import Qt3DCore
from PySide6.QtGui import (QVector3D, QQuaternion)

class GyroscopeWidget(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super().__init__()

        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 5))
        self.camera().setViewCenter(QVector3D(0, 0, 0))

        # For camera controls
        self.createScene()

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

    def update_rotation(self, yaw: float, pitch: float, roll: float):
        # Create the quaternion rotations for each axis
        quaternionYaw = QQuaternion.fromEulerAngles(0, -yaw, 0)
        quaternionPitch = QQuaternion.fromEulerAngles(-pitch, 0, 0)
        quaternionRoll = QQuaternion.fromEulerAngles(0, 0, -roll)

        # Combine all rotations in the proper order
        finalQuaternion = quaternionYaw * quaternionPitch * quaternionRoll

        # Apply the final quaternion rotation to the cube
        self.cubeTransform.setRotation(finalQuaternion)