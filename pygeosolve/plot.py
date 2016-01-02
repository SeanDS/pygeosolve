import sys

import PyQt4.Qt
from PyQt4.Qt import QApplication, QMainWindow
import PyQt4.QtCore
import PyQt4.QtGui
from PyQt4.QtGui import QGraphicsScene, QGraphicsView, QGraphicsLineItem as QLine

"""Plot classes"""

class Canvas(object):
    """Represents a drawing canvas for plotting primitives."""

    application = None
    """The Qt application object."""

    main_window = None
    """The Qt main window object."""

    scene = None
    """The Qt scene object."""

    view = None
    """The Qt view object."""

    def __init__(self, *args, **kwargs):
        """Creates a new canvas object and initialises it."""

        # create canvas contents
        self.create()

        # set some properties
        self.initialise()

    def create(self):
        # create application
        self.application = QApplication(sys.argv)
        self.main_window = QMainWindow()

        # create drawing area
        self.scene = QGraphicsScene()

        # create view
        self.view = QGraphicsView(self.scene, self.main_window)

    def initialise(self):
        # set close behaviour to prevent zombie processes
        self.main_window.setAttribute(PyQt4.QtCore.Qt.WA_DeleteOnClose, True)

        # set view antialiasing
        self.view.setRenderHints(PyQt4.QtGui.QPainter.Antialiasing \
        | PyQt4.Qt.QPainter.TextAntialiasing \
        | PyQt4.Qt.QPainter.SmoothPixmapTransform \
        | PyQt4.QtGui.QPainter.HighQualityAntialiasing)

        # set central widget to be the view
        self.main_window.setCentralWidget(self.view)

        # resize main window to fit content
        self.main_window.setFixedSize(500, 500)

        # set window title
        self.main_window.setWindowTitle('pygeosolve')

    def calibrate_view(self):
        # fit contents of scene in view
        self.view.fitInView(self.scene.itemsBoundingRect(), \
        PyQt4.QtCore.Qt.KeepAspectRatio)

        # set scale
        self.view.scale(5, 5)

    def add_line(self, line):
        """Adds a line to the scene.

        :param line: the :class:`~PyQt4.QtGui.QGraphicsLineItem` to add
        """

        # create new line
        graphicsLine = QLine()

        # set line properties
        graphicsLine.setLine(line.start().x.value, line.start().y.value, line.end().x.value, line.end().y.value)

        # add line to scene
        self.scene.addItem(graphicsLine)

    def show(self):
        """Shows the canvas on screen before exiting."""

        # calibrate view
        self.calibrate_view()

        # show on screen
        self.main_window.show()

        # exit with status
        sys.exit(self.application.exec_())
