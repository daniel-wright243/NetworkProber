from copy import deepcopy

import networkx

from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.PloidyAlgorithm import PolyPloidy
from SubFunctions.TreeSpotterFoldingFunction2 import FoldingFunction2
from SubFunctions.TreeSpotterFoldingFunction3 import FoldingFunction3

class TreeSpotterAlgorithm:

    def __init__(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        self.network = network

    def startAlgorithm(self, decision):
        # self.GetNonTreeBasedComponents(self.network)
        #PLANT THE NETWORK TO MAKE THE ALGORITHM WORK

        if 0 not in self.network.vertices:
            self.network.createVertex(0)
            self.network.createArc([0, self.network.root])
            self.network.oldRoot = self.network.root
            self.network.root = 0

        # self.network.displayGraph()

        # self.GetNonTreeBasedComponents(self.network)

        if self.network.isBinary(): # NETWORK IS BINARY
            if self.network.checkTreeBasedNonBinary2():
                self.network.root = self.network.oldRoot
                self.network.removeArc([0, 1])
                self.network.vertices.remove(0)
                return self.network
            else:
                # self.network.displayGraph()
                # self.GetNonTreeBasedComponentsBinary(self.network)
                if decision:
                    fa_temp = self.PolyPloidyAlgorithmBinary(self.network)
                    if [0, 1] in fa_temp.arcs[0]:
                        fa_temp.removeArc([0, 1])
                    if 0 in fa_temp.vertices:
                        fa_temp.vertices.remove(0)
                        fa_temp.root = fa_temp.oldRoot
                    return fa_temp
                    # pp = PolyPloidy(self.network)
                    # return pp.startAlgorithm(max(self.network.vertices))
                else:
                    fa_temp = self.FoldingAlgorithmBinary(self.network)
                    fa_temp.removeArc([0, 1])
                    fa_temp.vertices.remove(0)
                    fa_temp.root = fa_temp.oldRoot
                    return fa_temp
                    # fa = FoldingFunction2(self.network)
                    # fa_temp = FoldingFunction3(self.network).startAlgorithm()
                    # fa_temp.removeArc([0, 1])
                    # fa_temp.vertices.remove(0)
                    # fa_temp.root = fa_temp.oldRoot
                    # return fa.startAlgorithm()
                    # return fa_temp
        else: # NETWORK IS NON-BINARY
            if self.network.checkTreeBasedNonBinary2():
                self.network.root = self.network.oldRoot
                self.network.removeArc([0, 1])
                self.network.vertices.remove(0)
                return self.network
            else:
                if decision:
                    fa_temp = self.PolyPloidyAlgorithmNonBinary(self.network)
                    fa_temp.removeArc([0, 1])
                    fa_temp.vertices.remove(0)
                    fa_temp.root = fa_temp.oldRoot
                    print("PLOIDY LEVEL")
                    print(fa_temp.getPloidyLevels())
                    # fa_temp.displayGraph()
                    return fa_temp
                    pp = PolyPloidy(self.network)
                    return pp.startAlgorithm(max(self.network.vertices))
                else:
                    fa_temp = self.GetNonTreeBasedComponentsNonBinary(self.network, 1)
                    # fa = FoldingFunction2(self.network)
                    # fa_temp = FoldingFunction3(self.network).startAlgorithm()
                    # # return fa.startAlgorithm()
                    fa_temp.removeArc([0, 1])
                    fa_temp.vertices.remove(0)
                    fa_temp.root = fa_temp.oldRoot
                    return fa_temp

    def GetNonTreeBasedComponents(self, network):
        """

        :type network: PhylogeneticNetwork
        """

        # network.displayGraph()

        bpg = network.makeBiPartiteGraph()

        # bpg.displayGraph()

        cc = bpg.getConnectedComponents()

        bpg.hopcroftKarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = bpg.returnHKMatching()

        # print("CC")
        # print(cc)
        # print("BPG.U")
        # print(bpg.U)
        # print("BPG.V")
        # print(bpg.V)
        # print("pairU")
        # print(pairU)
        # print("pairV")
        # print(pairV)

        vertex_set = []
        edge_list = []

        # non_tree_based_connected_component_list = []

        for i in range(len(pairU)):
            U = i
            V = pairU[i]

            if V != 0:
                # self.matchingDot.node(str(i))
                vertex_set.append(i)
                # self.matchingDot.node(str(V + bpg.U))
                vertex_set.append(V + bpg.U)
                # self.matchingDot.edge(str(i), str(V + bpg.U))
                edge_list.append([i, V + bpg.U])

        ## print("VERTEX LIST")
        ## print(vertex_set)
        ## print("EDGE LIST")
        ## print(edge_list)

        non_tree_based_components = []

        for component in cc:
            ## print(component)
            for vertex in component:
                if vertex not in vertex_set and vertex > bpg.U:
                    non_tree_based_components.append(component)
                    break

        ## print("NON TREE-BASED COMPONENTS")
        ## print(non_tree_based_components)]]

        converted_component = []
        converted_component_trees = []
        converted_component_reticulation = []

        for component in non_tree_based_components:
            temp_comp = []
            temp_tree = []
            temp_reticulation = []
            for vertex in component:
                if vertex > bpg.U:
                    temp_comp.append(self.network.connected_reticulation_vertices[vertex - bpg.U])
                    temp_reticulation.append(self.network.connected_reticulation_vertices[vertex - bpg.U])
                else:
                    temp_comp.append(self.network.connected_tree_vertices[vertex])
                    temp_tree.append(self.network.connected_tree_vertices[vertex])
            converted_component.append(temp_comp)
            converted_component_trees.append(temp_tree)
            converted_component_reticulation.append(temp_reticulation)

        ## print("CONNECTED COMPONENT")
        ## print(converted_component)

        networkXGraph1 = networkx.DiGraph()
        for vertex in self.network.vertices:
            networkXGraph1.add_node(vertex)
        for vertex in self.network.arcs:
            for arc in vertex:
                networkXGraph1.add_edge(arc[0], arc[1])

        for i in range(len(converted_component)):
            temp_component = converted_component[i]
            for tree_vertex in converted_component_trees[i]:
                for arc in self.network.arcs[tree_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in self.network.reverseArcs[tree_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            for reticulation_vertex in converted_component_reticulation[i]:
                for arc in self.network.arcs[reticulation_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in self.network.reverseArcs[reticulation_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            ## print("TEMP COMPONENT")
            ## print(temp_component)

            lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

            component_network = self.network.getNetworkBelowVertexNetworkX(lca)

            # component_network.displayGraph()

            simplifiedNetwork = component_network.simplifyNetwork()

            fa_temp = FoldingFunction3(simplifiedNetwork).startAlgorithm()
            # return fa.startAlgorithm()
            # fa_temp.displayGraph()

            ## print("LCA")
            ## print(lca)

        # for component in converted_component:
        #     #ADD SURROUNDING VERTICES TO COMPONENT
        #     temp_component = component
        #     for vertex in component:
        #
        #     lca = self.lowest_common_ancestor_multiple(networkXGraph1, component)
        #     print("LCA")
        #     print(lca)



    def lowest_common_ancestor_multiple(self, G, nodes):
        if not nodes:
            return None
        lca = nodes[0]
        for node in nodes[1:]:
            if lca is None or node is None:
                break
            lca = networkx.lowest_common_ancestor(G, lca, node)
            if lca is None:
                break
        return lca





        #     u_list = []
        #     v_list = []
        #     for vertex in component:
        #         if vertex > bpg.U:
        #             v_list.append(vertex)
        #         else:
        #             u_list.append(vertex)
        #     if len(u_list)

    def GetNonTreeBasedComponentsBinary(self, network, choice):
        """

        :type network: PhylogeneticNetwork
        """
        N = deepcopy(network)
        bpg = N.makeBiPartiteGraph()

        cc = bpg.getConnectedComponents()

        bpg.hopcroftKarp()

        tree_vertex_array = deepcopy(N.connected_tree_vertices)
        reticulation_vertex_array = deepcopy(N.connected_reticulation_vertices)

        tree_vertex_array.remove(0)
        reticulation_vertex_array.remove(0)

        # bpg.displayMatchingGraph()

        pairU, pairV = bpg.returnHKMatching()

        # print("CC")
        # print(cc)
        # print("BPG.U")
        # print(bpg.U)
        # print("BPG.V")
        # print(bpg.V)
        # print("pairU")
        # print(pairU)
        # print("pairV")
        # print(pairV)

        vertex_set = []
        edge_list = []

        # non_tree_based_connected_component_list = []

        for i in range(len(pairU)):
            U = i
            V = pairU[i]

            if V != 0:
                # self.matchingDot.node(str(i))
                vertex_set.append(i)
                # self.matchingDot.node(str(V + bpg.U))
                vertex_set.append(V + bpg.U)
                # self.matchingDot.edge(str(i), str(V + bpg.U))
                edge_list.append([i, V + bpg.U])

        ## print("VERTEX LIST")
        ## print(vertex_set)
        ## print("EDGE LIST")
        ## print(edge_list)

        non_tree_based_components = []

        for component in cc:
            ## print(component)
            for vertex in component:
                if vertex not in vertex_set and vertex > bpg.U:
                    non_tree_based_components.append(component)
                    break

        # print("NON TREE-BASED COMPONENTS")
        # print(non_tree_based_components)

        converted_component = []
        converted_component_trees = []
        converted_component_reticulation = []

        for component in non_tree_based_components:
            temp_comp = []
            temp_tree = []
            temp_reticulation = []
            for vertex in component:
                if vertex > bpg.U:
                    temp_comp.append(reticulation_vertex_array[vertex - bpg.U - 1])
                    temp_reticulation.append(reticulation_vertex_array[vertex - bpg.U - 1])
                else:
                    temp_comp.append(tree_vertex_array[vertex - 1])
                    temp_tree.append(tree_vertex_array[vertex - 1])
            converted_component.append(temp_comp)
            converted_component_trees.append(temp_tree)
            converted_component_reticulation.append(temp_reticulation)

        # print("CONVERTED COMPONENT")
        # print(converted_component)

        # print("CONVERTED COMP")
        # print(converted_component)
        # print("CONVERTED TREE")
        # print(converted_component_trees)
        # print("CONVERTED RETICULATION")
        # print(converted_component_reticulation)
        # print("SELF.NETWORK.RETICULATIONVERTICES")
        # print(N.connected_reticulation_vertices)
        # print("SELF.NETWORK.TREEVERTICES")
        # print(N.connected_tree_vertices)

        temp_leaf_list = N.getAllLeafs()

        for i in range(len(converted_component)):

            networkXGraph1 = networkx.DiGraph()
            for vertex in N.vertices:
                if vertex != None:
                    networkXGraph1.add_node(vertex)
                    for arc in N.arcs[vertex]:
                        networkXGraph1.add_edge(arc[0], arc[1])
            # for vertex in N.arcs:
            #     for arc in vertex:
            #         networkXGraph1.add_edge(arc[0], arc[1])

            temp_component = converted_component[i]
            for tree_vertex in converted_component_trees[i]:
                for arc in N.arcs[tree_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.reverseArcs[tree_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            for reticulation_vertex in converted_component_reticulation[i]:
                for arc in N.arcs[reticulation_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.reverseArcs[reticulation_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            # print("TEMP COMPONENT")
            # print(temp_component)

            for vertex in temp_component:
                if vertex not in networkXGraph1.nodes:
                    temp_component.remove(vertex)

            for vertex in N.arcs:
                for arc in vertex:
                    if arc[0] not in N.vertices:
                        if arc in N.arcs[arc[0]]:
                            N.arcs[arc[0]].remove(arc)
                    elif arc[1] not in N.vertices:
                        if arc in N.arcs[arc[0]]:
                            N.arcs[arc[0]].remove(arc)
            lca = []
            component_network = []
            if None in temp_component:
                temp_component.remove(None)
            try:
                lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)
                if lca is None:
                    return N
                # print("LCA")
                # print(lca)
                component_network = N.getNetworkBelowVertexNetworkX(lca)
            except Exception as e:
                # self.network.displayGraph()
                print(temp_component)
                print(networkXGraph1.nodes)
                print(networkXGraph1.edges)
                network.displayGraph()
                bpg.displayGraph()
                print(str(e))

            component_vertices = component_network.vertices
            connection_arcs_into = []
            connection_arcs_outto = []
            in_out_two_vertices = []
            in_out_two_arcs_in = []
            in_out_two_arcs_out = []

            for vertex in component_vertices:
                if len(component_network.arcs[vertex]) == 1 and len(component_network.reverseArcs[vertex]) == 1:
                    in_out_two_vertices.append(vertex)
                    in_out_two_arcs_in.append([component_network.reverseArcs[vertex][0][1], component_network.reverseArcs[vertex][0][0]])
                    in_out_two_arcs_out.append(component_network.arcs[vertex][0])

            for vertex in component_vertices:
                for arc in N.arcs[vertex]:
                    if arc[1] not in component_vertices:
                        connection_arcs_outto.append(arc)
                for reverseArc in N.reverseArcs[vertex]:
                    if reverseArc[1] not in component_vertices:
                        connection_arcs_into.append([reverseArc[1], reverseArc[0]])

            # for vertex in component_network.arcs:
            #     for arc in vertex:
            #         if arc[1] not in component_vertices:
            #             connection_arcs.append(arc)
            # for vertex in component_network.reverseArcs:
            #     for arc in vertex:
            #         if arc[1] not in component_vertices:
            #             connection_arcs.append([arc[1], arc[0]])

            # component_network.displayGraph()

            # simplifiedNetwork = component_network.simplifyNetwork()

            # fa_temp = FoldingFunction3(simplifiedNetwork).startAlgorithm()
            if choice == 1:
                fa_temp = FoldingFunction3(component_network, network).startAlgorithm()
            else:
                fa_temp = PolyPloidy(component_network).startAlgorithm(max(network.vertices), network)
            # return fa.startAlgorithm()
            # fa_temp.displayGraph()

            # print("FA TEMP VERTICES")
            # print(fa_temp.vertices)

            vertex_above_old_root = network.reverseArcs[component_network.root][0][1]

            #REMOVE OLD COMPONENT FROM GRAPH
            for vertex in component_network.vertices:
                if vertex in N.vertices:
                    N.vertices.remove(vertex)
                for reverseArc in N.reverseArcs[vertex]:
                    N.removeArc([reverseArc[1], reverseArc[0]])
                for arc in network.arcs[vertex]:
                    N.removeArc(arc)
                if vertex in N.taxDict.keys():
                    N.taxDict.pop(vertex)

            # N.displayGraph()

            # self.network.displayGraph()

            for vertex in fa_temp.vertices:
                N.createVertex(vertex)

            for vertex in fa_temp.arcs:
                for arc in vertex:
                    N.createArc(arc)

            for key in fa_temp.taxDict.keys():
                N.taxDict[key] = fa_temp.taxDict.get(key)

            rv_vertices = []
            leaf_vertices = []
            for i in range(len(fa_temp.arcs)):
                if len(fa_temp.arcs[i]) == 1 and len(fa_temp.reverseArcs[i]) >= 2:
                    rv_vertices.append(i)
                if len(fa_temp.arcs[i]) == 0 and len(fa_temp.reverseArcs[i]) == 1:
                    leaf_vertices.append(i)
            # print("RV VERTICES")
            # print(rv_vertices)
            #
            # print("CONNECTION ARCS INTO")
            # print(connection_arcs_into)

            ca_list = []

            for arc in connection_arcs_into:
                finished = False
                if arc[1] in fa_temp.vertices:
                    N.createArc(arc)
                    finished = True
                else:
                    vertex_below = network.arcs[arc[1]][0][1]
                    if vertex_below not in fa_temp.vertices:
                        for arc_temp in network.reverseArcs[arc[1]]:
                            if arc_temp[1] in fa_temp.vertices:
                                vertex_above = arc_temp[1]
                                # print("VERTEX ABOVE")
                                # print(vertex_above)
                                for arc2 in fa_temp.arcs[vertex_above]:
                                    vertex_below = arc2[1]
                                # vertex_below = fa_temp.arcs[vertex_above][0][1]
                                #     print("VERTEX BELOW")
                                #     print(vertex_below)
                                    if vertex_below in rv_vertices:
                                        N.createArc([arc[0], vertex_below])
                                        finished = True
                                        break
                if finished == False:
                    ca_list.append(arc)

            print("CA LIST")
            print(ca_list)

            max_vertex = max(N.vertices) + 1

            # for arc in ca_list:
            #     start_vertex = arc[0]
            #     end_vertex = arc[1]
            #
            #     # end_vertex_leaf_below = OriginalPloidyLeafs.get(start_vertex)
            #     end_vertex_leaf_below = network.getLeafsBelowVertex(end_vertex)
            #     connected_vertex_leaf_below = N.getLeafsBelowVertex(end_vertex)
            #
            #
            #     vertex_above_start_vertex = N.reverseArcs[start_vertex][0][1]
            #
            #     print("END VERTEX LEAF BELOW")
            #     print(end_vertex_leaf_below)

                # if end_vertex_leaf_below != connected_vertex_leaf_below:
                #     for leaf in end_vertex_leaf_below:
                #         if leaf == None:
                #             continue
                #         print("N.reverseArcs")
                #         print(leaf)
                #         print(N.reverseArcs[leaf])
                #         vertex_above_leaf = N.reverseArcs[leaf][0][1]
                #         #MAKE NEW VERTEX TO CONNECT TO
                #         new_vertex_index = max_vertex
                #         N.createVertex(new_vertex_index)
                #         #CONNECT VERTEX TO NEW VERTEX
                #         N.createArc([vertex_above_start_vertex, new_vertex_index])
                #         #DELETE OLD LEAF ARC
                #         N.removeArc([vertex_above_leaf, leaf])
                #         #ADD ARC FROM VERTEX ABOVE LEAF TO NEW VERTEX
                #         N.createArc([vertex_above_leaf, new_vertex_index])
                #         #ADD ARC FROM NEW VERTEX TO LEAF
                #         N.createArc([new_vertex_index, leaf])




            # for arc in ca_list:
            #     if len(N.arcs[arc[0]]) == 0:
            #         for ra in N.reverseArcs[arc[0]]:
            #             arc_to_remove = [ra[1], ra[0]]
            #             N.removeArc(arc_to_remove)
            #             N.vertices.remove(arc[0])

            # for arc in ca_list:
            #     vertex_below = network.arcs[arc[1]][0][1]
            #     if vertex_below not in leaf_vertices:
            #         N.createArc([arc[0], vertex_below])

            for arc in connection_arcs_outto:
                if arc[0] in fa_temp.vertices:
                    N.createArc(arc)

            new_leaf_list = []
            for i in range(len(N.vertices)):
                if len(N.arcs[i]) == 0 and len(N.reverseArcs[i]) == 1:
                    new_leaf_list.append(i)

            # fa_temp.displayGraph()

            if choice != 1:
                N.createArc([vertex_above_old_root, fa_temp.root])
                OriginalPloidyNetwork, OriginalPloidyLeafs = network.getPloidyLevelOfEachVertexAndConnections()
                # print("ORIGINAL PLOIDY NETWORK")
                # print(OriginalPloidyNetwork)
                # print("ORIGINAL PLOIDY LEAFS")
                # print(OriginalPloidyLeafs)
                ComponentPloidyNetwork, CompontentPloidyLeafs = fa_temp.getPloidyLevelOfEachVertexAndConnections()
                # print("COMPONTENT PLOIDY NETWORK")
                # print(ComponentPloidyNetwork)
                # print("COMPONTENT PLOIDY LEAFS")
                # print(CompontentPloidyLeafs)
                for into_arc in connection_arcs_into:
                    start_vertex = into_arc[0]
                    end_vertex = into_arc[1]
                    con_vertex = []
                    end_vertex_ploidy_level = OriginalPloidyNetwork.get(end_vertex)
                    end_vertex_leaf_below = OriginalPloidyLeafs.get(end_vertex)
                    share_ploidy_level_keys = [key for key, val in ComponentPloidyNetwork.items() if val == end_vertex_ploidy_level]
                    # print("SHARE PLOIDY LEVEL KEYS")
                    # print(share_ploidy_level_keys)
                    share_ploidy_leaf_keys = [key for key, val in CompontentPloidyLeafs.items() if val == end_vertex_leaf_below]
                    # print("SHARE PLOIDY LEAF KEYS")
                    # print(share_ploidy_leaf_keys)
                    for key in share_ploidy_level_keys:
                        if key in share_ploidy_leaf_keys:
                            con_vertex.append(key)
                    if len(con_vertex) > 0:
                        N.createArc([start_vertex, con_vertex[0]])
            # print(new_leaf_list)
            # print(temp_leaf_list)
            # print(self.network.vertices)
            # print(self.network.arcs)
            # print(self.network.reverseArcs)

            # for leaf in new_leaf_list:
            #     if leaf not in temp_leaf_list:
            #         for arc in N.reverseArcs[leaf]:
            #             N.arcs[arc[1]].remove([arc[1], arc[0]])
            #             N.reverseArcs[leaf].remove(arc)
            #         if leaf in N.vertices:
            #             N.vertices.remove(leaf)

            vertex_list = []
            for i in range(len(N.arcs)):
                if len(N.arcs[i]) > 0 or len(N.reverseArcs[i]) > 0:
                    vertex_list.append(i)
            N.vertices = vertex_list

            for vertex in N.vertices:
                if len(N.arcs) > 0 and len(N.reverseArcs) == 0:
                    N.root = vertex

            break


        # print(new_leaf_list)
        # print(temp_leaf_list)
        # print(self.network.vertices)
        # print(self.network.arcs)
        # print(self.network.reverseArcs)

        # N.displayGraph()

        return N

        # self.network.displayGraph()


    def GetNonTreeBasedComponentsNonBinary(self, network, choice):
        """

        :type network: PhylogeneticNetwork
        """
        N = deepcopy(network)
        obpg = network.makeOmnianBipartiteGraph2()
        cc = obpg.getConnectedComponents()

        #ARC LIST TESTS
        for arc in N.getAllArcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception

        obpg.hopcroftKarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = obpg.returnHKMatching()

        vertex_set = []
        edge_list = []

        # non_tree_based_connected_component_list = []

        for i in range(len(pairU)):
            U = i
            V = pairU[i]

            if V != 0:
                # self.matchingDot.node(str(i))
                vertex_set.append(i)
                # self.matchingDot.node(str(V + bpg.U))
                vertex_set.append(V + obpg.U)
                # self.matchingDot.edge(str(i), str(V + bpg.U))
                edge_list.append([i, V + obpg.U])

        ## print("VERTEX LIST")
        ## print(vertex_set)
        ## print("EDGE LIST")
        ## print(edge_list)

        non_tree_based_components = []

        for component in cc:
            # print(component)
            for vertex in component:
                if vertex not in vertex_set and vertex <= obpg.U:
                    non_tree_based_components.append(component)
                    break

        # obpg.displayGraph()
        # print("TREEBASED COMPONENTS")
        # print(non_tree_based_components)

        converted_component = []
        converted_component_trees = []
        converted_component_reticulation = []

        ol, rl = self.network.getOmnianAndReticulationList()

        for component in non_tree_based_components:
            temp_comp = []
            temp_tree = []
            temp_reticulation = []
            for vertex in component:
                if vertex > obpg.U:
                    temp_comp.append(rl[vertex - obpg.U])
                    temp_reticulation.append(rl[vertex - obpg.U])
                else:
                    temp_comp.append(ol[vertex])
                    temp_tree.append(ol[vertex])
            converted_component.append(temp_comp)
            converted_component_trees.append(temp_tree)
            converted_component_reticulation.append(temp_reticulation)

        # print("CONVERTED COMPONENT")
        # print(converted_component)

        temp_leaf_list = self.network.getAllLeafs()

        for i in range(len(converted_component)):

            networkXGraph1 = networkx.DiGraph()
            for vertex in N.vertices:
                networkXGraph1.add_node(vertex)
            for vertex in N.arcs:
                for arc in vertex:
                    networkXGraph1.add_edge(arc[0], arc[1])

            temp_component = converted_component[i]
            for tree_vertex in converted_component_trees[i]:
                for arc in N.arcs[tree_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.reverseArcs[tree_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            for reticulation_vertex in converted_component_reticulation[i]:
                for arc in N.arcs[reticulation_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.reverseArcs[reticulation_vertex]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            # print("TEMP COMPONENT")
            # print(temp_component)

            for arc in N.getAllArcs():
                if arc[0] not in N.vertices or arc[1] not in N.vertices:
                    print(arc)
                    raise Exception

            lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

            component_network = N.getNetworkBelowVertexNetworkX(lca)

            component_vertices = component_network.vertices
            connection_arcs_into = []
            connection_arcs_outto = []

            # component_network.displayGraph()

            for vertex in component_vertices:
                for arc in N.arcs[vertex]:
                    if arc[1] not in component_vertices:
                        connection_arcs_outto.append(arc)
                for reverseArc in N.reverseArcs[vertex]:
                    if reverseArc[1] not in component_vertices:
                        connection_arcs_into.append([reverseArc[1], reverseArc[0]])

            # for vertex in component_network.arcs:
            #     for arc in vertex:
            #         if arc[1] not in component_vertices:
            #             connection_arcs.append(arc)
            # for vertex in component_network.reverseArcs:
            #     for arc in vertex:
            #         if arc[1] not in component_vertices:
            #             connection_arcs.append([arc[1], arc[0]])

            # component_network.displayGraph()

            # simplifiedNetwork = component_network.simplifyNetwork()

            # component_network.displayGraph()

            # fa_temp = FoldingFunction3(simplifiedNetwork).startAlgorithm()
            if choice == 1:
                fa_temp = FoldingFunction3(component_network, network).startAlgorithm()
            else:
                fa_temp = PolyPloidy(component_network).startAlgorithm(max(network.vertices), network)
                # fa_temp.displayGraph()
            # return fa.startAlgorithm()
            # fa_temp.displayGraph()

            print("NEW TAX DICT")
            print(fa_temp.taxDict)

            # print("FA TEMP VERTICES")
            # print(fa_temp.vertices)

            vertex_above_old_root = network.reverseArcs[component_network.root][0][1]

            #REMOVE OLD COMPONENT FROM GRAPH
            for vertex in component_network.vertices:
                if vertex in N.vertices:
                    N.vertices.remove(vertex)
                for reverseArc in N.reverseArcs[vertex]:
                    N.removeArc([reverseArc[1], reverseArc[0]])
                for arc in self.network.arcs[vertex]:
                    N.removeArc(arc)



            # self.network.displayGraph()

            for vertex in fa_temp.vertices:
                N.createVertex(vertex)

            for vertex in fa_temp.arcs:
                for arc in vertex:
                    N.createArc(arc)

            for key in fa_temp.taxDict.keys():
                N.taxDict[key] = fa_temp.taxDict.get(key)

            # for arc in connection_arcs_into:
            #     if arc[1] in fa_temp.vertices:
            #         N.createArc(arc)

            rv_vertices = []
            leaf_vertices = []
            for i in range(len(fa_temp.arcs)):
                if len(fa_temp.arcs[i]) == 1 and len(fa_temp.reverseArcs[i]) >= 2:
                    rv_vertices.append(i)
                if len(fa_temp.arcs[i]) == 0 and len(fa_temp.reverseArcs[i]) == 1:
                    leaf_vertices.append(i)

            ca_list = []

            N = self.reintegrationAlgorithm(N, fa_temp, connection_arcs_into, connection_arcs_outto, network)

            # for arc in connection_arcs_into:
            #     finished = False
            #     if arc[1] in fa_temp.vertices:
            #         N.createArc(arc)
            #         finished = True
            #     else:
            #         vertex_below = network.arcs[arc[1]][0][1]
            #         if vertex_below not in fa_temp.vertices:
            #             for arc_temp in network.reverseArcs[arc[1]]:
            #                 if arc_temp[1] in fa_temp.vertices:
            #                     vertex_above = arc_temp[1]
            #                     # print("VERTEX ABOVE")
            #                     # print(vertex_above)
            #                     for arc2 in fa_temp.arcs[vertex_above]:
            #                         vertex_below = arc2[1]
            #                     # vertex_below = fa_temp.arcs[vertex_above][0][1]
            #                     #     print("VERTEX BELOW")
            #                     #     print(vertex_below)
            #                         if vertex_below in rv_vertices:
            #                             N.createArc([arc[0], vertex_below])
            #                             finished = True
            #                             break
            #     # if finished == False:
            #     #     ca_list.append(arc)
            #
            # # for arc in ca_list:
            # #     vertex_below = network.arcs[arc[1]][0][1]
            # #     if vertex_below not in leaf_vertices:
            # #         N.createArc([arc[0], vertex_below])
            #
            #
            # for arc in connection_arcs_outto:
            #     if arc[0] in fa_temp.vertices:
            #         N.createArc(arc)
            #
            #
            #
            # new_leaf_list = []
            # for i in range(len(N.vertices)):
            #     if len(N.arcs[i]) == 0 and len(N.reverseArcs[i]) == 1:
            #         new_leaf_list.append(i)
            #
            # if choice != 1:
            #     print("ROOT CONNECTION")
            #     print([vertex_above_old_root, fa_temp.root])
            #     N.createArc([vertex_above_old_root, fa_temp.root])
            #
            #
            #
            # # print(new_leaf_list)
            # # print(temp_leaf_list)
            # # print(self.network.arcs)
            # # print(self.network.reverseArcs)
            #
            # # for leaf in new_leaf_list:
            # #     if leaf not in temp_leaf_list:
            # #         for arc in N.reverseArcs[leaf]:
            # #             N.arcs[arc[1]].remove([arc[1], arc[0]])
            # #             N.reverseArcs[leaf].remove(arc)
            # #         if leaf in N.vertices:
            # #             N.vertices.remove(leaf)
            #
            # vertex_list = []
            # for i in range(len(N.arcs)):
            #     if len(N.arcs[i]) > 0 or len(N.reverseArcs[i]) > 0:
            #         vertex_list.append(i)
            # N.vertices = vertex_list
            #
            # N = N.simplifyNetwork()
            #
            # N.displayGraph()
            #
            # #REGET THE ROOT
            #
            # for vertex in N.vertices:
            #     if len(N.arcs) > 0 and len(N.reverseArcs) == 0:
            #         N.root = vertex
            #
            # print("N.root")
            # print(N.root)
            # print("PLOIDY LEVEL")
            # print(N.getPloidyLevels())
            #
            # break
        # print(new_leaf_list)
        # print(temp_leaf_list)
        # print(self.network.vertices)
        # print(self.network.arcs)
        # print(self.network.reverseArcs)

        print("N TAX DICT")
        print(N.taxDict)

        return N

    def reintegrationAlgorithm(self, network, component, input_arc_list, output_arc_list, original_network):
        """

        :type component: PhylogeneticNetwork
        :type network: PhylogeneticNetwork
        """

        for arc in input_arc_list:
            #FIND PARENTS OF H(A)
            A_a = []
            B_b = []
            for arc_above in network.reverseArcs[arc[1]]:
                A_a.append(arc_above[1])
            if arc[0] in A_a:
                A_a.remove(arc[0])
            for arc_below in network.arcs[arc[1]]:
                B_b.append(arc_below[1])
            if arc[1] in component.vertices:
                if len(component.arcs[arc[1]]) == 1 and len(component.reverseArcs[arc[1]]) > 1:
                    network.createArc(arc)
                elif len(component.arcs[arc[1]]) > 1 and len(component.reverseArcs[arc[1]]) == 0:
                    network.createArc(arc)
                else:
                    print("COMPONENT.REVERSEARCS")
                    print(component.reverseArcs)
                    print("ARC[1]")
                    print(arc[1])
                    # component.displayGraph()
                    vertex_above = component.reverseArcs[arc[1]][0][1]
                    #vertex_above = A_a[0]
                    a_prime = [vertex_above, arc[1]]
                    network = self.subdivideArcAndConnect(a_prime, network, arc[0])
            else:
                vertex_above_exists = False
                vertex_above = 0
                vertex_below_exists = False
                vertex_below = 0
                for vertex in A_a:
                    if vertex in component.vertices:
                        vertex_above_exists = True
                        vertex_above = vertex
                for vertex in B_b:
                    if vertex in component.vertices:
                        vertex_below_exists = True
                        vertex_below = vertex
                if vertex_above_exists:
                    a_prime = network.arcs[vertex_above][0]
                    network = self.subdivideArcAndConnect(a_prime, network, arc[0])
                elif vertex_below_exists:
                    a_prime = network.reverseArcs[vertex_below][0]
                    network = self.subdivideArcAndConnect(a_prime, network, arc[0])
                else:
                    OriginalPloidyNetwork, OriginalPloidyLeafs = network.getPloidyLevelOfEachVertexAndConnections()
                    ComponentPloidyNetwork, CompontentPloidyLeafs = component.getPloidyLevelOfEachVertexAndConnections()
                    start_vertex = arc[0]
                    end_vertex = arc[1]
                    con_vertex = []
                    end_vertex_ploidy_level = OriginalPloidyNetwork.get(end_vertex)
                    end_vertex_leaf_below = OriginalPloidyLeafs.get(end_vertex)
                    share_ploidy_level_keys = [key for key, val in ComponentPloidyNetwork.items() if val == end_vertex_ploidy_level]
                    # print("SHARE PLOIDY LEVEL KEYS")
                    # print(share_ploidy_level_keys)
                    share_ploidy_leaf_keys = [key for key, val in CompontentPloidyLeafs.items() if val == end_vertex_leaf_below]
                    # print("SHARE PLOIDY LEAF KEYS")
                    # print(share_ploidy_leaf_keys)
                    for key in share_ploidy_level_keys:
                        if key in share_ploidy_leaf_keys:
                            con_vertex.append(key)
                    if len(con_vertex) > 0:
                        network.createArc([start_vertex, con_vertex[0]])
                    else:
                        if len(share_ploidy_leaf_keys) > 0:
                            network.createArc([start_vertex, share_ploidy_leaf_keys[0]])
                        else:
                            return network
        return network

                #subdivide a with a new vertex s, and create arc from t(a) to s

    def subdivideArcAndConnect(self, arc, network, connection_vertex):
        """

        :type network: PhylogeneticNetwork
        """

        S = max(network.vertices) + 1  # CREATE S
        network.createVertex(S)
        network.removeArc(arc) # REMOVE ORIGINAL ARC
        network.createArc([arc[0], S]) # ARC FROM INPUT TO S
        network.createArc([S, arc[1]]) # ARC FROM S TO OUTPUT
        network.createArc([connection_vertex, S])

        return network


    def FoldingAlgorithmBinary(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        N = deepcopy(network)
        i = 0
        while not N.checkTreeBasedBinary():
            N = self.GetNonTreeBasedComponentsBinary(N, 1)
            i = i + 1
            if i > 10:
                break
        return N

    def FoldingAlgorithmNonBinary(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        N = deepcopy(network)
        i = 0
        while not N.checkTreeBasedNonBinary2():
            N = self.GetNonTreeBasedComponentsNonBinary(N, 1)
            i = i + 1
            if i > 10:
                break
        print(N.vertices)
        print(N.getAllArcs())
        return N

    def PolyPloidyAlgorithmBinary(self, network):
        N = self.GetNonTreeBasedComponentsBinary(network, 0)
        return N

    def PolyPloidyAlgorithmNonBinary(self, network):
        N = self.GetNonTreeBasedComponentsNonBinary(network, 0)
        return N

    def omnianConnectedComponents(self, obpg, network):
        cc = obpg.getConnectedComponents()

        # ARC LIST TESTS
        for arc in network.getAllArcs():
            if arc[0] not in network.vertices or arc[1] not in network.vertices:
                print(arc)
                raise Exception

        obpg.hopcroftKarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = obpg.returnHKMatching()

        vertex_set = []
        edge_list = []

        # non_tree_based_connected_component_list = []

        for i in range(len(pairU)):
            U = i
            V = pairU[i]

            if V != 0:
                # self.matchingDot.node(str(i))
                vertex_set.append(i)
                # self.matchingDot.node(str(V + bpg.U))
                vertex_set.append(V + obpg.U)
                # self.matchingDot.edge(str(i), str(V + bpg.U))
                edge_list.append([i, V + obpg.U])

        ## print("VERTEX LIST")
        ## print(vertex_set)
        ## print("EDGE LIST")
        ## print(edge_list)

        non_tree_based_components = []

        for component in cc:
            # print(component)
            for vertex in component:
                if vertex not in vertex_set and vertex <= obpg.U:
                    non_tree_based_components.append(component)
                    break

        # obpg.displayGraph()
        # print("TREEBASED COMPONENTS")
        # print(non_tree_based_components)

        converted_component = []
        converted_component_trees = []
        converted_component_reticulation = []

        ol, rl = network.getOmnianAndReticulationList()

        for component in non_tree_based_components:
            temp_comp = []
            temp_tree = []
            temp_reticulation = []
            for vertex in component:
                if vertex > obpg.U:
                    temp_comp.append(rl[vertex - obpg.U])
                    temp_reticulation.append(rl[vertex - obpg.U])
                else:
                    temp_comp.append(ol[vertex])
                    temp_tree.append(ol[vertex])
            converted_component.append(temp_comp)
            converted_component_trees.append(temp_tree)
            converted_component_reticulation.append(temp_reticulation)

        return converted_component

    def bipartiteGraphAlgorithm(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        network_copy = deepcopy(network)
        # if network.isBinary():

        while not network.checkTreeBasedNonBinary2():
            VN = network_copy.vertices
            LN = network_copy.getAllLeafs()
            GN = network_copy.makeBiPartiteGraph()
            GN.hopcroftKarp()
            network_copy.applyOppositeMatchingToGraph2(GN)
            network_copy = network_copy.simplifyNetwork()
            LNPrime = network_copy.getAllLeafsInDegreeIndependant()
            while LN != LNPrime:
                CL = []
                for leaf in LNPrime:
                    if leaf not in LN:
                        CL.append(leaf)
                for vertex in CL:
                    network.arcs[vertex] = []
                    for reverseArc in network.reverseArcs[vertex]:
                        arc = [reverseArc[1], reverseArc[0]]
                        network_copy.removeArc(arc)
                    network_copy.vertices.remove(vertex)
                LNPrime = network_copy.getAllLeafsInDegreeIndependant()
            network = network_copy.simplifyNetwork()
            VNPrime = network_copy.vertices
            if VN == VNPrime:
                print("EARLY ESCAPE")
                return network_copy
        return network_copy

            # while not network.checkTreeBasedNonBinary2():
            #     G = network.makeBiPartiteGraph()
            #     G.displayMatchingGraph()
            #     G.hopcroftKarp()
            #     G.displayGraph()
            #     G.displayMatchingGraph()
            #     network.applyOppositeMatchingToGraph(G)
            #     network = network.simplifyNetwork()
        # else:
        #     # while not network.checkTreeBasedNonBinary2():
        #         original_leaves = network.getAllLeafs()
        #     #     G = network.makeBiPartiteGraph()
        #     #     G.hopcroftKarp()
        #     #     network.applyOppositeMatchingToGraph(G)
        #     #     network = network.simplifyNetwork()
        #
        #
        #         obpg = network.makeOmnianBipartiteGraph2()
        #         # cc = self.omnianConnectedComponents(obpg, network)
        #         network.applyOmnianOppositeMatchingToGraph(obpg)
        #         network = network.simplifyNetwork()
        #         new_leafs = network.getAllLeafs()
        #         for leaf in new_leafs:
        #             if leaf not in original_leaves:
        #                 network.arcs[leaf] = []
        #                 network.reverseArcs[leaf] = []
        #                 network.vertices.remove(leaf)
        # return network






