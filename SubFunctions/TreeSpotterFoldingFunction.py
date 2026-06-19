from copy import deepcopy

from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.BiPartiteGraph import BiPartiteGraph
from SubFunctions.MultiLabelledGraph import MultiLabelledGraph

class FoldingFunction:
    def __init__(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        self.network = network

    def runAlgorithm(self):
        N = self.network
        GN = N.makeBiPartiteGraph()

        # CHECK FOR CROSS PATTERN ON BIPARTITE GRAPH

        fvl, fel = self.GetForbiddenConfigurations(GN)
        cvl, ctvl, crvl = self.convertBPGVerticesToNetworkVertices(fvl, GN, N)
        if self.checkForbiddenConfiguration2(ctvl, crvl, N):
            FN = self.replaceForbiddenConfiguration2(ctvl, crvl, N)
        else:
            FN = self.replaceForbiddenConfiguration1(ctvl, crvl, N)
        #FN.displayGraph()

        mlg = MultiLabelledGraph(FN)

        FoldedNetwork = self.FoldNetwork(mlg, FN)

        return FoldedNetwork

    def GetForbiddenConfigurations(self, bpg):
        """

        :type bpg: BiPartiteGraph
        """

        # bpg.displayGraph()

        cc = bpg.getConnectedComponents()

        ## print(cc)
        ## print(bpg.U)
        ## print(bpg.V)
        ## print(bpg.edges)

        input_edges = []
        output_edges = []

        edges_list = []
        for i in range(len(bpg.edges)):
            if len(bpg.edges[i]) > 0:
                for j in range(len(bpg.edges[i])):
                    edges_list.append([i, (bpg.U + bpg.edges[i][j])])

        ## print(edges_list)

        new_arcs_list = [[] for _ in range(bpg.U+bpg.V)]

        for edge in edges_list:
            new_arcs_list[edge[0]].append(edge[1])

        forbiddenConfigArray = []
        forbiddenEdgeList = []
        forbiddenVertexList = []

        for i in range(len(new_arcs_list)):
            if len(new_arcs_list[i]) == 2:
                for j in range(len(new_arcs_list)):
                    if len(new_arcs_list[j]) == 2:
                        if i != j:
                            if new_arcs_list[i] == new_arcs_list[j]:
                                for vertex in new_arcs_list[i]:
                                    if [i, vertex] not in forbiddenEdgeList:
                                        forbiddenEdgeList.append([i, vertex])
                                    if i not in forbiddenVertexList:
                                        forbiddenVertexList.append(i)
                                    if vertex not in forbiddenVertexList:
                                        forbiddenVertexList.append(vertex)
                                for vertex in new_arcs_list[j]:
                                    if [j, vertex] not in forbiddenEdgeList:
                                        forbiddenEdgeList.append([j, vertex])
                                    if j not in forbiddenVertexList:
                                        forbiddenVertexList.append(j)
                                    if vertex not in forbiddenVertexList:
                                        forbiddenVertexList.append(vertex)

        ## print("FORBIDDEN EDGE LIST")
        ## print(forbiddenEdgeList)
        ## print("FORBIDDEN VERTEX LIST")
        ## print(forbiddenVertexList)

        return forbiddenVertexList, forbiddenEdgeList

    def convertBPGVerticesToNetworkVertices(self, BPG_Vertices, bpg, network):
        vertex_in_degree = [0] * (max(network.vertices) + 1)
        vertex_out_degree = [0] * (max(network.vertices) + 1)

        for vertex in network.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in network.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in network.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = [0]
        reticulation_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in network.arcs[i]:
                    if arc[1] in network.leafs:
                        leaf_below = True
                        break
                if not leaf_below:
                    tree_vertex_array.append(i)
            if vertex_in_degree[i] >= 2 and vertex_out_degree[i] == 1:
                reticulation_vertex_array.append(i)

        connected_tree_vertices = [0]
        connected_reticulation_vertices = [0]
        connected_edge_list = []

        for i in range(len(tree_vertex_array)):
            for j in range(len(reticulation_vertex_array)):
                if [tree_vertex_array[i], reticulation_vertex_array[j]] in network.arcs[tree_vertex_array[i]]:
                    if tree_vertex_array[i] not in connected_tree_vertices:
                        connected_tree_vertices.append(tree_vertex_array[i])
                    if reticulation_vertex_array[j] not in connected_reticulation_vertices:
                        connected_reticulation_vertices.append(reticulation_vertex_array[j])

        ## print("CONNECTED TREE VERTICES")
        ## print(connected_tree_vertices)

        for i in range(len(connected_tree_vertices)):
            if i != 0:
                for j in range(len(connected_reticulation_vertices)):
                    if j != 0:
                        if [connected_tree_vertices[i], connected_reticulation_vertices[j]] in network.arcs[connected_tree_vertices[i]]:
                            connected_edge_list.append([i, j])

        ## print("CONNECTED EDGE LIST")
        ## print(connected_edge_list)

        converted_vertex_set = []
        converted_reticulation_set = []
        converted_tree_set = []

        for vertex in BPG_Vertices:
            if vertex > bpg.U:
                converted_vertex_set.append(connected_reticulation_vertices[vertex - bpg.U])
                converted_reticulation_set.append(connected_reticulation_vertices[vertex - bpg.U])
            else:
                converted_vertex_set.append(connected_tree_vertices[vertex])
                converted_tree_set.append(connected_tree_vertices[vertex])

        ## print("CONVERTED VERTEX SET")
        ## print(converted_vertex_set)

        return converted_vertex_set, converted_tree_set, converted_reticulation_set

    def checkForbiddenConfiguration2(self, cvtl, cvrl, network):
        """

        :type network: PhylogeneticNetwork
        """
        arc_list = [[] for _ in range(len(cvrl))]

        for i in range(len(cvrl)):
            for arc in network.arcs[cvrl[i]]:
                arc_list[i].append(arc[1])

        if arc_list[0] == arc_list[1]:
            return True
        else:
            return False

    def replaceForbiddenConfiguration1(self, tree_vertex_list, reticulation_vertex_list, network):
        N = deepcopy(network)

        N.arcs[tree_vertex_list[0]].remove([tree_vertex_list[0], reticulation_vertex_list[0]])
        N.arcs[tree_vertex_list[0]].remove([tree_vertex_list[0], reticulation_vertex_list[1]])
        N.reverseArcs[reticulation_vertex_list[0]].remove([reticulation_vertex_list[0], tree_vertex_list[0]])
        N.reverseArcs[reticulation_vertex_list[1]].remove([reticulation_vertex_list[1], tree_vertex_list[0]])

        N.arcs[tree_vertex_list[1]].remove([tree_vertex_list[1], reticulation_vertex_list[0]])
        N.arcs[tree_vertex_list[1]].remove([tree_vertex_list[1], reticulation_vertex_list[1]])
        N.reverseArcs[reticulation_vertex_list[0]].remove([reticulation_vertex_list[0], tree_vertex_list[1]])
        N.reverseArcs[reticulation_vertex_list[1]].remove([reticulation_vertex_list[1], tree_vertex_list[1]])

        N.arcs[tree_vertex_list[0]].append([tree_vertex_list[0], reticulation_vertex_list[0]])
        N.arcs[tree_vertex_list[1]].append([tree_vertex_list[1], reticulation_vertex_list[0]])
        N.reverseArcs[reticulation_vertex_list[0]].append([reticulation_vertex_list[0], tree_vertex_list[0]])
        N.reverseArcs[reticulation_vertex_list[0]].append([reticulation_vertex_list[0], tree_vertex_list[1]])

        for arc in N.arcs[reticulation_vertex_list[0]]:
            N.arcs[reticulation_vertex_list[1]].append([reticulation_vertex_list[1], arc[1]])
            N.reverseArcs[arc[1]].append([arc[1], reticulation_vertex_list[1]])

            N.arcs[reticulation_vertex_list[0]].remove(arc)
            N.reverseArcs[arc[1]].remove([arc[1], arc[0]])

        N.arcs[reticulation_vertex_list[0]].append([reticulation_vertex_list[0], reticulation_vertex_list[1]])
        N.reverseArcs[reticulation_vertex_list[1]].append([reticulation_vertex_list[1], reticulation_vertex_list[0]])

        # for arc in N.arcs[re]

        # N.arcs[tree_vertex_list[0]].append([tree_vertex_list[0], tree_vertex_list[1]])
        # N.arcs[tree_vertex_list[1]].append([tree_vertex_list[1], reticulation_vertex_list[0]])
        # N.reverseArcs[tree_vertex_list[1]].append([tree_vertex_list[1], tree_vertex_list[0]])
        # N.reverseArcs[reticulation_vertex_list[0]].append([reticulation_vertex_list[0], tree_vertex_list[1]])
        #
        # for arc in N.arcs[reticulation_vertex_list[1]]:
        #     N.arcs[reticulation_vertex_list[0]].append([reticulation_vertex_list[0], arc[1]])
        #     N.reverseArcs[arc[1]].append([arc[1], reticulation_vertex_list[0]])
        #     N.arcs[reticulation_vertex_list[1]].remove(arc)
        #     N.reverseArcs[arc[1]].remove([arc[1], arc[0]])

        return N

    def replaceForbiddenConfiguration2(self, tree_vertex_list, reticulation_vertex_list, network):
        print("FORBIDDEN CONFIGURATION 2")
    def FoldNetwork(self, mlg, network):
        """

        :type network: PhylogeneticNetwork
        :type mlg: MultiLabelledGraph
        """

        # mlg.displayGraph()

        ## print("MLG.MULTILABELLEDVERTICES")
        ## print(mlg.multiLabelledVertices)

        ## print("MLG.REVERSEMULTILABELLEDVERTICES")
        ## print(mlg.reverseMultiLabelledVertices)

        for i in range(len(mlg.reverseMultiLabelledVertices)):
            if len(mlg.reverseMultiLabelledVertices[i]) > 0:
                first_arc_list = mlg.getArcListOfNetworkBelowVertex(i)
                for mlv in mlg.reverseMultiLabelledVertices[i]:
                    second_arc_list = mlg.getArcListOfNetworkBelowVertex(mlv)
                    if first_arc_list == second_arc_list:
                        #GET RID OF VERTICES BELOW THE SECOND VERTEX
                        mlg.removeNetworkBelowVertex(mlv)







