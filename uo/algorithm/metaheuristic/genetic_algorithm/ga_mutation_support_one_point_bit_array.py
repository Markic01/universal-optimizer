"""
..  _py_ones_count_max_problem_bit_array_solution_ga_support:

The :mod:`~opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem_bit_array_solution_ga_support`
contains class :class:`~opt.single_objective.comb.ones_count_max_problem.ones_count_max_problem_bit_array_solution_ga_support.OnesCountMaxProblemBitArraySolutionGaSupport`, 
that represents supporting parts of the `GA` algorithm, where solution of the :ref:`Problem_MinimumMultiCut` have `BitArray` 
representation.
"""
import sys
from pathlib import Path
directory = Path(__file__).resolve()
sys.path.append(directory)
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent.parent)

from abc import ABCMeta, abstractmethod
from typing import NamedTuple
from typing import TypeVar
from typing import Generic
from typing import Optional
from copy import deepcopy
from random import choice, random, randint

from bitstring import BitArray

from uo.problem.problem import Problem
from uo.solution.solution import Solution
from uo.algorithm.metaheuristic.population_based_metaheuristic import PopulationBasedMetaheuristic
from uo.algorithm.metaheuristic.genetic_algorithm.ga_mutation_support import GaMutationSupport

A_co = TypeVar("A_co", covariant=True)

class GaMutationSupportOnePointBitArray(GaMutationSupport[BitArray,A_co]):

    def __init__(self, mutation_probability:float)->None:
        """
        Create new `GaMutationSupport` instance
        """
        self.__mutation_probability:float = mutation_probability

    @property
    def mutation_probability(self)->float:
        """
        Property getter for mutation probability 

        :return: mutation probability 
        :rtype: float
        """
        return self.__mutation_probability    

    def __copy__(self):
        """
        Internal copy of the `GaMutationSupportOnePointBitArray`

        :return: new `GaMutationSupportOnePointBitArray` instance with the same properties
        :rtype: `GaMutationSupportOnePointBitArray`
        """
        sol = deepcopy(self)
        return sol

    def copy(self):
        """
        Copy the `GaMutationSupportOnePointBitArray` instance

        :return: new `GaMutationSupportOnePointBitArray` instance with the same properties
        :rtype: `GaMutationSupportOnePointBitArray`
        """
        return self.__copy__()

    def mutation(self, problem:Problem, solution:Solution, 
                optimizer:PopulationBasedMetaheuristic)->None:
        """
        Executes mutation within GA 
        
        :param `Problem` problem: problem that is solved
        :param `Solution` solution: item that is mutated 
        :param `Solution` mutant: outcome of the mutation 
        :param `PopulationBasedMetaheuristic` optimizer: optimizer that is executed
        :rtype: None
        """
        if solution.representation is None:
            return
        for i in range(len(solution.representation)):
            if random() < self.mutation_probability:
                solution.representation.invert(i)
        optimizer.write_output_values_if_needed("before_evaluation", "b_e")
        optimizer.evaluation += 1
        solution.evaluate(problem)
        optimizer.write_output_values_if_needed("after_evaluation", "b_e")

    def string_rep(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        """
        String representation of the ga support structure

        :param delimiter: delimiter between fields
        :type delimiter: str
        :param indentation: level of indentation
        :type indentation: int, optional, default value 0
        :param indentation_symbol: indentation symbol
        :type indentation_symbol: str, optional, default value ''
        :param group_start: group start string 
        :type group_start: str, optional, default value '{'
        :param group_end: group end string 
        :type group_end: str, optional, default value '}'
        :return: string representation of ga support instance
        :rtype: str
        """
        return 'GaMutationSupportOnePointBitArray'

    def __str__(self)->str:
        """
        String representation of the ga support instance

        :return: string representation of the ga support instance
        :rtype: str
        """
        return self.string_rep('|')

    def __repr__(self)->str:
        """
        Representation of the ga support instance

        :return: string representation of the ga support instance
        :rtype: str
        """
        return self.string_rep('\n')

    def __format__(self, spec:str)->str:
        """
        Formatted the ga support instance

        :param str spec: format specification
        :return: formatted ga support instance
        :rtype: str
        """
        return self.string_rep('|')


