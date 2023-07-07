from PyQt6.QtGui import QAction, QIcon
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolButton, QMenu, QPushButton, QVBoxLayout, QHBoxLayout

class Eraser(QToolButton):
    def __init__(self, parent):
        super().__init__(icon=QIcon("C:/GitHub/Paint/assets/eraser.png"), parent=parent)

        self.setStatusTip("Eraser")
        self.setCheckable(True)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        for i in self.parent().children():
            if isinstance(i, QToolButton):
                if i.isChecked():
                    i.setChecked(False)

        self.setChecked(True)
        self.parent().parent().active["type"] = "eraser"
        self.parent().parent().active["item"] = QtGui.QPen(Qt.GlobalColor.white, self.parent().parent().active["size"])

        self.parent().parent().setCustomCursor(QtGui.QCursor(QtGui.QPixmap("C:/GitHub/Paint/assets/eraser.png")))