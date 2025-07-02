import matplotlib
# класс, который связывает Matplotlib с PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# объект, содержащий график
from matplotlib.figure import Figure

import numpy as np

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width: int = 8, height: int = 4, dpi: int = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)      # контейнер для графика
        self.axes = fig.add_subplot()   # добавлен подграфик (область, где будет нарисован график)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)

    def plot_points(self, x_points: list[float], y_points: list[float], fmt: str = 'b-'):
        self.axes.plot(x_points, y_points, fmt)       # fmt формат отображения точек
        self.draw()

    def clear(self):
        self.axes.clear()
        self.draw()