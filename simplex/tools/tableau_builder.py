from .problem_parser import ProblemParser
from .constraint_standarizer import ConstraintStandarizer
from .simplex_tableau import SimplexTableau

class TableauBuilder:

    def __init__(self, filename):
        self.parser = ProblemParser(filename)
        self.standarizer = ConstraintStandarizer(self.parser.constraints)
        self.vars = self.parser.decision_vars + self.standarizer.new_vars
        self.problem_type = self.parser.problem_type

    def build(self):
        return SimplexTableau(
            self.vars,
            self.build_base_var(),
            self.build_constraints_array(),
            self.build_solution_array(),
            self.build_objective_array(),
        )

    def build_objective_array(self):
        objective_array = [
            float(item.split(".")[0]) for item in self.parser.objective.split()[1:]
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

        # Skip the signe and the last number
        for item in constraint[0:-2]:
            couples.append(item.split("."))

        # Seach for the coeff of the var in the constraint
        for var in self.vars:
            find_in = False
            for couple in couples:
                if couple[1] == var:
                    vector_constraint.append(float(couple[0]))
                    find_in = True
                    break
            if not find_in:
                vector_constraint.append(0)
        return vector_constraint

    def build_solution_array(self):
        solution_array = []
        for constraint in self.standarizer.standarized:
            solution_array.append(float(constraint[-1]))
        solution_array.append(0)
        return solution_array

    def build_base_var(self):
        base = []
        for constraint in self.standarizer.standarized:
            base.append(constraint[-3].split(".")[1])
        return base