from PyQt6.QtGui import QAction, QIcon
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QToolButton, QMenu, QPushButton, QVBoxLayout, QHBoxLayout

class Fill_Bucket(QToolButton):
    def __init__(self, parent):
        super().__init__(icon=QIcon("./assets/fill_bucket.png"), parent=parent)

        self.setStatusTip("Fill Bucket")
        self.setCheckable(True)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        for i in self.parent().children():
            if isinstance(i, QToolButton):
                if i.isChecked():
                    i.setChecked(False)

        self.setChecked(True)
        self.parent().parent().active["type"] = "fill_bucket"
        self.parent().parent().active["item"] = QtGui.QPen(self.parent().parent().active["color"] if self.parent().parent().active["color"] else Qt.GlobalColor.black, 1)

        self.parent().parent().setCustomCursor(QtGui.QCursor(QtGui.QPixmap("./assets/fill_bucket.png")))