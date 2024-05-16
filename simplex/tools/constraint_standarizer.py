class ConstraintStandarizer:

    def __init__(self, constraints):
        self.constraints = constraints
        self.new_vars = []
        self.nbr_ecart_var = 0
        self.nbr_artificial_var = 0
        self.standarized = self.standarize_constraints()

    def standarize_constraint(self, constraint):
        split_constraint = constraint.split(" ")
        for i in range(len(split_constraint)):
            if split_constraint[i] == "<=":
                self.nbr_ecart_var += 1
                split_constraint.insert(i, "+1.e" + str(self.nbr_ecart_var))
                self.new_vars.append("e" + str(self.nbr_ecart_var))
                break
        return split_constraint

    def standarize_constraints(self):
        standardized_constraints = []
        for constraint in self.constraints:
            standardized_constraints.append(self.standarize_constraint(constraint))
        return standardized_constraints