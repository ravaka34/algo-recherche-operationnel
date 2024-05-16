class SimplexTableau:

    def __init__ (self, vars=[], in_base_vars = [], constraints = [[]], solutions = [], z = []):
        self.vars = vars
        self.in_base_vars = in_base_vars
        self.constraints = constraints
        self.solutions = solutions
        self.z = z

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
                row += "{:^{width}}|".format(self.constraints[i][j], width=total_width)
            row += "{:^{width}}|".format(self.solutions[i], width=total_width)
            print(row)

        # Render the last row with the objective function coefficients
        row = "|{:^{width}}|".format("z", width=total_width)
        for coefficient in self.z:
            row += "{:^{width}}|".format(coefficient, width=total_width)
        row += "{:^{width}}|".format(self.solutions[-1], width=total_width)
        print(row)