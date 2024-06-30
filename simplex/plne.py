from simplex_2_phases import Simplex2Phases
from tableau_builder import TableauBuilder
from simplex_tableau import SimplexTableau

class PLNE(Simplex2Phases):

    def __init__(self, simplex_tableau: SimplexTableau, problem_type, fractional_result = False):
        super().__init__(simplex_tableau, problem_type, fractional_result)
        self.original_problem = self.tableau.str_problem
        self.original_tab = self.tableau
        self.result_keys = None
        self.optimum_z_value = None
        self.optimum_result = {}

    def is_subtree_pruned(self, z_value):
        if self.optimum_z_value == None:
            return False
        # Probleme de maximisation
        if self.problem_type == 1:
            print('eto')
            return z_value <= self.optimum_z_value
        #Probleme de minimisation
        if self.problem_type == -1:
            return z_value >= self.optimum_z_value
    
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
                    constraint = "\n1*"+key+" "+signe+" "+str(whole_number + (signe == '>='))
                    print(tableau.str_problem+constraint)
                    tab1 = TableauBuilder(str_problem=tableau.str_problem+constraint).build()
                    self.brunch(tab1)

        if all_integer and abs(result['z'] % 1) <= 1e-6:
            self.optimum_result ['result'] = result
            self.optimum_result ['tableau'] = tableau
            self.optimum_z_value = result['z']

    def solve(self):
        self.brunch(self.tableau)
        return self.optimum_result
    
    def render_result(self):
        print('The optimum result is :')
        tableau = self.optimum_result['tableau']
        print(tableau.str_problem)
        tableau.render()
        print(self.optimum_result['result'])
        
        


# str_problem = "Min -8*x1 -5*x2\n1*x1 +1*x2 <= 6\n9*x1 +5*x2 <= 45" 
# str_problem = "Max 3*x1 +4*x2\n2*x1 +1*x2 <= 6\n2*x1 +3*x2 <= 9" 
# str_problem = "Max 10*x1 +11*x2\n10*x1 +12*x2 <= 59" 
# str_problem = "Max 5*x1 +6*x2\n1*x1 +1*x2 <= 5\n4*x1 +7*x2 <= 28"
# str_problem = "Max 5x1 + 4x2\n1*x1 +x2 <= 5\n10x1 - 6x2 <= 45"
str_problem = "Max 10*x1 +14*x2 +12*x3\n1*x1 +3*x2 -2*x3 <= 40\n3*x1 +2*x2 +1*x3 <= 45\n1*x1 +1*x2 +4*x3 <= 38"
# str_problem = "Max 10*x1 +14*x2 +12*x3\n1*x1 +3*x2 +2*x3 <= 40\n3*x1 +2*x2 +1*x3 <= 45\n1*x1 +1*x2 +4*x3 <= 38"

tableau_builder = TableauBuilder(str_problem=str_problem)
plne_solver = PLNE(tableau_builder.build(), tableau_builder.problem_type)
plne_solver.solve()
plne_solver.render_result()
