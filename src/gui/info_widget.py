from PyQt5.QtWidgets import QDockWidget, QTableWidgetItem, QTableWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from gui.ui.info_widget_ui import Ui_InfoWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor

class InfoWidget(QDockWidget, Ui_InfoWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Теперь этот метод доступен через множественное наследование
        
        # Настройка таблицы
        self.matrixWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.matrixWidget.setSelectionMode(QTableWidget.NoSelection)

        self.horizontalLayout_gen = QtWidgets.QHBoxLayout()
        self.generationLabel = QtWidgets.QLabel("Current generation:")
        self.generationValue = QtWidgets.QLineEdit()
        self.generationValue.setEnabled(False)
        self.horizontalLayout_gen.addWidget(self.generationLabel)
        self.horizontalLayout_gen.addWidget(self.generationValue)
        self.verticalLayout.addLayout(self.horizontalLayout_gen)
        
        self.horizontalLayout_phase = QtWidgets.QHBoxLayout()
        self.phaseLabel = QtWidgets.QLabel("Current phase:")
        self.phaseValue = QtWidgets.QLineEdit()
        self.phaseValue.setEnabled(False)
        self.horizontalLayout_phase.addWidget(self.phaseLabel)
        self.horizontalLayout_phase.addWidget(self.phaseValue)
        self.verticalLayout.addLayout(self.horizontalLayout_phase)
        
        self.verticalLayout_bestChromosome = QtWidgets.QVBoxLayout()
        self.bestChromosomeLabel = QtWidgets.QLabel("Best chromosome:")
        self.bestChromosomeValue = QtWidgets.QTextEdit()
        self.bestChromosomeValue.setEnabled(False)
        self.verticalLayout_bestChromosome.addWidget(self.bestChromosomeLabel)
        self.verticalLayout_bestChromosome.addWidget(self.bestChromosomeValue)
        self.verticalLayout.addLayout(self.verticalLayout_bestChromosome)

        self.mutationTypeLabel = QtWidgets.QLabel("Mutation: Swap")
        self.mutationTypeLabel.setAlignment(Qt.AlignLeft)
        # Добавить в layout
        self.horizontalLayout_mutation = QtWidgets.QHBoxLayout()
        self.horizontalLayout_mutation.addWidget(self.mutationTypeLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_mutation)

        self.selectionTypeLabel = QtWidgets.QLabel("Selection: Roulette")
        self.selectionTypeLabel.setAlignment(Qt.AlignLeft)
        self.horizontalLayout_selection = QtWidgets.QHBoxLayout()
        self.horizontalLayout_selection.addWidget(self.selectionTypeLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_selection)


        # Выравнивание текста
        for widget in [self.bestSolCost, self.averageGenCost, 
                      self.generationValue, self.phaseValue]:
            widget.setAlignment(Qt.AlignRight)
            
        self.bestChromosomeValue.setAlignment(Qt.AlignLeft)
        
        # Настройка размеров
        self.bestChromosomeValue.setMaximumHeight(60)
        self.matrixWidget.setMaximumHeight(200)

    def update_info(self, data):
        """Обновляет все поля информации"""
        self.bestSolCost.setText(f"{data['best_fitness']:.2f}")
        self.averageGenCost.setText(f"{data['avg_fitness']:.2f}")
        self.generationValue.setText(str(data['current_generation']))

        self.bestSolCost.setStyleSheet("color: black;")
        self.averageGenCost.setStyleSheet("color: black;")
        self.generationValue.setStyleSheet("color: black;")
        
        # Перевод фазы на русский
        phase_names = {
            'init': "Инициализация",
            'selection': "Отбор",
            'crossover': "Скрещивание", 
            'mutation': "Мутация"
        }
        self.phaseValue.setText(phase_names.get(data['phase'], data['phase']))
        self.phaseValue.setStyleSheet("color: black;")
        
        # Форматирование лучшей хромосомы
        if data['best_solution']:
            chromo_str = " ".join(map(str, data['best_solution']))
        else:
            chromo_str = " "

        self.bestChromosomeValue.setPlainText(chromo_str)
        self.bestChromosomeValue.setStyleSheet("color: black;")

        cost_matrix = data.get('cost_matrix', [])
        n = len(cost_matrix)
        
        # Настраиваем таблицу матрицы
        self.matrixWidget.setRowCount(n)
        self.matrixWidget.setColumnCount(n)
        
        # Автоматически подбираем размер столбцов
        self.matrixWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.matrixWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        for i in range(n):
            for j in range(n):
                item = QtWidgets.QTableWidgetItem(str(cost_matrix[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.matrixWidget.setItem(i, j, item)
        
        # Устанавливаем заголовки
        self.matrixWidget.setHorizontalHeaderLabels([str(i) for i in range(n)])
        self.matrixWidget.setVerticalHeaderLabels([str(i) for i in range(n)])