from typing import TypedDict
from math import sqrt

from PyQt5.QtWidgets import QDockWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal

from SummerPractice.src.gui.parameters_dock_ui import Ui_ParametersDock

SettingsData = TypedDict('SettingsData', {
    'matrix': list[float],
    'steps_amount': int,
    'population_size': int,
    'mutation_rate': float,
    'crossover_rate': float,
})


class ParametersDock(QDockWidget, Ui_ParametersDock):
    goButtonClicked = pyqtSignal(dict, name='goButtonClicked')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.goButton.clicked.connect(self.emit_go_button_clicked)

    def verify_input(self) -> bool:
        matrix_text = self.matrixLineEdit.text()

        if not matrix_text:
            QMessageBox.critical(self, "Error", "All fields must be filled.")
            return False

        try:
            matrix = list(map(float, matrix_text.split()))
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid data entered for matrix.")
            return False

        if len(matrix) > 36 or len(matrix) < 4 or not sqrt(len(matrix)).is_integer():
            QMessageBox.critical(self, "Error", "Inappropriate matrix elements number.")
            return False

        if any(element < 0 for element in matrix):
            QMessageBox.critical(self, "Error", "Matrix elements cannot be negative.")
            return False

        if self.stepsAmountSpinBox.value() < 2:
            QMessageBox.critical(self, "Error", "Amount of steps must be greater than 1.")
            return False

        if self.populationSpinBox.value() < 5:
            QMessageBox.critical(self, "Error", "Amount of steps must be greater than 4.")
            return False

        if self.mutationSpinBox.value() < 0 or self.mutationLineEdit.value() > 1:
            QMessageBox.critical(self, "Error", "Mutation rate must not be greater than 1 or less than 0.")
            return False

        if self.crossoverSpinBox.value() < 0 or self.crossoverineEdit.value() > 1:
            QMessageBox.critical(self, "Error", "Crossover rate must not be greater than 1 or less than 0.")
            return False

        return True

    def emit_go_button_clicked(self):
        if not self.verify_input():
            return
        self.goButtonClicked.emit(self.get_settings())      # если данные валидны, вызывается метод для получения настроек

    def get_settings(self) -> SettingsData:
        return {
            'matrix': list(map(float, self.functionLineEdit.text().split())),
            'steps_amount': int,
            'population_size': int,
            'mutation_rate': float,
            'crossover_rate': float,
        }