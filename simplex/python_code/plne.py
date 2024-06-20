from simplex_2_phases import Simplex2Phases
from tableau_builder import TableauBuilder
from simplex_tableau import SimplexTableau

class PLNE(Simplex2Phases):

    def __init__(self, simplex_tableau: SimplexTableau, problem_type):
        super().__init__(simplex_tableau, problem_type)
        self.original_problem = self.tableau.str_problem
        self.original_tab = self.tableau
        self.result_keys = None
        self.optimum_z_value = None
        self.optimum_result = {}
        self.recorded_constraints = []

    def is_subtree_pruned(self, z_value):
        if self.optimum_z_value == None:
            return False
        if self.problem_type == 1:
            return z_value >= self.optimum_z_value
        if self.problem_type != 1:
            return z_value <= self.optimum_z_value

    def is_constraint_already_used(self, constraint):
        # Compare the current result against recorded results
        for record in self.recorded_constraints:
            if record == constraint :
                return True
        return False
                    
    
    def brunch(self, tableau):
        #Relaxation
        self.tableau = tableau
        # self.tableau.render()
        try:
            result = super().solve()
        except Exception as e:
            return
        
        #sous-branche est elague ne fournit pas de solution plus optimale que notre branche
        
        if self.is_subtree_pruned(result['z']):
            print('z value substree is pruned = '+ str(result['z'])+' z optimum value '+str(self.optimum_z_value))
            return 

        all_integer = True
        #Brunch
        for key in list(result.keys())[:-1]:
            if result[key] != 0 and abs(result[key] % 1) > 1e-6:
                all_integer = False
                whole_number = int(result[key])
                signes = "<= >="
                for signe in signes.split():
                    constraint = "\n1."+key+" "+signe+" "+str(whole_number + (signe == '>='))
                    if not self.is_constraint_already_used(constraint):
                        self.recorded_constraints.append(constraint)
                        print(self.original_problem+constraint)
                        tab1 = TableauBuilder(str_problem=self.original_problem+constraint).build()
                        self.brunch(tab1)

        if all_integer and abs(result['z'] % 1) <= 1e-6:
            self.optimum_result = result
            self.optimum_z_value = result['z']

    def solve(self):
        self.brunch(self.tableau)
        return self.optimum_result
        


str_problem = "Min -8.x1 -5.x2\n1.x1 +1.x2 <= 6\n9.x1 +5.x2 <= 45"

tableau_builder = TableauBuilder(str_problem=str_problem)
print(PLNE(tableau_builder.build(), tableau_builder.problem_type).solve())