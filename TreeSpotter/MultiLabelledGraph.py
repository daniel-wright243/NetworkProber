import os.path
import pathlib
import re
import tkinter as tkinter
from copy import deepcopy
from tkinter.filedialog import askopenfilename

import graphviz
import networkx

from TreeSpotter.DAG import DAG
from TreeSpotter.BiPartiteGraph import BiPartiteGraph

class MultiLabelledGraph:

    def __init__(self, network):
        """

        Parameters
        ----------
        network : DAG
        """
        print(network.vertices)

        self.vertices = []
        self.arcs = [[] for _ in range(5000)]
        self.root = network.root
        self.reverseArcs = [[] for _ in range(5000)]
        self.multiLabelledVertices = [[] for _ in range(5000)]
        self.reverseMultiLabelledVertices = [[] for _ in range(5000)]
        self.reverseMultiLabelledArcs = [[] for _ in range(5000)]

        input_arcs = [0 for _ in range(max(network.vertices) + 1)]
        output_arcs = [0 for _ in range(max(network.vertices) + 1)]
        for key, value in network.vertex_dict.items():
            output_arcs[key] = len(value["arcs"])
            input_arcs[key] = len(value["reverseArcs"])
        # for i in range(len(network.arcs)):
        #     output_arcs[i] = len(network.arcs[i])
        # for i in range(len(network.reverseArcs)):
        #     input_arcs[i] = len(network.reverseArcs[i])

        tree_vertices = []
        reticulation_vertices = []
        leaf_list = []

        for i in range(len(input_arcs)):
            if input_arcs[i] >= 2 and output_arcs[i] == 1:
                reticulation_vertices.append(i)
            elif input_arcs[i] == 1 and output_arcs[i] >= 2:
                tree_vertices.append(i)
            elif input_arcs[i] == 1 and output_arcs[i] == 0:
                leaf_list.append(i)


        # print("INPUT ARCS")
        # print(input_arcs)
        # print("OUTPUT ARCS")
        # print(output_arcs)
        #
        # print("TREE VERTICES")
        # print(tree_vertices)
        # print("RETICULATION VERTICES")
        # print(reticulation_vertices)
        # print("LEAF VERTICES")
        # print(len(leaf_list))

        current_vertex = int(max(network.vertices) + 1)

        # print("NETWORK.VERTICES")
        # print(network.vertices)
        #
        # print("CURRENT VERTEX")
        # print(current_vertex)

        path_list = network.get_all_paths()

        self.vertices.append(network.root)
        self.path_list = path_list

        # print("PATH LIST")
        # print(path_list)

        temp_arc_list = []
        done_path_list = []

        # print("PATH LIST")
        # print(path_list)

        arc_list = []

        for path in path_list:
            i = 0
            if len(path) > 0:
                current_path = []
                current_path.append(network.root)
                path.remove(network.root)
                pv = network.root
                j = 1
                for vertex in path:
                    if vertex not in self.vertices:
                        self.vertices.append(vertex)
                        self.arcs[pv].append([pv, vertex])
                        arc_list.append([pv, vertex])
                        self.reverseArcs[vertex].append([vertex, pv])
                        pv = vertex
                        temp_arc_list.append([path_list[i][j], path_list[i][j-1]])
                        current_path.append(vertex)
                    else:
                        done = False
                        for cv in self.reverseMultiLabelledVertices[pv]:
                            if [cv, vertex] in self.arcs[cv]:
                                pv = vertex
                                current_path.append(vertex)
                                done = True
                                break
                        for cv in self.reverseMultiLabelledVertices[vertex]:
                            if [pv, cv] in self.arcs[pv]:
                                pv = cv
                                current_path.append(cv)
                                done = True
                                break
                        if [pv, vertex] not in self.arcs[pv] and done == False:
                            self.vertices.append(current_vertex + 1)
                            self.arcs[pv].append([pv, current_vertex + 1])
                            arc_list.append([pv, current_vertex + 1])
                            try:
                                self.reverseArcs[current_vertex + 1].append([current_vertex + 1, pv])
                            except:
                                print("CURRENT VERTEX + 1")
                                print(current_vertex + 1)
                                print("PV")
                                print(pv)
                                print("REVERSEARCS")
                                print(self.reverseArcs)
                                print("NETWORK VERTICES")
                                print(network.vertices)
                                print("NETWORK ARCS")
                                print(network.arcs)
                                print("NETWORK ROOT")
                                print(network.root)
                                raise Exception
                            self.multiLabelledVertices[current_vertex + 1].append(vertex)
                            self.reverseMultiLabelledVertices[vertex].append(current_vertex + 1)
                            current_path.append(current_vertex + 1)
                            pv = current_vertex + 1
                            current_vertex = current_vertex + 1
                        elif done == False:
                            pv = vertex
                            current_path.append(vertex)
                done_path_list.append(current_path)
                j = j + 1
            i = i + 1

    def displayGraph(self): # uses graphviz to display the phylogenetic network
        label_array = [0 for _ in range(5000)]
        labelDict = {}
        self.dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        for i in self.vertices:
            if len(self.multiLabelledVertices[i]) > 0:
                self.dot.node(str(i), str(self.multiLabelledVertices[i][0]))
            else:
                self.dot.node(str(i))
        for vertex in self.arcs:
            for arc in vertex:
                self.dot.edge(str(arc[0]), str(arc[1]))
        self.dot.view()

    def writeToPADREFile(self):
        # Find the root of graph
        root = self.root
        # find all leaves of the graph
        self.leafs = []
        for i in range(len(self.arcs)):
            if len(self.arcs[i]) == 0 and len(self.reverseArcs[i]) > 0:
                self.leafs.append(i)
        nexus_array = []
        self.recursiveTreeNetworkToNEXUS(nexus_array, root)

        nexus_string = str(nexus_array)
        nexus_string.replace("[", "(")
        nexus_string.replace("]", ")")
        tree_string_prefix = "  [1] tree 'tree-1'=[&R] "
        nexus_complete_string = tree_string_prefix + nexus_string + "\n"

        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        dir_path = dir_path.replace("\\", "/")

        dir_path = dir_path + "/PADRE_Files/PADREInputFile.tre"

        # print("DIR PATH")
        # print(dir_path)
        #
        # directory = tkinter.filedialog.asksaveasfilename(initialfile='default.nex', defaultextension='.nex',
        #                                                  filetypes=(("NEXUS file", "*.nex"), ("all files", "*.*")))
        #
        # print("DIRECTORY")
        # print(directory)
        #
        # print(nexus_complete_string)

        for i in range(len(self.multiLabelledVertices)):
            if len(self.multiLabelledVertices[i]) > 0:
                # if len(self.multiLabelledVertices[i]) > 1:
                #     # print("BROKEN")
                nexus_string = nexus_string.replace(str(i), str(self.multiLabelledVertices[i][0]))

        ## print(nexus_string)

        nexus_string = nexus_string.replace("[", "(")
        nexus_string = nexus_string.replace("]", ")")

        nexus_string = nexus_string + ";"

        ## print(nexus_string)

        file = open(dir_path, 'w')
        file.write(nexus_string)
        file.close()

    def recursiveTreeNetworkToNEXUS(self, nexus_string, current_vertex):
        for i in range(len(self.arcs[current_vertex])):
            #IF NEXT VERTEX IS A LEAF
            if self.arcs[current_vertex][i][1] in self.leafs:
                nexus_string.append(self.arcs[current_vertex][i][1])
            else:
                nexus_string.append([])
                self.recursiveTreeNetworkToNEXUS(nexus_string[i], self.arcs[current_vertex][i][1])

    def readFromPADREFile(self, filename):
        root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '/PADRE Files/padre2commandli/'
        window_filename = askopenfilename(initialdir=root_dir)
        # filename = 'testFile'
        # concatFileName = 'NEXUS Files/' + filename + '.NEXUS'
        ## print(window_filename)
        openedNexusFile = open(window_filename)

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

    def createArc(self, arc):
        if arc not in self.arcs[arc[0]]:
            self.arcs[arc[0]].append(arc)
            reversed_arc = [arc[1], arc[0]]
            self.reverseArcs[arc[1]].append(reversed_arc)
            return "Success"
        else:
            return "Arc already exists"

    # def simplifyNetwork(self):
    #     simplifiedNetwork = deepcopy(self)
    #
    #     input_arcs = []
    #     output_arcs = []
    #     for i in range(len(self.arcs)):
    #         output_arcs.append(len(self.arcs[i]))
    #     for i in range(len(self.reverseArcs)):
    #         input_arcs.append(len(self.reverseArcs[i]))
    #
    #     for i in range(len(input_arcs)):
    #         if input_arcs[i] == 1 and output_arcs[i] == 1:
    #             print("I")
    #             print(i)
    #             # get vertex above current vertex
    #             vertex_above = simplifiedNetwork.reverseArcs[i][0][1]
    #             vertex_below = simplifiedNetwork.arcs[i][0][1]
    #             # removing edge from vertex above to i
    #             simplifiedNetwork.removeArc([vertex_above, i])
    #             # removing edge from i to vertex below
    #             simplifiedNetwork.removeArc([i, vertex_below])
    #             # creating arc from vertex above to vertex below
    #             simplifiedNetwork.createArc([vertex_above, vertex_below])
    #             # remove vertex i
    #             simplifiedNetwork.vertices.remove(i)
    #
    #             if len(self.multiLabelledVertices[i]) > 0:
    #                 simplifiedNetwork.reverseMultiLabelledVertices[simplifiedNetwork.multiLabelledVertices[i][0]].remove(i)
    #                 simplifiedNetwork.multiLabelledVertices[i] = []
    #
    #     return simplifiedNetwork

    def simplifyNetwork(self):
        simplifiedNetwork = deepcopy(self)
        vertex_in_degree = [0] * (max(self.vertices) + 1)
        vertex_out_degree = [0] * (max(self.vertices) + 1)

        for vertex_arcs in self.arcs:
            for arcs in vertex_arcs:
                vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        ## print("VERTEX IN DEGREE")
        ## print(vertex_in_degree)
        ## print("VERTEX OUT DEGREE")
        ## print(vertex_out_degree)
        ## print(simplifiedNetwork.arcs)
        ## print(simplifiedNetwork.reverseArcs)

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] == 1:
                ## print("I")
                ## print(i)
                # get vertex above current vertex
                vertex_above = simplifiedNetwork.reverseArcs[i][0][1]
                vertex_below = simplifiedNetwork.arcs[i][0][1]
                # removing edge from vertex above to i
                simplifiedNetwork.removeArc([vertex_above, i])
                # removing edge from i to vertex below
                simplifiedNetwork.removeArc([i, vertex_below])
                # creating arc from vertex above to vertex below
                simplifiedNetwork.createArc([vertex_above, vertex_below])
                # remove vertex i
                simplifiedNetwork.vertices.remove(i)

                if len(self.multiLabelledVertices[i]) > 0:
                    simplifiedNetwork.reverseMultiLabelledVertices[
                        simplifiedNetwork.multiLabelledVertices[i][0]].remove(i)
                    simplifiedNetwork.multiLabelledVertices[i] = []

        return simplifiedNetwork

    def getArcListOfNetworkBelowVertex(self, input_vertex):
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

        vertex_list.append(input_vertex)

        for arc in self.arcs[input_vertex]:
            arcList.append(arc)

        for vertex in vertices_below:
            vertex_list.append(vertex)
            for arc in self.arcs[vertex]:
                if len(self.multiLabelledVertices[arc[0]]) > 0:
                    arc[0] = self.multiLabelledVertices[arc[0]][0]
                if len(self.multiLabelledVertices[arc[1]]) > 0:
                    arc[1] = self.multiLabelledVertices[arc[1]][0]
                arcList.append(arc)

        ## print("ARCLIST")
        ## print(arcList)


    def removeNetworkBelowVertex(self, input_vertex):
        vertices_to_remove = self.getVerticesBelowVertex(input_vertex, input_vertex)
        # vertices_to_remove = self.getVerticesBelowVertexNetworkX(input_vertex)

        for vertex in vertices_to_remove:
            self.vertices.remove(vertex)
            for arc in self.arcs[vertex]:
                self.arcs[vertex].remove(arc)


    def getVerticesBelowVertex(self, original_split_vertex, split_vertex, vertex_array=[]):
        for arc in self.arcs[split_vertex]:
            vertex_array.append(arc[1])
            self.getVerticesBelowVertex(original_split_vertex, arc[1], vertex_array)
        fixed_vertex_array = []
        for vertex in vertex_array:
            if vertex not in fixed_vertex_array:
                fixed_vertex_array.append(vertex)
        return fixed_vertex_array

    # def getVerticesBelowVertexNetworkX(self, vertex):
    #     networkXGraph = networkx.DiGraph()
    #     vertex_list = []
    #     arc_list = []
    #     print(self.vertices)
    #     print(self.arcs)
    #     self.displayGraph()
    #     for vertex in self.vertices:
    #         if vertex not in vertex_list:
    #             networkXGraph.add_node(vertex)
    #             vertex_list.append(vertex)
    #     for vertex in self.arcs:
    #         for arc in vertex:
    #             if arc not in arc_list:
    #                 networkXGraph.add_edge(arc[0], arc[1])
    #                 arc_list.append(arc)
    #
    #     output_list = networkx.descendants(networkXGraph, vertex)
    #
    #     return output_list

