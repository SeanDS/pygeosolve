import sys

import PyQt4.Qt
import PyQt4.QtCore
import PyQt4.QtGui
from PyQt4.QtGui import QGraphicsLineItem as QLine

class Canvas(object):
    qApplication = None
    qMainWindow = None
    qScene = None
    qView = None

    def __init__(self, *args, **kwargs):
        # create and initialise GUI
        self.create()
        self.initialise()

    def create(self):
        # create application
        self.qApplication = PyQt4.Qt.QApplication(sys.argv)
        self.qMainWindow = MainWindow()

        # set close behaviour to prevent zombie processes
        self.qMainWindow.setAttribute(PyQt4.QtCore.Qt.WA_DeleteOnClose, True)

        # create drawing area
        self.qScene = GraphicsScene()

        # create view
        self.qView = GraphicsView(self.qScene, self.qMainWindow)

        # set window title
        self.qMainWindow.setWindowTitle('pygeosolve')
        
    def initialise(self):
        # set view antialiasing
        self.qView.setRenderHints(PyQt4.QtGui.QPainter.Antialiasing | PyQt4.Qt.QPainter.TextAntialiasing | PyQt4.Qt.QPainter.SmoothPixmapTransform | PyQt4.QtGui.QPainter.HighQualityAntialiasing)
        
        # set central widget to be the view
        self.qMainWindow.setCentralWidget(self.qView)

        # resize main window to fit content
        self.qMainWindow.setFixedSize(500, 500)

    def calibrateView(self):
        self.qView.fitInView(self.qScene.itemsBoundingRect(), PyQt4.QtCore.Qt.KeepAspectRatio)
        self.qView.scale(5, 5)
        
    def addLine(self, line):
        graphicsLine = QLine()
        graphicsLine.setLine(line.start.x.value, line.start.y.value, line.end.x.value, line.end.y.value)

        self.qScene.addItem(graphicsLine)

    def show(self):
        self.calibrateView()

        # show on screen
        self.qMainWindow.show()

        sys.exit(self.qApplication.exec_())

class MainWindow(PyQt4.Qt.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

class GraphicsScene(PyQt4.QtGui.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super(GraphicsScene, self).__init__(*args, **kwargs)

class GraphicsView(PyQt4.QtGui.QGraphicsView):  
    def __init__(self, *args, **kwargs):    
        # now initialise as normal
        super(GraphicsView, self).__init__(*args, **kwargs)