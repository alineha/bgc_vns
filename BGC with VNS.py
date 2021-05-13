from math import *
from sys import version
import time
import operator
import random
from input_output import *
from IPython.display import HTML
import matplotlib.pyplot as plt

SEED = 21938273
random.seed(SEED)
CONFLICT_WEIGHT = 10000
MAX_ITERATIONS = 1000
MAX_TIME = 10800
PARTITIONS = 4

class Solution():
    def __init__(self, colouring, graph):
        self.vertexes_by_colour = []
        self.colouring = colouring
        self.colour_weights = []
        for colour in range(0, graph.colours):
            self.colour_weights.append((colour, 0))
            self.vertexes_by_colour.append([])
        for vertex, colour in colouring.items():
            self.vertexes_by_colour[colour].append(vertex)
            self.colour_weights[colour] = (colour, self.colour_weights[colour][1] + graph.vertexes[vertex].weight)
    
    def __init__(self, graph):
        self.vertexes_by_colour = []
        self.colouring = {}
        self.colour_weights = []
        for colour in range(0, graph.colours):
            self.colour_weights.append((colour, 0))
            print(self.colour_weights)
            self.vertexes_by_colour.append([])

    def evaluate(self,graph):
        conflicts = graph.number_of_conflicts(self.colouring)
        print(f"{conflicts} conflicts")
        WEIGHT_INDEX_TUPLE = 1
        max_colour_weight = sorted(self.colour_weights, key = lambda x: x[1], reverse=True)[0][WEIGHT_INDEX_TUPLE]
        return max_colour_weight + conflicts * CONFLICT_WEIGHT

    def modify_colour(self,vertex,weight,new_colour):
        if vertex in self.colouring:    
            old_colour = self.colouring[vertex]
            self.colour_weights[old_colour] = (old_colour, self.colour_weights[old_colour][1] - weight)
            self.vertexes_by_colour[old_colour].remove(vertex)
        self.colouring[vertex] = new_colour
        self.colour_weights[new_colour] = (new_colour, self.colour_weights[new_colour][1] + weight)
        self.vertexes_by_colour[new_colour].append(vertex)

    def __str__(self):
        string = '----------------------------------\n'
        for vertex,colour in self.colouring.items():
            string+=f'Vertex {vertex} was coloured with {colour}\n'
        string+='----------------------------------\n'
        return string

# TODO explicar solução inicial
def initial_solution(graph):
    colour = (0,0)
    # sort por peso decrescente de vértice
    vertexes = sorted(graph.vertexes, key=operator.attrgetter("degree"), reverse=True)
    colouring = {}
    colouring[vertexes[0].index] = 0

    current_solution = Solution(graph)
    current_solution.colouring = colouring

    for v in vertexes:
        for colour in sorted(current_solution.colour_weights, key = lambda x: x[1]):
            if v.index not in colouring:
                can_be_coloured = True
                for w in v.adj:
                    if (w in colouring) and (colour[0] == colouring[w]):
                        can_be_coloured = False
                if can_be_coloured:
                    current_solution.modify_colour(v.index,v.weight,colour[0])

    for v in graph.vertexes:
        if v.index not in colouring:
            # v é vértice que tem conflito
            c = v.check_conflicts(colouring,graph.colours)
            current_solution.modify_colour(v.index,v.weight,min(zip(c, range(len(c))))[1])

    return current_solution

def time_to_stop(time,iterations):
    return (time >= MAX_TIME or iterations > MAX_ITERATIONS)

#SOLUTION MUST BE DEEP COPY
def balance_colours(graph, solution, greater_colour, lesser_colour, is_random):
    # set()s with the indexes of the vertexes coloured with the colours
    greater_vertexes = solution.vertexes_by_colour[greater_colour]
    recoloured_vertex_weight = 0
    recoloured_vertex = []

    if(is_random):
        recoloured_vertex = greater_vertexes[random.randrange(0,len(greater_vertexes))]
        recoloured_vertex_weight = graph.vertexes[recoloured_vertex].weight
    else:
        for v in greater_vertexes:
            if(graph.vertexes[v].weight >= recoloured_vertex_weight):
                recoloured_vertex_weight = graph.vertexes[v].weight
                recoloured_vertex = v

    solution.modify_colour(recoloured_vertex,recoloured_vertex_weight,lesser_colour)

    print(f'[{recoloured_vertex}, {recoloured_vertex_weight}] ({greater_colour} -> {lesser_colour})\n')

    return solution

