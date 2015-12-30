import sys

import PyQt4.Qt
import PyQt4.QtCore
import PyQt4.QtGui
from PyQt4.QtGui import QGraphicsLineItem as QLine

class Canvas(object):
    application = None
    main_window = None
    scene = None
    view = None

    def __init__(self, *args, **kwargs):
        # create and initialise GUI
        self.create()
        self.initialise()

    def create(self):
        # create application
        self.application = PyQt4.Qt.QApplication(sys.argv)
        self.main_window = MainWindow()

        # set close behaviour to prevent zombie processes
        self.main_window.setAttribute(PyQt4.QtCore.Qt.WA_DeleteOnClose, True)

        # create drawing area
        self.scene = GraphicsScene()

        # create view
        self.view = GraphicsView(self.scene, self.main_window)

        # set window title
        self.main_window.setWindowTitle('pygeosolve')
        
    def initialise(self):
        # set view antialiasing
        self.view.setRenderHints(PyQt4.QtGui.QPainter.Antialiasing | PyQt4.Qt.QPainter.TextAntialiasing | PyQt4.Qt.QPainter.SmoothPixmapTransform | PyQt4.QtGui.QPainter.HighQualityAntialiasing)
        
        # set central widget to be the view
        self.main_window.setCentralWidget(self.view)

        # resize main window to fit content
        self.main_window.setFixedSize(500, 500)

    def calibrateView(self):
        self.view.fitInView(self.scene.itemsBoundingRect(), PyQt4.QtCore.Qt.KeepAspectRatio)
        self.view.scale(5, 5)
        
    def addLine(self, line):
        graphicsLine = QLine()
        graphicsLine.setLine(line.start().x.value, line.start().y.value, line.end().x.value, line.end().y.value)

        self.scene.addItem(graphicsLine)

    def show(self):
        self.calibrateView()

        # show on screen
        self.main_window.show()

        sys.exit(self.application.exec_())

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