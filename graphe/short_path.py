"""
    Algorithm to know the short path from a specific vertex to the other vertices
"""
def moore_djikstra(oriented_graph, start_index, vertex_name):
    #Init all the vertices pi values to infinit except for the start index
    vertex_number = len(oriented_graph[0])
    pi_values = [[float('inf'), ''] for _ in range(vertex_number)]
    pi_values[start_index] = [0, vertex_name[start_index]]
    not_visited = { i : float('inf') for i in range(vertex_number) }
    not_visited[start_index] = 0
    print

    while not_visited:
        # current_index is min pi_values and is not_visited
        current_index = min(not_visited, key = not_visited.get)
        current_pi = pi_values[current_index][0]
        for i in range(vertex_number):
            distance = oriented_graph[current_index][i]
            #Get the neighboors
            if distance != 0:
                pi_value = distance + current_pi
                if pi_value < pi_values[i][0]:
                    pi_values[i] = [pi_value, f'{pi_values[current_index][1]}>'+vertex_name[i]]
                    not_visited[i] = pi_value
        not_visited.pop(current_index)
       
    return pi_values


def bellman_ford(oriented_graph, start_index):

    def arc_indexes(oriented_graph, vertex_number):
        indexes = []
        for i in range (vertex_number):
            for j in range(vertex_number):
                if oriented_graph[i][j] != 0:
                    indexes.append([i, j])
        return indexes

    vertex_number = len(oriented_graph[0])
    d = [float('inf')] * vertex_number
    pred = [-1] * vertex_number
    arc_indexes = arc_indexes(oriented_graph, vertex_number)
    d[start_index] = 0

    for _ in range(1, vertex_number):
        for u, v in arc_indexes:
            temp_d = d[u] + oriented_graph[u][v]
            #Mettre a jour la distance et son predecesseur
            if temp_d < d[v] :
                d[v] = temp_d
                pred[v] = u

    for u, v in arc_indexes:
        temp_d = d[u] + oriented_graph[u][v]
        if temp_d < d[v]:
           print ('Il existe un cycle absorbant')

    return d, pred
     
oriented_graph = [
    [0, 25, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 4, 0],
    [0, 1, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

test_negative = [
    [0, 5, 2],
    [0, 0, -10],
    [0, 0, 0]
]

test_cycle_absorbant = [
    [0, 1, 0],
    [0, 0, -3],
    [1, 0, 0]
]

exo = [
    [0, 4, 6, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 0, 6, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
vertex_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
print(moore_djikstra(exo, 0, vertex_name))
# print(bellman_ford(test_cycle_absorbant, 0))