from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import Qt, QtWidgets, QtCore

from gui.ui.main_window_ui import Ui_MainWindow
from gui.parameters_dock import ParametersDock
from gui.mpl_canvas import MplCanvas
from gui.info_widget import InfoWidget
from core.controller import GeneticController
from utils.utils import generate_cost_matrix
from matplotlib.ticker import MaxNLocator  # Добавляем 

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialize controller
        self.controller = GeneticController()
        self.controller.update_display.connect(self.update_display)

        # Setup UI components
        self.parametersDock = ParametersDock()
        self.infoWidget = InfoWidget()
        self.addDockWidget(Qt.Qt.LeftDockWidgetArea, self.parametersDock)
        self.addDockWidget(Qt.Qt.RightDockWidgetArea, self.infoWidget)

        self.canvas = MplCanvas(self.canvas)

        # Connect signals
        self.nextButton.clicked.connect(self.next_step)
        self.backButton.clicked.connect(self.prev_step)
        self.ffButton.clicked.connect(self.run_full)
        self.parametersDock.goButtonClicked.connect(self.start_algorithm)

        self.isPlaying = False
        self.parametersDock.mutation.stateChanged.connect(self.update_mutation_method)
        self.parametersDock.crossing.stateChanged.connect(self.update_selection_method)


        self.stopButton.clicked.connect(self.stop_algorithm)
        self.is_running = False  # Добавить флаг для отслеживания состояния

        self.actionImport_from_file.triggered.connect(self.import_matrix_from_file)
        self.actionFeelin_lucky.triggered.connect(self.generate_random_matrix)

    def import_matrix_from_file(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Import Matrix", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read().strip()
                    elements = list(map(float, content.split()))
                    
                    # Проверка на квадратную матрицу
                    n = int(len(elements) ** 0.5)
                    if n * n != len(elements):
                        QtWidgets.QMessageBox.warning(self, "Error", 
                            "Matrix must be square (N x N elements)")
                        return
                    
                    # Устанавливаем значения в интерфейс
                    self.parametersDock.matrixLineEdit.setText(content)
                    self.parametersDock.populationSpinBox.setValue(50)
                    self.parametersDock.stepsAmountSpinBox.setValue(100)
                    
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", 
                    f"Failed to import matrix: {str(e)}")

    def generate_random_matrix(self):
        # Диалог для ввода размера матрицы
        size, ok = QtWidgets.QInputDialog.getInt(
            self, 'Generate Matrix', 
            'Enter matrix size (N x N):', 5, 2, 20)
        
        if ok:
            try:
                # Генерируем матрицу
                cost_matrix = generate_cost_matrix(size)
                # Преобразуем в строку для отображения
                elements = ' '.join(str(item) for row in cost_matrix for item in row)
                
                # Устанавливаем значения в интерфейс
                self.parametersDock.matrixLineEdit.setText(elements)
                self.parametersDock.populationSpinBox.setValue(50)
                self.parametersDock.stepsAmountSpinBox.setValue(100)
                
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", 
                    f"Failed to generate matrix: {str(e)}")

    def stop_algorithm(self):
        if hasattr(self.controller, 'timer') and self.controller.timer.isActive():
            self.controller.timer.stop()
            del self.controller.timer
        self.is_running = False

    def run_full(self):
        self.is_running = True
        self.controller.run_full()

    def update_mutation_method(self, state):
        use_reversal = bool(state)
        if hasattr(self, 'controller'):
            self.controller.set_mutation_method(use_reversal)
        
        # Обновляем текст в интерфейсе
        mutation_text = "Mutation: Reversal" if use_reversal else "Mutation: Swap"
        self.infoWidget.mutationTypeLabel.setText(mutation_text)
        #print(f"Мутация изменена на: {'переворот' if use_reversal else 'точечная'}")

    def update_selection_method(self, state):
        use_tournament = bool(state)
        if hasattr(self, 'controller'):
            self.controller.set_selection_method(use_tournament)
        
        # Обновляем текст в интерфейсе
        selection_text = "Selection: Tournament" if use_tournament else "Selection: Roulette"
        self.infoWidget.selectionTypeLabel.setText(selection_text)
        #print(f"Метод отбора изменён на: {'турнирный' if use_tournament else 'рулетка'}")

    def start_algorithm(self, settings):
        try:
            elements = settings['matrix']
            n = int(len(elements) ** 0.5)
            cost_matrix = [elements[i*n:(i+1)*n] for i in range(n)]
            
            self.controller.initialize_solver(
                cost_matrix=cost_matrix,
                population_size=settings['population_size'],
                mutation_rate=settings['mutation_rate'],
                crossover_rate=settings['crossover_rate'],
                max_generations=settings['steps_amount'],
                early_stop=settings['early_stop'],
                use_reversal_mutation=settings['use_reversal'],
                use_tournament=settings['use_tournament']
            )
            
            mutation_text = "Mutation: Reversal" if settings['use_reversal'] else "Mutation: Swap"
            self.infoWidget.mutationTypeLabel.setText(mutation_text)
            
            selection_text = "Selection: Tournament" if settings['use_tournament'] else "Selection: Roulette"
            self.infoWidget.selectionTypeLabel.setText(selection_text)
            
            self.next_step()
        except Exception as e:
            print(f"Error starting algorithm: {e}")

    def next_step(self):
        if self.controller.step():
            pass

    def prev_step(self):
        self.controller.rollback()

    def run_full(self):
        self.controller.run_full()

    def update_display(self, data):
        # Update best solution info
        self.infoWidget.bestSolCost.setText(str(data['best_fitness']))
        self.infoWidget.averageGenCost.setText(f"{data['avg_fitness']:.2f}")
        
    # Обновляем информационную панель
        self.infoWidget.update_info(data)
        # Update matrix display
        n = len(data['cost_matrix'])
        self.infoWidget.matrixWidget.setRowCount(n)
        self.infoWidget.matrixWidget.setColumnCount(n)
        
        for i in range(n):
            for j in range(n):
                item = QTableWidgetItem(str((data['cost_matrix'][i][j])))
                self.infoWidget.matrixWidget.setItem(i, j, item)
                # Проверяем, является ли текущая ячейка частью лучшего решения
                if data['best_solution'] and j == data['best_solution'][i]:
                    item.setBackground(QtCore.Qt.green)
        
        # Update plot
        self.canvas.clear()
        if len(data['best_history']) > 1:
            ax = self.canvas.axes
        
        # Устанавливаем целочисленные деления
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            x = range(len(data['best_history']))
            self.canvas.plot_points(x, data['best_history'], 'r-')
            self.canvas.plot_points(x, data['avg_history'], 'b--')
            self.canvas.axes.legend(['Best fitness', 'Average fitness'])
            self.canvas.axes.set_xlabel('Steps')
            self.canvas.axes.set_ylabel('Fitness')
            self.canvas.draw()