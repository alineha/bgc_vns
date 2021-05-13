import copy

class Vertex():
    def __init__(self,index,weight):
        self.index = index
        self.weight = weight
        self.adj = set()

    @property
    def degree(self):
        return len(self.adj)

    def add_edge(self,adjacent_node):
        self.adj.add(adjacent_node)

    def is_adjacent_to(self,node):
        return (node.index in self.adj)

    def is_adjacent_to_index(self,index):
        return (index in self.adj)

    def check_conflicts(self,colouring,k):
        colours = [0]*k
        conflicts = []
        for v in self.adj:
            if v in colouring:
                colours[colouring[v]]+=1
        return colours

    def check_total_conflicts(self,colouring,get_list_of_conflicts=False):
        num_conflicts = 0
        conflicts = []
        for v in self.adj:
            if v in colouring:
                num_conflicts+=1
                if(get_list_of_conflicts):
                    conflicts.append(v)
        if get_list_of_conflicts:
            return num_conflicts,conflicts
        return num_conflicts

    def check_colours(self,colouring,k,get_list_of_conflicts=False):
        colour_conflicts = {}
        colouring_copy = copy.deepcopy(colouring)
        for i in range(0,k-1):
            colouring_copy[self.index] = i
            colour_conflicts[i] = self.check_total_conflicts(colouring_copy,k,get_list_of_conflicts)
        return colour_conflicts

    def __str__(self):
        return (f'VERTEX {self.index}\nWeight: {self.weight}\ncolour: {self.colour}\n')


class Graph():
    def __init__(self,weights,edges,colours):
        self.colours = colours
        self.vertexes = []
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

    def number_of_conflicts(self,colouring):
        n = 0
        for e in self.edges:
            if colouring[e[0]] == colouring[e[1]]:
                n+=1
        return n

    def __str__(self):
        string = f'colours: {self.colours}\nVertexes: {len(self.vertexes)}\nEdges: {len(self.edges)}\n---------\n'
        for v in self.vertexes:
            string+=str(v)
            string+='\n'
        return string