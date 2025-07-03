from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from core.genetic_solver import GeneticSolver
from utils.utils import generate_cost_matrix

class GeneticController(QObject):
    update_display = pyqtSignal(dict, name='update_display')
    
    def __init__(self):
        super().__init__()
        self.solver = None
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.generations_history = []  # Новый список для хранения номеров поколений

        
    def initialize_solver(self, cost_matrix=None, n=5, population_size=100, 
                        mutation_rate=0.1, crossover_rate=0.9, 
                        max_generations=1000, early_stop=50, use_reversal_mutation=False, use_tournament=False):
        if cost_matrix is None:
            cost_matrix = generate_cost_matrix(n)
            
        self.solver = GeneticSolver(
            cost_matrix=cost_matrix,
            population_size=population_size,
            mutation_rate=mutation_rate,
            crossover_rate=crossover_rate,
            max_generations=max_generations,
            early_stop=early_stop,
            use_reversal_mutation=use_reversal_mutation,
            use_tournament_selection=use_tournament 


        )
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.generations_history = []  # Сбрасываем историю поколений

    def set_mutation_method(self, use_reversal):
        if self.solver is not None:
            self.solver.set_mutation_method(use_reversal)

    def set_selection_method(self, use_tournament):
            if self.solver is not None:
                self.solver.set_selection_method(use_tournament)

    def step(self):
        if self.solver is None:
            return False
            
        if self.solver.step_clear():
            fitnesses = [self.solver._calculate_fitness(ch) for ch in self.solver.population]
            avg_fitness = sum(fitnesses) / len(fitnesses)
            
            self.best_fitness_history.append(self.solver.best_fitness)
            self.avg_fitness_history.append(avg_fitness)
            self.generations_history.append(self.solver.current_generation)
            
            data = {
                'current_generation': self.solver.current_generation,
                'best_solution': self.solver.best_solution,
                'best_fitness': self.solver.best_fitness,
                'avg_fitness': avg_fitness,
                'population': self.solver.population,
                'phase': self.solver.current_phase,
                'best_history': self.best_fitness_history,
                'avg_history': self.avg_fitness_history,
                'generations_history': self.generations_history,
                'cost_matrix': self.solver.cost_matrix
            }
            
            self.update_display.emit(data)
            return True
        return False
        
    def run_full(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._run_step)
        self.timer.start(10)  # 100ms задержка между шагами
        
    def _run_step(self):
        if not self.step() or not hasattr(self, 'timer') or not self.timer.isActive():
            if hasattr(self, 'timer'):
                self.timer.stop()
                del self.timer
            
    def rollback(self):
        if self.solver is not None and self.solver.rollback():
            if len(self.best_fitness_history) > 0:
                self.best_fitness_history.pop()
                self.avg_fitness_history.pop()
                fitnesses = [self.solver._calculate_fitness(ch) for ch in self.solver.population]
                avg_fitness = sum(fitnesses) / len(fitnesses)
                data = {
                                'current_generation': self.solver.current_generation,
                                'best_solution': self.solver.best_solution,
                                'best_fitness': self.solver.best_fitness,
                                'avg_fitness': avg_fitness,
                                'population': self.solver.population,
                                'phase': self.solver.current_phase,
                                'best_history': self.best_fitness_history,
                                'avg_history': self.avg_fitness_history,
                                'generations_history': self.generations_history,

                                'cost_matrix': self.solver.cost_matrix
                            }
                            
                self.update_display.emit(data)
            return True
        return False