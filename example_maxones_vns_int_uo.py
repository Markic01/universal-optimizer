from copy import deepcopy
from random import randint
from random import choice

from uo.target_problem.target_problem import TargetProblem
from uo.target_solution.target_solution import ObjectiveFitnessFeasibility
from uo.target_solution.target_solution import TargetSolution
from uo.algorithm.metaheuristic.variable_neighborhood_search.problem_solution_vns_support import ProblemSolutionVnsSupport
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import VnsOptimizer

class MaxOnesProblem(TargetProblem):

    def __init__(self, dim:int)->None:
        if dim <= 0:
            raise ValueError("Problem dimension should be positive!")
        if dim > 31:
            raise ValueError("Problem dimension should be less than 32")
        super().__init__("MaxOnesProblem", is_minimization=False, file_path=None, dimension=dim)   

    def __copy__(self):
        pr = deepcopy(self)
        return pr

    def copy(self):
        return self.__copy__()

    def load_from_file(self, data_format:str='txt')->None:
        return

    def string_representation(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        return ''

    def __str__(self)->str:
        return ''
    def __repr__(self)->str:
        return ''

    def __format__(self, spec:str)->str:
        return ''


class MaxOnesProblemBinaryIntSolution(TargetSolution):
    
    def __init__(self)->None:
        super().__init__("MaxOnesProblemBinaryIntSolution", fitness_value=None, objective_value=None, is_feasible=False)
        self.__representation = 42

    def __copy__(self):
        sol = deepcopy(self)
        return sol

    def copy(self):
        return self.__copy__()
        
    def copy_to(self, destination)->None:
        destination = self.__copy__()

    @property
    def representation(self)->int:
            return self.__representation

    @representation.setter
    def representation(self, value:int)->None:
        self.__representation = value

    def random_init(self, problem:TargetProblem)->None:
        limit:int = (1 << problem.dimension)-1
        self.representation = randint(1, limit)
        # make solution feasible 
        mask:int = ~0
        mask <<= 32-problem.dimension
        mask = ~mask 
        self.__representation &= mask

    def solution_code(self)->str:
        return bin(self.__representation)

    def calculate_objective_fitness_feasibility(self, problem:TargetProblem)->ObjectiveFitnessFeasibility:
        ones_count = bin(self.representation).count("1")
        return ObjectiveFitnessFeasibility(ones_count, ones_count, True)

    def solution_code_distance(solution_code_1:str, solution_code_2:str)->float:
        rep_1:int = int(solution_code_1, 2)
        rep_2:int = int(solution_code_2, 2)
        result = (rep_1 ^ rep_2).count(True)
        return result 

    def best_1_change_full(self, problem:TargetProblem)->bool:
        best_ind:int = None
        best_fv:float = self.fitness_value
        for i in range(0, problem.dimension):
            mask:int = 1 << i
            mask = ~mask
            self.representation ^= mask 
            new_fv = self.calculate_objective_fitness_feasibility(problem).fitness_value
            if new_fv > best_fv:
                best_ind = i
                best_fv = new_fv
            self.representation ^= mask 
        if best_ind is not None:
            mask:int = 1 << best_ind
            mask = ~mask
            self.representation ^= mask
            self.evaluate(problem)
            if self.fitness_value != best_fv:
                raise Exception('Fitness calculation within best_1_change_full function is not correct.')
            return True
        return False

    def best_1_change_first(self, problem:TargetProblem)->bool:
        best_ind:int = None
        best_fv:float = self.fitness_value
        for i in range(0, problem.dimension):
            mask:int = 1 << i
            mask = ~mask
            self.representation ^= mask 
            new_fv = self.calculate_objective_fitness_feasibility(problem).fitness_value
            if new_fv > best_fv:
                best_ind = i
                best_fv = new_fv
                mask:int = 1 << best_ind
                mask = ~mask
                self.representation ^= mask
                self.evaluate(problem)
                if self.fitness_value != best_fv:
                    raise Exception('Fitness calculation within best_1_change_first function is not correct.')
                return True
        return False


    def string_representation(self, delimiter:str='\n', indentation:int=0, indentation_symbol:str='   ', 
            group_start:str='{', group_end:str='}',)->str:
        return ''

    def __str__(self)->str:
        return ''

    def __repr__(self)->str:
        return ''

    def __format__(self, spec:str)->str:
        return ''

class MaxOnesProblemBinaryIntSolutionVnsSupport(ProblemSolutionVnsSupport):

    def randomize(self, k:int, problem:TargetProblem, solution:TargetSolution, solution_codes:list[str])->bool:
        tries:int = 0
        limit:int = 10000
        while tries < limit:
            positions:list[int] = []
            for i in range(0,k):
                positions.append(choice(range(k)))
            new_representation:int = solution.representation
            mask:int = 0
            for p in positions:
                mask |= 1 << p
            mask = ~mask
            solution.representation ^= mask
            all_ok:bool = True
            for sc in solution_codes:
                sc_representation = int(sc,2)
                if sc_representation != 0:
                    comp_result:int = (sc_representation ^ new_representation).bit_count()
                    if comp_result > k:
                        all_ok = False
            if all_ok:
                break
        if tries < limit:
            solution.representation = new_representation
            solution.evaluate(problem)
            return True
        else:
            return False 

problem_to_solve:MaxOnesProblem = MaxOnesProblem(dim=10)
initial_solution:MaxOnesProblemBinaryIntSolution = MaxOnesProblemBinaryIntSolution()
initial_solution.random_init(problem_to_solve)
vns_support:MaxOnesProblemBinaryIntSolutionVnsSupport = MaxOnesProblemBinaryIntSolutionVnsSupport()
optimizer:VnsOptimizer = VnsOptimizer(target_problem=problem_to_solve, 
        initial_solution=initial_solution, 
        problem_solution_vns_support=vns_support,
        evaluations_max=0, 
        seconds_max=10, 
        random_seed=None, 
        keep_all_solution_codes=False, 
        k_min=1, 
        k_max=3, 
        max_local_optima=10, 
        local_search_type='local_search_first_improvement')
optimizer.solution_code_distance_cache_cs.is_caching = False
optimizer.output_control.write_to_output_file = False
optimizer.optimize()
print('Best solution: {}'.format(optimizer.best_solution.solution_code()))            
print('Best solution fitness: {}'.format(optimizer.best_solution.fitness_value()))
print('Number of iterations: {}'.format(optimizer.iteration))            
