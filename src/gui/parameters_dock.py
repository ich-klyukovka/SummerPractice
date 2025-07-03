from typing import TypedDict
from math import sqrt
from PyQt5.QtWidgets import QDockWidget, QMessageBox, QLabel, QSpinBox
from PyQt5.QtCore import pyqtSignal
from gui.ui.parameters_dock_ui import Ui_ParametersDock

class ParametersDock(QDockWidget, Ui_ParametersDock):
    goButtonClicked = pyqtSignal(dict, name='goButtonClicked')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.goButton.clicked.connect(self.emit_go_button_clicked)
        
        # Set default values and ranges
        self.populationSpinBox.setRange(1, 1000)  # Минимум 1, максимум 1000
        self.populationSpinBox.setValue(50)
        
        self.stepsAmountSpinBox.setRange(1, 10000)  # Минимум 1, максимум 10000
        self.stepsAmountSpinBox.setValue(100)
        
        self.mutationLineEdit.setText("0.2")
        self.crossoverineEdit.setText("0.9")

        # Добавляем поле для early_stop
        self.earlyStopLabel = QLabel("Early stop generations:")
        self.earlyStopSpinBox = QSpinBox()
        self.earlyStopSpinBox.setRange(1, 1000)
        self.earlyStopSpinBox.setValue(20)
        
        # Добавляем новые элементы в layout перед кнопкой
        layout = self.verticalLayout
        layout.insertWidget(layout.count() - 2, self.earlyStopLabel)  # -2 чтобы добавить перед spacer и кнопкой
        layout.insertWidget(layout.count() - 2, self.earlyStopSpinBox)
        
        # Example matrix
        example_matrix = " ".join(["10", "20", "30", "40", "10", "20", "30", "40", "10"])
        self.matrixLineEdit.setText(example_matrix)

    def verify_input(self) -> bool:
        matrix_text = self.matrixLineEdit.text()

        if not matrix_text:
            QMessageBox.critical(self, "Ошибка", "Введите матрицу")
            return False

        try:
            elements = list(map(float, matrix_text.split()))
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Некорректные значения в матрице")
            return False

        # Проверяем, что элементов достаточно для квадратной матрицы (минимум 2x2)
        if len(elements) < 4:
            QMessageBox.critical(self, "Ошибка", "Минимальный размер матрицы 2x2 (4 элемента)")
            return False

        # Проверяем, что количество элементов образует квадратную матрицу
        n = int(len(elements) ** 0.5)
        if n * n != len(elements):
            QMessageBox.critical(self, "Ошибка", "Количество элементов должно образовывать квадратную матрицу")
            return False

        if any(element < 0 for element in elements):
            QMessageBox.critical(self, "Ошибка", "Элементы матрицы не могут быть отрицательными")
            return False
        try:
            mutation_rate = float(self.mutationLineEdit.text())
            if not 0 <= mutation_rate <= 1:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error", "Mutation rate must be between 0 and 1.")
            return False

        try:
            crossover_rate = float(self.crossoverineEdit.text())
            if not 0 <= crossover_rate <= 1:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error", "Crossover rate must be between 0 and 1.")
            return False

        if self.stepsAmountSpinBox.value() < 1:
            QMessageBox.critical(self, "Error", "Number of steps must be at least 1.")
            return False

        if self.populationSpinBox.value() < 1:
            QMessageBox.critical(self, "Error", "Population size must be at least 1.")
            return False

        if self.earlyStopSpinBox.value() < 1:
            QMessageBox.critical(self, "Error", "Early stop must be at least 1.")
            return False

        return True

    def emit_go_button_clicked(self):
        if not self.verify_input():
            return
            
        settings = {
            'matrix': list(map(float, self.matrixLineEdit.text().split())),
            'population_size': self.populationSpinBox.value(),
            'mutation_rate': float(self.mutationLineEdit.text()),
            'crossover_rate': float(self.crossoverineEdit.text()),
            'steps_amount': self.stepsAmountSpinBox.value(),
            'early_stop': self.earlyStopSpinBox.value(),
            'use_reversal': self.mutation.isChecked(),
            'use_tournament': self.crossing.isChecked()
        }
        
        self.goButtonClicked.emit(settings)
    