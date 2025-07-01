from genetic_solver import GeneticSolver
# from data_manager import DataManager
from utils import print_solution, save_solver_state, load_solver_state, generate_cost_matrix, print_cost_matrix
n = 5
cost_matrix = generate_cost_matrix(n)
print_cost_matrix(cost_matrix)
solver = GeneticSolver(
    cost_matrix=cost_matrix,
    population_size=3,
    mutation_rate=0.2,
    crossover_rate=0.9,
    max_generations=100,
    early_stop=10
)
b = 5
print(f"Выполнение {b} шагов:")
for _ in range(b):
    solver.step()

save_solver_state(solver, 'solver_state.json')

a = 2
print(f"\nОткат на {a} шага:")
for _ in range(a):
    solver.rollback()
solver.print_state()

print("\nЗагрузка сохраненного состояния:")
loaded_state = load_solver_state('solver_state.json')
solver = GeneticSolver(
    cost_matrix=loaded_state['cost_matrix'],
    **loaded_state['params']
)
solver.__dict__.update(loaded_state['state'])
solver.print_state()


print("\nПродолжение работы:")
solver.run()
print_solution(solver.best_solution, cost_matrix)
print_cost_matrix(cost_matrix)