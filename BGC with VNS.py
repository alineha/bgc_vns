import time
import operator
import random
from input_output import *

SEED = 21938273
random.seed(SEED)
WEIGHT_WEIGHT = 0.5
CONFLICTS_WEIGHT = 1-WEIGHT_WEIGHT

class Solution():
    def __init__(self,colouring,graph):
        self.colouring = colouring
        self.colour_weights = {}
        for colour in range(0,graph.colours):
            self.colour_weights[colour] = 0
        for vertex,colour in colouring.items():
            self.colour_weights[colour]+=graph.vertexes[vertex].weight

    def evaluate(self,conflicts):
        return min(self.colour_weights)+conflicts*10000

    def modify_colour(self,vertex,weight,new_colour):
        old_colour = self.colouring[vertex]
        self.colouring[vertex] = new_colour
        self.colour_weights[old_colour]-=weight
        self.colour_weights[new_colour]+=weight

def welsh_powell(graph):
    colour = 0
    vertexes = sorted(graph.vertexes, key=operator.attrgetter("degree"), reverse=True)
    colouring = {}
    colouring[vertexes[0].index] = 0

    for colour in range(0,graph.colours):
        for v in vertexes:
            if v.index not in colouring:
                can_be_coloured = True
                for w in v.adj:
                    if (w in colouring) and (colour == colouring[w]):
                        can_be_coloured = False
                if can_be_coloured:
                    colouring[v.index] = colour

    for v in g.vertexes:
        if v.index not in colouring:
            c = v.check_conflicts(colouring,graph.colours)
            colouring[v.index] = min(zip(c, range(len(c))))[1]

    return Solution(colouring,graph)

def time_to_stop(time,iterations):
    return (time>=10800 or iterations > 1000)

def random_neighbour(graph,s,k):
    if k == 1:
        return random_no_conflicts_neighbor(graph,s)
    if k == 2:
        return random_grenade_neighbor(graph,s)
    if k == 3:
        return 2
    if k == 4:
        return 3

def no_conflicts_colour(k,s,vertex):
    conflicts_by_colour = vertex.check_colours(s.colouring,k)
    print(conflicts_by_colour)
    min_weight = float('inf')
    min_colour = -1
    for i in range(0,k-1):
        if(s.colour_weights[i]<min_weight and conflicts_by_colour[i]==0):
            min_weight = s.colour_weights[i]
            min_colour = i

    if(min_colour!=-1):
        return min_colour
    else:
        return -1

def random_no_conflicts_neighbor(graph,s):
    len_vertexes = len(graph.vertexes)-1
    iterations = 0
    new_colour = -1
    while(new_colour==-1 and iterations<len_vertexes):
        vertex = graph.vertexes[random.randrange(0,len_vertexes)]
        new_colour = no_conflicts_colour(graph.colours,s,vertex)
        iterations+=1

    if new_colour==-1:
        return -1
    else:
        new_solution = copy.deepcopy(s)
        new_solution.modify_colour(vertex.index, vertex.weight, new_colour)
        return new_solution
        
def best_colour(graph,s,vertex):
    values = {}
    conflicts_by_colour = vertex.check_colours(s.colouring,graph.colours,True)

    for i in range(0,graph.colours-1):
        values[i] = WEIGHT_WEIGHT*s.colour_weights[i]+CONFLICTS_WEIGHT*conflicts_by_colour[i][0]

    new_colour = min(values, key=values.get)

    return new_colour,conflicts_by_colour[new_colour][1]

def grenade(graph,s,vertex):
    new_s = copy.deepcopy(s)
    new_colour,conflicts=best_colour(graph,s,vertex)
    new_s.modify_colour(vertex.index, vertex.weight, new_colour)
    
    for w in conflicts:
        w_best_colour = best_colour(graph,new_s,graph.vertexes[w])[0]
        new_s.modify_colour(w, graph.vertexes[w].weight, w_best_colour)
    
    return new_s


def random_grenade_neighbor(graph,s):
    len_vertexes = len(graph.vertexes)-1
    iterations = 0
    vertex = graph.vertexes[random.randrange(0,len_vertexes)]
    return grenade(graph,s,vertex)

# TO-DO
def local_search(k,solution,graph):
    i = 0

def VNS(graph):
    start_time = time.time()
    s = welsh_powell(graph)
    iterations = 0
    while not time_to_stop(time.time()-start_time,iterations):
        k = 1
        while k<=4:
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
    return s

g = read_file("\\instances\\cmb01")
VNS(g)


