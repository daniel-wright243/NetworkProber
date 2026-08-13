from queue import Queue

import graphviz
import networkx

INF = 2147483647
NIL = 0


class BiPartiteGraph:

    def __init__(self, U, V):
        self.U = U
        self.V = V
        self.edges = [[] for _ in range(U + 1)]

    def add_edge(self, U, V): # adds an edge to the bipartite graph
        if self.U >= U and self.V >= V:
            self.edges[U].append(V)
            return "Success"
        else:
            return "U or V not part of bipartite graph"

    def remove_edge(self, U, V): # removes an edge from the bipartite graph
        if U < len(self.edges):
            if V in self.edges[U]:
                self.edges[U].remove(V)
                return "Success"
            else:
                return "Edge does not exist"

    #hopcroft-karp algorithm from https://www.geeksforgeeks.org/hopcroft-karp-algorithm-for-maximum-matching-set-2-implementation/

    def bfs(self):
        Q = Queue()
        # First layer of vertices (set distance as 0)
        for u in range(1, self.U + 1):
            # If this is a free vertex, add it to queue
            if self.__pairU[u] == NIL:
                # u is not matched3
                self.__dist[u] = 0
                Q.put(u)
            # Else set distance as infinite so that this vertex
            # is considered next time
            else:
                self.__dist[u] = INF
        # Initialize distance to NIL as infinite
        self.__dist[NIL] = INF
        # Q is going to contain vertices of left side only.
        while not Q.empty():
            # Dequeue a vertex
            u = Q.get()
            # If this node is not NIL and can provide a shorter path to NIL
            if self.__dist[u] < self.__dist[NIL]:
                # Get all adjacent vertices of the dequeued vertex u
                for v in self.edges[u]:
                    #  If pair of v is not considered so far
                    # (v, pairV[V]) is not yet explored edge.
                    if self.__dist[self.__pairV[v]] == INF:
                        # Consider the pair and add it to queue
                        self.__dist[self.__pairV[v]] = self.__dist[u] + 1
                        Q.put(self.__pairV[v])
        # If we could come back to NIL using alternating path of distinct
        # vertices then there is an augmenting path
        return self.__dist[NIL] != INF

    # Returns true if there is an augmenting path beginning with free vertex u
    def dfs(self, u):
        if u != NIL:
            # Get all adjacent vertices of the dequeued vertex u
            for v in self.edges[u]:
                if self.__dist[self.__pairV[v]] == self.__dist[u] + 1:
                    # If dfs for pair of v also returns true
                    if self.dfs(self.__pairV[v]):
                        self.__pairV[v] = u
                        self.__pairU[u] = v
                        return True
            # If there is no augmenting path beginning with u.
            self.__dist[u] = INF
            return False
        return True

    def hopcroftkarp(self):
        # pairU[u] stores pair of u in matching where u
        # is a vertex on left side of Bipartite Graph.
        # If u doesn't have any pair, then pairU[u] is NIL
        self.__pairU = [0 for _ in range(self.U + 1)]

        # pairV[v] stores pair of v in matching. If v
        # doesn't have any pair, then pairU[v] is NIL
        self.__pairV = [0 for _ in range(self.V + 1)]

        # dist[u] stores distance of left side vertices
        # dist[u] is one more than dist[u'] if u is next
        # to u'in augmenting path
        self.__dist = [0 for _ in range(self.U + 1)]
        # Initialize result
        result = 0

        # Keep updating the result while there is an
        # augmenting path.
        while self.bfs():
            # Find a free vertex
            for u in range(1, self.U + 1):
                # If current vertex is free and there is
                # an augmenting path from current vertex
                if self.__pairU[u] == NIL and self.dfs(u):
                    result += 1
        return result

    def return_hk_matching(self): # grabs the pairing matchings that are generated after using the hopcroft-karp algorthim
        self.hopcroftkarp()
        # while 0 in self.__pairU:
        #     self.__pairU.remove(0)
        # while 0 in self.__pairV:
        #     self.__pairV.remove(0)
        return self.__pairU, self.__pairV

    def display_graph(self): # displays the bipartite graph using graphviz
        self.dot = graphviz.Digraph('BiPartiteGraph', comment='BiPartiteGraph')
        for i in range(self.U + self.V):
            if i != 0 and i != self.U:
                self.dot.node(str(i))
        for i in range(len(self.edges)):
            if len(self.edges[i]) != 0:
                for j in range(len(self.edges[i])):
                    self.dot.edge(str(i), str(self.edges[i][j] + self.U))
        self.dot.view()

    def create_graph_image(self):
        digraph_image = graphviz.Digraph('Images/BiPartiteGraph', comment='BiPartiteGraph')
        # print(self.U)
        # print(self.V)
        # print(self.edges)
        # for i in range(self.U + self.V):
        #     digraph_image.node(str(i+1))
        # for i in range(len(self.edges)):
        #     if len(self.edges[i]) != 0:
        #         for j in range(len(self.edges[i])):
        #             digraph_image.edge(str(i), str(self.edges[i][j] + self.U))
        for i in range(self.U + self.V):
            if i != 0 and i != self.U:
                digraph_image.node(str(i))
        for i in range(len(self.edges)):
            if len(self.edges[i]) != 0:
                for j in range(len(self.edges[i])):
                    digraph_image.edge(str(i), str(self.edges[i][j] + self.U))
        digraph_image.render('Images/BiPartiteGraphImage', format='png', view=False)

    def display_matching_graph(self):
        self.hopcroftkarp()

        self.matchingDot = graphviz.Digraph('Matching_BipartiteGraph', comment='Matching_BipartiteGraph')

        for i in range(len(self.__pairU)):
            U = i
            V = self.__pairU[i]

            if V != 0:
                self.matchingDot.node(str(i))
                self.matchingDot.node(str(V + self.U))
                self.matchingDot.edge(str(i), str(V + self.U))

        self.matchingDot.view()

        # while 0 in self.__pairU:
        #     self.__pairU.remove(0)
        # while 0 in self.__pairV:
        #     self.__pairV.remove(0)
        # self.matchingDot = graphviz.Digraph('Matching_BipartiteGraph', comment='Matching_BipartiteGraph')
        # for i in range(len(self.__pairU)):
        #     self.matchingDot.node(str(i+1))
        #     print("STR I + 1")
        #     print(str(i+1))
        #     if i+1+len(self.__pairU) != self.U:
        #         self.matchingDot.node(str(i+1+len(self.__pairU)))
        # for i in range(len(self.__pairU)):
        #     self.matchingDot.edge(str(self.__pairU[i]), str(self.__pairV[i] + 1 + len(self.__pairU)))
        # self.matchingDot.view()

    def create_matching_graph(self):
        self.hopcroftkarp()
        digraph_image = graphviz.Digraph('Images/HKMatchingGraph', comment='HKMatchingGraph')
        # while 0 in self.__pairU:
        #     self.__pairU.remove(0)
        # while 0 in self.__pairV:
        #     self.__pairV.remove(0)
        # print("SELF.__PAIRU")
        # print(self.__pairU)
        # print("SELF.__PAIRV")
        # print(self.__pairV)

        for i in range(len(self.__pairU)):
            U = i
            V = self.__pairU[i]

            if V != 0:
                digraph_image.node(str(i))
                digraph_image.node(str(V + self.U))
                digraph_image.edge(str(i), str(V + self.U))



        # for i in range(len(self.__pairU)):
        #     node_check = True
        #     if self.__pairU[i] == 0 and self.__pairV == 0:
        #         node_check = False
        #     else:
        #         node_check = True
        #     if node_check:
        #         digraph_image.node(str(self.__pairV[i]))
        #         digraph_image.node(str(self.__pairU[i] + self.U))
        #
        #         digraph_image.edge(str(self.__pairV[i]), str(self.__pairU[i] + self.U))


        # for i in range(len(self.__pairV)): # made vertices in matching graph
        #     digraph_image.node(str(self.__pairV[i]))
        #     digraph_image.node(str(self.__pairU[i] + self.U))
        # for i in range(len(self.__pairV)): # create edges in matching graph
        #     digraph_image.edge(str(self.__pairV[i]), str(self.__pairU[i] + self.U))
        digraph_image.render('Images/HKMatchingGraph', format='png', view=False)

    def check_perfect_matching(self):
        self.hopcroftkarp()
        while 0 in self.__pairU:
            self.__pairU.remove(0)
        while 0 in self.__pairV:
            self.__pairV.remove(0)
        if len(self.__pairU) == self.U and len(self.__pairV) == self.V:
            return True
        else:
            return False

    def get_connected_components(self):
        networkXGraph = networkx.Graph()
        # print("SELF.U")
        # print(self.U)
        # print("SELF.V")
        # print(self.V)
        # print("SELF.EDGES")
        # print(self.edges)
        edges_list = []
        for i in range(len(self.edges)):
            if len(self.edges[i]) > 0:
                for j in range(len(self.edges[i])):
                    edges_list.append([i, (self.U + self.edges[i][j])])
        #print(edges_list)
        networkXGraph = networkx.Graph()
        for i in range(self.U + self.V):
            if i != 0 and i != self.U:
                networkXGraph.add_node(i)
        for edge in edges_list:
            networkXGraph.add_edge(edge[0], edge[1])
        connected_components = networkx.connected_components(networkXGraph)
        #print("CONNECTED COMPONENTS")
        #for cc in connected_components:
            #print(cc)
        return connected_components
        #print(connected_components)
        #for vertex in self.vertices:
        #    networkXGraph.add_node(vertex)
        #for vertex in self.arcs:
        #    for arc in vertex:
        #        networkXGraph.add_edge(arc[0], arc[1])

