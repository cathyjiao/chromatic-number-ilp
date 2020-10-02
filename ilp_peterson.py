# ILP for Graph Coloring using Python MIP - Mixed-Integer Programming Package
# Setup: Use Python 3 and "pip install mip"
# Author: Cathy Jiao (2019)

from mip import Model, xsum, minimize, BINARY, OptimizationStatus


def ilp_graph_coloring(n, edges):
    """
    Integer LP for a Graph coloring
    :param n: (int) number of vertices in the graph
    :param edges: list of tuples of the edges in the graph e.g. a triangle graph would be [(1,2), (2,3),( 3,1)]
    """

    # initialize model
    model = Model('graph_coloring')

    # color variables w1,...,wn (binary variables, 0 or 1)
    w = [model.add_var(var_type=BINARY) for i in range(n)]

    # vertex color variables (binary variables, 0 or 1)
    # initialized as 2d list, each list represents the color variables for a vertex
    x = [[model.add_var(var_type=BINARY) for j in range(n)] for i in range(n)]

    # objective function, minimize number of variables
    model.objective = minimize(xsum(w[i] for i in range(n)))

    # first constraint, each vertex must have exactly one color
    for i in range(n):
        model += xsum(x[i][j] for j in range(n)) == 1

    # second constraint, not adjacent vertices can share an edge
    for k in range(n):
        for (i, j) in edges:
            model += x[i][k] + x[j][k] <= w[k]

    # solve
    status = model.optimize()

    # print results
    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution cost {} found'.format(model.objective_value))
        for v in model.vars:
            if abs(v.x) > 0:  # only printing non-zeros
                print('{} : {}'.format(v.name, v.x))


# ======== INPUT =========
# Peterson Graph has ten vertices
n = 10

# Edges in a Petersen graph
# The way the vertices are numbered:
# The 5 outer vertices, starting from the uppermost vertex and going clockwise is labeled 0 to 4
# The 5 inter vertices (which form a star), starting from the uppermost vertex and going clockwise is labeled 5 to 9
edges = [
    (0, 1),
    (0, 4),
    (0, 5),
    (1, 2),
    (1, 6),
    (2, 3),
    (2, 7),
    (3, 4),
    (3, 8),
    (4, 9),
    (5, 7),
    (5, 8),
    (6, 8),
    (6, 9),
    (7, 9)
]

# solve ILP on Petersen graph
ilp_graph_coloring(n, edges)

# ======== OUTPUT =========
# There are 110 variables:
# Variables 0 to 9 are color variables
# Variables 10 to 19 are color variables for vertex 1 (eg variable var(18) is value of assigning vertex 1 to color 8)
# The remaining variables are color variables for the remaining vertices
# optimal solution cost 3.0 found
# var(0) : 1.0 (color 0 is used)
# var(1) : 1.0 (color 1 is used)
# var(8) : 1.0 (color 8 is used)
# var(18) : 1.0  (vertex 1 is assigned color 8)
# var(20) : 1.0  (vertex 2 is assigned color 0)
# var(38) : 1.0  (vertex 3 is assigned color 8)
# var(41) : 1.0  (vertex 4 is assigned color 1)
# var(50) : 1.0 (vertex 5 is assigned color 0)
# var(60) : 1.0  (vertex 6 is assigned color 0)
# var(71) : 1.0  (vertex 7 is assigned color 1)
# var(81) : 1.0  (vertex 8 is assigned color 1)
# var(98) : 1.0  (vertex 9 is assigned color 8)
# var(108) : 1.0 (vertex 10 is assigned color 8)
# The remaining variables are assigned a value of 0
