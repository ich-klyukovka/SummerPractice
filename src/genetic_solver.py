import random 
import copy

class GeneticSolver:
    def __init__(self, cost_matrix, population_size=100, mutation_rate=0.1, 
                 crossover_rate=0.9, max_generations=1000, early_stop=50):
        """        
            cost_matrix: матрица затрат NxN (list of lists)
            population_size: размер популяции (int)
            mutation_rate: вероятность мутации (float, 0-1)
            crossover_rate: вероятность скрещивания (float, 0-1)
            max_generations: максимальное число поколений (int)
            early_stop: останов после N поколений без улучшений (int)
        """
        self.cost_matrix = cost_matrix  
        self.n = len(cost_matrix)  
        self.population_size = population_size  
        self.mutation_rate = mutation_rate  
        self.crossover_rate = crossover_rate 
        self.max_generations = max_generations 
        self.early_stop = early_stop  
        self.no_improvement_count = 0 
        
        # Текущая фаза алгоритма: 'init', 'selection', 'crossover', 'mutation'
        self.current_phase = 'init'
        
        # История для отката
        self.history = [] 
        self.current_generation = 0  
        self.best_solution = None  
        self.best_fitness = float('inf')
        
        self.population = [] 
        self.selected = []  
        self.children = []  

    def _initialize_population(self):
        self.population = [  # Инициализация начальной популяции
            random.sample(range(self.n), self.n)
            for _ in range(self.population_size)  
        ]

    def _calculate_fitness(self, chromosome):
        return sum(self.cost_matrix[i][job] for i, job in enumerate(chromosome))  # Расчет стоимости решения

    def _update_best_solution(self):
        for chromosome in self.population:  # Перебираем все особи в популяции
            fitness = self._calculate_fitness(chromosome)  
            if fitness < self.best_fitness:  # Если найдено лучшее решение, то замена
                self.best_fitness = fitness 
                self.best_solution = copy.deepcopy(chromosome)  # Сохраняем лучшее решение
                self.no_improvement_count = 0 
            else:
                self.no_improvement_count += 1 

    def _do_selection(self):
        fitnesses = [1 / (self._calculate_fitness(ch) + 1) for ch in self.population]  # Инвертированные значения приспособленности
        total_fitness = sum(fitnesses)  # Сумма всех значений приспособленности
        probabilities = [f / total_fitness for f in fitnesses]  # Вероятности выбора каждой особи
        
        self.selected = random.choices(  # Выбор особей с учетом их вероятностей
            self.population, 
            weights=probabilities, 
            k=self.population_size  # Выбираем столько же особей, сколько в популяции
        )

    def _ordered_crossover(self, parent1, parent2): # скрещивание
        size = self.n  
        child1, child2 = [-1] * size, [-1] * size 
        
        start, end = sorted(random.sample(range(size), 2))  
        child1[start:end+1] = parent1[start:end+1]  
        child2[start:end+1] = parent2[start:end+1]  
        
        self._fill_child(child1, parent2, end, start)  # Заполнение оставшихся позиций
        self._fill_child(child2, parent1, end, start)
        
        return child1, child2 

    def _fill_child(self, child, parent, end, start):
        size = self.n 
        current_pos = (end + 1) % size 
        parent_pos = current_pos 
        
        while -1 in child: 
            if parent[parent_pos] not in child: 
                child[current_pos] = parent[parent_pos]  
                current_pos = (current_pos + 1) % size  
            parent_pos = (parent_pos + 1) % size  

    def _apply_mutation(self, chromosome):
        if random.random() < self.mutation_rate:  
            idx1, idx2 = random.sample(range(self.n), 2)  
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]  
        
        if random.random() < self.mutation_rate: 
            start, end = sorted(random.sample(range(self.n), 2)) 
            chromosome[start:end+1] = chromosome[start:end+1][::-1]  
        
        return chromosome 

    def _do_crossover(self):
        self.children = []
        parents = self.selected.copy()  # Создаем копию списка выбранных родителей
        random.shuffle(parents)  # Перемешиваем родителей случайным образом
        
        for i in range(0, len(parents), 2):  # Перебираем родителей парами
            if i+1 >= len(parents):  # Если не хватает пары
                self.children.append(parents[i])  # Добавляем одиночную особь
                break
            
            parent1, parent2 = parents[i], parents[i+1] 
            
            if random.random() < self.crossover_rate:  
                child1, child2 = self._ordered_crossover(parent1, parent2)  
            else:
                child1, child2 = parent1.copy(), parent2.copy() 
            
            self.children.extend([child1, child2])  # Добавляем потомков в список

    def _do_mutation(self):
        self.population = [self._apply_mutation(ch) for ch in self.children]  # Применяем мутации
        self._update_best_solution()  
        self.current_generation += 1  

    def _save_state(self):
        state = { 
            'population': copy.deepcopy(self.population),
            'selected': copy.deepcopy(self.selected),
            'children': copy.deepcopy(self.children),
            'best_solution': copy.deepcopy(self.best_solution),
            'best_fitness': self.best_fitness,
            'current_generation': self.current_generation,
            'current_phase': self.current_phase,
            'no_improvement_count': self.no_improvement_count
        }
        self.history.append(state)  # Добавляем состояние в историю

    def rollback(self):
        if not self.history:
            return False 
        
        state = self.history.pop() 
        self.population = state['population'] 
        self.selected = state['selected']  
        self.children = state['children']  
        self.best_solution = state['best_solution']
        self.best_fitness = state['best_fitness']  
        self.current_generation = state['current_generation']
        self.current_phase = state['current_phase']  
        self.no_improvement_count = state['no_improvement_count']
        
        return True  

    def step(self):
        if self.current_generation >= self.max_generations:  
            print("Достигнуто максимальное число поколений")
            return False
        
        self._save_state()  # Сохраняем текущее состояние
        
        if self.current_phase == 'init':  # Фаза инициализации
            print("\n=== ФАЗА ИНИЦИАЛИЗАЦИИ ===")
            self._initialize_population()  
            print(f"Инициализирована популяция из {self.population_size} особей")
            for i in range(len(self.population)):
                print(f"Особь {i}: {self.population[i]} (Стоимость: {self._calculate_fitness(self.population[i])})")
            self.current_phase = 'selection'
        
        elif self.current_phase == 'selection':  # Фаза отбора
            print("\n=== ФАЗА ОТБОРА ===")
            print(f"Поколение {self.current_generation}")
            self._do_selection() 
            print("Лучшие особи после отбора:")
            selected_fitness = [(ch, self._calculate_fitness(ch)) for ch in self.selected]
            selected_fitness.sort(key=lambda x: x[1])
            for i in range(len(selected_fitness)):
                print(f"Особь {i}: {selected_fitness[i][0]} (Стоимость: {selected_fitness[i][1]})")
            self.current_phase = 'crossover'  
        
        elif self.current_phase == 'crossover':  # Фаза скрещивания
            print("\n=== ФАЗА СКРЕЩИВАНИЯ ===")
            self._do_crossover()  
            print(f"Создано {len(self.children)} потомков")
            print("Примеры потомков:")
            for i in range(len(self.children)):
                print(f"Потомок {i}: {self.children[i]} (Стоимость: {self._calculate_fitness(self.children[i])})")
            self.current_phase = 'mutation'  
        
        elif self.current_phase == 'mutation':  # Фаза мутации
            print("\n=== ФАЗА МУТАЦИИ ===")
            prev_population = copy.deepcopy(self.population) 
            self._do_mutation() 
            
            print("Изменения после мутаций:")
            for i in range(len(self.population)):
                if self.population[i] != prev_population[i]:
                    print(f"Особь {i}: {prev_population[i]} -> {self.population[i]}")
                else:
                    print(f"Особь {i} не изменилась")
            
            print("\nЛучшее решение текущего поколения:")
            print(f"Особь: {self.best_solution} (Стоимость: {self.best_fitness})")
            
            if self.current_generation >= self.max_generations:  # Проверка на завершение
                print("Достигнуто максимальное число поколений")
                return False
            
            if self.no_improvement_count >= self.early_stop:
                print(f"Ранняя остановка: нет улучшений {self.early_stop} поколений")
                return False
            
            self.current_phase = 'selection'
        
        return True 
    
    def step_clear(self):
        if self.current_generation >= self.max_generations:  
            return False
        
        self._save_state()  
        
        if self.current_phase == 'init':  # Фаза инициализации 
            self._initialize_population()
            self.current_phase = 'selection'
        
        elif self.current_phase == 'selection':  # Фаза отбора 
            self._do_selection()
            self.current_phase = 'crossover'
        
        elif self.current_phase == 'crossover':  # Фаза скрещивания 
            self._do_crossover()
            self.current_phase = 'mutation'
        
        elif self.current_phase == 'mutation':  # Фаза мутации 
            self._do_mutation()
            
            if self.current_generation >= self.max_generations:  # Проверка на завершение
                return False
            
            if self.no_improvement_count >= self.early_stop: 
                return False
            
            self.current_phase = 'selection'  
        
        return True  

    def run(self):
        while self.step_clear(): 
            pass

    def print_state(self):
        print("\n____ТЕКУЩЕЕ СОСТОЯНИЕ АЛГОРИТМА____")
        print(f"Поколение: {self.current_generation}")
        print(f"Фаза: {self.current_phase}")
        print(f"Лучшая стоимость: {self.best_fitness}")
        print(f"Лучшее решение: {self.best_solution}")
        
        