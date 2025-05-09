from PyQt6.QtWidgets import QToolBar, QWidget
from ..buttons import Pen, Eraser, Fill_Bucket

class Utils_ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setMovable(False)

        self.addWidget(Pen(self))
        self.addWidget(Fill_Bucket(self))
        self.addWidget(Eraser(self))

    def addWidget(self, widget: QWidget):
        super().addWidget(widget)
        self.addSeparator()