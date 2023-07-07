from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel, QToolBar, QStatusBar, QMainWindow, QSizePolicy, QFileDialog, QWidget, QMessageBox
from PyQt6.QtCore import Qt
from ..toolbar import Main_ToolBar, Utils_ToolBar, Color_ToolBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Paint")
        self.setWindowIcon(QtGui.QIcon("C:/GitHub/Paint/assets/icon.png"))

        self.addToolBar(Main_ToolBar(self))
        self.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)
        self.addToolBar(Utils_ToolBar(self))
        self.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)
        self.addToolBar(Color_ToolBar(self))

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
    
        self.active = {"item": None, "type": None, "color": Qt.GlobalColor.black, "size": 10}

        self.last_x, self.last_y = None, None

        self.history = []
        self.saved = True
        self.filePath = False

    def setColor(self, color):
        self.active["color"] = QtGui.QColor(color)

        if self.active["type"] and self.active["type"] != "eraser":
            self.active["item"].setColor(QtGui.QColor(color))

    def setSize(self, size):
        self.active["size"] = size

        if self.active["size"]:
            self.active["size"].setWidth(size)

    def makeNewCanvas(self):
        if not self.saved:
            confirm = QMessageBox()
            confirm.setText("Do you want to save your work?")
            confirm.setIcon(QMessageBox.Icon.Warning)
            confirm.addButton(QMessageBox.StandardButton.Yes)
            confirm.addButton(QMessageBox.StandardButton.No)
            confirm.addButton(QMessageBox.StandardButton.Cancel)

            confirm.exec()

            if confirm.standardButton(confirm.clickedButton()) == QMessageBox.StandardButton.Yes:
                self.saveImage()

            elif confirm.standardButton(confirm.clickedButton()) != QMessageBox.StandardButton.No:
                return

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
        self.saved = True
        self.filePath = False

    def saveAsImage(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")

        if filePath == "":
            return
                
        self.canvas.image.save(filePath)
        self.filePath = filePath

        self.saved = True

    def saveImage(self):
        if not self.filePath:
            self.saveAsImage()
            return

        self.canvas.image.save(self.filePath)

        self.saved = True

    def openImage(self):
        if not self.saved:
            confirm = QMessageBox()
            confirm.setText("Do you want to save your work?")
            confirm.setIcon(QMessageBox.Icon.Warning)
            confirm.addButton(QMessageBox.StandardButton.Yes)
            confirm.addButton(QMessageBox.StandardButton.No)
            confirm.addButton(QMessageBox.StandardButton.Cancel)

            confirm.exec()

            if confirm.standardButton(confirm.clickedButton()) == QMessageBox.StandardButton.Yes:
                self.saveImage()
            
            elif confirm.standardButton(confirm.clickedButton()) != QMessageBox.StandardButton.No:
                return

        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")

        if filePath == "":
            return
        
        with open(filePath, "rb") as f:
            data = f.read()

        self.canvas.image.loadFromData(data)
        self.canvas.image = self.canvas.image.scaled(self.canvas.width(), self.canvas.height(), Qt.AspectRatioMode.IgnoreAspectRatio)
        self.canvas.update()

        self.filePath = filePath

        self.saved = True

    def closeEvent(self, event: QtGui.QCloseEvent):
        if not self.saved:
            confirm = QMessageBox()
            confirm.setText("Do you want to save your work?")
            confirm.setIcon(QMessageBox.Icon.Warning)
            confirm.addButton(QMessageBox.StandardButton.Yes)
            confirm.addButton(QMessageBox.StandardButton.No)
            confirm.addButton(QMessageBox.StandardButton.Cancel)

            confirm.exec()

            if confirm.standardButton(confirm.clickedButton()) == QMessageBox.StandardButton.Yes:
                self.saveImage()

            elif confirm.standardButton(confirm.clickedButton()) != QMessageBox.StandardButton.No:
                event.ignore()
                return
            
        event.accept()

    def setCustomCursor(self, cursor):
        self.setCursor(cursor)

class Canvas(QWidget):
    def __init__(self, parent: MainWindow):
        super().__init__(parent)

        self.image = QtGui.QImage(self.width(), self.height(), QtGui.QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)

        self.setMinimumSize(400, 400)

        self.last_x, self.last_y = None, None

    def drawPoint(self, x, y):
        painter = QtGui.QPainter(self.image)
        pen = self.parent().active["item"]
        painter.setPen(pen)
        painter.drawPoint(x, y)

        self.update()

    def drawLine(self, x, y):
        painter = QtGui.QPainter(self.image)
        pen = self.parent().active["item"]
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, x, y)

        self.last_x, self.last_y = x, y

        self.update()

    def fill(self, x, y):
        painter = QtGui.QPainter(self.image)
        pen = self.parent().active["item"]
        painter.setPen(pen)
        
        image = self.image
        color = image.pixel(x, y)

        queue = [(x, y)]
        visited = set()

        while queue:
            x, y = queue.pop()
            if image.pixel(x, y) == color:
                painter.drawPoint(x, y)

                points = []
                cx, cy = x, y
                for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    xx, yy = cx + x, cy + y
                    if (xx >= 0 and xx < image.width() and yy >= 0 and yy < image.height() and (xx, yy) not in visited):
                        points.append((xx, yy))
                        visited.add((xx, yy))

                queue = points + queue
        
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if self.parent().active["type"]:
            if self.parent().active["type"] in ("pen", "eraser"):
                self.drawPoint(event.pos().x(), event.pos().y())
            
            elif self.parent().active["type"] in ("fill_bucket"):
                self.fill(event.pos().x(), event.pos().y())

            self.parent().saved = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.parent().active["type"]:
            if self.parent().active["type"] in ("pen", "eraser"):
                if not self.last_x:
                    self.last_x, self.last_y = event.pos().x(), event.pos().y()
                    return

                self.drawLine(event.pos().x(), event.pos().y())
            
            self.parent().saved = False

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self.last_x, self.last_y = None, None

    def paintEvent(self, event):
        canvasPainter = QtGui.QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

# MAKE A SERVER TO UPLOAD PICTURES TOO