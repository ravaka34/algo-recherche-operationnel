from fractions import Fraction
from tools import is_entier

class SimplexTableau:

    def __init__ (self, vars=[], in_base_vars = [], constraints = [[]], solutions = [], z = [], str_problem = "", fract_result = False):
        self.fract_result = fract_result
        self.vars = vars
        self.in_base_vars = in_base_vars
        self.constraints = constraints
        self.solutions = solutions
        self.z = z
        self.str_problem = str_problem

    def removed_artificial_version(self, row):
        new_row = []
        for i in range(len(row)):
            if self.vars[i][0] != 'a':
                new_row.append(row[i])
        return new_row
       
    def remove_artificial_cols(self):
        for i in range(len(self.constraints)):
            self.constraints[i] = self.removed_artificial_version(self.constraints[i])
        self.z = self.removed_artificial_version(self.z)
        self.vars = self.removed_artificial_version(self.vars)

    def has_artificial_var(self):
        for var in self.vars:
            if var[0] == 'a':
                return True
        return False

    def render_float(self, nbr):
        entier =  is_entier(nbr)
        # Entier
        if entier :
           return str(int(nbr))
        elif entier == False and self.fract_result:
            fraction = Fraction(nbr).limit_denominator()
            return f"{fraction.numerator}/{fraction.denominator}"
        else:
            return str(nbr)

    def render(self):
        # Determine the number of variables
        num_vars = len(self.vars)

        # Calculate the total width of the tableau
        total_width = max(len(var) for var in self.vars) + 2

        # Render the first row with variable names
        header = "|{:^{width}}|".format("", width=total_width)
        for var in self.vars:
            header += "{:^{width}}|".format(var, width=total_width)
        header += "{:^{width}}|".format("", width=total_width)
        print(header)

        # Render the remaining rows with constraints and solutions
        for i in range(len(self.constraints)):
            row = "|{:^{width}}|".format(self.in_base_vars[i], width=total_width)
            for j in range(num_vars):
                # row += "{:^{width}}|".format(self.constraints[i][j], width=total_width)
                row += "{:^{width}}|".format(self.render_float(self.constraints[i][j]), width=total_width)
            row += "{:^{width}}|".format(self.render_float(self.solutions[i]), width=total_width)
            print(row)

        # Render the last row with the objective function coefficients
        row = "|{:^{width}}|".format("z", width=total_width)
        for coefficient in self.z:
            row += "{:^{width}}|".format(self.render_float(coefficient), width=total_width)
        row += "{:^{width}}|".format(self.render_float(self.solutions[-1]), width=total_width)
        print(row)
        print("\n")