from graph import *

def read_file(filepath):
    weights = []
    edges = []
    file = open(filepath, "r")
    line = file.readline().strip().split(" ")
    num_vertexes = int(line[0])
    num_edges = int(line[1])
    num_colours = int(line[2])

    line = file.readline().strip().split(" ")
    i = 0
    while i < num_vertexes:
        weights.append(float(line[i]))
        i+=1

    i = 0
    while i < num_edges:
        line = file.readline().strip().split(" ")
        edges.append([int(line[0]),int(line[1])])
        i+=1

    file.close()

    return Graph(weights,edges,num_colours)