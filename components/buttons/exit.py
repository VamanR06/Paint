from PyQt6.QtGui import QAction
import sys

class Exit(QAction):
    def __init__(self, parent):
        super().__init__(text="Exit", parent=parent)

        self.setStatusTip("Click here to exit")

        self.triggered.connect(self.on_trigger)

    def on_trigger(self):
        sys.exit()