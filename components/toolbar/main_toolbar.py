from PyQt6.QtWidgets import QToolBar, QStatusBar
from PyQt6.QtCore import Qt
from ..buttons import File, Exit

class Main_ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setMovable(False)

        self.addWidget(File(self))
        self.addAction(Exit(self))