from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMessageBox
import sys

class Exit(QAction):
    def __init__(self, parent):
        super().__init__(text="Exit", parent=parent)

        self.setStatusTip("Click here to exit")

        self.triggered.connect(self.on_trigger)

    def on_trigger(self):
        if not self.parent().parent().saved:
            confirm = QMessageBox()
            confirm.setText("Do you want to save your work?")
            confirm.setIcon(QMessageBox.Icon.Warning)
            confirm.addButton(QMessageBox.StandardButton.Yes)
            confirm.addButton(QMessageBox.StandardButton.No)
            confirm.addButton(QMessageBox.StandardButton.Cancel)

            confirm.exec()

            if confirm.standardButton(confirm.clickedButton()) == QMessageBox.StandardButton.Yes:
                self.parent().parent().saveImage()

            elif confirm.standardButton(confirm.clickedButton()) != QMessageBox.StandardButton.No:
                return
            
        sys.exit()