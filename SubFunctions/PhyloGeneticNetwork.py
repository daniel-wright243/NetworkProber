# import other subfunctions
import random

import matplotlib
import matplotlib.pyplot
import networkx as nx

from SubFunctions.BiPartiteGraph import BiPartiteGraph
from SubFunctions.SoftlyTreeBasedFunction import SoftlyTreeBasedAlgorithm

#for showing the network in image form
import graphviz
import os
import pathlib

os.environ["PATH"] += os.pathsep + str(pathlib.Path(__file__).parent.parent.resolve()) + '/venv/Lib/site-packages/graphviz/Graphviz/bin'


#for copying classes
from copy import deepcopy

#use networkx for getting all paths in a network
import networkx

#################################################################
#
# Phylogenetic Network Class
#
# Inputs:
#   Takes in vertices as an array of all vertices eg: [1,2,3,4,5,6,7,8]
#   Takes in array of arcs between vertices eg: [[1,2],[1,3]]
#   Takes in root of the network to base network off of
#
#################################################################


class PhylogeneticNetwork:

    def __init__(self, vertices, arcs, root, taxDict={}):
        self.vertices = vertices
        self.arcs = [[] for _ in range(5000)]
        for arc in self.arcs:
            arc = []
        for i in range(len(arcs)):
            self.arcs[arcs[i][0]].append(arcs[i])
        if root not in self.vertices:
            raise Exception("Root not in vertices list")
        else:
            self.root = root
        self.all_path_array = []
        self.reverseArcs = [[] for _ in range(5000)]
        for vertex in self.arcs:
            if len(vertex) > 0:
                for arc in vertex:
                    reversed_arc = [arc[1], arc[0]]
                    self.reverseArcs[reversed_arc[0]].append(reversed_arc)
        self.taxDict = taxDict
        self.leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                self.leafs.append(i)
            # if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) == 0:
            #     if i in self.vertices:
            #         self.vertices.remove(i)
        self.oldRoot = 1



    # creates an arc between two vertices in the phylogenetic network
    def createArc(self, arc):
        if arc not in self.arcs[arc[0]]:
            self.arcs[arc[0]].append(arc)
            reversed_arc = [arc[1], arc[0]]
            self.reverseArcs[arc[1]].append(reversed_arc)
            return "Success"
        else:
            return "Arc already exists"

    # creates a vertex in the phylogenetic network
    def createVertex(self, vertex):
        if type(vertex) == int:
            if vertex not in self.vertices:
                self.vertices.append(vertex)
                #for i in range(len(self.arcs), vertex):
                #    self.arcs.append([])
                #    self.reverseArcs.append([])
                return "Success"
            else:
                return "Vertex already exists in network"
        else:
            return "Vertex array size must be 1"

    # removes an arc from the phylogenetic network
    def removeArc(self, arc): # removes an arc from the phylogenetic network
        if type(arc) == list:
            if arc in self.arcs[arc[0]]:
                self.arcs[arc[0]].remove(arc)
                reversed_arc = [arc[1], arc[0]]
                self.reverseArcs[arc[1]].remove(reversed_arc)
                return "Success"
            else:
                return "Arc does not exist"
        else:
            return "Arc size invalid"

    # gets all paths in the network
    def getAllPaths(self): # gets all node paths in the phylogenetic network
        # make networkx graph
        networkXGraph = networkx.DiGraph()
        for vertex in self.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])
        # find leaves in the network
        leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        path_list = []
        for leaf in leafs:
            networkx_path_list = networkx.all_simple_paths(networkXGraph, self.root, leaf)
            for path in networkx_path_list:
                path_list.append(path)
        return path_list

    def checkCyclicity(self): # checks for cyclicity in the phylogenetic network (used to check treebasedness)
        networkXGraph = networkx.Graph()
        for vertex in self.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])
        cycles = networkx.cycle_basis(networkXGraph, self.root)
        if len(cycles) > 0:
            return True
        else:
            return False

    def makeBiPartiteGraph(self, vertices_to_not_include=[]): # finds reticulation and tree vertices and makes a bipartite graph using them
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = [0]
        reticulation_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in self.arcs[i]:
                #     if arc[1] in self.leafs:
                #         leaf_below = True
                #         break
                # if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)

        self.tree_vertex_array = tree_vertex_array
        self.reticulation_vertex_array = reticulation_vertex_array

        self.connected_tree_vertices = [0]
        self.connected_reticulation_vertices = [0]
        connected_edge_list = []

        for i in range(len(tree_vertex_array)):
            for j in range(len(reticulation_vertex_array)):
                if [tree_vertex_array[i], reticulation_vertex_array[j]] in self.arcs[tree_vertex_array[i]]:
                    if tree_vertex_array[i] not in self.connected_tree_vertices:
                        self.connected_tree_vertices.append(tree_vertex_array[i])
                    if reticulation_vertex_array[j] not in self.connected_reticulation_vertices:
                        self.connected_reticulation_vertices.append(reticulation_vertex_array[j])

        # print("CONNECTED TREE VERTICES")
        # print(self.connected_tree_vertices)

        for i in range(len(self.connected_tree_vertices)):
            if i != 0:
                for j in range(len(self.connected_reticulation_vertices)):
                    if j != 0:
                        if [self.connected_tree_vertices[i], self.connected_reticulation_vertices[j]] in self.arcs[self.connected_tree_vertices[i]]:
                            connected_edge_list.append([i, j])

        # print("CONNECTED EDGE LIST")
        # print(connected_edge_list)
        #
        # print("BIPARTITE GRAPH PARAMETERS")
        # print([len(self.connected_tree_vertices) - 1, len(self.connected_reticulation_vertices) - 1])


        tempBipGraph = BiPartiteGraph(len(self.connected_tree_vertices) - 1, len(self.connected_reticulation_vertices) - 1)

        for edge in connected_edge_list:
            # print("EDGE")
            # print([edge[0], edge[1]])
            tempBipGraph.addEdge(edge[0], edge[1])

        return tempBipGraph

    def displayGraph(self): # uses graphviz to display the phylogenetic network
        self.dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        for i in self.vertices:
            self.dot.node(str(i))
        for vertex in self.arcs:
            for arc in vertex:
                self.dot.edge(str(arc[0]), str(arc[1]))
        self.dot.view()

    def displayGraphNoInteriorVertices(self):
        self.dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        for i in self.vertices:
            if i in leafs:
                self.dot.node(str(i))
            else:
                self.dot.node(str(i), label='')
        for vertex in self.arcs:
            for arc in vertex:
                self.dot.edge(str(arc[0]), str(arc[1]))
        self.dot.view()

    def createGraphImage(self):
        digraph_image = graphviz.Digraph('Images/Phylogenetic Network', comment='Phylogenetic Network')
        # digraph_image.attr(rankdir="LR")
        digraph_image.attr(labelloc="b")
        # print("SELF>VERTICES")
        # print(self.vertices)
        leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in self.vertices:
            if vertex in leafs:
                if vertex in self.taxDict:
                    digraph_image.node(str(vertex), shape="point", xlabel=self.taxDict[vertex], labelloc="b")
                else:
                    digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
            else:
                digraph_image.node(str(vertex), label='', shape="point")
        for vertex in self.arcs:
            for arc in vertex:
                digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
        digraph_image.render('Images/PhylogeneticNetworkImage', format='png', view=False)

    def applyMatchingToGraph(self, matchingGraph, vertices_removed=[]): # applies the inputted Bipartite Matching graph's matching to the phylogenetic network
        """

        :type matchingGraph: BiPartiteGraph
        """
        if type(matchingGraph) == BiPartiteGraph:
            edge_list = []
            # for i in range(len(matchingGraph.edges)): # get list of edges in Bip Graph
            #     if len(matchingGraph.edges[i]) > 0:
            #         print(matchingGraph.edges[i])
            #         edge_list.append([i, (matchingGraph.edges[i][0] + matchingGraph.U)])
            # pairU, pairV = matchingGraph.returnHKMatching()
            # edges_to_be_kept = []
            # for i in range(len(pairU)): # get list of edges in Bip Graph Matching
            #     edges_to_be_kept.append([self.tree_vertex_array[pairV[i] - 1], self.reticulation_vertex_array[pairU[i] - 1]])
            # bipartite_graph_edges = []
            # for i in range(len(matchingGraph.edges)):
            #     if len(matchingGraph.edges[i]) > 0:
            #         for j in range(len(matchingGraph.edges[i])):
            #             bipartite_graph_edges.append([self.tree_vertex_array[i - 1], self.reticulation_vertex_array[matchingGraph.edges[i][j] - 1]])
            #             print(matchingGraph.edges[i][j])
            # reverseArcsToBeRemoved = []
            # for i in range(len(bipartite_graph_edges)):
            #     edge = bipartite_graph_edges[i]
            #     if edge not in edges_to_be_kept:
            #         self.removeArc(edge)


            pairU, pairV = matchingGraph.returnHKMatching()

            for i in range(len(pairV)):
                if pairV[i] != 0:
                    edge_list.append([pairV[i], i])

            vertex_in_degree = [0] * (max(self.vertices) + 1)
            vertex_out_degree = [0] * (max(self.vertices) + 1)

            for vertex in self.arcs:
                if len(vertex) > 0:
                    for arcs in vertex:
                        if arcs[0] in self.vertices:
                            vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                        if arcs[1] in self.vertices:
                            vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

            reticulation_vertices = []
            tree_vertices = []

            for i in range(len(vertex_in_degree)):
                if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                    reticulation_vertices.append(i)
                elif vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                    tree_vertices.append(i)

            connected_tree_vertices = []
            connected_reticulation_vertices = []

            for tree_vertex in tree_vertices:
                for reticulation_vertex in reticulation_vertices:
                    if [tree_vertex, reticulation_vertex] in self.arcs[tree_vertex]:
                        if tree_vertex not in connected_tree_vertices:
                            connected_tree_vertices.append(tree_vertex)
                        if reticulation_vertex not in connected_reticulation_vertices:
                            connected_reticulation_vertices.append(reticulation_vertex)

            converted_edge_list = []

            for edge in edge_list:
                converted_edge_list.append([connected_tree_vertices[edge[0]-1], connected_reticulation_vertices[edge[1]-1]])

            # print("CONVERTED EDGE LIST")
            # print(converted_edge_list)

            for arc in converted_edge_list:
                self.removeArc(arc)

        else:
            return "Invalid matching graph class type"

    def applyOppositeMatchingToGraph(self, matchingGraph, vertices_removed=[]):
        self.getTreeAndReticulationVertexArray(True)
        if type(matchingGraph) == BiPartiteGraph:
            pairU, pairV = matchingGraph.returnHKMatching()
            edges_to_be_removed = []

            pairU, pairV = matchingGraph.returnHKMatching()

            # for i in range(len(pairV)):
            #     if pairV[i] != 0:
            #         edges_to_be_removed.append([pairV[i], i])

            tree_vertices = self.connected_tree_vertices
            reticulation_vertices = self.connected_reticulation_vertices

            tree_vertices.remove(0)
            reticulation_vertices.remove(0)

            while 0 in pairU:
                pairU.remove(0)
            while 0 in pairV:
                pairV.remove(0)
            for i in range(len(pairU)):
                print(str(pairV[i] - 1) + ", " + str(pairU[i] - 1))
                edges_to_be_removed.append([tree_vertices[pairU[i] - 1], reticulation_vertices[pairV[i] - 1]])
            print("EDGES TO BE REMOVED")
            print(edges_to_be_removed)
            for edge in edges_to_be_removed:
                self.removeArc(edge)
        else:
            return "Invalid matching graph class type"

    def applyOppositeMatchingToGraph2(self, matchingGraph):
        if type(matchingGraph) == BiPartiteGraph:
            edge_list = []
            # for i in range(len(matchingGraph.edges)): # get list of edges in Bip Graph
            #     if len(matchingGraph.edges[i]) > 0:
            #         print(matchingGraph.edges[i])
            #         edge_list.append([i, (matchingGraph.edges[i][0] + matchingGraph.U)])
            # pairU, pairV = matchingGraph.returnHKMatching()
            # edges_to_be_kept = []
            # for i in range(len(pairU)): # get list of edges in Bip Graph Matching
            #     edges_to_be_kept.append([self.tree_vertex_array[pairV[i] - 1], self.reticulation_vertex_array[pairU[i] - 1]])
            # bipartite_graph_edges = []
            # for i in range(len(matchingGraph.edges)):
            #     if len(matchingGraph.edges[i]) > 0:
            #         for j in range(len(matchingGraph.edges[i])):
            #             bipartite_graph_edges.append([self.tree_vertex_array[i - 1], self.reticulation_vertex_array[matchingGraph.edges[i][j] - 1]])
            #             print(matchingGraph.edges[i][j])
            # reverseArcsToBeRemoved = []
            # for i in range(len(bipartite_graph_edges)):
            #     edge = bipartite_graph_edges[i]
            #     if edge not in edges_to_be_kept:
            #         self.removeArc(edge)


            pairU, pairV = matchingGraph.returnHKMatching()

            for i in range(len(pairV)):
                if pairV[i] != 0:
                    edge_list.append([pairV[i], i])

            vertex_in_degree = [0] * (max(self.vertices) + 1)
            vertex_out_degree = [0] * (max(self.vertices) + 1)

            for vertex in self.arcs:
                if len(vertex) > 0:
                    for arcs in vertex:
                        if arcs[0] in self.vertices:
                            vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                        if arcs[1] in self.vertices:
                            vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

            reticulation_vertices = []
            tree_vertices = []

            for i in range(len(vertex_in_degree)):
                if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                    reticulation_vertices.append(i)
                elif vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                    tree_vertices.append(i)

            connected_tree_vertices = []
            connected_reticulation_vertices = []

            for tree_vertex in tree_vertices:
                for reticulation_vertex in reticulation_vertices:
                    if [tree_vertex, reticulation_vertex] in self.arcs[tree_vertex]:
                        if tree_vertex not in connected_tree_vertices:
                            connected_tree_vertices.append(tree_vertex)
                        if reticulation_vertex not in connected_reticulation_vertices:
                            connected_reticulation_vertices.append(reticulation_vertex)

            converted_edge_list = []

            for edge in edge_list:
                converted_edge_list.append([connected_tree_vertices[edge[0]-1], connected_reticulation_vertices[edge[1]-1]])

            # print("CONVERTED EDGE LIST")
            # print(converted_edge_list)

            for arc in converted_edge_list:
                self.removeArc(arc)

        else:
            return "Invalid matching graph class type"

    def getTreeAndReticulationVertexArray(self, all_vertices):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        self.tree_vertex_array = []
        self.reticulation_vertex_array = []
        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                self.tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                self.reticulation_vertex_array.append(i)

        # remove any tree vertices that don't have any reticulation vertices in their arc list
        if not all_vertices:
            for vertex in self.tree_vertex_array:
                reticulation_vertex_check = False
                for arc in self.arcs[vertex]:
                    if arc[1] in self.reticulation_vertex_array:
                        reticulation_vertex_check = True
                        break
                if not reticulation_vertex_check:
                   self.tree_vertex_array.remove(vertex)

        return self.tree_vertex_array, self.reticulation_vertex_array

    # def simplifyNetwork(self):
    #     simplifiedNetwork = deepcopy(self)
    #     vertex_in_degree = [0] * (len(self.vertices) + 1)
    #     vertex_out_degree = [0] * (len(self.vertices) + 1)
    #     for vertex_arcs in self.arcs:
    #         for arcs in vertex_arcs:
    #             vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
    #             vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1
    #
    #     for i in range(len(vertex_in_degree)):
    #         if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 1:
    #             #get vertex above current vertex
    #             vertex_above = simplifiedNetwork.reverseArcs[i][0][1]
    #             vertex_below = simplifiedNetwork.arcs[i][0][1]
    #             #removing edge from vertex above to i
    #             simplifiedNetwork.removeArc([vertex_above, i])
    #             #removing edge from i to vertex below
    #             simplifiedNetwork.removeArc([i, vertex_below])
    #             #creating arc from vertex above to vertex below
    #             simplifiedNetwork.createArc([vertex_above, vertex_below])
    #             #remove vertex i
    #             simplifiedNetwork.vertices.remove(i)
    #     return simplifiedNetwork

    def simplifyNetwork(self):
        simplifiedNetwork = deepcopy(self)
        vertex_in_degree = [0] * (max(self.vertices) + 2)
        vertex_out_degree = [0] * (max(self.vertices) + 2)

        for vertex_arcs in self.arcs:
            for arcs in vertex_arcs:
                vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 1:
                # get vertex above current vertex
                vertex_above = simplifiedNetwork.reverseArcs[i][0][1]
                vertex_below = simplifiedNetwork.arcs[i][0][1]
                #removing edge from vertex above to i
                simplifiedNetwork.removeArc([vertex_above, i])
                #removing edge from i to vertex below
                simplifiedNetwork.removeArc([i, vertex_below])
                #creating arc from vertex above to vertex below
                simplifiedNetwork.createArc([vertex_above, vertex_below])
                #remove vertex i
                if i in simplifiedNetwork.vertices:
                    simplifiedNetwork.vertices.remove(i)

        return simplifiedNetwork


    def getVerticesBelowVertex(self, original_split_vertex, split_vertex, vertex_array=[]):
        for arc in self.arcs[split_vertex]:
            vertex_array.append(arc[1])
            self.getVerticesBelowVertex(original_split_vertex, arc[1],  vertex_array)
        fixed_vertex_array = []
        for vertex in vertex_array:
            if vertex not in fixed_vertex_array:
                fixed_vertex_array.append(vertex)
        return fixed_vertex_array

    def getVerticesAboveVertex(self, original_split_vertex, split_vertex, vertex_array=[]):
        for arc in self.reverseArcs[split_vertex]:
            vertex_array.append(arc[1])
            self.getVerticesAboveVertex(original_split_vertex, arc[1], vertex_array)
        fixed_vertex_array = []
        for vertex in vertex_array:
            if vertex not in fixed_vertex_array:
                fixed_vertex_array.append(vertex)
        return fixed_vertex_array

    def getNetworkBelowVertex(self, vertex):
        vertices_below_vertex = self.getVerticesBelowVertex(vertex, vertex)
        vertex_list = deepcopy(vertices_below_vertex)
        vertex_list.append(vertex)
        arcList = []
        for vertex_below in vertex_list:
            for arc in self.arcs[vertex_below]:
                arcList.append(arc)
        return PhylogeneticNetwork(vertex_list, arcList, vertex)

    def getNetworkBelowVertexNetworkX(self, input_vertex):
        networkXGraph = networkx.DiGraph()
        for vertex in self.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.arcs:
            if type(vertex) == list:
                for arc in vertex:
                    networkXGraph.add_edge(arc[0], arc[1])
            else:
                networkXGraph.add_edge(vertex[0], vertex[1])
        vertices_below = networkx.descendants(networkXGraph, input_vertex)
        vertex_list = []
        arcList = []
        temp_tax_dict = {}

        vertex_list.append(input_vertex)

        for arc in self.arcs[input_vertex]:
            arcList.append(arc)

        for vertex in vertices_below:
            vertex_list.append(vertex)
            for arc in self.arcs[vertex]:
                arcList.append(arc)
            if vertex in self.taxDict.keys():
                temp_tax_dict[vertex] = self.taxDict.get(vertex)

        return PhylogeneticNetwork(vertex_list, arcList, input_vertex, temp_tax_dict)

    def getAllLeafs(self):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        return leaf_vertex_array

    def getAllLeafsInDegreeIndependant(self):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] >= 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        return leaf_vertex_array

    def getNetworkAboveVertex(self, vertex):
        vertices_above_vertex = self.getVerticesAboveVertex(vertex, vertex)
        vertex_list = deepcopy(vertices_above_vertex)
        vertex_list.append(vertex)
        arcList = []
        for vertex_above in vertices_above_vertex:
            for arc in self.arcs[vertex_above]:
                arcList.append(arc)
                if arc[1] not in vertex_list:
                    print(arc[1])
                    vertex_list.append(arc[1])
        return PhylogeneticNetwork(vertex_list, arcList, vertex)

    def addVertexOnEdge(self, vertex_num, edge):
        #add new vertex
        self.createVertex(vertex_num)
        # print("CREATE VERTEX ON EDGE")
        # print(vertex_num)
        #remove edge
        self.removeArc([edge[0], edge[1]])
        #add new edge from edge[0] to vertex_num
        self.createArc([edge[0], vertex_num])
        #add new edge from vertex_num to edge[1]
        self.createArc([vertex_num, edge[1]])

    def getCyclebasis(self):
        networkXGraph = networkx.Graph()
        for vertex in self.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])
        cycles = networkx.cycle_basis(networkXGraph, self.root)
        return cycles

    def checkDoubleRoT(self):
        tree_array, reticulation_array = self.getTreeAndReticulationVertexArray(False)
        for tree_vertex in tree_array:
            arcs_below = self.arcs[tree_vertex]
            for arcs in arcs_below:
                if arcs[1] in tree_array:
                    return True
        for reticulation_vertex in reticulation_array:
            arcs_below = self.arcs[reticulation_vertex]
            for arcs in arcs_below:
                if arcs[1] in reticulation_array:
                    return True
        return False

    def getConnectedComponentOfGraphFromBPGraph(self):
        BPGraph = self.makeBiPartiteGraph()
        #BPGraph.displayGraph()
        #REMOVE VERTICES THAT HAVE TO EDGES
        # print("BPGRAPH U")
        # print(BPGraph.U)
        # print("BPGRAPH V")
        # print(BPGraph.V)
        # print("BPGRAPH EDGES")
        # print(BPGraph.edges)

        #GRAB CONNECTED COMPONENTS OF BP GRAPH
        connected_components = BPGraph.getConnectedComponents()
        # print(connected_components)
        #CONVERT CC TO ACTUAL VERTEX INDEX
        #tv, rv = self.getTreeAndReticulationVertexArray(False)

        resolved_comps = []

        for component in connected_components:
            temp_comp = []
            for vertex in component:
                if vertex > BPGraph.U:
                    temp_comp.append(self.connected_reticulation_vertices[vertex - BPGraph.U])
                else:
                    temp_comp.append(self.connected_tree_vertices[vertex])
            if temp_comp not in resolved_comps:
                resolved_comps.append(temp_comp)

        # print("RESOLVED COMPS")
        # print(resolved_comps)

        return resolved_comps

    def makeBipartiteGraphNoLeafs(self):
        # vertex_in_degree = [[] for _ in range(max(self.vertices))]
        # vertex_out_degree = [[] for _ in range(max(self.vertices))]
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)
        # print("MAX SELF VERTICES")
        # print(max(self.vertices))
        # print("vertices list")
        # print(self.vertices)
        for vertex_arcs in self.arcs:
            # print("Vertex Arc")
            # print(vertex_arcs)
            if len(vertex_arcs) > 0:
                for arcs in vertex_arcs:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    # print(vertex_out_degree[arcs[0]])
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        self.tree_vertex_array = []
        self.reticulation_vertex_array = []
        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 2:
                self.tree_vertex_array.append(i)
            if vertex_in_degree[i] == 2 and vertex_out_degree[i] == 1:
                self.reticulation_vertex_array.append(i)

        # remove any tree vertices that don't have any reticulation vertices in their arc list
        for vertex in self.tree_vertex_array:
            reticulation_vertex_check = False
            for arc in self.arcs[vertex]:
                if arc[1] in self.reticulation_vertex_array:
                    reticulation_vertex_check = True
                    break
            if not reticulation_vertex_check:
                self.tree_vertex_array.remove(vertex)
            for arc in self.arcs[vertex]:
                if vertex_out_degree[arc[1]] == 0:
                    self.tree_vertex_array.remove(vertex)

        tempBipGraph = BiPartiteGraph(len(self.tree_vertex_array), len(self.reticulation_vertex_array))

        for i in range(len(self.tree_vertex_array)):
            for arc in self.arcs[self.tree_vertex_array[i]]:
                for j in range(len(self.reticulation_vertex_array)):
                    if self.reticulation_vertex_array[j] == arc[1]:
                        tempBipGraph.addEdge(i + 1, j + 1)
        return tempBipGraph

    def getAllOmnians(self):

        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = [0]
        reticulation_vertex_array = []
        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in self.arcs[i]:
                    if arc[1] in self.leafs:
                        leaf_below = True
                        break
                if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        omnian_list = []

        # print("RETICULATION_VERTEX_ARRAy")
        # print(reticulation_vertex_array)

        for i in range(len(self.arcs)):
            if len(self.arcs[i]) > 0:
                omnian_check = True

                for arc in self.arcs[i]:
                    if arc[1] not in reticulation_vertex_array:
                        omnian_check = False

                if omnian_check:
                    omnian_list.append(i)

        return omnian_list



    def checkTreeBasedOmnian(self):
        #self.displayGraph()
        bp = self.makeOmnianBipartiteGraph()
        omnian_vertices = self.getAllOmnians()
        bp.hopcroftKarp()
        # bp.displayGraph()
        #bp.displayGraph()
        #bp.displayMatchingGraph()
        matching = bp.returnHKMatching()
        # print("HKMatching")
        # print(matching)

        HKOmnianVertices = matching[0]
        HKReticulationVertices = matching[1]

        # print("TREEVERTICES")
        # print(TreeVertices)
        # print("RETICULATIONVERTICES")
        # print(ReticulationVertices)
        #
        # print("SELF.TREEVERTICES")
        # print(self.connected_tree_vertices)
        # print("SELF.RETICULATIONVERTICES")
        # print(self.connected_reticulation_vertices)

        matchedOmnianVertices = []
        matchedReticulationVertices = []

        # for rt_vertex in HKReticulationVertices:
        #     print("RT VERTEX")
        #     print(rt_vertex)
        #     matchedReticulationVertices.append(self.omnian_rv[rt_vertex - 1])
        #
        # for t_vertex in HKOmnianVertices:
        #     print("T_VERTEX")
        #     print(t_vertex)
        #     matchedOmnianVertices.append(self.omnian_list[t_vertex - 1])

        # print("MATCHEDRETICULATIONVERTICES")
        # print(matchedReticulationVertices)
        #
        # print("matchedOmnianVertices")
        # print(matchedOmnianVertices)
        #
        # print("OMNIAN VERTICES")
        # print(omnian_vertices)

        if len(omnian_vertices) == len(HKOmnianVertices):
            tree_based = True
        else:
            tree_based = False

        return tree_based

    def makeOmnianBipartiteGraph(self):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = [0]
        reticulation_vertex_array = []
        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in self.arcs[i]:
                    if arc[1] in self.leafs:
                        leaf_below = True
                        break
                if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        omnian_list = [0]
        omnian_arcs = []
        omnian_rv = [0]

        # print("RETICULATION_VERTEX_ARRAy")
        # print(reticulation_vertex_array)

        for i in range(len(self.arcs)):
            if len(self.arcs[i]) > 0:
                omnian_check = True
                connected_rv = []

                for arc in self.arcs[i]:
                    if arc[1] not in reticulation_vertex_array:
                        omnian_check = False
                    else:
                        connected_rv.append(arc[1])

                if omnian_check:
                    omnian_list.append(i)
                    for rv in connected_rv:
                        if rv not in omnian_rv:
                            omnian_rv.append(rv)
                        omnian_arcs.append([i, rv])

        # print("OMNIAN LIST")
        # print(omnian_list)
        # print("omnian_rv")
        # print(omnian_rv)

        temp_bip_graph = BiPartiteGraph(len(omnian_list) - 1, len(omnian_rv) - 1)

        for edge in omnian_arcs:
            temp_bip_graph.addEdge(omnian_list.index(edge[0]), omnian_rv.index(edge[1]))

        self.omnian_list = omnian_list
        self.omnian_rv = omnian_rv

        return temp_bip_graph

    def makeOmnianBipartiteGraph2(self):
        omnian_list = self.getAllOmnians()

        omnian_list = [0] + omnian_list

        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = []
        reticulation_vertex_array = []
        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in self.arcs[i]:
                    if arc[1] in self.leafs:
                        leaf_below = True
                        break
                if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        connected_omnian_vertices = [0]
        connected_reticulation_vertices = [0]
        connected_omnian_arcs = []

        for i in range(len(omnian_list)):
            for j in range(len(reticulation_vertex_array)):
                if [omnian_list[i], reticulation_vertex_array[j]] in self.arcs[omnian_list[i]]:
                    if omnian_list[i] not in connected_omnian_vertices:
                        connected_omnian_vertices.append(omnian_list[i])
                    if reticulation_vertex_array[j] not in connected_reticulation_vertices:
                        connected_reticulation_vertices.append(reticulation_vertex_array[j])

        for i in range(len(connected_omnian_vertices)):
            if i != 0:
                for j in range(len(connected_reticulation_vertices)):
                    if j != 0:
                        if [connected_omnian_vertices[i], connected_reticulation_vertices[j]] in self.arcs[connected_omnian_vertices[i]]:
                            connected_omnian_arcs.append([i, j])

        tempBipGraph = BiPartiteGraph(len(connected_omnian_vertices) - 1, len(connected_reticulation_vertices) - 1)

        for edge in connected_omnian_arcs:
            tempBipGraph.addEdge(edge[0], edge[1])

        return tempBipGraph



    def hasReticulations(self):
        input_arcs = []
        output_arcs = []
        for i in range(len(self.arcs)):
            output_arcs.append(len(self.arcs[i]))
        for i in range(len(self.reverseArcs)):
            input_arcs.append(len(self.reverseArcs[i]))

        tree_vertices = []
        reticulation_vertices = []

        for i in range(len(input_arcs)):
            if input_arcs[i] >= 2 and output_arcs[i] == 1:
                reticulation_vertices.append(i)
            elif input_arcs[i] == 1 and output_arcs[i] >= 2:
                tree_vertices.append(i)

        if len(reticulation_vertices) > 0:
            return True
        else:
            return False

    def displayGraphHighlightEdges(self, edge_list, vertex_list):
        self.dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        # print(self.vertices)
        # for i in self.vertices:
        #     if i in vertex_list:
        #         # self.dot.node(str(i), color='green')
        #         self.dot.node(str(i), penwidth='2')
        #     else:
        #         # self.dot.node(str(i), color='red')
        #         self.dot.node(str(i))
        # for vertex in self.arcs:
        #     for arc in vertex:
        #         if arc in edge_list:
        #             # self.dot.edge(str(arc[0]), str(arc[1]), color='green')
        #             self.dot.edge(str(arc[0]), str(arc[1]), penwidth='2')
        #         else:
        #             # self.dot.edge(str(arc[0]), str(arc[1]), color='red')
        #             self.dot.edge(str(arc[0]), str(arc[1]))

        self.dot.attr(labelloc="b")
        # print("SELF>VERTICES")
        # print(self.vertices)
        leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in self.vertices:
            if vertex in leafs:
                if vertex in self.taxDict:
                    self.dot.node(str(vertex), shape="point", xlabel=self.taxDict[vertex], labelloc="b")
                else:
                    if vertex in vertex_list:
                        self.dot.node(str(vertex), shape="point", xlabel=str(vertex), color='blue', penwidth='2')
                    else:
                        self.dot.node(str(vertex), shape="point")
            else:
                if vertex in vertex_list:
                    self.dot.node(str(vertex), label='', shape="point", color='blue', penwidth='2')
                else:
                    self.dot.node(str(vertex), label='', shape="point")
        for vertex in self.arcs:
            for arc in vertex:
                if arc in edge_list:
                    self.dot.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2), color='blue', penwidth='2')
                else:
                    self.dot.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))

        self.dot.view()

    def displayGraphFigure(self, square_array, triangle_array):
        self.dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        self.dot.attr(labelloc="b")
        leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in self.vertices:
            if vertex in leafs:
                if vertex in self.taxDict:
                    if vertex in triangle_array:
                        self.dot.node(str(vertex), label='', shape="triangle", style='filled', fixedsize='true', height='0.1', width='0.1', fillcolor='black')
                    else:
                        self.dot.node(str(vertex), shape="point", xlabel=self.taxDict[vertex], labelloc="b")
                else:
                    if vertex in square_array:
                        self.dot.node(str(vertex), label='', shape="square", style='filled', fixedsize='true', height='0.1', width='0.1', fillcolor='black')
                    elif vertex in triangle_array:
                        self.dot.node(str(vertex), label='', shape="triangle", style='filled', fixedsize='true', height='0.1', width='0.1', fillcolor='black')
                    else:
                        self.dot.node(str(vertex), label='', shape="point")
            else:
                if vertex in square_array:
                    self.dot.node(str(vertex), label='', shape="square", style='filled', fixedsize='true', height='0.1', width='0.1', fillcolor='black')
                elif vertex in triangle_array:
                    self.dot.node(str(vertex), label='', shape="triangle", style='filled', fixedsize='true', height='0.1', width='0.1', fillcolor='black')
                else:
                    self.dot.node(str(vertex), label='', shape="point")
        for vertex in self.arcs:
            for arc in vertex:
                # if arc in edge_list:
                #     self.dot.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.05), color='blue', penwidth='2')
                # else:
                self.dot.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.05))

        self.dot.view()

    def compareTwoSubGraphs(self, vertex_list1, edge_list1, vertex_list2, edge_list2):
        networkXGraph1 = networkx.DiGraph()
        for vertex in vertex_list1:
            networkXGraph1.add_node(vertex)
        for arc in edge_list1:
            networkXGraph1.add_edge(arc[0], arc[1])

        networkXGraph2 = networkx.DiGraph()
        for vertex in vertex_list2:
            networkXGraph2.add_node(vertex)
        for arc in edge_list2:
            networkXGraph2.add_edge(arc[0], arc[1])

        is_isomorphic = networkx.is_isomorphic(networkXGraph1, networkXGraph2)

        return is_isomorphic

    def isEqualToOtherNetwork(self, network2):
        """

        :type network2: PhylogeneticNetwork
        """
        if self.arcs == network2.arcs and self.vertices == network2.vertices:
            return True
        else:
            return False

    def isBinary(self):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        for i in range(len(vertex_out_degree)):
            if vertex_out_degree[i] > 2:
                return False

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] > 2:
                return False

        return True

    def checkTreeBasedBinary(self):
        bpg = self.makeBiPartiteGraph()
        bpg.hopcroftKarp()

        if bpg.U == 0 and bpg.V == 0:
            return True

        #CHECK IF BPG MATCHING COVERS ALL RETICULATION VERTICES

        pairU, pairV = bpg.returnHKMatching()

        # print("pairU")
        # print(pairU)
        # print("pairV")
        # print(pairV)

        reticulation_vertices_matched = []

        for i in range(len(pairV)):
            if pairV[i] != 0:
                reticulation_vertices_matched.append(i)

        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        reticulation_vertices = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 2 and vertex_out_degree[i] == 1:
                reticulation_vertices.append(i)

        # print("RETICULATION VERTICES MATCHED")
        # print(reticulation_vertices_matched)
        # print("RETICULATION VERTICES")
        # print(reticulation_vertices)

        if len(reticulation_vertices_matched) == len(reticulation_vertices):
            return True
        else:
            return False

        # for i in range(len(pairU)):
        #     if pairU[i] == 0 and pairV[i] == 0:
        #         continue
        #     else:
        #         reticulation_vertices_matched.append(pairU[i])
        #
        # all_reticulations_matched_check = True
        #
        # for i in range(0, bpg.V):
        #     if i not in reticulation_vertices_matched:
        #         all_reticulations_matched_check = False
        #
        # print(all_reticulations_matched_check)
        #
        # return all_reticulations_matched_check

        # return bpg.checkPerfectMatching()

    def checkTreeBasedNonBinary(self):
        bpg = self.makeBiPartiteGraph()
        bpg.hopcroftKarp()
        HKMatchingU, HKMatchingV = bpg.returnHKMatching()
        omnian_list = self.getAllOmnians()

        if len(HKMatchingU) == len(omnian_list):
            return True
        else:
            return False

    def checkTreeBasedNonBinary2(self):
        obpg = self.makeOmnianBipartiteGraph2()
        # obpg.displayGraph()
        obpg.hopcroftKarp()
        matchingU, matchingV = obpg.returnHKMatching()
        while 0 in matchingU:
            matchingU.remove(0)

        # print("MATCHINGU")
        # print(matchingU)
        # print("MATCHINGV")
        # print(matchingV)

        omnian_list = self.getAllOmnians()

        # print("OMNIAN LIST")
        # print(omnian_list)
        # print(matchingU)
        # print(matchingV)

        # print("OMNIAN LIST")
        # print(omnian_list)

        if len(matchingU) == len(omnian_list):
            return True
        else:
            return False

    def getAllOmnians(self):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = [0]
        reticulation_vertex_array = []
        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in self.arcs[i]:
                    if arc[1] in self.leafs:
                        leaf_below = True
                        break
                if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        omnian_list = []
        omnian_arcs = []
        omnian_rv = []

        # print("RETICULATION_VERTEX_ARRAy")
        # print(reticulation_vertex_array)

        for i in range(len(self.arcs)):
            if len(self.arcs[i]) > 0:
                omnian_check = True
                connected_rv = []

                for arc in self.arcs[i]:
                    if arc[1] not in reticulation_vertex_array:
                        omnian_check = False
                    else:
                        connected_rv.append(arc[1])

                if omnian_check:
                    omnian_list.append(i)
                    for rv in connected_rv:
                        if rv not in omnian_rv:
                            omnian_rv.append(rv)
                        omnian_arcs.append([i, rv])

        # print("OMNIAN LIST")
        # print(omnian_list)
        # print("omnian_rv")
        # print(omnian_rv)

        return omnian_list

    def checkIfNetworkIsTreeBasedBaseTree(self):
        temp_graph = deepcopy(self)
        bp = temp_graph.makeBiPartiteGraph()
        bp.hopcroftKarp()
        # bp.displayGraph()
        temp_graph.applyMatchingToGraph(temp_graph)
        #temp_graph.displayGraph()
        if self.vertices.sort() == temp_graph.vertices.sort() and self.getAllLeafs().sort() == temp_graph.getAllLeafs().sort():
            return True
        else:
            return False

    def checkSoftlyTreeBased(self):
        stb = SoftlyTreeBasedAlgorithm(self)
        return stb.startAlgorithm()

    def getAllArcs(self):
        arc_list = []
        for vertex in self.arcs:
            if len(vertex) > 0:
                for arc in vertex:
                    arc_list.append(arc)
        return arc_list

    def displayGraphNetworkX(self):

        networkXGraph = networkx.DiGraph()
        for vertex in self.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])

        nx.draw_networkx(networkXGraph, pos=nx.spring_layout(networkXGraph))

    def createGraphImageNetworkX(self):

        networkXGraph = networkx.DiGraph()
        for vertex in self.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])

        networkXGraph2 = networkx.DiGraph()

        leafs = {}

        for vertex in networkXGraph.nodes:
            if vertex == self.root:
                networkXGraph2.add_node(vertex, subset=0)
            elif networkXGraph.out_degree[vertex] == 0:
                # print("NXDAG")
                ## print(len(nx.dag_longest_path(networkXGraph)))
                networkXGraph2.add_node(vertex, subset=len(nx.dag_longest_path(networkXGraph)))
                leafs[vertex] = vertex
            else:
                networkXGraph2.add_node(vertex, subset=len(max(nx.all_simple_paths(networkXGraph, self.root, vertex), key=lambda x: len(x))))
                # print("VERTEX")
                # print(vertex)
                # print("SUBSET")
                ## print(len(max(nx.all_simple_paths(networkXGraph, self.root, vertex), key=lambda x: len(x))))

        for edge in networkXGraph.edges:
            networkXGraph2.add_edge(edge[0], edge[1])


        # for vertex in self.arcs:
        #     for arc in vertex:
        #         networkXGraph2.add_edge(arc[0], arc[1])

        # pos = nx.kamada_kawai_layout(networkXGraph)
        pos = nx.multipartite_layout(networkXGraph2, align='vertical')
        fig = matplotlib.pyplot.figure()
        networkx.draw(networkXGraph2, pos, ax=fig.add_subplot(), alpha=1, node_size=10, node_color='white', edgecolors='black', labels=leafs)
        fig.savefig("Images/PhylogeneticNetworkImage.png")

    # def hierarchy_pos(self, G, root, pos=None):
    #     for node in G.nodes:
    #         if node == root:
    #             if pos is None:
    #                 pos = {node: (0)}
    #             else:
    #                 pos[node] = (0)
    #         else:
    #             if pos is None:
    #                 pos = {node: (0.5, max(nx.all_simple_paths(G, root, node), key=lambda x: len(x)))}
    #             else:
    #                 pos[node] = (0.5, max(nx.all_simple_paths(G, root, node), key=lambda x: len(x)))
    #     return pos

    def applyComponentToGraph(self, component, matching):
        print("COMPONENT")
    #     print(component)
    #     print("MATCHING")
    #     print(matching)

    def getReticulationVertices(self):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        reticulation_vertices = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertices.append(i)

        return reticulation_vertices

    def getTreeVertices(self):
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertices = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                tree_vertices.append(i)

        return tree_vertices

    def getPloidyLevels(self):
        leafs = []

        print("SELF.VERTICES")
        print(self.vertices)

        root = self.root

        for i in range(len(self.arcs)):
            if len(self.arcs[i]) >= 1 and len(self.reverseArcs[i]) == 0:
                root = i
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) == 1:
                leafs.append(i)

        # for vertex in self.vertices:
        #     if len(self.arcs[vertex]) >= 1 and len(self.reverseArcs[vertex]) == 0:
        #         root = vertex
        #     if len(self.arcs[vertex]) == 0 and len(self.reverseArcs[vertex]) == 1:
        #         leafs.append(vertex)

        networkXGraph = networkx.DiGraph()
        for vertex in self.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])

        ploidy_dict = {}
        ploidy_array = []

        try:
            for leaf in leafs:
                paths = nx.all_simple_paths(networkXGraph, source=root, target=leaf)
                i = 0
                for path in paths:
                    i = i + 1
                ploidy_dict[leaf] = i
                ploidy_array.append(i)
        except:
            self.displayGraph()
            print(root)
            print(self.root)
            print(self.arcs)
            print(self.reverseArcs)
            print(self.vertices)


        return ploidy_dict, ploidy_array

    def getBaseTree(self):
        GN = self.makeBiPartiteGraph()
        GN.hopcroftKarp()
        new_network = deepcopy(self)
        new_network.applyOppositeMatchingToGraph(GN)
        return new_network

    def displayBaseTree(self):
        base_tree = self.getBaseTree()
        arc_list = base_tree.getAllArcs()
        # self.displayGraphHighlightEdges(arc_list, base_tree.vertices)
        self.displayGraphBoldEdges(arc_list, base_tree.vertices)

    def displayGraphBoldEdges(self, arc_list, vertex_list):
        digraph_image = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in self.vertices:
            if vertex in leafs:
                if vertex in self.taxDict:
                    if vertex in vertex_list:
                        digraph_image.node(str(vertex), shape="point", xlabel=self.taxDict[vertex], labelloc="b", penwidth='2')
                    else:
                        digraph_image.node(str(vertex), shape="point", xlabel=self.taxDict[vertex], labelloc="b")
                else:
                    if vertex in vertex_list:
                        digraph_image.node(str(vertex), shape="point", xlabel=str(vertex), penwidth='2')
                    else:
                        digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
            else:
                if vertex in vertex_list:
                    digraph_image.node(str(vertex), label='', shape="point", penwidth='2')
                else:
                    digraph_image.node(str(vertex), label='', shape="point")
        for vertex in self.arcs:
            for arc in vertex:
                if arc in arc_list:
                    digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2), penwidth='2')
                else:
                    digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
        digraph_image.view()

    def displayOverlayWithAnotherNetwork(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        edge_list = network.getAllArcs()
        vertex_list = network.vertices
        self.dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        # print(self.vertices)
        for i in self.vertices:
            if i in vertex_list:
                self.dot.node(str(i), color='green')
            else:
                self.dot.node(str(i), color='red')
        for vertex in self.arcs:
            for arc in vertex:
                if arc in edge_list:
                    self.dot.edge(str(arc[0]), str(arc[1]), color='green')
                else:
                    self.dot.edge(str(arc[0]), str(arc[1]), color='red')
        self.dot.view()

    def createBaseTreeImage(self):
        base_tree = self.getBaseTree()
        arc_list = base_tree.getAllArcs()
        # self.displayGraphHighlightEdges(arc_list, base_tree.vertices)
        vertex_list = base_tree.vertices
        # self.displayGraphBoldEdges(arc_list, base_tree.vertices)

        digraph_image = graphviz.Digraph('Images/BaseTree', comment='Phylogenetic Network')
        # digraph_image.attr(rankdir="LR")
        digraph_image.attr(labelloc="b")
        # print("SELF>VERTICES")
        # print(self.vertices)
        leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                leafs.append(i)
        for vertex in self.vertices:
            if vertex in leafs:
                if vertex in self.taxDict:
                    if vertex in vertex_list:
                        digraph_image.node(str(vertex), shape="point", xlabel=self.taxDict[vertex], labelloc="b",
                                           penwidth='2')
                    else:
                        digraph_image.node(str(vertex), shape="point", xlabel=self.taxDict[vertex], labelloc="b")
                else:
                    if vertex in vertex_list:
                        digraph_image.node(str(vertex), shape="point", xlabel=str(vertex), penwidth='2')
                    else:
                        digraph_image.node(str(vertex), shape="point", xlabel=str(vertex))
            else:
                if vertex in vertex_list:
                    digraph_image.node(str(vertex), label='', shape="point", penwidth='2')
                else:
                    digraph_image.node(str(vertex), label='', shape="point")
        for vertex in self.arcs:
            for arc in vertex:
                if arc in arc_list:
                    digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2), penwidth='2')
                else:
                    digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))
        digraph_image.render('Images/BaseTree', format='png', view=False)

    def getOmnianAndReticulationList(self):
        omnian_list = self.getAllOmnians()

        omnian_list = [0] + omnian_list

        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = []
        reticulation_vertex_array = []
        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in self.arcs[i]:
                    if arc[1] in self.leafs:
                        leaf_below = True
                        break
                if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        connected_omnian_vertices = [0]
        connected_reticulation_vertices = [0]
        connected_omnian_arcs = []

        for i in range(len(omnian_list)):
            for j in range(len(reticulation_vertex_array)):
                if [omnian_list[i], reticulation_vertex_array[j]] in self.arcs[omnian_list[i]]:
                    if omnian_list[i] not in connected_omnian_vertices:
                        connected_omnian_vertices.append(omnian_list[i])
                    if reticulation_vertex_array[j] not in connected_reticulation_vertices:
                        connected_reticulation_vertices.append(reticulation_vertex_array[j])

        for i in range(len(connected_omnian_vertices)):
            if i != 0:
                for j in range(len(connected_reticulation_vertices)):
                    if j != 0:
                        if [connected_omnian_vertices[i], connected_reticulation_vertices[j]] in self.arcs[
                            connected_omnian_vertices[i]]:
                            connected_omnian_arcs.append([i, j])

        return connected_omnian_vertices, connected_reticulation_vertices

    def getPloidyLevelOfEachVertexAndConnections(self):
        levelDict = {}
        leafsBelowDict = {}
        paths = self.getAllPaths()
        for vertex in self.vertices:
            level = 0
            for path in paths:
                if vertex in path:
                    level = level + 1
                    leaf = path[len(path) - 1]
                    if vertex not in leafsBelowDict.keys():
                        leafsBelowDict[vertex] = [self.taxDict.get(leaf)]
                    else:
                        if self.taxDict.get(leaf) not in leafsBelowDict.get(vertex):
                            tempArray = leafsBelowDict.get(vertex)
                            tempArray.append(self.taxDict.get(leaf))
                            leafsBelowDict[vertex] = tempArray
            levelDict[vertex] = level

        return levelDict, leafsBelowDict

    def getLeafsBelowVertex(self, vertex):
        leafs_below = []
        paths = self.getAllPaths()
        for path in paths:
            if vertex in path:
                leaf = path[len(path) - 1]
                if leaf not in leafs_below:
                    leafs_below.append(leaf)
        return leafs_below

    def isTreeChild(self):
        omnianSet = self.getAllOmnians()
        if len(omnianSet) == 0:
            return True
        else:
            return False

    def isNormal(self):
        if self.isTreeChild():

            networkXGraph = networkx.DiGraph()
            for vertex in self.vertices:
                networkXGraph.add_node(vertex)
            for vertex in self.arcs:
                for arc in vertex:
                    networkXGraph.add_edge(arc[0], arc[1])

            for vertex1 in self.vertices:
                for vertex2 in self.vertices:
                    simple_paths = nx.all_simple_paths(networkXGraph, vertex1, vertex2)
                    path_lengths = []
                    for path in simple_paths:
                        path_lengths = len(path)
                    if type(path_lengths) != int:
                        if 1 in path_lengths:
                            for length in path_lengths:
                                if length > 1:
                                    return False
            return True
        else:
            return False

    def applyOmnianOppositeMatchingToGraph(self, matchingGraph, vertices_removed=[]):

        omnian_list = self.getAllOmnians()

        omnian_list = [0] + omnian_list

        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex in self.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in self.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in self.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = []
        reticulation_vertex_array = []
        leaf_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in self.arcs[i]:
                    if arc[1] in self.leafs:
                        leaf_below = True
                        break
                if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 0:
                leaf_vertex_array.append(i)

        connected_omnian_vertices = [0]
        connected_reticulation_vertices = [0]
        connected_omnian_arcs = []

        for i in range(len(omnian_list)):
            for j in range(len(reticulation_vertex_array)):
                if [omnian_list[i], reticulation_vertex_array[j]] in self.arcs[omnian_list[i]]:
                    if omnian_list[i] not in connected_omnian_vertices:
                        connected_omnian_vertices.append(omnian_list[i])
                    if reticulation_vertex_array[j] not in connected_reticulation_vertices:
                        connected_reticulation_vertices.append(reticulation_vertex_array[j])

        for i in range(len(connected_omnian_vertices)):
            if i != 0:
                for j in range(len(connected_reticulation_vertices)):
                    if j != 0:
                        if [connected_omnian_vertices[i], connected_reticulation_vertices[j]] in self.arcs[
                            connected_omnian_vertices[i]]:
                            connected_omnian_arcs.append([i, j])

        # ol, rl = self.getOmnianAndReticulationList()
        if type(matchingGraph) == BiPartiteGraph:
            pairU, pairV = matchingGraph.returnHKMatching()
            edges_to_be_removed = []

            pairU, pairV = matchingGraph.returnHKMatching()

            # print("PAIRU")
            # print(pairU)
            # print("PAIRV")
            # print(pairV)

            # for i in range(len(pairV)):
            #     if pairV[i] != 0:
            #         edges_to_be_removed.append([pairV[i], i])
            while 0 in pairU:
                pairU.remove(0)
            while 0 in pairV:
                pairV.remove(0)
            for i in range(len(pairU)):
                print(str(pairV[i] - 1) + ", " + str(pairU[i] - 1))
                edges_to_be_removed.append([connected_omnian_vertices[pairV[i]], connected_reticulation_vertices[pairU[i]]])
            for edge in edges_to_be_removed:
                self.removeArc(edge)
        else:
            return "Invalid matching graph class type"

    def get_base_tree(self):
        bpg = self.makeBiPartiteGraph()
        bpg.hopcroftKarp()
        network = deepcopy(self)
        network.applyOppositeMatchingToGraph2(bpg)

        return network
