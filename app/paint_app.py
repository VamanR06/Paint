from PyQt6 import QtWidgets, QtGui
from components.windows.main_window import MainWindow
from components.system_tray.system_tray import System_Tray
import pathlib, os

os.chdir(pathlib.Path(__file__).parent.absolute())

class PaintApp(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])

        self.setWindowIcon(QtGui.QIcon("./assets/icon.png"))

        self.setQuitOnLastWindowClosed(True)

        self.window = MainWindow()
        self.window.show()

        self.tray = System_Tray(app=self)

app = PaintApp()

app.exec()