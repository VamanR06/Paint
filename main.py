import sys
from PyQt6 import QtGui, QtWidgets
from components.windows.main_window import MainWindow

app = QtWidgets.QApplication([])
window = MainWindow()

window.show()

app.exec()