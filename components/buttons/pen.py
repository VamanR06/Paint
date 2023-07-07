from PyQt6.QtGui import QAction, QIcon
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolButton, QMenu, QPushButton, QVBoxLayout, QHBoxLayout

class Pen(QToolButton):
    def __init__(self, parent):
        super().__init__(icon=QIcon("C:/GitHub/Paint/assets/pen.png"), parent=parent)

        self.setStatusTip("Pen")
        self.setCheckable(True)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        for i in self.parent().children():
            if isinstance(i, QToolButton):
                if i.isChecked():
                    i.setChecked(False)

        self.setChecked(True)
        self.parent().parent().active["type"] = "pen"
        self.parent().parent().active["item"] = QtGui.QPen(self.parent().parent().active["color"] if self.parent().parent().active["color"] else Qt.GlobalColor.black, self.parent().parent().active["size"])
    
        self.parent().parent().setCustomCursor(QtGui.QCursor(QtGui.QPixmap("C:/GitHub/Paint/assets/pen.png")))