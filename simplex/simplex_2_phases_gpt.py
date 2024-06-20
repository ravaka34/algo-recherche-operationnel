def print_tableau(tableau):
    for row in tableau:
        print('\t'.join(map(str, row)))
    print()

def pivot_on(tableau, row, col):
    i, j = row, col
    pivot = tableau[i][j]
    
    # Normalize pivot row
    tableau[i] = [x / pivot for x in tableau[i]]
    
    # Zero out the rest of the column
    for r in range(len(tableau)):
        if r != i:
            factor = tableau[r][j]
            tableau[r] = [tableau[r][k] - factor * tableau[i][k] for k in range(len(tableau[0]))]

def phase1(A, b, num_artificial):
    m, n = len(A), len(A[0])
    
    # Construct the initial tableau for Phase 1
    tableau = [row[:] + [0] * num_artificial + [b[i]] for i, row in enumerate(A)]
    
    # Add artificial variables to the tableau
    for i in range(m):
        tableau[i][n + i] = 1
    
    # Add objective row for Phase 1
    tableau.append([0] * n + [1] * num_artificial + [0])
    
    # Subtract artificial variables from the objective row
    for i in range(m):
        tableau[-1] = [tableau[-1][j] - tableau[i][j] for j in range(len(tableau[0]))]
    
    # Perform Simplex iterations for Phase 1
    while any(x > 0 for x in tableau[-1][:-1]):
        col = tableau[-1].index(max(tableau[-1][:-1]))
        ratios = [(tableau[i][-1] / tableau[i][col], i) for i in range(m) if tableau[i][col] > 0]
        if not ratios:
            raise ValueError("Linear program is unbounded.")
        row = min(ratios)[1]
        pivot_on(tableau, row, col)
    
    return tableau

def phase2(tableau, c):
    m, n = len(tableau) - 1, len(tableau[0]) - 1
    tableau[-1] = c + [0] * (len(tableau[0]) - len(c))
    
    for i in range(m):
        tableau[-1] = [tableau[-1][j] - c[i] * tableau[i][j] for j in range(len(tableau[0]))]
    
    # Perform Simplex iterations for Phase 2
    while any(x > 0 for x in tableau[-1][:-1]):
        col = tableau[-1].index(max(tableau[-1][:-1]))
        ratios = [(tableau[i][-1] / tableau[i][col], i) for i in range(m) if tableau[i][col] > 0]
        if not ratios:
            raise ValueError("Linear program is unbounded.")
        row = min(ratios)[1]
        pivot_on(tableau, row, col)
    
    return tableau

def simplex_method(A, b, c):
    num_artificial = len(b)
    
    # Phase 1: Find a feasible solution
    tableau = phase1(A, b, num_artificial)
    if tableau[-1][-1] != 0:
        raise ValueError("No feasible solution found.")
    
    # Remove artificial variables from the tableau
    for i in range(len(tableau)):
        tableau[i] = tableau[i][:len(tableau[i]) - num_artificial - 1] + [tableau[i][-1]]
    
    # Phase 2: Optimize the original objective function
    tableau = phase2(tableau, c)
    
    return tableau

# Example problem
A = [
    [1, 1],
    [-1, 1]
]
b = [4, 2]
c = [1, 2]

tableau = simplex_method(A, b, c)

print("Final Tableau:")
print_tableau(tableau)

print("Optimal value:", tableau[-1][-1])
print("Optimal solution:", [tableau[i][-1] for i in range(len(tableau) - 1)])
