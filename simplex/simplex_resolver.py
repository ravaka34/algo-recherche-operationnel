from simplex_tableau import SimplexTableau
from tableau_builder import TableauBuilder


class SimplexResolver:

    def __init__(self, simplex_tableau: SimplexTableau, problem_type):
        self.tableau = simplex_tableau
        self.problem_type = problem_type

    def col_pivot(self):
        # Choix variable entrante
        # recherche maximum positive ou minimum negative
        if self.problem_type == 1:
            max_value = max(self.tableau.z)
            if max_value <= 0:
                return None
            return self.tableau.z.index(max_value)
        else:
            min_value = min(self.tableau.z)
            if min_value >= 0:
                return None
            return self.tableau.z.index(min_value)

    def row_pivot(self, col_pivot):
        minimum = float("inf")
        row_pivot = -1
        for i in range(0, len(self.tableau.constraints)):
            if self.tableau.constraints[i][col_pivot] == 0:
                continue
            rapport = self.tableau.solutions[i] / self.tableau.constraints[i][col_pivot]
            if (rapport > 0 and rapport < minimum) or (
                rapport == minimum and self.tableau.in_base_vars[i][0] == "a"
            ):
                row_pivot = i
                minimum = rapport

        # La solution est deja optimale
        if row_pivot == -1:
            raise Exception("Solution illimite rencontre")
        return row_pivot

    def search_pivot(self):
        col_pivot = self.col_pivot()
        if col_pivot == None:
            return None
        row_pivot = self.row_pivot(col_pivot)
        return [row_pivot, col_pivot]

    # rendre la valeur du pivot a 1
    def make_pivot_value_1(self, row_pivot, col_pivot):
        pivot_value = self.tableau.constraints[row_pivot][col_pivot]
        self.tableau.constraints[row_pivot] = [
            x / pivot_value for x in self.tableau.constraints[row_pivot]
        ]
        self.tableau.solutions[row_pivot] = (
            self.tableau.solutions[row_pivot] / pivot_value
        )

    # Annuler les pseudo-pivots dans les containtes et les solutions des variables dans base
    # pseudo-pivot les valeurs qui ont la meme colonne que le pivot
    def nullify_same_cols_constraints_pseudo_pivot(self, row_pivot, col_pivot):
        for i in range(0, len(self.tableau.constraints)):
            if i == row_pivot:
                continue
            # valeur du chiffre sur la meme colonne que le pivot
            pseudo_pivot = self.tableau.constraints[i][col_pivot]
            self.tableau.constraints[i] = [
                x - pseudo_pivot * y
                for x, y in zip(
                    self.tableau.constraints[i], self.tableau.constraints[row_pivot]
                )
            ]
            self.tableau.solutions[i] = (
                self.tableau.solutions[i]
                - pseudo_pivot * self.tableau.solutions[row_pivot]
            )

    # Annuler les pseudo-pivots dans l'objective et la solution de l'objective
    def nullify_same_cols_objective_pivot(self, row_pivot, col_pivot):
        pseudo_pivot = self.tableau.z[col_pivot]
        self.tableau.z = [
            x - pseudo_pivot * y
            for x, y in zip(self.tableau.z, self.tableau.constraints[row_pivot])
        ]
        # print(self.tableau.solutions[-1],pseudo_pivot, self.tableau.solutions[row_pivot])
        print(self.tableau.solutions[-1]- pseudo_pivot * self.tableau.solutions[row_pivot])
        self.tableau.solutions[-1] = (
            self.tableau.solutions[-1]
            - pseudo_pivot * self.tableau.solutions[row_pivot]
        )

    def update_in_base_var(self, row_pivot, col_pivot):
        self.tableau.in_base_vars[row_pivot] = self.tableau.vars[col_pivot]

    def solve(self):
        pivot = self.search_pivot()
        while pivot != None:
            row_pivot, col_pivot = pivot

            self.make_pivot_value_1(row_pivot, col_pivot)
            self.nullify_same_cols_constraints_pseudo_pivot(row_pivot, col_pivot)
            self.nullify_same_cols_objective_pivot(row_pivot, col_pivot)
            self.update_in_base_var(row_pivot, col_pivot)
            pivot = self.search_pivot()
            self.tableau.render()
        return self.extract_result()

    def extract_result(self):
        result = {}
        for var in self.tableau.vars:
            if var[0] == "x":
                found = False
                # Search the value of the variable among the in base vars
                for i in range(len(self.tableau.in_base_vars)):
                    if self.tableau.in_base_vars[i] == var:
                        result[var] = self.tableau.solutions[i]
                        found = True
                        break
                if not found:
                    result[var] = 0
        result["z"] = self.tableau.solutions[-1]
        return result