from simplex_resolver import SimplexResolver
from tableau_builder import TableauBuilder

class Simplex2Phases(SimplexResolver):
    
    def phaseone(self):
        self.problem_type = -1 #Min
        for i in range(len(self.tableau.vars)):
            if 'a' in self.tableau.vars[i]:
                self.tableau.z[i] = -1
            else:
                self.tableau.z[i] = 0
        self.update_z()
        print('phase one')
        self.tableau.render()
        super().solve()
        
    def update_z(self):
        for col in range(len(self.tableau.z)):
            if self.tableau.vars[col] in self.tableau.in_base_vars:
                row = self.tableau.in_base_vars.index(self.tableau.vars[col])
                self.nullify_same_cols_objective_pivot(row, col)
            
    def phasetwo(self, original_z):
        self.tableau.z = original_z
        #Remove the artificial cols
        self.tableau.render()
        self.tableau.remove_artificial_cols()
        self.update_z()
        # self.tableau.z = original_z
        print('phase two')
        self.tableau.render()
        return super().solve()
    
    def is_infeasible(self):
        return self.tableau.solutions[-1] != 0

    def solve(self):
        if self.tableau.has_artificial_var():
            real_problem_type = self.problem_type
            original_problem = self.tableau.z[:]
            self.phaseone()
            if self.is_infeasible():
                raise Exception('Ce probleme est Infeasible')
            self.problem_type = real_problem_type
            result = self.phasetwo(original_problem)
            return result
        result = super().solve()
        return result
    

# str_problem = "Min -8*x1 -5*x2\n1*x1 +1*x2 <= 6\n1*x1 >= 5\n9*x1 +5*x2 <= 45"
# str_problem = "Max 4*x1 +5*x2\n2*x1 +3*x2 <= 6\n3*x1 +1*x2 >= 3" 
# str_problem = "Min 2*x1 +3*x2\n0.5*x1 +0.25*x2 <= 4\n1*x1 +3*x2 >= 36\n1*x1 +1*x2 = 10" 
# str_problem = ""
# tableau_builder = TableauBuilder(str_problem=str_problem)
# print(Simplex2Phases(tableau_builder.build(), tableau_builder.problem_type).solve())