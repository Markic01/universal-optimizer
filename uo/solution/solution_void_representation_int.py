import math

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)

from copy import deepcopy
from random import randrange
from random import choice

from typing import NamedTuple
from typing import Optional

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution
from uo.solution.evaluation_cache_control_statistics import EvaluationCacheControlStatistics
from uo.solution.distance_calculation_cache_control_statistics import DistanceCalculationCacheControlStatistics

class SolutionVoidInt(Solution[int, str]):
    
    def __init__(self, random_seed:int=None, 
            fitness_value:float=-math.inf, 
            objective_value:float=-math.inf, 
            is_feasible:bool=False, 
            evaluation_cache_is_used:bool=False, 
            evaluation_cache_max_size:int=0,
            distance_calculation_cache_is_used:bool=False,
            distance_calculation_cache_max_size:int=0)->None:
        super().__init__(random_seed=random_seed, 
                fitness_value=fitness_value, fitness_values=[], 
                objective_value=objective_value, objective_values=[],
                is_feasible=is_feasible, 
                evaluation_cache_is_used=evaluation_cache_is_used,
                evaluation_cache_max_size=evaluation_cache_max_size,
                distance_calculation_cache_is_used=distance_calculation_cache_is_used,
                distance_calculation_cache_max_size=distance_calculation_cache_max_size)

    def __copy__(self):
        pr = deepcopy(self)
        return pr

    def copy(self):
        return self.__copy__()

    def argument(self, representation:int)->str:
        return "42"

    def init_random(self, problem:Problem)->None:
        self.representation = 42


    def init_from(self, representation:int, problem:Problem)->None:
        if not isinstance(representation, int):
            raise TypeError('Parameter \'representation\' must have type \'int\'.')
        self.representation = representation

    def native_representation(self, representation_str:str)->int:
        return 42

    def calculate_quality_directly(self, representation:int, 
            problem:Problem)->QualityOfSolution:
        return QualityOfSolution(42, None, 42, None, True)

    def representation_distance_directly(self, solution_code_1:str, solution_code_2:str)->float:
        return 42.0

    def __str__(self)->str:
        return super().__str__()

    def __repr__(self)->str:
        return super().__repr__()

    def __format__(self, spec:str)->str:
        return super().__format__(spec)    
