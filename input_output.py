from graph import *
import os

def get_input(args):
    if not os.path.isfile(args[2]):   
        print("File not found: %s" % args[2])
        exit(1)
    
    out_file = args[1]
    in_file = args[2]

    try:
        SEED = int(args[3])
        CONFLICT_WEIGHT = int(args[4])
        MAX_ITERATIONS = int(args[5])
        MAX_TIME = int(args[6])
        PARTITIONS = int(args[7])
    except TypeError:
        print("Wrong argument types, use: [Output file name] [Input file name] [Seed] [Conflict weight] [Max # iterations] [Max time (seconds)] [# of partitions]")
        exit(1)

    return out_file,in_file,SEED,CONFLICT_WEIGHT,MAX_ITERATIONS,MAX_TIME,PARTITIONS


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