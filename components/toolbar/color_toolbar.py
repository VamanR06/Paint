from PyQt6 import QtGui
from PyQt6.QtWidgets import QToolBar, QStatusBar, QPushButton, QColorDialog
from PyQt6.QtCore import Qt

COLORS = [
    '#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
    '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

class Color_ToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setMovable(False)

        for i in COLORS:
            button = PaletteButton(i, self)
            self.addWidget(button)

        self.custom_color = QPushButton()
        self.setStyleSheet("background-color: #FFFFFF")

        self.custom_color.clicked.connect(self.openColorPicker)

        self.addWidget(self.custom_color)

    def openColorPicker(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.parent().setColor(color)
            red, green, blue = color.toRgb().red(), color.toRgb().green(), color.toRgb().blue()
            self.custom_color.setStyleSheet(f"background-color: rgb({red}, {green}, {blue})")

class PaletteButton(QPushButton):
    def __init__(self, color, parent):
        super().__init__(parent)
        self.setCheckable(True)

        self.color = color
        if color == "#000000":
            self.setChecked(True)

        self.setStyleSheet(f"background-color: {color}")
        self.pressed.connect(self.on_click)
    
    def on_click(self):
        for i in self.parent().children():
            if isinstance(i, PaletteButton):
                if i.isChecked():
                    i.setChecked(False)

        self.parent().parent().setColor(self.color)