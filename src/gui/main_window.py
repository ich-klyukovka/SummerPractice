from PyQt5.QtWidgets import QMainWindow
from PyQt5 import Qt

from SummerPractice.src.gui.main_window_ui import Ui_MainWindow
from SummerPractice.src.gui.parameters_dock import ParametersDock
from SummerPractice.src.gui.mpl_canvas import MplCanvas
from SummerPractice.src.gui.info_widget import InfoWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.parametersDock = ParametersDock()
        self.infoWidget = InfoWidget()
        self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.parametersDock)
        self.addDockWidget(Qt.Qt.RightDockWidgetArea, self.infoWidget)

        self.canvas = MplCanvas(self.canvas)

        self.nextButton.clicked.connect(self.next)

        #self.parametersDock.goButtonClicked.connect(self.plotFunction)

        self.isPlaying = False

    def next(self):
        print('Next')
