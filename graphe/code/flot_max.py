def create_non_oriented_graph(oriented_graph):
    vertex_number = len(oriented_graph[0])
    graph = [[0]*vertex_number for _ in range(vertex_number) ]
    for i in range(vertex_number):
        for j in range(vertex_number):
            if oriented_graph[i][j] != 0:
                graph[i][j] = 1
                graph[j][i] = 1
    return graph

def explore(graph, vertex, target, already_visited, path, solutions):
    if vertex == target:
        solutions.append(path[:])
        return

    for j in range(len(graph[0])):
        #Explore all neighboors and check if it is already in the current path
        if graph[vertex][j] != 0 and j not in path:
            path.append(j)
            explore(graph, j, target, already_visited, path, solutions)
            #Backtracking
            path.pop()

def ford_fulkerson(graph, s, t):
    def init_f(graph):
        vertex_number = len(graph[0])
        f = {}
        for i in range(vertex_number):
            for j in range(vertex_number):
                if graph[i][j] != 0:
                    f[f'({i},{j})'] = {
                        'cap': graph[i][j],
                        'flot_qtt':0
                    }
        return f
    
    def min_residual_capacity(f, path):
        min_cap = float('inf')
        for i in range(len(path)-1):
            #Calculate the qtt of flow each arc can handle
            tmp = 0
            arc = f'({path[i]},{path[i+1]})'
            #On va faire ajout 
            if arc in f:
                tmp = f[arc]['cap'] - f[arc]['flot_qtt']
            #On peut annuler jusqu a ce que 0
            else:
                tmp = f[f'({path[i+1]},{path[i]})']['flot_qtt']
            if tmp < min_cap:
                min_cap = tmp 
        return min_cap
    
    #Creation de flot
       # Reperage des arc et asignation inital de flot 0 
    f = init_f(graph)
    #Reperage de tous les chemins
    paths = []
    explore(create_non_oriented_graph(graph), s, t, [], [s], paths)
    #Pour chaque chemin trouve on fait amelioration
    for path in paths:
        # recherche la variation => min [capacity - flot]
        variation = min_residual_capacity(f, path)

        
        for i in range(len(path)-1):
            #Si dans le sens on augmente
            arc = f'({path[i]},{path[i+1]})'
            if arc in f:
                f[arc]['flot_qtt'] = f[arc]['flot_qtt'] + variation
            #Sinon on diminue
            else:
                f[f'({path[i+1]},{path[i]})']['flot_qtt'] = f[f'({path[i+1]},{path[i]})']['flot_qtt'] - variation

    #Sommer les arcs sortants de s
    flot = 0
    for key in f.keys():
        if f'({s},' in key:
            flot = flot + f[key]['flot_qtt']
    f['flot'] = flot
    return f

# 0 : s, a : 1, b : 2, 
graph = [
    [0, 5, 0, 3, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 10],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 3],
    [0, 0, 0, 8, 0, 0, 0],
    [4, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


simple_graph = [
    [0, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0],
]

# solutions = []
# explore(simple_graph, 0, 5, [], [0], solutions)
# print(solutions)

    

# print(create_non_oriented_graph([[0, 1, 0], [0, 0, 0], [0, 1, 0]]))
print(ford_fulkerson(graph, 5, 6))

# solutions = []
# explore(create_non_oriented_graph(graph), 5, 6, [], [5], solutions)
# print(solutions)
