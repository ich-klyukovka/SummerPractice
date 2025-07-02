from PyQt5.QtWidgets import QDockWidget
from SummerPractice.src.gui.info_widget_ui import Ui_InfoWidget

class InfoWidget(QDockWidget, Ui_InfoWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)