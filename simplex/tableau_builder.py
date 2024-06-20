from problem_parser import ProblemParser
from constraint_standarizer import ConstraintStandarizer
from simplex_tableau import SimplexTableau
from fractions import Fraction

class TableauBuilder:

    def __init__(self, filename=None, str_problem=None):
        self.parser = ProblemParser(filename=filename, str_problem=str_problem)
        self.standarizer = ConstraintStandarizer(self.parser.constraints)
        self.vars = sorted(self.parser.decision_vars + self.standarizer.new_vars, key=self.custom_sort_vars_key)
        self.problem_type = self.parser.problem_type
    
    def custom_sort_vars_key(self, item):
        # Define the desired order of elements
        order = {'x': 0, 'e': 1, 'a': 2}

        # Extract the prefix (e.g., 'x', 'e', 'a')
        prefix = item[0]

        # Return the index based on the desired order
        return order.get(prefix, float('inf')), item
    
    def transform_nbr_str_to_float(self, nbr_str):
        #So that we can handle fraction number
        # fraction = Fraction(nbr_str)
        return float(nbr_str)

    def build(self):
        return SimplexTableau(
            self.vars,
            self.build_base_var(),
            self.build_constraints_array(),
            self.build_solution_array(),
            self.build_objective_array(),
            self.parser.str_problem
        )

    def build_objective_array(self):
        objective_array = [
            self.transform_nbr_str_to_float(item.split(".")[0]) for item in self.parser.objective.split()[1:]
        ]
        return objective_array + [0] * len(self.standarizer.new_vars)

    def build_constraints_array(self):
        constraints_array = []
        for constraint in self.standarizer.standarized:
            constraints_array.append(self.build_vector_constraint(constraint))
        return constraints_array

    def build_vector_constraint(self, constraint):
        couples = []
        vector_constraint = []

        # Skip the sign and the last number
        for item in constraint[0:-2]:
            couples.append(item.split("."))

        # Seach for the coeff of the var in the constraint
        for var in self.vars:
            find_in = False
            for couple in couples:
                if couple[1] == var:
                    vector_constraint.append(self.transform_nbr_str_to_float(couple[0]))
                    find_in = True
                    break
            if not find_in:
                vector_constraint.append(0)
        return vector_constraint

    def build_solution_array(self):
        solution_array = []
        for constraint in self.standarizer.standarized:
            solution_array.append(self.transform_nbr_str_to_float(constraint[-1]))
        solution_array.append(0)
        return solution_array

    def build_base_var(self):
        base = []
        for constraint in self.standarizer.standarized:
            base.append(constraint[-3].split(".")[1])
        return base