def random_neighbour(graph,s,k):
    if k == 1:
        return random_neighbour1n2(graph,s,False)
    if k == 2:
        return random_neighbour1n2(graph,s,True)
    if k == 3:
        return 2
    if k == 4:
        return 3
    if k == 5:
        return random_neighbour5(graph,s)
        
def generate_random_colour(graph,solution,partitions):
    i = random.randrange(0,floor((graph.colours/partitions)))
    if(i==graph.colours):
        i-=1

    sorted_colours = sorted(solution.colour_weights, key = lambda x: x[1], reverse=True)
    greater_colour = sorted_colours[0][0]
    lesser_colour = sorted_colours[-i][0]
    new_solution = copy.deepcopy(solution)

    return(greater_colour,lesser_colour,new_solution)

# Tranfers the heaviest/a random vertex from the heaviest colour to a random non-heaviest colour.
def random_neighbour1n2(graph, solution, randomBalance):
    greater_colour,lesser_colour,new_solution = generate_random_colour(graph,solution,PARTITIONS)
    balance_colours(graph,new_solution,greater_colour,lesser_colour, randomBalance)
    print(solution.evaluate(graph), new_solution.evaluate(graph))
    return new_solution

# Transfers enough vertexes from the heaviest colour to a random colour to make the heaviest colour not be the heaviest anymore
def random_neighbour3(graph, solution):
    greater_colour,lesser_colour,new_solution = generate_random_colour(graph,solution,1)
    while(new_solution.colour_weights)
    print(solution.evaluate(graph), new_solution.evaluate(graph))
    return new_solution


# The conflict correction neighbourhood - if the algorithm got to this one, it means there is a need to lessen the number of conflicts
# Changes a random vertex to the colour that would give it the least number of conflicts
def random_neighbour5(graph, solution):
    v = random.randrange(0,floor(len(graph.vertexes)-1))

    new_solution = copy.deepcopy(solution)
    conflicts = graph.vertexes[v].check_conflicts(new_solution.colouring,graph.colours)
    new_solution.modify_colour(v,graph.vertexes[v].weight,min(zip(conflicts, range(len(conflicts))))[1])
    print(f'[{v}, {graph.vertexes[v].weight}] ({solution.colouring[v]} -> {new_solution.colouring[v]})\n')
    print(solution.evaluate(graph), new_solution.evaluate(graph))
    return new_solution

# TODO
def local_search(k,solution,graph):
    i = 0

def VNS(graph):
    start_time = time.time()
    s = initial_solution(graph)
    iterations = 0
    
    iterations_result = []

    while not time_to_stop(time.time()-start_time,iterations):
        k = 1
        while k <= 4:
            s1 = random_neighbour(graph,s,k)
            if s1 != -1:
                s2 = local_search(k,s1,graph)
                if s2.evaluate(graph.number_of_conflicts(s2.colouring))<s.evaluate(graph.number_of_conflicts(s.colouring)):
                    s = s2
                    k = 1
                else:
                    k = k+1
            else:
                k = k+1
        iterations+=1
        iterations_result.append(s)

    plt.figure(figsize=(10, 6))     
    plt.scatter(list(range(0, iterations)), iterations_result)
    plt.xlabel('Iterations')
    plt.ylabel('Solution')
    plt.title('Dados')
    plt.show()

    return s

#D:\\Documents\\workspace\\git\\bgc_vns\\
g = read_file("D:\\Documents\\workspace\\git\\bgc_vns\instances\\cmb01")
solution = initial_solution(g)
# VNS(g)


