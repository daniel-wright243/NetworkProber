import os.path
import pathlib
import re
import tkinter as tkinter
from copy import deepcopy
from tkinter.filedialog import askopenfilename

import graphviz
import networkx

from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.BiPartiteGraph import BiPartiteGraph

class MultiLabelledGraph:

    def __init__(self, network):
        """

        Parameters
        ----------
        network : PhylogeneticNetwork
        """
        print(network.vertices)

        self.vertices = []
        self.arcs = [[] for _ in range(5000)]
        self.root = network.root
        self.reverseArcs = [[] for _ in range(5000)]
        self.multiLabelledVertices = [[] for _ in range(5000)]
        self.reverseMultiLabelledVertices = [[] for _ in range(5000)]
        self.reverseMultiLabelledArcs = [[] for _ in range(5000)]

        input_arcs = [0 for _ in range(len(network.arcs) + 1)]
        output_arcs = [0 for _ in range(len(network.arcs) + 1)]
        for i in range(len(network.arcs)):
            output_arcs[i] = len(network.arcs[i])
        for i in range(len(network.reverseArcs)):
            input_arcs[i] = len(network.reverseArcs[i])

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

        path_list = network.getAllPaths()

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

                    #pv = vertex
        #ADD MULTI LABELLED VERTICES AND ARCS

        # path_list = network.getAllPaths()
        #
        # for path in path_list:
        #     if len(path) > 0:
        #         path.remove(network.root)
        #         pv = network.root
        #         for vertex in path:
        #             if vertex in self.vertices:
        #                 self.vertices.append(current_vertex + 1)
        #                 self.arcs[pv].append([pv, current_vertex + 1])
        #                 self.multiLabelledVertices[current_vertex + 1].append(vertex)
        #                 self.reverseMultiLabelledVertices[vertex].append(current_vertex + 1)
        #                 pv = current_vertex + 1
        #             else:
        #                 pv = vertex

                    # else:
                    #     self.vertices.append(current_vertex + 1)
                    #     self.arcs[pv].append([pv, current_vertex + 1])
                    #     self.reverseArcs[current_vertex + 1].append([current_vertex + 1, pv])
                    #     self.multiLabelledVertices[current_vertex + 1].append(vertex)
                    #     self.reverseMultiLabelledVertices[vertex].append(current_vertex + 1)
                    #     pv = current_vertex + 1
                    #     current_vertex = current_vertex + 1


                    # else:
                    #     if [pv, vertex] not in self.arcs[pv]:
                    #         self.vertices.append(current_vertex + 1)
                    #         self.arcs[pv].append([pv, current_vertex + 1])
                    #         self.reverseArcs[current_vertex + 1].append([current_vertex + 1, pv])
                    #         self.multiLabelledVertices[current_vertex + 1].append(vertex)
                    #         self.reverseMultiLabelledVertices[vertex].append(current_vertex + 1)
                    #         pv = current_vertex + 1
                    #         current_vertex = current_vertex + 1


    # def __init__(self, network):
    #     """
    #
    #     Parameters
    #     ----------
    #     network : PhylogeneticNetwork
    #     """
    #     self.vertices = network.vertices
    #     self.arcs = network.arcs
    #     self.root = network.root
    #     self.reverseArcs = network.reverseArcs
    #     self.multiLabelledVertices = [[] for _ in range(5000)]
    #     self.reverseMultiLabelledVertices = [[] for _ in range(5000)]
    #     self.reverseMultiLabelledArcs = [[] for _ in range(5000)]
    # #     #tree_vertex_array, reticulation_vertex_array = network.getTreeAndReticulationVertexArray(True)
    # #
    #     input_arcs = []
    #     output_arcs = []
    #     for i in range(len(self.arcs)):
    #         output_arcs.append(len(self.arcs[i]))
    #     for i in range(len(self.reverseArcs)):
    #         input_arcs.append(len(self.reverseArcs[i]))
    #
    #     tree_vertices = []
    #     reticulation_vertices = []
    #
    #     for i in range(len(input_arcs)):
    #         if input_arcs[i] >= 2 and output_arcs[i] == 1:
    #             reticulation_vertices.append(i)
    #         elif input_arcs[i] == 1 and output_arcs[i] >= 2:
    #             tree_vertices.append(i)
    #
    #     print("TREE VERTICES")
    #     print(tree_vertices)
    #     print("RETICULATION VERTICES")
    #     print(reticulation_vertices)
    #
    #     tree_vertex_array = []
    #     reticulation_vertex_array = []
    # #
    # #     # for t_vertex in tree_vertices:
    # #     #     for r_vertex in reticulation_vertices:
    # #     #         if [t_vertex, r_vertex] in self.arcs[t_vertex]:
    # #     #             if t_vertex not in tree_vertex_array:
    # #     #                 tree_vertex_array.append(t_vertex)
    # #     #                 if r_vertex not in reticulation_vertex_array:
    # #     #                     reticulation_vertex_array.append(r_vertex)
    #
    #
    #     print("RETICULATION VERTEX ARRAY")
    #     print(reticulation_vertex_array)
    #
    #     current_vertex = max(network.vertices) + 1
    # #
    # #     #network.displayGraph()
    # #
    # #     #network.getNetworkBelowVertex(8).displayGraph()
    # #
    #     network_below_list = []
    #     network_array = []
    # #
    # #     #network.displayGraph()
    #
    #     temp_network = deepcopy(network)
    #
    #     #temp_network.displayGraph()
    #
    #     for reticulation_vertex in reticulation_vertices:
    #         network_array.append(temp_network)
    #
    #         reticulation_vertex = reticulation_vertex
    #         print("RETICULATION VERTEX")
    #         print(reticulation_vertex)
    #         #SPLIT FOR MULTILABELLED GRAPHS ON RETICULATION VERTEXS
    #
    #         #GET ALL VERTICES ABOVE THE RETICULATION
    #         vertices_above = []
    #         for arc in temp_network.reverseArcs[reticulation_vertex]:
    #             vertices_above.append(arc[1])
    #
    #         print("VERTICES ABOVE")
    #         print(vertices_above)
    # #
    # #         #GET ALL OF THE NETWORK BELOW THE RETICULATION VERTEX
    # #         # network_below = network.getNetworkBelowVertex(reticulation_vertex)
    # #
    #         network_below = temp_network.getNetworkBelowVertexNetworkX(reticulation_vertex)
    #         network_below_list.append(network_below)
    #
    #         print("NETWORK BELOW ARCS")
    #         print(network_below.arcs)
    #
    #         print("NETWORK BELOW VERTICES")
    #         print(network_below.vertices)
    #
    #         print("VERTICES ABOVE")
    #         print(vertices_above)
    # #
    # #         #GET RID OF ARC GOING TO OTHER VERTICES
    # #         #print("VETICES_ABOVE[1]")
    # #         #print(vertices_above[1])
    #         print("RETICULATION VERTEX")
    #         print(reticulation_vertex)
    #         print("VERTICES ABOVE")
    #         print(vertices_above)
    #         print("SELF.ARCS.VERTICESABOVE")
    #         print(self.arcs[vertices_above[1]])
    #         for i in range(1, len(vertices_above)):
    #             print("REMOVING ARC")
    #             print([vertices_above[i], reticulation_vertex])
    #             temp_network.arcs[vertices_above[i]].remove([vertices_above[i], reticulation_vertex])
    #             temp_network.reverseArcs[reticulation_vertex].remove([reticulation_vertex, vertices_above[i]])
    # #         #self.arcs[vertices_above[1]].remove([vertices_above[1], reticulation_vertex])
    # #
    #         print("SELF.ARCS.VERTICESABOVE2")
    #         print(temp_network.arcs[vertices_above[1]])
    #
    #         #STITCH NETWORK BELOW ONTO SECOND VERTEX
    #         network_below_root = network_below.root
    #         print("ROOT")
    #         print(network_below_root)
    #
    #         #CONNECT NEW ROOT TO NETWORK BELOW
    #
    #         # self.vertices.append(current_vertex + 1)
    #         # self.arcs[vertices_above[1]].append([vertices_above[1], current_vertex + 1])
    #         # self.reverseArcs[current_vertex + 1].append([current_vertex + 1, vertices_above[1]])
    #         # self.multiLabelledVertices[network_below_root].append(current_vertex + 1)
    #         # current_vertex = current_vertex + 1
    #
    #         assigned_vertices = {}
    #
    #         print("NETWORK_BELOW.VERTICES")
    #         print(network_below.vertices)
    #         print("NETWORK_BELOW.ARCS")
    #         print(network_below.arcs)
    #
    #         vertices_used = []
    #
    #         for i in range(1, len(vertices_above)):
    #             vertex_above = vertices_above[i]
    #             #CONNECT ROOT
    #             temp_network.vertices.append(current_vertex + 1)
    #             self.multiLabelledVertices[current_vertex + 1].append(network_below.root)
    #             self.reverseMultiLabelledVertices[network_below.root].append(current_vertex + 1)
    #             temp_network.arcs[vertices_above[i]].append([vertices_above[i], current_vertex + 1])
    #             temp_network.reverseArcs[current_vertex + 1].append([current_vertex + 1, vertices_above[i]])
    #             current_vertex = current_vertex + 1
    #             #ADD REST OF NETWORK
    #             for vertex in network_below.vertices:
    #                 if vertex != network_below.root:
    #                     temp_network.vertices.append(current_vertex + 1)
    #                     self.multiLabelledVertices[current_vertex + 1].append(vertex)
    #                     self.reverseMultiLabelledVertices[vertex].append(current_vertex + 1)
    #                     current_vertex = current_vertex + 1
    #                     # for r_arc in network_below.reverseArcs[vertex]:
    #                     #     self.arcs[r_arc[1]].append([current_vertex + 1, self.multiLabelledVertices[r_arc[0]]])
    #             for vertex in network_below.arcs:
    #                 for old_arc in vertex:
    #                     print("OLD ARC 0")
    #                     print(old_arc)
    #                     print("REVERSEMULTILABELLEDVERTICES")
    #                     print(self.reverseMultiLabelledVertices)
    #                     print(self.reverseMultiLabelledVertices[old_arc[0]])
    #                     temp_network.arcs[self.reverseMultiLabelledVertices[old_arc[0]][0]].append([self.reverseMultiLabelledVertices[old_arc[0]][0], self.reverseMultiLabelledVertices[old_arc[1]][0]])
    #                     temp_network.reverseArcs[self.reverseMultiLabelledVertices[old_arc[1]][0]].append([self.reverseMultiLabelledVertices[old_arc[1]][0], self.reverseMultiLabelledVertices[old_arc[0]][0]])
    #             self.reverseMultiLabelledVertices = [[] for _ in range(5000)]
    #
    #
    #
    #
    #
    #
    #         # for i in range(1, len(vertices_above)):
    #         #     #ATTACH NEW NETWORK
    #         #
    #         #
    #         #
    #         #     for vertex in network_below.vertices:
    #         #         self.vertices.append(current_vertex + 1)
    #         #         self.multiLabelledVertices[current_vertex + 1].append(vertex)
    #         #         current_vertex = current_vertex + 1
    #
    #
    #
    #
    #
    #
    #         # for vertex in network_below.vertices:
    #         #     if vertex not in vertices_used:
    #         #         for i in range(len(vertices_above) - 1):
    #         #             self.vertices.append(current_vertex + 1)
    #         #             assigned_vertices[vertex] = current_vertex + 1
    #         #             # self.multiLabelledVertices[vertex].append(current_vertex + 1)
    #         #             self.multiLabelledVertices[current_vertex + 1].append(vertex)
    #         #             print("CURRENT VERTEX")
    #         #             print(current_vertex + 1)
    #         #             current_vertex = current_vertex + 1
    #         #             vertices_used.append(vertex)
    #
    #                 # self.vertices.append(current_vertex + 1)
    #                 # assigned_vertices[vertex] = current_vertex + 1
    #                 # #self.multiLabelledVertices[vertex].append(current_vertex + 1)
    #                 # self.multiLabelledVertices[current_vertex + 1].append(vertex)
    #                 # print("CURRENT VERTEX")
    #                 # print(current_vertex + 1)
    #                 # current_vertex = current_vertex + 1
    #                 # vertices_used.append(vertex)
    #
    #         print("ASSIGNED VERTICES")
    #         print(assigned_vertices)
    #
    #         # for i in range(1, len(vertices_above)):
    #         #     self.arcs[vertices_above[i]].append([vertices_above[i], assigned_vertices[network_below_root]])
    #         #     self.reverseArcs[assigned_vertices[network_below_root]].append([assigned_vertices[network_below_root], vertices_above[i]])
    #
    #         # self.arcs[vertices_above[1]].append([vertices_above[1], assigned_vertices[network_below_root]])
    #         # self.reverseArcs[assigned_vertices[network_below_root]].append([assigned_vertices[network_below_root], vertices_above[1]])
    #         # self.multiLabelledVertices[network_below_root].append(assigned_vertices[network_below_root])
    #
    #         print("SELF.ARCS.VERTICESABOVE3")
    #         print(self.arcs[vertices_above[1]])
    #
    #         #self.displayGraph()
    #
    #         arcs_used = []
    #
    #         # for vertex in network_below.arcs:
    #         #     if type(vertex) == list: #MULTIPLE VERTICES
    #         #         for arc in vertex:
    #         #             if arc not in arcs_used:
    #         #                 self.arcs[assigned_vertices[arc[0]]].append([assigned_vertices[arc[0]], assigned_vertices[arc[1]]])
    #         #                 self.reverseArcs[assigned_vertices[arc[1]]].append([assigned_vertices[arc[1]], assigned_vertices[arc[0]]])
    #         #                 arcs_used.append(arc)
    #         #     else:   #ONLY 1 VERTEX
    #         #         if vertex not in arcs_used:
    #         #             self.arcs[assigned_vertices[vertex[0]]].append([assigned_vertices[vertex[0]], assigned_vertices[vertex[1]]])
    #         #             self.reverseArcs[assigned_vertices[vertex[1]]].append([assigned_vertices[vertex[1]], assigned_vertices[vertex[0]]])
    #         #             arcs_used.append(vertex)
    #
    #     #self.displayGraph()
    #
    #     print("SELF.VERTICES")
    #     print(self.vertices)
    #     print("SELF.ARCS")
    #     print(self.arcs)
    #     print("SELF.MULTILABELLEDVERTICES")
    #     print(self.multiLabelledVertices)
    #     print("RETICULATION VERTICES")
    #     print(reticulation_vertices)
    #
    #     self.vertices = temp_network.vertices
    #     self.root = temp_network.root
    #     self.arcs = temp_network.arcs
    #     self.reverseArcs = temp_network.reverseArcs

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

