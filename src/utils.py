import json
import random
from colorama import Fore, Style

def generate_cost_matrix(n, min_cost=1, max_cost=100):
        return [
            [random.randint(min_cost, max_cost) for _ in range(n)]
            for _ in range(n)
        ]

def print_cost_matrix(matrix):
    print("\nМатрица затрат (кандидат → работа):")
    print("     " + " ".join(f"{j:5}" for j in range(len(matrix))))
    print("    " + "-" * (6 * len(matrix)))
    for i, row in enumerate(matrix):
        print(f"{Fore.GREEN}{i:2} |{Style.RESET_ALL} " + " ".join(f"{cost:5}" for cost in row))

def save_solver_state(solver, filename):
    state = {
        'cost_matrix': solver.cost_matrix,
        'params': {
            'population_size': solver.population_size,
            'mutation_rate': solver.mutation_rate,
            'crossover_rate': solver.crossover_rate,
            'max_generations': solver.max_generations,
            'early_stop': solver.early_stop
        },
        'state': {
            'population': solver.population,
            'selected': solver.selected,
            'children': solver.children,
            'best_solution': solver.best_solution,
            'best_fitness': solver.best_fitness,
            'current_generation': solver.current_generation,
            'current_phase': solver.current_phase,
            'no_improvement_count': solver.no_improvement_count,
            'history_size': len(solver.history)
        }
    }
    with open(filename, 'w') as f:
        json.dump(state, f)

def load_solver_state(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def print_solution(solution, cost_matrix):
    total_cost = 0
    print("Назначения:")
    for candidate, job in enumerate(solution):
        cost = cost_matrix[candidate][job]
        total_cost += cost
        print(f"Кандидат {candidate} -> Работа {job} (Стоимость: {cost})")
    print(f"Общая стоимость: {total_cost}")

def print_population_stats(population, cost_matrix):
    fitnesses = [sum(cost_matrix[i][job] for i, job in enumerate(ch)) for ch in population]
    print(f"Лучшая стоимость: {min(fitnesses)}")
    print(f"Худшая стоимость: {max(fitnesses)}")
    print(f"Средняя стоимость: {sum(fitnesses)/len(fitnesses):.2f}")