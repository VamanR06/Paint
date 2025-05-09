import sys
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMenu, QToolButton, QMessageBox

class File(QToolButton):
    def __init__(self, parent):
        super().__init__(text="File", parent=parent)

        self.setStatusTip("File")

        menu = QMenu()
        menu.addAction(New(self))
        menu.addAction(Open(self))
        menu.addAction(Save(self))
        menu.addAction(SaveAs(self))
        menu.addAction(Exit(self))

        self.setMenu(menu)

        self.clicked.connect(self.on_trigger)

    def on_trigger(self):
        self.showMenu()

class New(QAction):
    def __init__(self, parent):
        super().__init__("New", parent)

        self.triggered.connect(self.on_trigger)

        self.setShortcut(QKeySequence("Ctrl+n"))

    def on_trigger(self):
        self.parent().parent().parent().makeNewCanvas()

class Open(QAction):
    def __init__(self, parent):
        super().__init__("Open", parent)

        self.triggered.connect(self.on_trigger)

        self.setShortcut(QKeySequence("Ctrl+o"))

    def on_trigger(self):
        self.parent().parent().parent().openImage()

class Save(QAction):
    def __init__(self, parent):
        super().__init__("Save", parent)

        self.triggered.connect(self.on_trigger)

        self.setShortcut(QKeySequence("Ctrl+s"))

    def on_trigger(self):
        self.parent().parent().parent().saveImage()

class SaveAs(QAction):
    def __init__(self, parent):
        super().__init__("Save As", parent)

        self.triggered.connect(self.on_trigger)

        self.setShortcut(QKeySequence("Ctrl+Shift+s"))

    def on_trigger(self):
        self.parent().parent().parent().saveAsImage()

class Exit(QAction):
    def __init__(self, parent):
        super().__init__(text="Exit", parent=parent)

        self.triggered.connect(self.on_trigger)

        self.setShortcut(QKeySequence("Ctrl+q"))

    def on_trigger(self):
        if not self.parent().parent().parent().saved:
            confirm = QMessageBox()
            confirm.setText("Do you want to save your work?")
            confirm.setIcon(QMessageBox.Icon.Warning)
            confirm.addButton(QMessageBox.StandardButton.Yes)
            confirm.addButton(QMessageBox.StandardButton.No)
            confirm.addButton(QMessageBox.StandardButton.Cancel)

            confirm.exec()

            if confirm.standardButton(confirm.clickedButton()) == QMessageBox.StandardButton.Yes:
                if not self.parent().parent().parent().saveImage():
                    return

            elif confirm.standardButton(confirm.clickedButton()) != QMessageBox.StandardButton.No:
                return
            
        sys.exit()