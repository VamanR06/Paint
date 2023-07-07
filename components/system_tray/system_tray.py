from PyQt6 import QtGui, QtWidgets
from ..windows.main_window import MainWindow

class System_Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()

        self.app = app

        self.setIcon(QtGui.QIcon("C:/GitHub/Paint/assets/icon.png"))
        self.setVisible(True)

        tray_menu = QtWidgets.QMenu()
        
        self.quit_app = QtGui.QAction("Quit")
        self.quit_app.triggered.connect(app.quit)
        
        self.reopen_app = QtGui.QAction("Open")
        self.reopen_app.triggered.connect(lambda: self.app.window.show() if self.app.lastWindowClosed else None)

        tray_menu.addAction(self.reopen_app)
        tray_menu.addAction(self.quit_app)

        self.setContextMenu(tray_menu)