from simplex_resolver import SimplexResolver
from tableau_builder import TableauBuilder

class Simplex2Phases(SimplexResolver):

    def express_var_from_constraint(self, var_name, constraint):
        expression = []
        for i in range(0, len(constraint)):
            if self.tableau.vars[i] != var_name:
                expression.append(-1*constraint[i])
            else:
                expression.append(0)
        return expression

    def get_matrix_expression(self, var_name):
        nbr_vars = len(self.tableau.vars)
        i = 0
        for constraint in self.constraints:
            for j in range(0, nbr_vars):
                if self.tableau.vars[j] == var_name and constraint[j] != 0:
                    expression = self.express_var_from_constraint(var_name, constraint)
                    expression.append(self.tableau.solutions[i])
                    return expression
            i += 1

    def sum_artificial_var(self):
        expressions = []
        for var_name in self.tableau.vars:
            if var_name[0] == 'a':
                expressions.append(self.get_matrix_expression(var_name))
        #do a matrix sum between the expressions
        return [sum(x) for x in zip(*expressions)]
    
    def phaseone(self):
        real_problem_type = self.problem_type
        self.problem_type = -1 #Min
        #adding the the old problem into the simplex tableau
        self.tableau.add_row('O', self.tableau.z, self.tableau.solutions[-1])
        #adding the new problem to solve
        artificial_var_sum = self.sum_artificial_var()
        self.tableau.z = artificial_var_sum[:-1]
        self.tableau.solutions[-1] = -artificial_var_sum[-1]
        super().solve()
        self.problem_type = real_problem_type

    def phasetwo(self):
        #Remove the last row and the artificial columns
        self.tableau.z = self.constraints[-1]
        self.tableau.solutions.pop()
        self.tableau.constraints.pop()
        self.tableau.in_base_vars.pop()
        #Remove the artificial cols
        self.tableau.remove_artificial_cols()
        super().solve()

    def solve(self):
        self.phaseone()
        self.tableau.render()
        self.phasetwo()
        self.tableau.render()
        
tableau_builder = TableauBuilder('problem.txt')
print(Simplex2Phases(tableau_builder.build(), tableau_builder.problem_type).solve())