from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMenu, QToolButton

class Edit(QToolButton):
    def __init__(self, parent):
        super().__init__(text="Edit", parent=parent)

        self.setStatusTip("Edit")

        menu = QMenu()
        menu.addAction(Undo(self))
        menu.addAction(Redo(self))

        self.setMenu(menu)

        self.clicked.connect(self.on_trigger)

    def on_trigger(self):
        self.showMenu()

class Undo(QAction):
    def __init__(self, parent):
        super().__init__("Undo", parent)

        self.triggered.connect(self.on_trigger)

        self.setShortcut(QKeySequence("Ctrl+z"))

    def on_trigger(self):
        self.parent().parent().parent().undo()

class Redo(QAction):
    def __init__(self, parent):
        super().__init__("Redo", parent)

        self.triggered.connect(self.on_trigger)

        self.setShortcuts([QKeySequence("Ctrl+y"), QKeySequence("Ctrl+Shift+z")])

    def on_trigger(self):
        self.parent().parent().parent().redo()