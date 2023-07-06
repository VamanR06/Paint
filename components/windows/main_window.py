from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel, QToolBar, QStatusBar, QMainWindow, QSizePolicy, QFileDialog
from PyQt6.QtCore import Qt
from ..toolbar import Main_ToolBar, Utils_ToolBar, Color_ToolBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.addToolBar(Main_ToolBar(self))
        self.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)
        self.addToolBar(Utils_ToolBar(self))
        self.addToolBarBreak(Qt.ToolBarArea.TopToolBarArea)
        self.addToolBar(Color_ToolBar(self))

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)

        self.image = QtGui.QImage(self.canvas.width(), self.canvas.height(), QtGui.QImage.Format.Format_RGB32)
    
        self.setStatusBar(QStatusBar(self))

        self.active = {"item": None, "type": None, "color": Qt.GlobalColor.black, "size": 10}

        self.last_x, self.last_y = None, None

        self.history = []
        self.saved = False

    def setColor(self, color):
        self.active["color"] = QtGui.QColor(color)

        if self.active["type"] and self.active["type"] != "eraser":
            self.active["item"].setColor(QtGui.QColor(color))

    def setSize(self, size):
        self.active["size"] = size

        if self.active["size"]:
            self.active["size"].setWidth(size)

    def makeNewCanvas(self):
        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)

    def saveImage(self):
        filePath = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)")

        if not filePath:
            return
                
        self.image.save(filePath[0])

    # def resizeEvent(self, event: QtGui.QResizeEvent):
    #     canvas = self.label.pixmap()
    #     canvas = canvas.scaled(self.width(), self.height())
    #     self.label.setPixmap(canvas)

class Canvas(QLabel):
    def __init__(self, parent: MainWindow):
        super().__init__(parent)
        canvas = QtGui.QPixmap(800, 800)
        canvas.fill(Qt.GlobalColor.white)
        self.setPixmap(canvas)

        # self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setAlignment(Qt.AlignmentFlag.AlignAbsolute)
        # self.setMinimumSize(10,10)

        self.last_x, self.last_y = None, None

    def drawPoint(self, x, y):
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = self.parent().active["item"]
        painter.setPen(pen)
        painter.drawPoint(x, y)
        painter.end()
        self.setPixmap(canvas)

    def drawLine(self, x, y):
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = self.parent().active["item"]
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, x, y)
        painter.end()
        self.setPixmap(canvas)

        self.last_x, self.last_y = x, y

    def fill(self, x, y):
        canvas = self.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = self.parent().active["item"]
        painter.setPen(pen)
        
        image = canvas.toImage()
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

        painter.end()
        self.setPixmap(canvas)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if self.parent().active["type"]:
            if self.parent().active["type"] in ("pen", "eraser"):
                self.drawPoint(event.pos().x(), event.pos().y())
            
            elif self.parent().active["type"] in ("fill_bucket"):
                self.fill(event.pos().x(), event.pos().y())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.parent().active["type"]:
            if self.parent().active["type"] in ("pen", "eraser"):
                if not self.last_x:
                    self.last_x, self.last_y = event.pos().x(), event.pos().y()
                    return

                self.drawLine(event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self.last_x, self.last_y = None, None

    # def resizeEvent(self, event: QtGui.QResizeEvent):
    #     canvas = self.pixmap()
    #     canvas = canvas.scaled(self.width(), self.height(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
    #     self.setPixmap(canvas)