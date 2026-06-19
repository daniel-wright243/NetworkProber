from copy import deepcopy

import graphviz
import networkx

from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.BiPartiteGraph import BiPartiteGraph
from SubFunctions.MultiLabelledGraph import MultiLabelledGraph


class FoldingFunction2:

    def __init__(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        self.network = network

    def startAlgorithm(self):
        N = self.network
        GN = N.makeBiPartiteGraph()
        # GN.displayGraph()
        fn_exists, fn_tree_vertices, fn_reticulation_vertices, fn_edges = self.checkForForbiddenConfiguration1(N, GN)
        if fn_exists:
            for i in range(len(fn_tree_vertices)):
                if self.checkForbiddenConfiguration2(fn_tree_vertices[i], fn_reticulation_vertices[i], N):
                    N = self.replaceForbiddenConfiguration2(fn_tree_vertices[i], fn_reticulation_vertices[i], N)
                    #N.displayGraph()
                    ## print("FORBIDDEN CONFIGURATION 2")
                else:
                    N = self.replaceForbiddenConfiguration1(fn_tree_vertices[i], fn_reticulation_vertices[i], N)
                    #N.displayGraph()
                    ## print("FORBIDDEN CONFIGURATION 1")
        # N.displayGraph()
        # RESOLVE THE REST OF THE NETWORK
        MN = MultiLabelledGraph(N)
        # MN.displayGraph()

        NPrime = self.foldNetworkSimplifiedMLG(MN)

        if type(NPrime) == MultiLabelledGraph:
            NPrime = self.convertMLGToPhylogeneticNetwork(NPrime)

        return NPrime

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

        ## print("ARC LIST")
        ## print(arc_list)
        ## print(mlg.arcs)

        NPrime = PhylogeneticNetwork(vertex_list, arc_list, root)

        return NPrime

    def checkForForbiddenConfiguration1(self, N, GN):
        input_edges = []
        output_edges = []

        edges_list = []
        for i in range(len(GN.edges)):
            if len(GN.edges[i]) > 0:
                for j in range(len(GN.edges[i])):
                    edges_list.append([i, (GN.U + GN.edges[i][j])])

        ## print(edges_list)

        new_arcs_list = [[] for _ in range(GN.U + GN.V)]

        for edge in edges_list:
            new_arcs_list[edge[0]].append(edge[1])

        total_tree_vertex_array = []
        total_reticulation_vertex_array = []
        total_edge_array = []

        for i in range(len(new_arcs_list)):
            temp_tree_vertex_list = []
            temp_reticulation_vertex_list = []
            temp_edge_list = []
            for j in range(len(new_arcs_list)):
                if i != j:
                    if len(new_arcs_list[i]) == 2 and len(new_arcs_list[j]) == 2:
                        if new_arcs_list[i] == new_arcs_list[j]:
                            if i not in temp_tree_vertex_list:
                                temp_tree_vertex_list.append(i)
                            if j not in temp_tree_vertex_list:
                                temp_tree_vertex_list.append(j)
            for tree_vertex in temp_tree_vertex_list:
                for vertex in new_arcs_list[tree_vertex]:
                    if [tree_vertex, vertex] not in temp_edge_list:
                        temp_edge_list.append([tree_vertex, vertex])
                    if vertex not in temp_reticulation_vertex_list:
                        temp_reticulation_vertex_list.append(vertex)

            if len(temp_tree_vertex_list) > 0:
                temp_tree_vertex_list.sort()
                if temp_tree_vertex_list not in total_tree_vertex_array:
                    total_tree_vertex_array.append(temp_tree_vertex_list)
                    temp_reticulation_vertex_list.sort()
                    total_reticulation_vertex_array.append(temp_reticulation_vertex_list)
                    temp_edge_list.sort()
                    total_edge_array.append(temp_edge_list)


        ## print("TOTAL TREE VERTEX ARRAY")
        ## print(total_tree_vertex_array)
        ## print("TOTAL RETICULATION VERTEX ARRAY")
        ## print(total_reticulation_vertex_array)
        ## print("TOTAL EDGE VERTEX ARRAY")
        ## print(total_edge_array)

        vertex_in_degree = [0] * (max(N.vertices) + 1)
        vertex_out_degree = [0] * (max(N.vertices) + 1)

        for vertex in N.arcs:
            if len(vertex) > 0:
                for arcs in vertex:
                    if arcs[0] in N.vertices:
                        vertex_out_degree[arcs[0]] = vertex_out_degree[arcs[0]] + 1
                    if arcs[1] in N.vertices:
                        vertex_in_degree[arcs[1]] = vertex_in_degree[arcs[1]] + 1

        tree_vertex_array = [0]
        reticulation_vertex_array = []

        for i in range(len(vertex_in_degree)):
            if vertex_in_degree[i] == 1 and vertex_out_degree[i] >= 2:
                leaf_below = False
                for arc in N.arcs[i]:
                    if arc[1] in N.leafs:
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
                if [tree_vertex_array[i], reticulation_vertex_array[j]] in N.arcs[tree_vertex_array[i]]:
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
                        if [connected_tree_vertices[i], connected_reticulation_vertices[j]] in N.arcs[connected_tree_vertices[i]]:
                            connected_edge_list.append([i, j])

        ## print("CONNECTED EDGE LIST")
        ## print(connected_edge_list)

        converted_tree_set = []
        converted_reticulation_set = []
        converted_edge_set = []
        if len(total_tree_vertex_array) > 0:
            if type(total_tree_vertex_array[0]) == list:
                for set in total_tree_vertex_array:
                    new_set = []
                    for vertex in set:
                        new_set.append(connected_tree_vertices[vertex - GN.U])
                    converted_tree_set.append(new_set)

            if type(total_reticulation_vertex_array[0]) == list:
                for set in total_reticulation_vertex_array:
                    new_set = []
                    for vertex in set:
                        new_set.append(connected_reticulation_vertices[vertex - GN.U])
                    converted_reticulation_set.append(new_set)

            if type(total_edge_array[0]) == list:
                for set in total_edge_array:
                    new_set = []
                    for edge in set:
                        new_edge = []
                        new_edge.append(connected_tree_vertices[edge[0] - GN.U])
                        new_edge.append(connected_reticulation_vertices[edge[1] - GN.U])
                        new_set.append(new_edge)
                    converted_edge_set.append(new_set)


        ## print("CONVERTED TREE SET")
        ## print(converted_tree_set)

        ## print("CONVERTED RETICULATION SET")
        ## print(converted_reticulation_set)

        ## print("CONVERTED EDGE SET")
        ## print(converted_edge_set)

        if len(converted_tree_set) > 0:
            exists = True
        else:
            exists = False

        return exists, converted_tree_set, converted_reticulation_set, converted_edge_set

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
        """

        :type network: PhylogeneticNetwork
        """

        N = deepcopy(network)

        amount_of_multi_arcs = len(tree_vertex_list)

        if amount_of_multi_arcs > 1:
            if amount_of_multi_arcs == 2: # STANDARD FORBIDDEN CONFIGURATION 1
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
            else: # EXTENDED FORBIDDEN CONFIGURATION 1
                ## print("EXTENDED FORBIDDEN CONFIGURATION")
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
                N.reverseArcs[reticulation_vertex_list[1]].append(
                    [reticulation_vertex_list[1], reticulation_vertex_list[0]])

                for i in range(2, amount_of_multi_arcs):
                    #REMOVE OLD ARCS FROM ADDITIONAL MULTIARCS TO RETICULATION VERTICES 2

                    N.arcs[tree_vertex_list[i]].remove([tree_vertex_list[i], reticulation_vertex_list[1]])
                    N.reverseArcs[reticulation_vertex_list[1]].remove([reticulation_vertex_list[1], tree_vertex_list[i]])

            return N

    def replaceForbiddenConfiguration2(self, tree_vertex_list, reticulation_vertex_list, network):
        """

        :type network: PhylogeneticNetwork
        """

        N = deepcopy(network)

        amount_of_multiarcs = len(tree_vertex_list)

        if amount_of_multiarcs > 1:
            if amount_of_multiarcs == 2:
                vertex_above = N.reverseArcs[tree_vertex_list[1]][0][1]
                ## print("VERTEX ABOVE")
                ## print(vertex_above)

                vertex_below = N.arcs[reticulation_vertex_list[0]][0][1]

                # GET RID OF NETWORK FROM VERTEX ABOVE TO VERTEX BELOW

                ## print("VERTEX ABOVE ARCS")
                ## print(N.arcs[vertex_above])

                arcs_below_vertex_above = network.arcs[vertex_above]

                ## print("ARCS BELOW VERTEX ABOVE")

                for arc in arcs_below_vertex_above:
                    ## print(arc)
                    N.arcs[vertex_above].remove(arc)
                    N.reverseArcs[arc[1]].remove([arc[1], arc[0]])

                for vertex in tree_vertex_list:
                    for arc in network.arcs[vertex]:
                        N.arcs[vertex].remove(arc)
                        N.reverseArcs[arc[1]].remove([arc[1], arc[0]])
                    N.vertices.remove(vertex)

                for vertex in reticulation_vertex_list:
                    for arc in network.arcs[vertex]:
                        N.arcs[vertex].remove(arc)
                        N.reverseArcs[arc[1]].remove([arc[1], arc[0]])
                    N.vertices.remove(vertex)

                # ADD AN ARC FROM VERTEX ABOVE TO VERTEX BELOW

                N.arcs[vertex_above].append([vertex_above, vertex_below])
                N.reverseArcs.append([vertex_below, vertex_above])
            else:
                vertices_above_count = [0 for _ in range(max(network.vertices))]
                for vertex in tree_vertex_list:
                    for arc in network.reverseArcs[vertex]:
                        vertices_above_count[arc[1]] = vertices_above_count[arc[1]] + 1

                max_value = 0
                value_index = 0
                for i in range(len(vertices_above_count)):
                    if vertices_above_count[i] > max_value:
                        max_value = vertices_above_count[i]
                        value_index = i

                vertex_above = value_index

                vertex_below = network.arcs[reticulation_vertex_list[0]][0][1]

                arcs_below_vertex_above = network.arcs[vertex_above]

                for arc in arcs_below_vertex_above:
                    ## print(arc)
                    N.arcs[vertex_above].remove(arc)
                    N.reverseArcs[arc[1]].remove([arc[1], arc[0]])

                for vertex in tree_vertex_list:
                    for arc in network.arcs[vertex]:
                        N.arcs[vertex].remove(arc)
                        N.reverseArcs[arc[1]].remove([arc[1], arc[0]])
                    N.vertices.remove(vertex)

                for vertex in reticulation_vertex_list:
                    for arc in network.arcs[vertex]:
                        N.arcs[vertex].remove(arc)
                        N.reverseArcs[arc[1]].remove([arc[1], arc[0]])
                    N.vertices.remove(vertex)

                # ADD AN ARC FROM VERTEX ABOVE TO VERTEX BELOW

                N.arcs[vertex_above].append([vertex_above, vertex_below])
                N.reverseArcs.append([vertex_below, vertex_above])

                #FIND OUT WHICH VERTICES ARE THE EXTRA ONES
                extra_vertices = []

                for i in range(len(vertices_above_count)):
                    if i != value_index and vertices_above_count[i] != 0:
                        extra_vertices.append(i)

                #FIND WHICH TREE VERTICES CONNECT TO THESE EXTRA VERTICES

                extra_tree_vertices = []

                for vertex in extra_vertices:
                    for arc in N.arcs[vertex]:
                        if arc[1] in tree_vertex_list:
                            extra_tree_vertices.append(arc[1])


                ## print("EXTRA VERTICES")
                ## print(extra_vertices)

                #PUT ARC FROM EXTRA VERTICES TO VERTEX BELOW

                for vertex in extra_tree_vertices:
                    N.arcs[vertex].append([vertex, vertex_below])
                    N.reverseArcs[vertex_below].append([vertex_below, vertex])

        #N.displayGraph()

        return N


    def foldNetworkPathMethod(self, network):
        """

        :type network: PhylogeneticNetwork
        """

        N = deepcopy(network)
        # N.displayGraph()

        input_arcs = [0 for _ in range(len(N.arcs) + 1)]
        output_arcs = [0 for _ in range(len(N.arcs) + 1)]
        for i in range(len(N.arcs)):
            output_arcs[i] = len(N.arcs[i])
        for i in range(len(N.reverseArcs)):
            input_arcs[i] = len(N.reverseArcs[i])

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

        ## print("INPUT ARCS")
        ## print(input_arcs)
        ## print("OUTPUT ARCS")
        ## print(output_arcs)

        ## print("TREE VERTICES")
        ## print(tree_vertices)
        ## print("RETICULATION VERTICES")
        ## print(reticulation_vertices)
        ## print("LEAF VERTICES")
        ## print(len(leaf_list))

        current_vertex = max(N.vertices) + 1

        ## print("NETWORK.VERTICES")
        ## print(network.vertices)

        ## print("CURRENT VERTEX")
        ## print(current_vertex)

        path_list = N.getAllPaths()

        vertices = []
        arcs = [[] for _ in range(5000)]
        root = network.root
        reverseArcs = [[] for _ in range(5000)]
        multiLabelledVertices = [[] for _ in range(5000)]
        reverseMultiLabelledVertices = [[] for _ in range(5000)]

        temp_arc_list = []
        done_path_list = []

        ## print("PATH LIST")
        ## print(path_list)

        arc_list = []

        vertices.append(root)

        for path in path_list:
            i = 0
            if len(path) > 0:
                current_path = []
                current_path.append(network.root)
                path.remove(network.root)
                pv = network.root
                j = 1
                new_break = False
                for vertex in path:
                    if not new_break:
                        if vertex not in vertices:
                            vertices.append(vertex)
                            if [pv, vertex] not in arc_list:
                                arc_list.append([pv, vertex])
                            #arc_list.append([pv, vertex])
                            reverseArcs[vertex].append([vertex, pv])
                            pv = vertex
                            temp_arc_list.append([path_list[i][j], path_list[i][j-1]])
                            current_path.append(vertex)
                        else:
                            if vertex in tree_vertices:
                                pv = vertex
                                current_path.append(vertex)
                            else:
                                done = False
                                for cv in reverseMultiLabelledVertices[pv]:
                                    if [cv, vertex] in arcs[cv]:
                                        pv = vertex
                                        current_path.append(vertex)
                                        done = True
                                        break
                                for cv in reverseMultiLabelledVertices[vertex]:
                                    if [pv, cv] in arcs[pv]:
                                        pv = cv
                                        current_path.append(cv)
                                        done = True
                                        break
                                if [pv, vertex] not in arcs[pv] and done == False:

                                    ## print("TEST")
                                    ## print([pv, vertex])

                                    arcs[pv].append([pv, vertex])
                                    if [pv, vertex] not in arc_list:
                                        arc_list.append([pv, vertex])

                                    # vertices.append(current_vertex + 1)
                                    # arc_list.append([pv, current_vertex + 1])
                                    #
                                    # arcs[pv].append([current_vertex + 1, vertex])
                                    # arc_list.append([current_vertex + 1, vertex])

                                    break

                                    # vertices.append(current_vertex + 1)
                                    # arcs[pv].append([pv, current_vertex + 1])
                                    # arc_list.append([pv, current_vertex + 1])
                                    # reverseArcs[current_vertex + 1].append([current_vertex + 1, pv])
                                    # multiLabelledVertices[current_vertex + 1].append(vertex)
                                    # reverseMultiLabelledVertices[vertex].append(current_vertex + 1)
                                    # current_path.append(current_vertex + 1)
                                    # pv = current_vertex + 1
                                    # current_vertex = current_vertex + 1
                                elif done == False:
                                    pv = vertex
                                    current_path.append(vertex)

        ## print("VERTEX LIST")
        ## print(vertices)
        ## print("ARC LIST")
        ## print(arc_list)

        NPrime = PhylogeneticNetwork(vertices, arc_list, root)
        # NPrime.displayGraph()

        return NPrime



    def foldNetworkMultiLabelledGraph(self, network):
        """

        :type network: MultiLabelledGraph
        """


        MN = deepcopy(network)

        ## print(MN.multiLabelledVertices)

        # MN.displayGraph()

        networks_below_multilabelledvertices = self.recheckNetworksBelowVertices(MN)

        sorted_indices_list = [i[0] for i in sorted(enumerate(networks_below_multilabelledvertices), key=lambda x: x[1])]
        sorted_indices_list.reverse()

        for i in range(len(sorted_indices_list)):
            if networks_below_multilabelledvertices[i] != 0:
                MN = self.MergeNetworkOnMLVertex(i, MN.reverseMultiLabelledVertices[i], MN)
                networks_below_multilabelledvertices = self.recheckNetworksBelowVertices(MN)

                sorted_indices_list = [i[0] for i in sorted(enumerate(networks_below_multilabelledvertices), key=lambda x: x[1])]
                sorted_indices_list.reverse()
            else: # ALGORITHM IS FINISHED
                break

        return MN

        # sorted_indices_list.reverse()
        # print("SORTED INDICES LIST")
        # print(sorted_indices_list)

    def MergeNetworkOnMLVertex(self, vertex, converted_vertex_list, network):
        """

        :type network: MultiLabelledGraph
        """

        for cv in converted_vertex_list:
            vertices_below_vertex = network.getVerticesBelowVertex(cv, cv)

            #ADD VERTEX FROM CONVERTED VERTEX TO ORIGINAL VERTEX

            network.arcs[converted_vertex_list].append([converted_vertex_list, vertex])
            network.reverseArcs[vertex].append([vertex, converted_vertex_list])

            #REMOVE VERTICES BELOW THE CONVERTED VERTEX LIST USING VERTICES BELOW VERTEX

            for vertex_below in vertices_below_vertex:
                network.arcs[vertex_below] = []
                network.reverseArcs[vertex_below] = []
                network.vertices.remove(vertex_below)

            #REMOVE MULTILABELLED VERTICES REFERENCES

            network.multiLabelledVertices[cv].remove(vertex)
            network.reverseMultiLabelledVertices[vertex].remove(cv)

        return network

    def recheckNetworksBelowVertices(self, MN):

        networks_below_multilabelledvertices = [0 for _ in range(5000)]

        for array in MN.multiLabelledVertices:
            if len(array) > 0:
                for vertex in array:
                    vertices_below_vertex = MN.getVerticesBelowVertex(vertex, vertex)
                    ## print("VERTICES BELOW")
                    ## print(vertex)
                    ## print(vertices_below_vertex)
                    networks_below_multilabelledvertices[len(vertices_below_vertex)] = len(vertices_below_vertex)
        ## print("MULTILABELLEDVERTICESARCLIST")
        ## print(networks_below_multilabelledvertices)

        return networks_below_multilabelledvertices

    def foldNetworkSimplifiedMLG(self, MN):
        """

        :type MN: MultiLabelledGraph
        """

        MN = MN.simplifyNetwork()
        # MN.displayGraph()

        # GET ALL TREE VERTICES OF THE MULTI-LABELLED GRAPH

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

        #GET NETWORK BELOW EVERY TREE VERTEX

        networks_below_tree_vertices = []

        for vertex in tree_vertices:
            networks_below_tree_vertices.append(self.getNetworkBelowVertex(MN, vertex))

        # networks_below_tree_vertices.sort(key=lambda x: x.size)

        networks_below_tree_vertices = sorted(networks_below_tree_vertices, key=lambda x: x.number_of_nodes(), reverse=True)
        tree_vertices = sorted(tree_vertices, key=lambda x: self.getNetworkBelowVertex(MN, x).number_of_nodes(), reverse=True)

        ## print("NETWORKSBELOWTREEVERTICES")

        # MN.displayGraph()


        is_it_equal_matrix = [[] for _ in range(len(tree_vertices))]

        for i in range(len(networks_below_tree_vertices)):
            is_it_equal_matrix[i] = [[] for _ in range(len(tree_vertices))]
            for j in range(len(networks_below_tree_vertices)):
                if i != j:
                    graph1 = networks_below_tree_vertices[i]
                    ## print("GRAPH1")
                    ## print(tree_vertices[i])
                    ## print(graph1.nodes)
                    ## print(graph1.edges)
                    graph2 = networks_below_tree_vertices[j]
                    ## print("GRAPH2")
                    ## print(tree_vertices[j])
                    ## print(graph2.nodes)
                    ## print(graph2.edges)
                    mlg = MN
                    if self.checkIfTwoGraphsAreIsomorphic(graph1, graph2) and self.checkIfTwoNetworksShareSameLeafToRootLength(graph1, graph2, mlg):
                        is_it_equal_matrix[i][j].append(1)
                        if i == 14 and j == 15:
                            ## print("BREAKPOINT")
                            ## print(graph1.nodes)
                            self.displayNetworkXGraph(graph1)
                            ## print(graph2.nodes)
                            self.displayNetworkXGraph(graph2)
                    else:
                        is_it_equal_matrix[i][j].append(0)
                else:
                    is_it_equal_matrix[i][j].append(0)

        ## print("ISITEQUALMATRIX")
        ## print(is_it_equal_matrix)

        # for i in range(len(is_it_equal_matrix)):
        #     ## print(is_it_equal_matrix[i])

        #SIMULARITY MATRIX IS FINISHED AND SORTED BASED ON SIZE

        #MERGE TOP ROW AND THEN RECOMPUTE AND CONTINUE ULTIL ALL ONES ARE SATISFIED

        ## print("REVERSEARCS")
        ## print(MN.reverseArcs)

        vertices_already_merged = []

        for i in range(len(is_it_equal_matrix)):
            if tree_vertices[i] not in vertices_already_merged:
                for j in range(len(is_it_equal_matrix)):
                    if i != j:
                        if is_it_equal_matrix[i][j][0] == 1:
                            MN, vertices_merged = self.mergeTwoNetworks(networks_below_tree_vertices[i], networks_below_tree_vertices[j], MN)
                            ## print("VERTICESMERGED")
                            ## print(vertices_merged)
                            for vertex in vertices_merged:
                                vertices_already_merged.append(vertex)

                            for vertex in vertices_merged:
                                if len(MN.multiLabelledVertices[vertex]) > 0:
                                    converted_vertex = MN.multiLabelledVertices[vertex][0]
                                    MN.reverseMultiLabelledVertices[converted_vertex].remove(vertex)
                                    MN.multiLabelledVertices[vertex] = []



        #FIND OUT WHICH VERTICES CANT BE MERGED USING TREE VERTICES

        for i in range(len(MN.reverseMultiLabelledVertices)):
            if MN.reverseMultiLabelledVertices[i] not in tree_vertices:
                for vertex in MN.reverseMultiLabelledVertices[i]:
                    vertex_to_merge_to = vertex
                    MN = self.mergeTwoVertices(i, vertex_to_merge_to, MN)

        MN = MN.simplifyNetwork()

        #RETURN MULTILABELLED GRAPH ONCE ALL MULTI-LABELLED VERTICES HAVE BEEN MERGED

        return MN


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

        ## print("MLG.REVERSEARCS[GRAPH1_ROOT]")
        ## print(mlg.reverseArcs[graph1_root[0]])

        vertex_above_graph1_root = mlg.reverseArcs[graph1_root[0]][0][1]

        ## print("GRAPH2NODES")
        ## print(graph2_nodes)
        ## print("GRAPH2ROOT")
        ## print(graph2_root)

        for node in graph2_nodes:
            if node != graph2_root[0]:
                mlg.arcs[node] = []
                mlg.reverseArcs[node] = []
                if node in mlg.vertices:
                    mlg.vertices.remove(node)
            else:
                mlg.arcs[node] = []

        ## print("REVERSEARCS")
        ## print(mlg.reverseArcs)

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

        ## print("GRAPH2ARCS")

        # for arc in graph2_arcs:
        #     ## print(arc)

        return mlg, graph2_nodes

    def mergeTwoVertices(self, vertex1, vertex2, mlg):
        """

        :type mlg: MultiLabelledGraph
        """

        #GET VERTEX ABOVE VERTEX1

        ## print("VERTEX 1")
        ## print(vertex1)
        ## print("VERTEX 2")
        ## print(vertex2)
        ## print(mlg.reverseArcs[vertex1])

        max_vertex = max(mlg.vertices)

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

    def getLengthOfNetwork(self, graph):
        """

        :type graph: networkx.DiGraph
        """
        return graph.size

    def getNetworkBelowVertex(self, MN, vertex):

        vertices_below_vertex = MN.getVerticesBelowVertex(vertex, vertex, [])

        if vertex not in vertices_below_vertex:
            vertices_below_vertex.append(vertex)

        vertices_below_vertex.sort()

        ## print("VERTICES BELOW VERTEX")
        ## print(vertices_below_vertex)
        ## print(vertex)

        networkXGraph = networkx.DiGraph()
        for vertex in vertices_below_vertex:
            networkXGraph.add_node(vertex)
            for arc in MN.arcs[vertex]:
                networkXGraph.add_edge(arc[0], arc[1])

        ## print("MN EDGES")
        ## print(MN.arcs)

        ## print("NETWORKXGRAPH EDGES")
        ## print(networkXGraph.edges)

        return networkXGraph

    def checkIfTwoGraphsAreIsomorphic(self, graph1, graph2):

        return networkx.is_isomorphic(graph1, graph2)


    def getLengthofRootToLeaves(self, graph1, mlg1):
        """
        :type mlg1: MultiLabelledGraph
        """
        leaf_list = [x for x in graph1.nodes() if graph1.out_degree(x) == 0 and graph1.in_degree(x) == 1]
        root = [n for n, d in graph1.in_degree() if d == 0]

        length_of_path_list = [[] for _ in range(100)]

        ## print("GETLENGTHOFROOTTOLEAVES")

        ## print(graph1.nodes)
        ## print(graph1.edges)
        ## print(leaf_list)
        ## print(root)

        for leaf in leaf_list:
            ## print(leaf)
            path = networkx.all_simple_paths(graph1, root[0], leaf)
            path_list = []
            for vertex in path:
                path_list.append(path)
            if len(mlg1.reverseMultiLabelledVertices[leaf]) > 0:
                length_of_path_list[len(path_list)].append(mlg1.reverseMultiLabelledVertices[leaf][0])
            else:
                length_of_path_list[len(path_list)].append(leaf)

        return length_of_path_list

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

        ## print(graph1_length_of_root_to_leaf)
        ## print(graph2_length_of_root_to_leaf)

        for i in range(len(graph1_length_of_root_to_leaf)):
            graph1_temp = graph1_length_of_root_to_leaf[i]
            graph1_temp.sort()
            graph2_temp = graph2_length_of_root_to_leaf[i]
            graph2_temp.sort()
            if graph1_temp != graph2_temp:
                return False

        return True

    def displayNetworkXGraph(self, graph):
        self.dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        for i in graph.nodes:
            if graph.nodes[i] != {}:
                self.dot.node(str(graph.nodes[i]))
        for arc in graph.edges:
            self.dot.edge(str(arc[0]), str(arc[1]))
        self.dot.view()

    

