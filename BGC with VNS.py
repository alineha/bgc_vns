import time
import operator

class Vertex():
    index = -1
    weight = 0.0
    adj = set()
    color = False

    @property 
    def colored(self):
        if self.color == False:
            return False
        else:
            return True
    
    @property
    def degree(self):
        return len(self.adj)

    def __init__(self,index,weight):
        self.index = index
        self.weight = weight
        self.adj = set()
        self.color = False

    def add_edge(self,adjacent_node):
        self.adj.add(adjacent_node)

    def is_adjacent_to(self,node):
        return (node.index in self.adj)

    def is_adjacent_to_index(self,index):
        return (index in self.adj)

    def check_colors(self,G):
        colors = [0]*G.colors
        for v in self.adj:
            colors[G.vertexes[v].color]+=1
        return colors

    def __str__(self):
        return (f'VERTEX {self.index}\nWeight: {self.weight}\nColor: {self.color}\n')


class Graph():
    vertexes = []
    colors = 0
    numEdges = 0
    edges = []
    
    def __init__(self,weights,edges,colors):
        self.colors = colors
        i=0
        for weight in weights:
            self.vertexes.append(Vertex(i, weight))
            i+=1
        self.edges = edges
        for edge in edges:
            self.vertexes[edge[0]].add_edge(edge[1])
            self.vertexes[edge[1]].add_edge(edge[0])

    def are_connected(self,index1,index2):
        return self.vertexes[index1].is_adjacent_to(index2)

    def number_of_conflicts(self):
        n = 0
        for e in self.edges:
            if self.vertexes[e[0]].color == self.vertexes[e[1]].color:
                n+=1
        return n

    def __str__(self):
        string = f'Colors: {self.colors}\nVertexes: {len(self.vertexes)}\nEdges: {len(self.edges)}\n---------\n'
        for v in self.vertexes:
            string+=str(v)
            string+='\n'
        return string

def welshPowell(G):
    color = 0
    vertexes = sorted(G.vertexes, key=operator.attrgetter("degree"), reverse=True)
    coloring = {}

    vertexes[0].color = 0
    coloring[vertexes[0].index] = 0

    for color in range(0,G.colors):
        for v in vertexes:
            if not v.colored:
                canBeColored = True
                for w in v.adj:
                    if color == g.vertexes[w].color:
                        canBeColored = False
                if canBeColored:
                    v.color = color

    for v in g.vertexes:
        if not v.colored:
            c = v.check_colors(G)
            v.color = min(zip(c, range(len(c))))[1]

def readFile(filepath):
    weights = []
    edges = []
    file = open(filepath, "r")
    line = file.readline().strip().split(" ")
    numVertexes = int(line[0])
    numEdges = int(line[1])
    numColors = int(line[2])

    line = file.readline().strip().split(" ")
    i = 0
    while i < numVertexes:
        weights.append(float(line[i]))
        i+=1

    i = 0
    while i < numEdges:
        line = file.readline().strip().split(" ")
        edges.append([int(line[0]),int(line[1])])
        i+=1

    file.close()

    return Graph(weights,edges,numColors)

g = readFile("/instances/cmb01")
welshPowell(g)
print(g.number_of_conflicts())


