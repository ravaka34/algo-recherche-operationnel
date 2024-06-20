def graph_color(graph):
    """
    Finds the minimum number of colors required to color 
    the graph such that no two adjacent vertices have the same color.
    
    Parameters:
        graph (List[List[int]]): An adjacency matrix representing the graph. `graph[i][j]` is 1 if 
        there is an edge between vertices i and j, otherwise 0.
        ex:     
            A---B---C
            | / | \ |
            D---E---F
        [
            [0, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 1],
            [1, 1, 0, 0, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 1, 0],
        ]

    
    Returns:
        Tuple[int, List[List[int]]]: A tuple containing the minimum number 
        of colors required (`min_k`) and a list of all possible colorings
        achieving that minimum (`record_solution`).
    """

    def order_by_degree_desc(graph):
        """
        Order the graph by their respective degrees following the desc order

        Parameter:
            graph (List[List[int]]): An adjacency matrix representing the graph. `graph[i][j]` is 1 if 
            there is an edge between vertices i and j, otherwise 0.
        
        Return: 
        [{"row_index": int, "degrees": "color": int}]: An array of dictionnary order by the degrees of the vertex following the desc order.
        """
        vertex_desc_order = []
        i = 0
        for row in graph:
            vertex_desc_order.append(
                {
                    "row_index": i,
                    "degrees": sum(row),
                    "color": -1
                }
            )
            i += 1
        vertex_desc_order = sorted(vertex_desc_order, key=lambda x: x["degrees"], reverse=True)

        #Transform it to dictionnary to ease the use
        dict_vertex_desc_order = {}
        for value in vertex_desc_order:
            dict_vertex_desc_order[value["row_index"]] = value

        return dict_vertex_desc_order 

    def color_vertex_non_adj(row_index, graph, color, vertex_desc_order):
        """
        Color all the vertex that are non adjacent to the vertex (represented by row_index) with the same color

        Parameters:
            row_index int: the row of the vertex
            graph: the graph represented by a 2d matrix
            color: the color
            vertex_desc_order {{"row_index": int, "degrees": "color": int}}: A dictionnary of
             dictionnary order by the degrees of the vertex following the desc order where the value color is initialized by -1.

        Return:
        the updated vertex_desc_order updated
        
        """
        for col in range(len(graph[row_index])):
            #Skip if it is adjacent or already coloured
            if graph[row_index][col] == 1 or vertex_desc_order[col]["color"] != -1 :
                continue
            vertex_desc_order[col]["color"] = color

        return vertex_desc_order
    
    current_color = 0
    vertex_desc_order = order_by_degree_desc(graph)
    for vertex in vertex_desc_order.values():
        if vertex["color"] != -1:
            continue
        vertex["color"] = current_color
        #Color all the non adjacent vertex with the same color
        vertex_desc_order = color_vertex_non_adj(vertex["row_index"], graph, current_color, vertex_desc_order)
        current_color += 1

    return vertex_desc_order


# graph = [
#     [0, 1, 1, 0, 1],
#     [1, 0, 0, 1, 1],
#     [1, 0, 0, 0, 1],
#     [0, 1, 0, 0, 0],
#     [1, 1, 1, 0, 0]
# ]

#ITU
graph = [
    [0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0]

]

solution = graph_color(graph)
print(solution)



