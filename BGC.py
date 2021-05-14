from math import *
import sys
import time
import operator
import random
from input_output import *
from IPython.display import HTML
import matplotlib.pyplot as plt

# Standard values for the parameters
# seed = 21938273
# conflict_weight = 10000
# max_iterations = 1000
# max_time = 1800
# partitions = 4

out_file,in_file,seed,conflict_weight,max_iterations,max_time,partitions = get_input(sys.argv)

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
            self.vertexes_by_colour.append([])

    def evaluate(self,graph):
        conflicts = graph.number_of_conflicts(self.colouring)
        WEIGHT_INDEX_TUPLE = 1
        max_colour_weight = sorted(self.colour_weights, key = lambda x: x[1], reverse=True)[0][WEIGHT_INDEX_TUPLE]
        return max_colour_weight + conflicts * conflict_weight

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
    return (time >= max_time or iterations > max_iterations)

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

    return solution

def random_neighbour(graph,s,k):
    if k == 1:
        return random_neighbour1n2(graph,s,False)
    if k == 2:
        return random_neighbour1n2(graph,s,True)
    if k == 3:
        return random_neighbour3(graph,s)
    if k == 4:
        return random_neighbour4(graph,s)
    if k == 5:
        return random_neighbour5(graph,s)
        
def get_colours_to_swap(graph,solution,partitions):
    i = random.randrange(0,floor((graph.colours/partitions)))
    if(i==graph.colours): i-=1 #acho que não precisa

    sorted_colours = get_colors_by_weight(solution)
    greater_colour = sorted_colours[0][0]
    lesser_colour = sorted_colours[-i][0]
    new_solution = copy.deepcopy(solution)

    return(greater_colour, lesser_colour, new_solution)

def get_colors_by_weight(solution):
    return sorted(solution.colour_weights, key = lambda x: x[1], reverse=True)

# Tranfers the heaviest/a random vertex from the heaviest colour to a random non-heaviest colour.
def random_neighbour1n2(graph, solution, randomBalance):
    greater_colour, lesser_colour, new_solution = get_colours_to_swap(graph,solution,partitions)
    balance_colours(graph,new_solution, greater_colour, lesser_colour, randomBalance)
    return new_solution

# Transfers enough vertexes from the heaviest colour to random colours to make the heaviest colour not be the heaviest anymore
def random_neighbour3(graph, solution):
    sorted_colours = sorted(solution.colour_weights, key = lambda x: x[1], reverse=True)
    greater_colour = sorted_colours[0][0]
    greater_colour_weight = sorted_colours[0][1]

    snd_greater_colour = sorted_colours[1][0]
    snd_greater_colour_weight = sorted_colours[1][1]
    new_solution = copy.deepcopy(solution)

    while(greater_colour_weight > snd_greater_colour_weight):
        i = random.randrange(2,(graph.colours))
        lesser_colour = sorted_colours[i][0]

        greater_vertexes = new_solution.vertexes_by_colour[greater_colour]
        recoloured_vertex = greater_vertexes[random.randrange(0,len(greater_vertexes))]
        recoloured_vertex_weight = graph.vertexes[recoloured_vertex].weight

        new_solution.modify_colour(recoloured_vertex,recoloured_vertex_weight,lesser_colour)

        greater_colour_weight = new_solution.colour_weights[greater_colour][1]
        snd_greater_colour_weight = new_solution.colour_weights[snd_greater_colour][1]

    return new_solution

# Transfers enough vertexes from the heaviest colour to a random colour to make them have a similar weight
def random_neighbour4(graph, solution):
    sorted_colours = sorted(solution.colour_weights, key = lambda x: x[1], reverse=True)
    greater_colour = sorted_colours[0][0]
    greater_colour_weight = sorted_colours[0][1]

    i = random.randrange(1,(graph.colours))
    lesser_colour = sorted_colours[i][0]
    lesser_colour_weight = sorted_colours[i][1]
    new_solution = copy.deepcopy(solution)

    while(greater_colour_weight > lesser_colour_weight):
        greater_vertexes = new_solution.vertexes_by_colour[greater_colour]
        recoloured_vertex = greater_vertexes[random.randrange(0,len(greater_vertexes))]
        recoloured_vertex_weight = graph.vertexes[recoloured_vertex].weight

        new_solution.modify_colour(recoloured_vertex,recoloured_vertex_weight,lesser_colour)

        greater_colour_weight = new_solution.colour_weights[greater_colour][1]
        lesser_colour_weight = new_solution.colour_weights[lesser_colour][1]

    return new_solution

# The conflict correction neighbourhood - if the algorithm got to this one, it means there is a need to lessen the number of conflicts
# Changes a random vertex to the colour that would give it the least number of conflicts
def random_neighbour5(graph, solution):
    new_solution = copy.deepcopy(solution)
    v = random.randrange(0,floor(len(graph.vertexes)-1))
    conflicts = graph.vertexes[v].check_conflicts(new_solution.colouring,graph.colours)
    new_solution.modify_colour(v,graph.vertexes[v].weight, min(zip(conflicts, range(len(conflicts))))[1])
    return new_solution

def local_search(k, solution, graph): 
    best_solution = copy.deepcopy(solution)
    found_best = True
    while(found_best):
        greater_colour = get_colors_by_weight(best_solution)[0][0]
        greater_vertexes = best_solution.vertexes_by_colour[greater_colour]
        j = 0
        found_best = False
        while j < graph.colours and not found_best: # N(s)
            new_solution = copy.deepcopy(best_solution)
            for v in greater_vertexes:
                new_solution.modify_colour(v,graph.vertexes[v].weight, j)
                if(new_solution.evaluate(graph) < best_solution.evaluate(graph)):
                    best_solution = copy.deepcopy(new_solution)
                    found_best = True
                    break
            j+=1
    return best_solution

def VNS(graph,out_file):
    f = open(out_file, "w")

    start_time = time.time()
    current_time = 0
    s = initial_solution(graph)
    iterations = 0
    
    iterations_result = []
    print(in_file[-5:])
    while not time_to_stop(current_time,iterations):
        k = 1
        while k <= 4 and not time_to_stop(current_time,iterations):
            s1 = random_neighbour(graph,s,k)
            s2 = local_search(k,s1,graph)
            if s2.evaluate(graph)<s.evaluate(graph):
                s = copy.deepcopy(s2)
                k = 1
            else:
                k = k+1
            iterations+=1
            iterations_result.append(s.evaluate(graph))
            current_time = time.time()-start_time

    f.write(f"INSTANCE: {in_file[-5:]}\nFINAL SOLUTION: {s.evaluate(graph)}\n# OF CONFLICTS: {graph.number_of_conflicts(s.colouring)}\n")
    f.write(f"ITERATIONS: {iterations}\nTIME: {current_time} seconds\n")
    f.write(f"SEED: {seed}\nCONFLICT_WEIGHT: {conflict_weight}\nMAX # OF ITERATIONS: {max_iterations}\n")
    f.write(f"MAX TIME: {max_time} seconds\n# OF PARTITIONS: {partitions}")

    plt.figure(figsize=(10, 6))     
    plt.scatter(list(range(0, iterations)), iterations_result)
    plt.xlabel('Iterations')
    plt.ylabel('Solution')
    plt.title(f'{in_file[-5:]} - SEED: {seed} - TIME: {current_time}')
    plt.show()

    return s

def main():
    random.seed(seed)
    graph = read_file(in_file)
    VNS(graph,out_file)

if __name__ == "__main__":
	main()



