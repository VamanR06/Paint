import sys
from PyQt6 import QtGui, QtWidgets
from components.windows.main_window import MainWindow
from components.system_tray.system_tray import System_Tray

app = QtWidgets.QApplication([])
app.setQuitOnLastWindowClosed(True)

app.__dict__["window"] = MainWindow()

app.__dict__["window"].show()

tray = System_Tray(app=app)

app.exec()