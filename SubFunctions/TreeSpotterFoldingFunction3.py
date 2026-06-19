from copy import deepcopy

import graphviz
import networkx
from phylo2vec.base import to_vector

from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.MultiLabelledGraph import MultiLabelledGraph
from SubFunctions.Measures import *

class FoldingFunction3:

    def __init__(self, network, full_network):
        """

        :type network: PhylogeneticNetwork
        """
        self.network = network
        self.full_network = full_network
        self.convertedMergeVertices = []

    def startAlgorithm(self):
        N = self.network
        GN = N.makeBiPartiteGraph()
        MN = MultiLabelledGraph(N)

        simplifiedMN = MN.simplifyNetwork()
        # simplifiedMN.displayGraph()
        NPrime = self.foldNetworkSimplifiedMLGRandicCompare(simplifiedMN)

        if type(NPrime) == MultiLabelledGraph:
            NPrime = self.convertMLGToPhylogeneticNetwork(NPrime)

        max_vertex = max(self.full_network.vertices) + 1

        for vertex in self.convertedMergeVertices:
            NPrime = self.convertVertex(NPrime, vertex, max_vertex)
            max_vertex = max_vertex + 1

        # NPrime.displayGraph()

        NPrime.taxDict = N.taxDict

        return NPrime

    def startAlgorithmFullNetwork(self):
        N = self.network
        GN = N.makeBiPartiteGraph()
        MN = MultiLabelledGraph(N)

        simplifiedMN = MN.simplifyNetwork()
        NPrime = self.foldNetworkSimplifiedMLGRandicCompare(simplifiedMN)

        if type(NPrime) == MultiLabelledGraph:
            NPrime = self.convertMLGToPhylogeneticNetwork(NPrime)

        NPrime.taxDict = N.taxDict

        return NPrime


    def foldNetworkSimplifiedMLG(self, MN):
        """

        :type MN: MultiLabelledGraph
        """

        input_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        output_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        for i in range(len(MN.arcs)):
            output_arcs[i] = len(MN.arcs[i])
        for i in range(len(MN.reverseArcs)):
            input_arcs[i] = len(MN.reverseArcs[i])

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

        # print("TREE VERTICES")
        # print(tree_vertices)
        # print("LEAF VERTICES")
        # print(leaf_list)
        # print("Multi-Labelled-Vertices")
        # print(MN.multiLabelledVertices)

        networks_below_tree_vertices = []

        for vertex in tree_vertices:
            network_below_vertex = self.getNetworkBelowVertex(MN, vertex)
            networks_below_tree_vertices.append(network_below_vertex)
            # print("VERTEX")
            # print(vertex)
            # print("VERTEX NODES")
            # print(network_below_vertex.nodes)
            # print("VERTEX EDGES")
            # print(network_below_vertex.edges)

        networks_below_tree_vertices = sorted(networks_below_tree_vertices, key=lambda x: x.number_of_nodes(), reverse=True)
        tree_vertices = sorted(tree_vertices, key=lambda x: self.getNetworkBelowVertex(MN, x).number_of_nodes(), reverse=True)

        # for i in range(len(networks_below_tree_vertices)):
        #     network = networks_below_tree_vertices[i]
        #     print("NETWORK VERTICES")
        #     print(network.nodes)
        #     print("NETWORK EDGES")
        #     print(network.edges)
        #     print("TREE VERTEX")
        #     print(tree_vertices[i])

        is_it_equal_matrix = [[] for _ in range(len(networks_below_tree_vertices))]

        for i in range(len(networks_below_tree_vertices)):
            is_it_equal_matrix[i] = [[] for _ in range(len(tree_vertices))]
            for j in range(len(networks_below_tree_vertices)):
                if i != j:
                    graph1 = networks_below_tree_vertices[i]
                    graph2 = networks_below_tree_vertices[j]

                    if self.checkIfTwoGraphsAreIsomorphic(graph1, graph2) and self.checkIfTwoNetworksShareSameLeafToRootLength(graph1, graph2, MN):
                        is_it_equal_matrix[i][j].append(1)
                    else:
                        is_it_equal_matrix[i][j].append(0)
                else:
                    is_it_equal_matrix[i][j].append(0)

        # print("TREE VERTICES")
        # print(tree_vertices)
        #
        # print("MATRIX")
        # print(is_it_equal_matrix)

        # for i in range(len(is_it_equal_matrix)):
        #     print(is_it_equal_matrix[i])

        vertices_already_merged = []

        # MN.displayGraph()

        for i in range(len(is_it_equal_matrix)):
            if tree_vertices[i] not in vertices_already_merged:
                for j in range(len(is_it_equal_matrix)):
                    if tree_vertices[i] in MN.vertices and tree_vertices[j] in MN.vertices:
                        if is_it_equal_matrix[i][j][0] == 1:
                            # MN, vertices_merged = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], MN)
                            MN, vertices_merged = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], MN, tree_vertices[i], tree_vertices[j])
                            # print("I and J")
                            # print("i: " + str(tree_vertices[i]) + "\nj: " + str(tree_vertices[j]))
                            # print("VERTICES MERGED")
                            # print(vertices_merged)
                            for vertex in vertices_merged:
                                vertices_already_merged.append(vertex)

                            # if 134 in MN.vertices:
                            #     print("IT BROKE")

                            for vertex in vertices_merged:
                                if len(MN.multiLabelledVertices[vertex]) > 0:
                                    converted_vertex = MN.multiLabelledVertices[vertex][0]
                                    MN.reverseMultiLabelledVertices[converted_vertex].remove(vertex)
                                    MN.multiLabelledVertices[vertex] = []

        # MN.displayGraph()



        for i in range(len(MN.reverseMultiLabelledVertices)):
            if MN.reverseMultiLabelledVertices[i] not in tree_vertices:
                for vertex in MN.reverseMultiLabelledVertices[i]:
                    if vertex in MN.vertices and i in MN.vertices:
                        vertex_to_merge_to = vertex
                        MN = self.mergeTwoVertices2(i, vertex_to_merge_to, MN)

        MN = MN.simplifyNetwork()
        # MN.displayGraph()

        return MN


    def foldNetworkSimplifiedMLGRandicCompare(self, MN):
        """

        :type MN: MultiLabelledGraph
        """

        input_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        output_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        for i in range(len(MN.arcs)):
            output_arcs[i] = len(MN.arcs[i])
        for i in range(len(MN.reverseArcs)):
            input_arcs[i] = len(MN.reverseArcs[i])

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

        # print("TREE VERTICES")
        # print(tree_vertices)
        # print("LEAF VERTICES")
        # print(leaf_list)
        # print("Multi-Labelled-Vertices")
        # print(MN.multiLabelledVertices)

        networks_below_tree_vertices = []

        for vertex in tree_vertices:
            network_below_vertex = self.getNetworkBelowVertex(MN, vertex)
            networks_below_tree_vertices.append(network_below_vertex)
            # print("VERTEX")
            # print(vertex)
            # print("VERTEX NODES")
            # print(network_below_vertex.nodes)
            # print("VERTEX EDGES")
            # print(network_below_vertex.edges)

        networks_below_tree_vertices = sorted(networks_below_tree_vertices, key=lambda x: x.number_of_nodes(), reverse=True)
        tree_vertices = sorted(tree_vertices, key=lambda x: self.getNetworkBelowVertex(MN, x).number_of_nodes(), reverse=True)

        # for i in range(len(networks_below_tree_vertices)):
        #     network = networks_below_tree_vertices[i]
        #     print("NETWORK VERTICES")
        #     print(network.nodes)
        #     print("NETWORK EDGES")
        #     print(network.edges)
        #     print("TREE VERTEX")
        #     print(tree_vertices[i])

        is_it_equal_matrix = [[] for _ in range(len(networks_below_tree_vertices))]

        for i in range(len(networks_below_tree_vertices)):
            is_it_equal_matrix[i] = [[] for _ in range(len(tree_vertices))]
            for j in range(len(networks_below_tree_vertices)):
                if i != j:
                    graph1 = networks_below_tree_vertices[i]
                    graph2 = networks_below_tree_vertices[j]

                    # print("GRAPH1 EDGES")
                    # print(graph1.edges)
                    # print("GRAPH2 EDGES")
                    # print(graph2.edges)

                    # if graph1.edges == graph2.edges:
                    #     print("SAVED TIME")
                    #     is_it_equal_matrix[i][j].append(1)
                    if self.checkIfTwoGraphsAreIsomorphic(graph1, graph2) and self.checkIfTwoNetworksShareSameLeafToRootLength(graph1, graph2, MN):
                        is_it_equal_matrix[i][j].append(1)
                    else:
                        is_it_equal_matrix[i][j].append(0)
                else:
                    is_it_equal_matrix[i][j].append(0)

        # print("TREE VERTICES")
        # print(tree_vertices)
        #
        # print("MATRIX")
        # print(is_it_equal_matrix)
        #
        # for i in range(len(is_it_equal_matrix)):
        #     print(is_it_equal_matrix[i])

        vertices_already_merged = []

        # MN.displayGraph()

        for i in range(len(is_it_equal_matrix)):
            if tree_vertices[i] not in vertices_already_merged:
                for j in range(len(is_it_equal_matrix)):
                    if tree_vertices[i] in MN.vertices and tree_vertices[j] in MN.vertices:
                        if is_it_equal_matrix[i][j][0] == 1:
                            # MN, vertices_merged = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], MN)
                            #CHECK TO SEE WHICH MERGE GETS US CLOSER TO THE ORIGINAL NETWORK USING THE RANDIC INDEX IN MEASURE 1

                            MN1, vertices_merged1 = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], deepcopy(MN), tree_vertices[i], tree_vertices[j])
                            MN2, vertices_merged2 = self.mergeTwoNetworks2(networks_below_tree_vertices[j], networks_below_tree_vertices[i], deepcopy(MN), tree_vertices[j], tree_vertices[i])

                            MN1_Measure = measure1(MN1, self.network)
                            MN2_Measure = measure1(MN2, self.network)

                            if MN2_Measure > MN1_Measure:
                                MN = MN2
                                vertices_merged = vertices_merged2
                            else:
                                MN = MN1
                                vertices_merged = vertices_merged1

                            # MN, vertices_merged = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], MN, tree_vertices[i], tree_vertices[j])
                            # print("I and J")
                            # print("i: " + str(tree_vertices[i]) + "\nj: " + str(tree_vertices[j]))
                            # print("VERTICES MERGED")
                            # print(vertices_merged)
                            for vertex in vertices_merged:
                                vertices_already_merged.append(vertex)

                            # if 134 in MN.vertices:
                            #     print("IT BROKE")

                            for vertex in vertices_merged:
                                if len(MN.multiLabelledVertices[vertex]) > 0:
                                    converted_vertex = MN.multiLabelledVertices[vertex][0]
                                    MN.reverseMultiLabelledVertices[converted_vertex].remove(vertex)
                                    MN.multiLabelledVertices[vertex] = []

        # MN.displayGraph()



        for i in range(len(MN.reverseMultiLabelledVertices)):
            if MN.reverseMultiLabelledVertices[i] not in tree_vertices:
                for vertex in MN.reverseMultiLabelledVertices[i]:
                    if vertex in MN.vertices and i in MN.vertices:
                        vertex_to_merge_to = vertex

                        #CHECK TO SEE WHICH MERGE IS CLOSER TO ORIGINAL NETWORK
                        MN1 = self.mergeTwoVertices2(i, vertex_to_merge_to, deepcopy(MN))
                        MN2 = self.mergeTwoVertices2(vertex_to_merge_to, i, deepcopy(MN))

                        MN1_Vertex_Measure = measure1(MN1, self.network)
                        MN2_Vertex_Measure = measure1(MN2, self.network)

                        if MN2_Vertex_Measure < MN1_Vertex_Measure:
                            MN = MN2
                        else:
                            MN = MN1


                        # MN = self.mergeTwoVertices2(i, vertex_to_merge_to, MN)

        MN = MN.simplifyNetwork()
        # MN.displayGraph()

        return MN

    def mergeTwoVertices2(self, vertex1, vertex2, mlg):
        """

        :type mlg: MultiLabelledGraph
        """
        max_vertex = max(mlg.vertices)
        if max_vertex + 1 not in self.convertedMergeVertices:
            self.convertedMergeVertices.append(max_vertex + 1)

        vertex_above_vertex1 = mlg.reverseArcs[vertex1][0][1]
        vertex_above_vertex2 = mlg.reverseArcs[vertex2][0][1]

        #GET RID OF VERTEX2

        mlg.arcs[vertex2] = []
        mlg.reverseArcs[vertex2] = []
        mlg.arcs[vertex_above_vertex2].remove([vertex_above_vertex2, vertex2])
        mlg.vertices.remove(vertex2)

        #MAKE NEW VERTEX AND CONNECT IT TO VERTEX ABOVE VERTEX 1

        mlg.vertices.append(max_vertex + 1)
        mlg.arcs[vertex_above_vertex1].append([vertex_above_vertex1, max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, vertex_above_vertex1])
        #
        #CONNECT NEW VERTEX TO VERTEX 1

        mlg.arcs[max_vertex + 1].append([max_vertex + 1, vertex1])
        mlg.reverseArcs[vertex1].append([vertex1, max_vertex + 1])

        #REMOVE CONNECTION FROM VERTEX ABOVE VERTEX 1 TO VERTEX 1

        mlg.arcs[vertex_above_vertex1].remove([vertex_above_vertex1, vertex1])
        mlg.reverseArcs[vertex1].remove([vertex1, vertex_above_vertex1])

        #CONNECT VERTEX ABOVE VERTEX 2 TO NEW VERTEX

        mlg.arcs[vertex_above_vertex2].append([vertex_above_vertex2, max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, vertex_above_vertex2])

        if len(mlg.multiLabelledVertices[vertex1]) > 0:
            # print("CONVERTING")
            # print(vertex1)
            # print(mlg.multiLabelledVertices[vertex1][0])
            self.convertVertexMLG(mlg, vertex1, mlg.multiLabelledVertices[vertex1][0])

        return mlg


    def mergeTwoNetworks2(self, graph1, graph2, mlg, graph1_root, graph2_root):

        graph1_vertices = graph1.nodes
        graph2_vertices = graph2.nodes

        graph1_arcs = graph1.edges
        graph2_arcs = graph2.edges

        max_vertex = max(mlg.vertices)
        if max_vertex + 1 not in self.convertedMergeVertices:
            self.convertedMergeVertices.append(max_vertex + 1)

        # graph1_root = [n for n, d in graph1.in_degree() if d == 0]
        # graph2_root = [n for n, d in graph1.in_degree() if d == 0]

        # print(mlg.reverseArcs[graph2_root])

        #FIND VERTEX ABOVE GRAPH2ROOT AND VERTEX ABOVE GRAPH1ROOT

        # print("GRAPH1ROOT")
        # print(graph1_root)
        # print("GRAPH2ROOT")
        # print(graph2_root)
        # print(mlg.reverseMultiLabelledVertices[graph2_root])

        vertex_above_graph1_root = mlg.reverseArcs[graph1_root][0][1]
        vertex_above_graph2_root = mlg.reverseArcs[graph2_root][0][1]

        # print("VERTEX ABOVE GRAPH1 ROOT")
        # print(vertex_above_graph1_root)
        #
        # print("VERTEX ABOVE GRAPH2 ROOT")
        # print(vertex_above_graph2_root)

        #GET RID OF GRAPH2 FROM MLG

        for node in graph2_vertices:
            mlg.arcs[node] = []
            mlg.reverseArcs[node] = []
            # mlg.reverseMultiLabelledVertices[mlg.multiLabelledVertices[node][0]] = []
            # mlg.multiLabelledVertices[node] = []
            if node in mlg.vertices:
                mlg.vertices.remove(node)



        #MAKE VERTEX BETWEEN GRAPH1ROOT AND VERTEX ABOVE GRAPH1

        mlg.vertices.append(max_vertex + 1)

        #CONNECT VERTEX ABOVE GRAPH1_ROOT TO NEW VERTEX AND CONNECT NEW VERTEX TO GRAPH1ROOT

        mlg.arcs[vertex_above_graph1_root].append([vertex_above_graph1_root, max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, vertex_above_graph1_root])
        mlg.arcs[max_vertex + 1].append([max_vertex + 1, graph1_root])
        mlg.reverseArcs[graph1_root].append([graph1_root, max_vertex + 1])

        #REMOVE VERTEX FROM VERTEXABOVEGRAPH1 TO GRAPH1ROOT

        mlg.arcs[vertex_above_graph1_root].remove([vertex_above_graph1_root, graph1_root])
        mlg.reverseArcs[graph1_root].remove([graph1_root, vertex_above_graph1_root])

        #CONNECT VERTEX ABOVE GRAPH2ROOT TO NEW VERTEX

        mlg.arcs[vertex_above_graph2_root].append([vertex_above_graph2_root, max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, vertex_above_graph2_root])

        #REMOVE VERTEX FROM VERTEXABOVEGRAPH2 TO GRAPH2ROOT

        mlg.arcs[vertex_above_graph2_root].remove([vertex_above_graph2_root, graph2_root])

        max_vertex = max_vertex + 1

        # for vertex in graph1_vertices:
        #     if len(mlg.multiLabelledVertices[vertex]) > 0:
        #         print("CONVERTING")
        #         print(vertex)
        #         print(mlg.multiLabelledVertices[vertex][0])
        #         self.convertVertexMLG(mlg, vertex, mlg.multiLabelledVertices[vertex][0])

        return mlg, graph2_vertices




    def getNetworkBelowVertex(self, MN, vertex):

        vertices_below_vertex = MN.getVerticesBelowVertex(vertex, vertex, [])
        # vertices_below_vertex = MN.getVerticesBelowVertexNetworkX(vertex)

        if vertex not in vertices_below_vertex:
            vertices_below_vertex.append(vertex)

        vertices_below_vertex.sort()

        # print("VERTICES BELOW VERTEX")
        # print(vertices_below_vertex)
        # print(vertex)

        networkXGraph = networkx.DiGraph()
        for vertex in vertices_below_vertex:
            networkXGraph.add_node(vertex)
            for arc in MN.arcs[vertex]:
                networkXGraph.add_edge(arc[0], arc[1])

        # print("MN EDGES")
        # print(MN.arcs)
        #
        # print("NETWORKXGRAPH EDGES")
        # print(networkXGraph.edges)

        return networkXGraph

    def checkIfTwoNetworksShareSameLeafToRootLength(self, graph1, graph2, mlg):

        graph1_length_of_root_to_leaf = self.getLengthofRootToLeaves(graph1, mlg)
        graph2_length_of_root_to_leaf = self.getLengthofRootToLeaves(graph2, mlg)

        for i in range(len(graph1_length_of_root_to_leaf)):
            if len(graph1_length_of_root_to_leaf[i]) > 0:
                for j in range(len(graph1_length_of_root_to_leaf[i])):
                    if len(mlg.multiLabelledVertices[graph1_length_of_root_to_leaf[i][j]]) > 0:
                        graph1_length_of_root_to_leaf[i][j] = mlg.multiLabelledVertices[graph1_length_of_root_to_leaf[i][j]][0]

        for i in range(len(graph2_length_of_root_to_leaf)):
            if len(graph2_length_of_root_to_leaf[i]) > 0:
                for j in range(len(graph2_length_of_root_to_leaf[i])):
                    if len(mlg.multiLabelledVertices[graph2_length_of_root_to_leaf[i][j]]) > 0:
                        graph2_length_of_root_to_leaf[i][j] = mlg.multiLabelledVertices[graph2_length_of_root_to_leaf[i][j]][0]

        # print(graph1_length_of_root_to_leaf)
        # print(graph2_length_of_root_to_leaf)

        for i in range(len(graph1_length_of_root_to_leaf)):
            graph1_temp = graph1_length_of_root_to_leaf[i]
            graph1_temp.sort()
            graph2_temp = graph2_length_of_root_to_leaf[i]
            graph2_temp.sort()
            if graph1_temp != graph2_temp:
                return False

        return True

    def getLengthofRootToLeaves(self, graph1, mlg1):
        """
        :type mlg1: MultiLabelledGraph
        """
        leaf_list = [x for x in graph1.nodes() if graph1.out_degree(x) == 0 and graph1.in_degree(x) == 1]
        root = [n for n, d in graph1.in_degree() if d == 0]

        length_of_path_list = [[] for _ in range(100)]

        # print("GETLENGTHOFROOTTOLEAVES")
        #
        # print(graph1.nodes)
        # print(graph1.edges)
        # print(leaf_list)
        # print(root)

        for leaf in leaf_list:
            # print(leaf)
            path = networkx.all_simple_paths(graph1, root[0], leaf)
            path_list = []
            for vertex in path:
                path_list.append(path)
            if len(mlg1.reverseMultiLabelledVertices[leaf]) > 0:
                length_of_path_list[len(path_list)].append(mlg1.reverseMultiLabelledVertices[leaf][0])
            else:
                length_of_path_list[len(path_list)].append(leaf)

        return length_of_path_list

    def checkIfTwoGraphsAreIsomorphic(self, graph1, graph2):

        return networkx.is_isomorphic(graph1, graph2)




    def mergeTwoNetworks(self, graph1, graph2, mlg):
        """

        :type mlg: MultiLabelledGraph
        """
        graph1_nodes = graph1.nodes
        graph2_nodes = graph2.nodes

        graph1_arcs = graph1.edges
        graph2_arcs = graph2.edges

        graph1_root = [n for n, d in graph1.in_degree() if d == 0]
        graph2_root = [n for n, d in graph2.in_degree() if d == 0]

        max_vertex = max(mlg.vertices)
        if max_vertex + 1 not in self.convertedMergeVertices:
            self.convertedMergeVertices.append(max_vertex + 1)

        # print("MLG.REVERSEARCS[GRAPH1_ROOT]")
        # print(mlg.reverseArcs[graph1_root[0]])

        vertex_above_graph1_root = mlg.reverseArcs[graph1_root[0]][0][1]

        # print("GRAPH2NODES")
        # print(graph2_nodes)
        # print("GRAPH2ROOT")
        # print(graph2_root)

        for node in graph2_nodes:
            if node != graph2_root[0]:
                mlg.arcs[node] = []
                mlg.reverseArcs[node] = []
                if node in mlg.vertices:
                    mlg.vertices.remove(node)
            else:
                mlg.arcs[node] = []

        # print("REVERSEARCS")
        # print(mlg.reverseArcs)

        #create new vertex to connect to

        mlg.vertices.append(max_vertex + 1)

        #CONNECT VERTEX ABOVE TO NEW VERTEX

        mlg.arcs[vertex_above_graph1_root].append([vertex_above_graph1_root, max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, vertex_above_graph1_root])

        #CONNECT GRAPH2 ROOT TO NEW VERTEX

        mlg.arcs[graph2_root[0]].append([graph2_root[0], max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, graph2_root[0]])

        #CONNECT NEW VERTEX TO GRAPH1 ROOT

        mlg.arcs[max_vertex + 1].append([max_vertex + 1, graph1_root[0]])
        mlg.reverseArcs[graph1_root[0]].append([graph1_root[0], max_vertex + 1])

        #REMOVE OLD ARC FROM VERTEX ABOVE TO GRAPH1ROOT

        mlg.arcs[vertex_above_graph1_root].remove([vertex_above_graph1_root, graph1_root[0]])
        mlg.reverseArcs[graph1_root[0]].remove([graph1_root[0], vertex_above_graph1_root])

        #CONNECT GRAPH2 ROOT TO GRAPH1 ROOT

        # mlg.arcs[graph2_root[0]].append([graph2_root[0], graph1_root[0]])
        # mlg.reverseArcs[graph1_root[0]].append([graph1_root[0], graph2_root[0]])

        #GET RID OF GRAPH2 FROM MLG

        # print("GRAPH2ARCS")
        #
        # for arc in graph2_arcs:
        #     print(arc)

        return mlg, graph2_nodes

    def mergeTwoVertices(self, vertex1, vertex2, mlg):
        """

        :type mlg: MultiLabelledGraph
        """

        #GET VERTEX ABOVE VERTEX1

        # print("VERTEX 1")
        # print(vertex1)
        # print("VERTEX 2")
        # print(vertex2)
        # print(mlg.reverseArcs[vertex1])

        max_vertex = max(mlg.vertices)
        if max_vertex + 1 not in self.convertedMergeVertices:
            self.convertedMergeVertices.append(max_vertex + 1)

        # vertex_above = mlg.reverseArcs[vertex1][0][1]
        #
        # if [vertex_above, vertex2] not in mlg.arcs[vertex_above]:
        #     mlg.arcs[vertex_above].append([vertex_above, vertex2])
        #     mlg.reverseArcs[vertex2].append([vertex2, vertex_above])

        # mlg.displayGraph()

        #GET VERTEX ABOVE VERTEX1
        vertex_above_vertex1 = mlg.reverseArcs[vertex1][0][1]

        #MAKE NEW VERTEX
        mlg.vertices.append(max_vertex + 1)

        #CONNECT VERTEX ABOVE VERTEX1 TO NEW VERTEX
        mlg.arcs[vertex_above_vertex1].append([vertex_above_vertex1, max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, vertex_above_vertex1])

        #CONNECT NEW VERTEX TO VERTEX1
        mlg.arcs[max_vertex + 1].append([max_vertex + 1, vertex1])
        mlg.reverseArcs[vertex1].append([vertex1, max_vertex + 1])

        #CONNECT VERTEX2 TO NEW VERTEX
        mlg.arcs[vertex2].append([vertex2, max_vertex + 1])
        mlg.reverseArcs[max_vertex + 1].append([max_vertex + 1, vertex2])

        #REMOVE ARC FROM VERTEX ABOVE VERTEX1 TO VERTEX1
        mlg.arcs[vertex_above_vertex1].remove([vertex_above_vertex1, vertex1])
        mlg.reverseArcs[vertex1].remove([vertex1, vertex_above_vertex1])

        # mlg.arcs[vertex2].append([vertex2, vertex1])
        # mlg.reverseArcs[vertex1].append([vertex1, vertex2])

        return mlg

    def convertMLGToPhylogeneticNetwork(self, mlg):
        """

        :type mlg: MultiLabelledGraph
        """
        vertex_list = mlg.vertices

        arc_list = []

        for vertex in mlg.arcs:
            for arc in vertex:
                arc_list.append(arc)

        for vertex in mlg.vertices:
            if len(mlg.arcs[vertex]) == 0 and len(mlg.reverseArcs[vertex]) == 0:
                mlg.vertices.remove(vertex)

        root = mlg.root

        # print("ARC LIST")
        # print(arc_list)
        # print(mlg.arcs)

        NPrime = PhylogeneticNetwork(vertex_list, arc_list, root)

        return NPrime

    def networkBelowVertexToVector(self, MN, input_vertex):
        """

        :type MN: MultiLabelledGraph
        """
        vertices_below_vertex = MN.getVerticesBelowVertex(input_vertex, input_vertex, [])
        # vertices_below_vertex = MN.getVerticesBelowVertexNetworkX(vertex)

        if input_vertex not in vertices_below_vertex:
            vertices_below_vertex.append(input_vertex)

        vertices_below_vertex.sort()

        vertex_set_before = []
        vertex_set_converted = []

        # MN.

        # self.multiLabelledVertices[current_vertex + 1].append(vertex)

        for vertex in vertices_below_vertex:
            if len(MN.multiLabelledVertices[vertex]) > 0:
                vertex_set_before.append(vertex)
                vertex_set_converted.append(MN.multiLabelledVertices[vertex][0])
            # else:
            #     vertex_set_converted.append(vertex)

        # vertex_set_converted.sort()

        arc_list = []

        for vertex in vertices_below_vertex:
            for arc in MN.arcs[vertex]:
                first_vertex = arc[0]
                second_vertex = arc[1]

                # if len(MN.multiLabelledVertices[first_vertex]) > 0:
                #     first_vertex = MN.multiLabelledVertices[first_vertex][0]
                # if len(MN.multiLabelledVertices[second_vertex]) > 0:
                #     second_vertex = MN.multiLabelledVertices[second_vertex][0]

                arc_list.append([first_vertex, second_vertex])

        phy_network = PhylogeneticNetwork(vertices_below_vertex, arc_list, input_vertex)

        root = input_vertex
        # find all leaves of the graph
        self.leafs = []
        for i in range(len(phy_network.arcs)):
            if len(phy_network.arcs[i]) == 0 and len(phy_network.reverseArcs[i]) > 0:
                self.leafs.append(i)
        nexus_array = []
        self.recursiveTreeNetworkToNEXUS(nexus_array, root, phy_network)

        nexus_string = str(nexus_array)

        # for i in range(len(vertex_set_before)):
        #     nexus_string = nexus_string.replace(str(vertex_set_before[i]), str(vertex_set_converted[i]))

        nexus_string = nexus_string.replace("[", "(")
        nexus_string = nexus_string.replace("]", ")")
        nexus_string = nexus_string.replace(" ", "")

        nexus_string = nexus_string + ";"

        print(nexus_string)

        vec_string = to_vector(nexus_string)

        # vec_string = phylo2vec.base.to_vector(nexus_string)

        return vec_string

    def recursiveTreeNetworkToNEXUS(self, nexus_string, current_vertex, phy_network):
        for i in range(len(phy_network.arcs[current_vertex])):
            #IF NEXT VERTEX IS A LEAF
            if phy_network.arcs[current_vertex][i][1] in self.leafs:
                nexus_string.append(phy_network.arcs[current_vertex][i][1])
            else:
                nexus_string.append([])
                self.recursiveTreeNetworkToNEXUS(nexus_string[i], phy_network.arcs[current_vertex][i][1], phy_network)

    def foldNetworkSimplifiedMLGRandicCompare2(self, MN):
        """

        :type MN: MultiLabelledGraph
        """

        input_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        output_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        for i in range(len(MN.arcs)):
            output_arcs[i] = len(MN.arcs[i])
        for i in range(len(MN.reverseArcs)):
            input_arcs[i] = len(MN.reverseArcs[i])

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

        # print("TREE VERTICES")
        # print(tree_vertices)
        # print("LEAF VERTICES")
        # print(leaf_list)
        # print("Multi-Labelled-Vertices")
        # print(MN.multiLabelledVertices)

        networks_below_tree_vertices = []



        for vertex in tree_vertices:
            network_below_vertex = self.networkBelowVertexToVector(MN, vertex)
            networks_below_tree_vertices.append(network_below_vertex)
            # print("VERTEX")
            # print(vertex)
            # print("VERTEX NODES")
            # print(network_below_vertex.nodes)
            # print("VERTEX EDGES")
            # print(network_below_vertex.edges)

        networks_below_tree_vertices = sorted(networks_below_tree_vertices, key=lambda x: x.number_of_nodes(), reverse=True)
        tree_vertices = sorted(tree_vertices, key=lambda x: self.networkBelowVertexToVector(MN, x).size(), reverse=True)

        # for i in range(len(networks_below_tree_vertices)):
        #     network = networks_below_tree_vertices[i]
        #     print("NETWORK VERTICES")
        #     print(network.nodes)
        #     print("NETWORK EDGES")
        #     print(network.edges)
        #     print("TREE VERTEX")
        #     print(tree_vertices[i])

        is_it_equal_matrix = [[] for _ in range(len(networks_below_tree_vertices))]

        for i in range(len(networks_below_tree_vertices)):
            is_it_equal_matrix[i] = [[] for _ in range(len(tree_vertices))]
            for j in range(len(networks_below_tree_vertices)):
                if i != j:
                    vector1 = networks_below_tree_vertices[i]
                    vector2 = networks_below_tree_vertices[j]

                    if vector1 == vector2:
                        print("SAVED TIME")
                        is_it_equal_matrix[i][j].append(1)
                    else:
                        is_it_equal_matrix.append(0)

                    # print("GRAPH1 EDGES")
                    # print(graph1.edges)
                    # print("GRAPH2 EDGES")
                    # print(graph2.edges)

                    # if graph1.edges == graph2.edges:
                    #     print("SAVED TIME")
                    #     is_it_equal_matrix[i][j].append(1)
                    # if self.checkIfTwoGraphsAreIsomorphic(graph1, graph2) and self.checkIfTwoNetworksShareSameLeafToRootLength(graph1, graph2, MN):
                    #     is_it_equal_matrix[i][j].append(1)
                    # else:
                    #     is_it_equal_matrix[i][j].append(0)
                else:
                    is_it_equal_matrix[i][j].append(0)

        # print("TREE VERTICES")
        # print(tree_vertices)
        #
        # print("MATRIX")
        # print(is_it_equal_matrix)
        #
        # for i in range(len(is_it_equal_matrix)):
        #     print(is_it_equal_matrix[i])

        vertices_already_merged = []

        # MN.displayGraph()

        for i in range(len(is_it_equal_matrix)):
            if tree_vertices[i] not in vertices_already_merged:
                for j in range(len(is_it_equal_matrix)):
                    if tree_vertices[i] in MN.vertices and tree_vertices[j] in MN.vertices:
                        if is_it_equal_matrix[i][j][0] == 1:
                            # MN, vertices_merged = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], MN)
                            #CHECK TO SEE WHICH MERGE GETS US CLOSER TO THE ORIGINAL NETWORK USING THE RANDIC INDEX IN MEASURE 1

                            MN1, vertices_merged1 = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], deepcopy(MN), tree_vertices[i], tree_vertices[j])
                            MN2, vertices_merged2 = self.mergeTwoNetworks2(networks_below_tree_vertices[j], networks_below_tree_vertices[i], deepcopy(MN), tree_vertices[j], tree_vertices[i])

                            MN1_Measure = measure1(MN1, self.network)
                            MN2_Measure = measure1(MN2, self.network)

                            if MN2_Measure < MN1_Measure:
                                MN = MN2
                                vertices_merged = vertices_merged2
                            else:
                                MN = MN1
                                vertices_merged = vertices_merged1

                            # MN, vertices_merged = self.mergeTwoNetworks2(networks_below_tree_vertices[i], networks_below_tree_vertices[j], MN, tree_vertices[i], tree_vertices[j])
                            # print("I and J")
                            # print("i: " + str(tree_vertices[i]) + "\nj: " + str(tree_vertices[j]))
                            # print("VERTICES MERGED")
                            # print(vertices_merged)
                            for vertex in vertices_merged:
                                vertices_already_merged.append(vertex)

                            # if 134 in MN.vertices:
                            #     print("IT BROKE")

                            for vertex in vertices_merged:
                                if len(MN.multiLabelledVertices[vertex]) > 0:
                                    converted_vertex = MN.multiLabelledVertices[vertex][0]
                                    MN.reverseMultiLabelledVertices[converted_vertex].remove(vertex)
                                    MN.multiLabelledVertices[vertex] = []

        # MN.displayGraph()



        for i in range(len(MN.reverseMultiLabelledVertices)):
            if MN.reverseMultiLabelledVertices[i] not in tree_vertices:
                for vertex in MN.reverseMultiLabelledVertices[i]:
                    if vertex in MN.vertices and i in MN.vertices:
                        vertex_to_merge_to = vertex

                        #CHECK TO SEE WHICH MERGE IS CLOSER TO ORIGINAL NETWORK
                        MN1 = self.mergeTwoVertices2(i, vertex_to_merge_to, deepcopy(MN))
                        MN2 = self.mergeTwoVertices2(vertex_to_merge_to, i, deepcopy(MN))

                        MN1_Vertex_Measure = measure1(MN1, self.network)
                        MN2_Vertex_Measure = measure1(MN2, self.network)

                        if MN2_Vertex_Measure < MN1_Vertex_Measure:
                            MN = MN2
                        else:
                            MN = MN1


                        # MN = self.mergeTwoVertices2(i, vertex_to_merge_to, MN)

        MN = MN.simplifyNetwork()
        # MN.displayGraph()

        return MN

    def convertVertex(self, network, vertex1, vertex2):
        """

        :type network: PhylogeneticNetwork
        """
        #AIM TO CONVERT VERTEX 1 INDEX TO VERTEX 2 INDEX

        #GET ALL ARCS GOING AWAY FROM VERTEX 1
        outgoing_arcs = []
        for arc in network.arcs[vertex1]:
            outgoing_arcs.append(arc)
        incoming_arcs = []
        for arc in network.reverseArcs[vertex1]:
            incoming_arcs.append(arc)

        for arc in outgoing_arcs:
            network.createArc([vertex2, arc[1]])

        for reverse_arc in incoming_arcs:
            network.createArc([reverse_arc[1], vertex2])

        for arc in outgoing_arcs:
            network.removeArc(arc)

        for reverse_arc in incoming_arcs:
            network.removeArc([reverse_arc[1], reverse_arc[0]])

        network.vertices.remove(vertex1)

        return network

    def convertVertexMLG(self, mlg, vertex1, vertex2):
        """

        :type mlg: MultiLabelledGraph
        """
        outgoing_arcs = []
        for arc in mlg.arcs[vertex1]:
            outgoing_arcs.append(arc)
        incoming_arcs = []
        for arc in mlg.reverseArcs[vertex1]:
            incoming_arcs.append(arc)

        for arc in outgoing_arcs:
            mlg.createArc([vertex2, arc[1]])

        for reverse_arc in incoming_arcs:
            mlg.createArc([reverse_arc[1], vertex2])

        for arc in outgoing_arcs:
            mlg.removeArc(arc)

        for reverse_arc in incoming_arcs:
            mlg.removeArc([reverse_arc[1], reverse_arc[0]])

        mlg.vertices.remove(vertex1)

        return mlg

    def foldNetworkSimplifiedMLGRandicCompare2(self, MN):
        input_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        output_arcs = [0 for _ in range(len(MN.arcs) + 1)]
        for i in range(len(MN.arcs)):
            output_arcs[i] = len(MN.arcs[i])
        for i in range(len(MN.reverseArcs)):
            input_arcs[i] = len(MN.reverseArcs[i])

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

        networks_below_tree_vertices = []

        for vertex in tree_vertices:
            network_below_vertex = self.getNetworkBelowVertex(MN, vertex)
            networks_below_tree_vertices.append(network_below_vertex)
            # print("VERTEX")
            # print(vertex)
            # print("VERTEX NODES")
            # print(network_below_vertex.nodes)
            # print("VERTEX EDGES")
            # print(network_below_vertex.edges)

        networks_below_tree_vertices = sorted(networks_below_tree_vertices, key=lambda x: x.number_of_nodes(),
                                              reverse=True)
        tree_vertices = sorted(tree_vertices, key=lambda x: self.getNetworkBelowVertex(MN, x).number_of_nodes(),
                               reverse=True)

        # for i in range(len(networks_below_tree_vertices)):
        #     network = networks_below_tree_vertices[i]
        #     print("NETWORK VERTICES")
        #     print(network.nodes)
        #     print("NETWORK EDGES")
        #     print(network.edges)
        #     print("TREE VERTEX")
        #     print(tree_vertices[i])

        is_it_equal_matrix = [[] for _ in range(len(networks_below_tree_vertices))]

        for i in range(len(networks_below_tree_vertices)):
            is_it_equal_matrix[i] = [[] for _ in range(len(tree_vertices))]
            for j in range(len(networks_below_tree_vertices)):
                if i != j:
                    graph1 = networks_below_tree_vertices[i]
                    graph2 = networks_below_tree_vertices[j]

                    # print("GRAPH1 EDGES")
                    # print(graph1.edges)
                    # print("GRAPH2 EDGES")
                    # print(graph2.edges)

                    # if graph1.edges == graph2.edges:
                    #     print("SAVED TIME")
                    #     is_it_equal_matrix[i][j].append(1)
                    if self.checkIfTwoGraphsAreIsomorphic(graph1,
                                                          graph2) and self.checkIfTwoNetworksShareSameLeafToRootLength(
                            graph1, graph2, MN):
                        is_it_equal_matrix[i][j].append(1)
                    else:
                        is_it_equal_matrix[i][j].append(0)
                else:
                    is_it_equal_matrix[i][j].append(0)



