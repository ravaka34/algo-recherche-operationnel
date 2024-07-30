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

def ford_fulkerson(graph, s, t, vertex_name):
    def calculate_flot(f):
        flot = 0
        for key in f.keys():
            if f'({s},' in key:
                flot = flot + f[key]['flot_qtt']
        return flot

    def init_f(graph):
        vertex_number = len(graph[0])
        f = {}
        for i in range(vertex_number):
            for j in range(vertex_number):
                if type(graph[i][j]) == list:
                     f[f'({i},{j})'] = {
                        'cap': graph[i][j][0],
                        'flot_qtt': graph[i][j][1]
                    }
                elif type(graph[i][j]) == int and graph[i][j] != 0:
                    f[f'({i},{j})'] = {
                        'cap': graph[i][j],
                        'flot_qtt':0
                    }
        print(f)
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
    step_number = 1
    #Pour chaque chemin trouve on fait amelioration
    for path in paths:
        variation = min_residual_capacity(f, path)
        if variation == 0:
            continue
        print("".join('-' for i in range(20)))
        print("Step number : "+str(step_number))
        render_path(path, vertex_name)
        # recherche la variation => min [capacity - flot]
       
        print("min variation ="+str(variation))
        for i in range(len(path)-1):
            #Si dans le sens on augmente
            arc = f'({path[i]},{path[i+1]})'
            if arc in f:
                render_variation(f, arc, variation, vertex_name)
                f[arc]['flot_qtt'] = f[arc]['flot_qtt'] + variation
            #Sinon on diminue
            else:
                render_variation(f, f'({path[i+1]},{path[i]})', -variation, vertex_name)
                f[f'({path[i+1]},{path[i]})']['flot_qtt'] = f[f'({path[i+1]},{path[i]})']['flot_qtt'] - variation
        step_number += 1
        print('Current flot = '+str(calculate_flot(f)))
               

    #Sommer les arcs sortants de s
    flot = 0
    for key in f.keys():
        if f'({s},' in key:
            flot = flot + f[key]['flot_qtt']
    f['flot'] = flot
    return f

def render_path(path, vertex_name):
    print('>'.join(vertex_name[i] for i in path))

def render_variation(f, key, variation, vertex_name):
        s = key.strip("()")
        # Split the string by the comma
        parts = s.split(",")
        # Convert the resulting substrings to integers
        i = int(parts[0])
        j = int(parts[1])
        cap = f[key]['cap']
        curr_qtt_flot = f[key]['flot_qtt']
        print(vertex_name[i]+'->'+vertex_name[j]+f'=> cap={cap}, qtt_flot={curr_qtt_flot}, variation={variation}, qtt_flot_after_update={curr_qtt_flot+variation}')

def render_result(f, vertex_name):
    for key in f:
        if key == 'flot':
            print('flot = '+str(f[key]))
            break
        s = key.strip("()")
        # Split the string by the comma
        parts = s.split(",")
        # Convert the resulting substrings to integers
        i = int(parts[0])
        j = int(parts[1])
        cap = f[key]['cap']
        qtt_flot = f[key]['flot_qtt']
        print(vertex_name[i]+'->'+vertex_name[j]+f'=> cap={cap}, qtt_flot={qtt_flot}')

exo = [
    #S1 S2 S3 T1 T2 T3 T4 T5 S  P
    [0, 2000, 0, 3000, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2000, 1000, 1000, 0, 0, 0, 0],
    [0, 2000, 0, 0, 0, 3000, 0, 0, 0, 0],
    [0, 0, 0, 0, 2000, 0, 7000, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2000, 1500, 0, 0],
    [0, 0, 0, 0, 3000, 0, 0, 1000, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 8000],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 4000],
    [5000, 4000, 3000, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

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
    [0, 0, 1, 0, 0, 0]
]

# solutions = []
# explore(simple_graph, 0, 5, [], [0], solutions)
# print(solutions)

    
vertex_name =['S1', 'S2', 'S3', 'T1', 'T2', 'T3', 'T4', 'T5', 'S', 'T']

# print(create_non_oriented_graph([[0, 1, 0], [0, 0, 0], [0, 1, 0]]))
ford_fulkerson(exo, 8, 9, vertex_name)

# solutions = []
# explore(create_non_oriented_graph(graph), 5, 6, [], [5], solutions)
# print(solutions)
