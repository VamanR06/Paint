from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QToolButton

class File(QToolButton):
    def __init__(self, parent):
        super().__init__(text="File", parent=parent)

        self.setStatusTip("File")

        menu = QMenu()
        menu.addAction(New(self))
        menu.addAction(Open(self))
        menu.addAction(Save(self))
        menu.addAction(SaveAs(self))

        self.setMenu(menu)

        self.clicked.connect(self.on_trigger)

    def on_trigger(self):
        self.showMenu()

class New(QAction):
    def __init__(self, parent):
        super().__init__("New", parent)

        self.triggered.connect(self.on_trigger)

    def on_trigger(self):
        self.parent().parent().parent().makeNewCanvas()

class Open(QAction):
    def __init__(self, parent):
        super().__init__("Open", parent)

class Save(QAction):
    def __init__(self, parent):
        super().__init__("Save", parent)

class SaveAs(QAction):
    def __init__(self, parent):
        super().__init__("Save As", parent)

        self.triggered.connect(self.on_trigger)

    def on_trigger(self):
        self.parent().parent().parent().saveImage()