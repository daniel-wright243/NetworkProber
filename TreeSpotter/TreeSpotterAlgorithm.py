from copy import deepcopy

import networkx

from TreeSpotter.DAG import DAG
from TreeSpotter.PloidyAlgorithm import PolyPloidy
from TreeSpotter.BiPartiteGraph import BiPartiteGraph
from SubFunctions.TreeSpotterFoldingFunction2 import FoldingFunction2
from TreeSpotter.TreeSpotterFoldingFunction3 import FoldingFunction3

class TreeSpotterAlgorithm:

    def __init__(self, network):
        """

        :type network: DAG
        """
        self.network = network

    def start_algorithm(self, decision):
        # self.GetNonTreeBasedComponents(self.network)
        #PLANT THE NETWORK TO MAKE THE ALGORITHM WORK

        if 0 not in self.network.vertices:
            self.network.add_vertex(0)
            self.network.add_arc([0, self.network.root])
            self.network.oldRoot = self.network.root
            self.network.root = 0

        # self.network.displayGraph()

        # self.GetNonTreeBasedComponents(self.network)

        if self.network.is_binary(): # NETWORK IS BINARY
            if self.network.check_tree_based_non_binary():
                self.network.root = self.network.oldRoot
                if [0, 1] in self.network.arcs:
                    self.network.remove_arc([0, 1])
                if 0 in self.network.vertices:
                    self.network.remove_vertex(0)
                # self.network.vertices.remove(0)
                return self.network
            else:
                # self.network.displayGraph()
                # self.GetNonTreeBasedComponentsBinary(self.network)
                if decision:
                    fa_temp = self.poly_ploidy_algorithm_binary(self.network)
                    if [0, 1] in fa_temp.arcs[0]:
                        fa_temp.remove_arc([0, 1])
                    if 0 in fa_temp.vertices:
                        fa_temp.remove_vertex(0)
                        # fa_temp.vertices.remove(0)
                        fa_temp.root = fa_temp.oldRoot
                    return fa_temp
                    # pp = PolyPloidy(self.network)
                    # return pp.startAlgorithm(max(self.network.vertices))
                else:
                    fa_temp = self.folding_algorithm_binary(self.network)
                    fa_temp.remove_arc([0, 1])
                    fa_temp.remove_vertex(0)
                    # fa_temp.vertices.remove(0)
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
            if self.network.check_tree_based_non_binary():
                self.network.root = self.network.oldRoot
                self.network.remove_arc([0, 1])
                self.network.remove_vertex(0)
                # self.network.vertices.remove(0)
                return self.network
            else:
                if decision:
                    fa_temp = self.poly_ploidy_algorithm_non_binary(self.network)
                    fa_temp.remove_arc([0, 1])
                    fa_temp.remove_vertex(0)
                    fa_temp.root = fa_temp.oldRoot
                    # print("PLOIDY LEVEL")
                    # print(fa_temp.get_ploidy_levels())
                    # fa_temp.displayGraph()
                    return fa_temp
                    pp = PolyPloidy(self.network)
                    return pp.startAlgorithm(max(self.network.vertices))
                else:
                    fa_temp = self.get_non_tree_based_components_non_binary(self.network, 1)
                    # fa = FoldingFunction2(self.network)
                    # fa_temp = FoldingFunction3(self.network).startAlgorithm()
                    # # return fa.startAlgorithm()
                    fa_temp.remove_arc([0, 1])
                    fa_temp.remove_vertex(0)
                    # fa_temp.vertices.remove(0)
                    fa_temp.root = fa_temp.oldRoot
                    return fa_temp

    def get_non_tree_based_components(self, network):
        """

        :type network: DAG
        """

        # network.displayGraph()

        bpg = network.make_bipartite_graph()

        # bpg.displayGraph()

        cc = bpg.get_connected_components()

        bpg.hopcroftkarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = bpg.return_hk_matching()

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

        ctv, crv, cel = self.network.get_connected_tree_and_reticulation_vertices()

        for component in non_tree_based_components:
            temp_comp = []
            temp_tree = []
            temp_reticulation = []
            for vertex in component:
                if vertex > bpg.U:
                    # temp_comp.append(self.network.connected_reticulation_vertices[vertex - bpg.U])
                    # temp_reticulation.append(self.network.connected_reticulation_vertices[vertex - bpg.U])
                    temp_comp.append(crv[vertex - bpg.U])
                    temp_reticulation.append(crv[vertex - bpg.U])
                else:
                    temp_comp.append(ctv[vertex])
                    temp_tree.append(ctv[vertex])
            converted_component.append(temp_comp)
            converted_component_trees.append(temp_tree)
            converted_component_reticulation.append(temp_reticulation)

        ## print("CONNECTED COMPONENT")
        ## print(converted_component)

        networkXGraph1 = networkx.DiGraph()

        for key, value in self.network.vertex_dict.items():
            networkXGraph1.add_node(key)
            for arc in value["arcs"]:
                networkXGraph1.add_edge(arc[0], arc[1])

        # for vertex in self.network.vertices:
        #     networkXGraph1.add_node(vertex)
        # for vertex in self.network.arcs:
        #     for arc in vertex:
        #         networkXGraph1.add_edge(arc[0], arc[1])

        for i in range(len(converted_component)):
            temp_component = converted_component[i]
            for tree_vertex in converted_component_trees[i]:
                for arc in self.network.vertex_dict[tree_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in self.network.vertex_dict[tree_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            for reticulation_vertex in converted_component_reticulation[i]:
                for arc in self.network.vertex_dict[reticulation_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in self.network.vertex_dict[reticulation_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])


        # for i in range(len(converted_component)):
        #     temp_component = converted_component[i]
        #     for tree_vertex in converted_component_trees[i]:
        #         for arc in self.network.arcs[tree_vertex]:
        #             if arc[1] not in temp_component:
        #                 temp_component.append(arc[1])
        #         for arc in self.network.reverseArcs[tree_vertex]:
        #             if arc[1] not in temp_component:
        #                 temp_component.append(arc[1])
        #     for reticulation_vertex in converted_component_reticulation[i]:
        #         for arc in self.network.arcs[reticulation_vertex]:
        #             if arc[1] not in temp_component:
        #                 temp_component.append(arc[1])
        #         for arc in self.network.reverseArcs[reticulation_vertex]:
        #             if arc[1] not in temp_component:
        #                 temp_component.append(arc[1])
            ## print("TEMP COMPONENT")
            ## print(temp_component)

            lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

            component_network = self.network.get_network_below_vertex_network_x(lca)

            # component_network.displayGraph()

            simplifiedNetwork = component_network.simplify_network()

            fa_temp = FoldingFunction3(simplifiedNetwork).startAlgorithm(False)
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

    def get_non_tree_based_components_binary(self, network, choice):
        """

        :type network: DAG
        """
        N = deepcopy(network)
        bpg = N.make_bipartite_graph()

        cc = bpg.get_connected_components()

        bpg.hopcroftkarp()

        tree_vertex_array, reticulation_vertex_array = N.get_tree_and_reticulation_vertices()

        # tree_vertex_array = deepcopy(N.connected_tree_vertices)
        # reticulation_vertex_array = deepcopy(N.connected_reticulation_vertices)

        if 0 in tree_vertex_array:
            tree_vertex_array.remove(0)
        if 0 in reticulation_vertex_array:
            reticulation_vertex_array.remove(0)

        # bpg.displayMatchingGraph()

        pairU, pairV = bpg.return_hk_matching()

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

        temp_leaf_list = N.get_all_leaves()

        for i in range(len(converted_component)):

            networkXGraph1 = networkx.DiGraph()
            for key, value in N.vertex_dict.items():
                networkXGraph1.add_node(key)
                for arcs in value["arcs"]:
                    networkXGraph1.add_edge(arcs[0], arcs[1])


            # for vertex in N.vertices:
            #     if vertex != None:
            #         networkXGraph1.add_node(vertex)
            #         for arc in N.arcs[vertex]:
            #             networkXGraph1.add_edge(arc[0], arc[1])
            # for vertex in N.arcs:
            #     for arc in vertex:
            #         networkXGraph1.add_edge(arc[0], arc[1])

            temp_component = converted_component[i]

            for tree_vertex in converted_component_trees[i]:
                for arc in N.vertex_dict[tree_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.vertex_dict[tree_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
            for reticulation_vertex in converted_component_reticulation[i]:
                for arc in N.vertex_dict[reticulation_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.vertex_dict[reticulation_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])

            # for tree_vertex in converted_component_trees[i]:
            #     for arc in N.arcs[tree_vertex]:
            #         if arc[1] not in temp_component:
            #             temp_component.append(arc[1])
            #     for arc in N.reverseArcs[tree_vertex]:
            #         if arc[1] not in temp_component:
            #             temp_component.append(arc[1])
            # for reticulation_vertex in converted_component_reticulation[i]:
            #     for arc in N.arcs[reticulation_vertex]:
            #         if arc[1] not in temp_component:
            #             temp_component.append(arc[1])
            #     for arc in N.reverseArcs[reticulation_vertex]:
            #         if arc[1] not in temp_component:
            #             temp_component.append(arc[1])
            # print("TEMP COMPONENT")
            # print(temp_component)

            for vertex in temp_component:
                if vertex not in networkXGraph1.nodes:
                    temp_component.remove(vertex)

            for key, value in N.vertex_dict.items():
                for arc in value["arcs"]:
                    if arc[0] not in N.vertices:
                        if arc in N.vertex_dict[arc[0]]["arcs"]:
                            N.remove_arc(arc)
                    elif arc[1] not in N.vertices:
                        if arc in N.vertex_dict[arc[0]]["arcs"]:
                            N.remove_arc(arc)

            # for vertex in N.arcs:
            #     for arc in vertex:
            #         if arc[0] not in N.vertices:
            #             if arc in N.arcs[arc[0]]:
            #                 N.arcs[arc[0]].remove(arc)
            #         elif arc[1] not in N.vertices:
            #             if arc in N.arcs[arc[0]]:
            #                 N.arcs[arc[0]].remove(arc)
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
                component_network = N.get_network_below_vertex_network_x(lca)
            except Exception as e:
                # self.network.displayGraph()
                print(temp_component)
                print(networkXGraph1.nodes)
                print(networkXGraph1.edges)
                network.display_graph()
                bpg.display_graph()
                print(str(e))

            component_vertices = component_network.vertices
            connection_arcs_into = []
            connection_arcs_outto = []
            in_out_two_vertices = []
            in_out_two_arcs_in = []
            in_out_two_arcs_out = []

            for vertex in component_vertices:
                if len(component_network.vertex_dict[vertex]["arcs"]) == 1 and len(component_network.vertex_dict[vertex]["reverseArcs"]) == 1:
                    in_out_two_vertices.append(vertex)
                    in_out_two_arcs_in.append([component_network.vertex_dict[vertex]["reverseArcs"][0][1], component_network.vertex_dict[vertex]["reverseArcs"][0][0]])
                    in_out_two_arcs_out.append(component_network.vertex_dict[vertex]["arcs"][0])

            # for vertex in component_vertices:
            #     if len(component_network.arcs[vertex]) == 1 and len(component_network.reverseArcs[vertex]) == 1:
            #         in_out_two_vertices.append(vertex)
            #         in_out_two_arcs_in.append([component_network.reverseArcs[vertex][0][1], component_network.reverseArcs[vertex][0][0]])
            #         in_out_two_arcs_out.append(component_network.arcs[vertex][0])

            for vertex in component_vertices:
                for arc in N.vertex_dict[vertex]["arcs"]:
                    if arc[1] not in component_vertices:
                        connection_arcs_outto.append(arc)
                for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                    if reverseArc[1] not in component_vertices:
                        connection_arcs_into.append([reverseArc[1], reverseArc[0]])

            # for vertex in component_vertices:
            #     for arc in N.arcs[vertex]:
            #         if arc[1] not in component_vertices:
            #             connection_arcs_outto.append(arc)
            #     for reverseArc in N.reverseArcs[vertex]:
            #         if reverseArc[1] not in component_vertices:
            #             connection_arcs_into.append([reverseArc[1], reverseArc[0]])

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
                fa_temp = FoldingFunction3(component_network, network).startAlgorithm(False)
            else:
                fa_temp = PolyPloidy(component_network).startAlgorithm(max(network.vertices), network)
            # return fa.startAlgorithm()
            # fa_temp.displayGraph()

            # print("FA TEMP VERTICES")
            # print(fa_temp.vertices)

            vertex_above_old_root = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
            # vertex_above_old_root = network.reverseArcs[component_network.root][0][1]

            for vertex in component_network.vertices:
                if vertex in N.vertices:
                    N.remove_vertex(vertex)
                # for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                #     N.remove_arc([reverseArc[1], reverseArc[0]])
                # for arc in N.vertex_dict[vertex]["arcs"]:
                #     N.remove_arc(arc)
                # if vertex in N.taxa.keys():
                #     N.taxa.pop(vertex)

            #REMOVE OLD COMPONENT FROM GRAPH
            # for vertex in component_network.vertices:
            #     if vertex in N.vertices:
            #         N.vertices.remove(vertex)
            #     for reverseArc in N.reverseArcs[vertex]:
            #         N.removeArc([reverseArc[1], reverseArc[0]])
            #     for arc in network.arcs[vertex]:
            #         N.removeArc(arc)
            #     if vertex in N.taxDict.keys():
            #         N.taxDict.pop(vertex)

            # N.displayGraph()

            # self.network.displayGraph()



            for vertex in fa_temp.vertices:
                N.add_vertex(vertex)

            for arc in fa_temp.arcs:
                N.add_arc(arc)

            for key in fa_temp.taxa.keys():
                N.taxa[key] = fa_temp.taxa.get(key)

            # for vertex in fa_temp.arcs:
            #     for arc in vertex:
            #         N.createArc(arc)
            #
            # for key in fa_temp.taxDict.keys():
            #     N.taxDict[key] = fa_temp.taxDict.get(key)

            rv_vertices = []
            leaf_vertices = []

            for key, value in fa_temp.vertex_dict.items():
                if len(value["arcs"]) == 1 and len(value["reverseArcs"]) >= 2:
                    rv_vertices.append(key)
                elif len(value["arcs"]) == 0 and len(value["reverseArcs"]) == 1:
                    leaf_vertices.append(key)


            # for i in range(len(fa_temp.arcs)):
            #     if len(fa_temp.arcs[i]) == 1 and len(fa_temp.reverseArcs[i]) >= 2:
            #         rv_vertices.append(i)
            #     if len(fa_temp.arcs[i]) == 0 and len(fa_temp.reverseArcs[i]) == 1:
            #         leaf_vertices.append(i)
            # print("RV VERTICES")
            # print(rv_vertices)
            #
            # print("CONNECTION ARCS INTO")
            # print(connection_arcs_into)

            ca_list = []

            for arc in connection_arcs_into:
                finished = False
                if arc[1] in fa_temp.vertices:
                    N.add_arc(arc)
                    finished = True
                else:
                    vertex_below = network.vertex_dict[arc[1]]["arcs"][0][1]
                    # vertex_below = network.arcs[arc[1]][0][1]
                    if vertex_below not in fa_temp.vertices:
                        for arc_temp in network.vertex_dict[arc[1]]["reverseArcs"]:
                        # for arc_temp in network.reverseArcs[arc[1]]:
                            if arc_temp[1] in fa_temp.vertices:
                                vertex_above = arc_temp[1]
                                # print("VERTEX ABOVE")
                                # print(vertex_above)
                                for arc2 in fa_temp.vertex_dict[vertex_above]["arcs"]:
                                    vertex_below = arc2[1]
                                # for arc2 in fa_temp.arcs[vertex_above]:
                                #     vertex_below = arc2[1]
                                # vertex_below = fa_temp.arcs[vertex_above][0][1]
                                #     print("VERTEX BELOW")
                                #     print(vertex_below)
                                    if vertex_below in rv_vertices:
                                        N.add_arc([arc[0], vertex_below])
                                        finished = True
                                        break
                if finished == False:
                    ca_list.append(arc)

            # print("CA LIST")
            # print(ca_list)

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
                    N.add_arc(arc)

            new_leaf_list = []
            for key, value in N.vertex_dict.items():
                if len(value["arcs"]) == 0 and len(value["reverseArcs"]) == 1:
                    new_leaf_list.append(key)
            # for i in range(len(N.vertices)):
            #     if len(N.arcs[i]) == 0 and len(N.reverseArcs[i]) == 1:
            #         new_leaf_list.append(i)

            # fa_temp.displayGraph()

            if choice != 1:
                N.add_arc([vertex_above_old_root, fa_temp.root])
                OriginalPloidyNetwork, OriginalPloidyLeafs = network.get_ploidy_level_of_each_vertex_and_connections()
                # print("ORIGINAL PLOIDY NETWORK")
                # print(OriginalPloidyNetwork)
                # print("ORIGINAL PLOIDY LEAFS")
                # print(OriginalPloidyLeafs)
                ComponentPloidyNetwork, CompontentPloidyLeafs = fa_temp.get_ploidy_level_of_each_vertex_and_connections()
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
                        N.add_arc([start_vertex, con_vertex[0]])
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
            for key, value in N.vertex_dict.items():
                if len(value["arcs"]) > 0 or len(value["reverseArcs"]) > 0:
                    vertex_list.append(key)
                if len(value["arcs"]) > 0 and len(value["reverseArcs"]) == 0:
                    N.root = vertex
            # for i in range(len(N.arcs)):
            #     if len(N.arcs[i]) > 0 or len(N.reverseArcs[i]) > 0:
            #         vertex_list.append(i)
            N.vertices = vertex_list


            # for vertex in N.vertices:
            #     if len(N.arcs) > 0 and len(N.reverseArcs) == 0:
            #         N.root = vertex

            break


        # print(new_leaf_list)
        # print(temp_leaf_list)
        # print(self.network.vertices)
        # print(self.network.arcs)
        # print(self.network.reverseArcs)

        # N.displayGraph()

        return N

        # self.network.displayGraph()


    def get_non_tree_based_components_non_binary(self, network, choice):
        """

        :type network: DAG
        """
        N = deepcopy(network)
        obpg = network.make_omnian_bipartite_graph()
        cc = obpg.get_connected_components()

        #ARC LIST TESTS
        for arc in N.get_all_arcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception

        obpg.hopcroftkarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = obpg.return_hk_matching()

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

        ol, rl, cel = self.network.get_connected_omnian_and_reticulation_list()

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

        temp_leaf_list = self.network.get_all_leaves()

        for i in range(len(converted_component)):
            networkXGraph1 = networkx.DiGraph()
            for key, value in network.vertex_dict.items():
                networkXGraph1.add_node(key)
                for arc in value["arcs"]:
                    networkXGraph1.add_edge(arc[0], arc[1])

            # for vertex in N.vertices:
            #     networkXGraph1.add_node(vertex)
            # for vertex in N.arcs:
            #     for arc in vertex:
            #         networkXGraph1.add_edge(arc[0], arc[1])

            temp_component = converted_component[i]
            for tree_vertex in converted_component_trees[i]:
                for arc in N.vertex_dict[tree_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.vertex_dict[tree_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                # for arc in N.arcs[tree_vertex]:
                #     if arc[1] not in temp_component:
                #         temp_component.append(arc[1])
                # for arc in N.reverseArcs[tree_vertex]:
                #     if arc[1] not in temp_component:
                #         temp_component.append(arc[1])
            for reticulation_vertex in converted_component_reticulation[i]:
                for arc in N.vertex_dict[reticulation_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.vertex_dict[reticulation_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                # for arc in N.arcs[reticulation_vertex]:
                #     if arc[1] not in temp_component:
                #         temp_component.append(arc[1])
                # for arc in N.reverseArcs[reticulation_vertex]:
                #     if arc[1] not in temp_component:
                #         temp_component.append(arc[1])
            # print("TEMP COMPONENT")
            # print(temp_component)

            for arc in N.get_all_arcs():
                if arc[0] not in N.vertices or arc[1] not in N.vertices:
                    print(arc)
                    raise Exception

            lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

            component_network = N.get_network_below_vertex_network_x(lca)

            component_vertices = component_network.vertices
            connection_arcs_into = []
            connection_arcs_outto = []

            # component_network.displayGraph()

            for vertex in component_vertices:
                for arc in N.vertex_dict[vertex]["arcs"]:
                    if arc[1] not in component_vertices:
                        connection_arcs_outto.append(arc)
                for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                    if reverseArc[1] not in component_vertices:
                        connection_arcs_into.append([reverseArc[1], reverseArc[0]])

            # for vertex in component_vertices:
            #     for arc in N.arcs[vertex]:
            #         if arc[1] not in component_vertices:
            #             connection_arcs_outto.append(arc)
            #     for reverseArc in N.reverseArcs[vertex]:
            #         if reverseArc[1] not in component_vertices:
            #             connection_arcs_into.append([reverseArc[1], reverseArc[0]])

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
                fa_temp = FoldingFunction3(component_network, network).startAlgorithm(False)
            else:
                fa_temp = PolyPloidy(component_network).startAlgorithm(max(network.vertices), network)
                # fa_temp.displayGraph()
            # return fa.startAlgorithm()
            # fa_temp.displayGraph()

            # print("NEW TAX DICT")
            # print(fa_temp.taxDict)

            # print("FA TEMP VERTICES")
            # print(fa_temp.vertices)

            vertex_above_old_root = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
            # vertex_above_old_root = network.reverseArcs[component_network.root][0][1]

            for vertex in component_network.vertices:
                if vertex in N.vertices:
                    N.vertices.remove(vertex)
                for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                    N.remove_arc([reverseArc[1], reverseArc[0]])
                for arc in N.vertex_dict[vertex]["arcs"]:
                    N.remove_arc(arc)

            #REMOVE OLD COMPONENT FROM GRAPH
            # for vertex in component_network.vertices:
            #     if vertex in N.vertices:
            #         N.vertices.remove(vertex)
            #     for reverseArc in N.reverseArcs[vertex]:
            #         N.removeArc([reverseArc[1], reverseArc[0]])
            #     for arc in self.network.arcs[vertex]:
            #         N.removeArc(arc)



            # self.network.displayGraph()

            for vertex in fa_temp.vertices:
                N.add_vertex(vertex)

            for arc in fa_temp.arcs:
                N.add_arc(arc)


            # for vertex in fa_temp.arcs:
            #     for arc in vertex:
            #         N.createArc(arc)

            for key in fa_temp.taxa.keys():
                N.taxa[key] = fa_temp.taxa.get(key)

            # for arc in connection_arcs_into:
            #     if arc[1] in fa_temp.vertices:
            #         N.createArc(arc)

            rv_vertices = []
            leaf_vertices = []

            for key, value in fa_temp.vertex_dict.items():
                if len(value["arcs"]) == 1 and len(value["reverseArcs"]) >= 2:
                    rv_vertices.append(key)
                elif len(value["arcs"]) == 0 and len(value["reverseArcs"]) == 1:
                    leaf_vertices.append(key)

            # for i in range(len(fa_temp.arcs)):
            #     if len(fa_temp.arcs[i]) == 1 and len(fa_temp.reverseArcs[i]) >= 2:
            #         rv_vertices.append(i)
            #     if len(fa_temp.arcs[i]) == 0 and len(fa_temp.reverseArcs[i]) == 1:
            #         leaf_vertices.append(i)

            ca_list = []

            N = self.reintegration_algorithm(N, fa_temp, connection_arcs_into, connection_arcs_outto, network)

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

        # print("N TAX DICT")
        # print(N.taxa)

        return N

    def reintegration_algorithm(self, network, component, input_arc_list, output_arc_list, original_network):
        """

        :type component: DAG
        :type network: DAG
        """


        for arc in input_arc_list:
            #FIND PARENTS OF H(A)
            A_a = []
            B_b = []
            for arc_above in network.vertex_dict[arc[1]]["reverseArcs"]:
                A_a.append(arc_above[1])
            # for arc_above in network.reverseArcs[arc[1]]:
            #     A_a.append(arc_above[1])
            if arc[0] in A_a:
                A_a.remove(arc[0])
            # if arc[0] in A_a:
            #     A_a.remove(arc[0])
            for arc_below in network.vertex_dict[arc[1]]["arcs"]:
                B_b.append(arc_below[1])
            # for arc_below in network.arcs[arc[1]]:
            #     B_b.append(arc_below[1])
            if arc[1] in component.vertices:
                if len(component.vertex_dict[arc[1]]["arcs"]) == 1 and len(component.vertex_dict[arc[1]]["reverseArcs"]) > 1:
                    network.add_arc(arc)
                elif len(component.vertex_dict[arc[1]]["arcs"]) == 1 and len(component.vertex_dict[arc[1]]["reverseArcs"]) > 1:
                    network.add_arc(arc)
                else:
                    # print("COMPONENT.REVERSEARCS")
                    # print(component.reverse_arcs)
                    # print("ARC[1]")
                    # print(arc[1])
                    # component.displayGraph()
                    # print(component.vertex_dict[arc[1]]["reverseArcs"])
                    if len(component.vertex_dict[arc[1]]["reverseArcs"]) > 0:
                        vertex_above = component.vertex_dict[arc[1]]["reverseArcs"][0][1]
                        # vertex_above = component.reverseArcs[arc[1]][0][1]
                        # vertex_above = A_a[0]
                        a_prime = [vertex_above, arc[1]]
                        network = self.subdivide_arc_and_connect(a_prime, network, arc[0])
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
                            a_prime = network.vertex_dict[vertex_above]["arcs"][0]
                            # a_prime = network.arcs[vertex_above][0]
                            network = self.subdivide_arc_and_connect(a_prime, network, arc[0])
                        elif vertex_below_exists:
                            a_prime = network.vertex_dict[vertex_below]["reverseArcs"][0]
                            # a_prime = network.reverseArcs[vertex_below][0]
                            network = self.subdivide_arc_and_connect(a_prime, network, arc[0])
                        else:
                            OriginalPloidyNetwork, OriginalPloidyLeafs = network.get_ploidy_level_of_each_vertex_and_connections()
                            ComponentPloidyNetwork, CompontentPloidyLeafs = component.get_ploidy_level_of_each_vertex_and_connections()
                            start_vertex = arc[0]
                            end_vertex = arc[1]
                            con_vertex = []
                            end_vertex_ploidy_level = OriginalPloidyNetwork.get(end_vertex)
                            end_vertex_leaf_below = OriginalPloidyLeafs.get(end_vertex)
                            share_ploidy_level_keys = [key for key, val in ComponentPloidyNetwork.items() if
                                                       val == end_vertex_ploidy_level]
                            # print("SHARE PLOIDY LEVEL KEYS")
                            # print(share_ploidy_level_keys)
                            share_ploidy_leaf_keys = [key for key, val in CompontentPloidyLeafs.items() if
                                                      val == end_vertex_leaf_below]
                            # print("SHARE PLOIDY LEAF KEYS")
                            # print(share_ploidy_leaf_keys)
                            for key in share_ploidy_level_keys:
                                if key in share_ploidy_leaf_keys:
                                    con_vertex.append(key)
                            if len(con_vertex) > 0:
                                network.add_arc([start_vertex, con_vertex[0]])
                            else:
                                if len(share_ploidy_leaf_keys) > 0:
                                    network.add_arc([start_vertex, share_ploidy_leaf_keys[0]])
                                else:
                                    return network
                # if len(component.arcs[arc[1]]) == 1 and len(component.reverseArcs[arc[1]]) > 1:
                #     network.createArc(arc)
                # elif len(component.arcs[arc[1]]) > 1 and len(component.reverseArcs[arc[1]]) == 0:
                #     network.createArc(arc)
                # else:
                #     print("COMPONENT.REVERSEARCS")
                #     print(component.reverseArcs)
                #     print("ARC[1]")
                #     print(arc[1])
                #     # component.displayGraph()
                #     vertex_above = component.reverseArcs[arc[1]][0][1]
                #     #vertex_above = A_a[0]
                #     a_prime = [vertex_above, arc[1]]
                #     network = self.subdivideArcAndConnect(a_prime, network, arc[0])
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
                    a_prime = network.vertex_dict[vertex_above]["arcs"][0]
                    # a_prime = network.arcs[vertex_above][0]
                    network = self.subdivide_arc_and_connect(a_prime, network, arc[0])
                elif vertex_below_exists:
                    a_prime = network.vertex_dict[vertex_below]["reverseArcs"][0]
                    # a_prime = network.reverseArcs[vertex_below][0]
                    network = self.subdivide_arc_and_connect(a_prime, network, arc[0])
                else:
                    OriginalPloidyNetwork, OriginalPloidyLeafs = network.get_ploidy_level_of_each_vertex_and_connections()
                    ComponentPloidyNetwork, CompontentPloidyLeafs = component.get_ploidy_level_of_each_vertex_and_connections()
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
                        network.add_arc([start_vertex, con_vertex[0]])
                    else:
                        if len(share_ploidy_leaf_keys) > 0:
                            network.add_arc([start_vertex, share_ploidy_leaf_keys[0]])
                        else:
                            return network
        return network

                #subdivide a with a new vertex s, and create arc from t(a) to s

    def subdivide_arc_and_connect(self, arc, network, connection_vertex):
        """

        :type network: DAG
        """

        S = max(network.vertices) + 1  # CREATE S
        network.add_vertex(S)
        network.remove_arc(arc) # REMOVE ORIGINAL ARC
        network.add_arc([arc[0], S]) # ARC FROM INPUT TO S
        network.add_arc([S, arc[1]]) # ARC FROM S TO OUTPUT
        network.add_arc([connection_vertex, S])

        return network


    def folding_algorithm_binary(self, network):
        """

        :type network: DAG
        """
        N = deepcopy(network)
        i = 0
        while not N.check_tree_based_binary():
            N = self.get_non_tree_based_components_binary(N, 1)
            i = i + 1
            if i > 10:
                break
        return N

    def folding_algorithm_non_binary(self, network):
        """

        :type network: DAG
        """
        N = deepcopy(network)
        i = 0
        while not N.check_tree_based_non_binary():
            N = self.get_non_tree_based_components_non_binary(N, 1)
            i = i + 1
            if i > 10:
                break
        # print(N.vertices)
        # print(N.get_all_arcs())
        return N

    def poly_ploidy_algorithm_binary(self, network):
        N = self.get_non_tree_based_components_binary(network, 0)
        return N

    def poly_ploidy_algorithm_non_binary(self, network):
        N = self.get_non_tree_based_components_non_binary(network, 0)
        return N

    def omnian_connected_components(self, obpg, network):
        """

        :type network: DAG
        :type obpg: BiPartiteGraph
        """
        cc = obpg.get_connected_components()

        # ARC LIST TESTS
        for arc in network.get_all_arcs():
            if arc[0] not in network.vertices or arc[1] not in network.vertices:
                print(arc)
                raise Exception

        obpg.hopcroftkarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = obpg.return_hk_matching()

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

        ol, rl = network.get_connected_omnian_and_reticulation_list()

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

    def bipartite_graph_algorithm(self, network):
        """

        :type network: DAG
        """
        network_copy = deepcopy(network)
        # if network.isBinary():

        while not network.check_tree_based_non_binary():
            VN = network_copy.vertices
            LN = network_copy.get_all_leaves()
            GN = network_copy.make_bipartite_graph()
            GN.hopcroftkarp()
            network_copy.apply_opposite_matching_to_graph(GN)
            network_copy = network_copy.simplify_network()
            LNPrime = network_copy.get_all_leaves()

            while LN != LNPrime:
                CL = []
                for leaf in LNPrime:
                    if leaf not in LN:
                        CL.append(leaf)
                for vertex in CL:
                    network_copy.remove_vertex(vertex)
                LNPrime = network_copy.get_all_leaves()
            network = network_copy.simplify_network()
            VNPrime = network_copy.vertices
            if VN == VNPrime:
                return network_copy

        return network_copy

        #     while LN != LNPrime:
        #         CL = []
        #         for leaf in LNPrime:
        #             if leaf not in LN:
        #                 CL.append(leaf)
        #         for vertex in CL:
        #             network.arcs[vertex] = []
        #             for reverseArc in network.reverseArcs[vertex]:
        #                 arc = [reverseArc[1], reverseArc[0]]
        #                 network_copy.removeArc(arc)
        #             network_copy.vertices.remove(vertex)
        #         LNPrime = network_copy.getAllLeafsInDegreeIndependant()
        #     network = network_copy.simplifyNetwork()
        #     VNPrime = network_copy.vertices
        #     if VN == VNPrime:
        #         print("EARLY ESCAPE")
        #         return network_copy
        # return network_copy

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

    def tree_based_to_normal_algorithm(self, network):
        """

        :type network: DAG
        """

        temp_network = deepcopy(network)

        while not network.is_normal():

            VN = temp_network.vertices
            LN = temp_network.get_all_leaves()

            obpg = network.make_omnian_bipartite_graph()
            obpg.hopcroftkarp()
            # M = obpg.return_hk_matching()

            temp_network.apply_omnian_opposite_matching_to_graph(obpg)

            LNPrime = temp_network.get_all_leaves()

            while LN != LNPrime:
                CL = []
                for leaf in LNPrime:
                    if leaf not in LN:
                        CL.append(leaf)
                for vertex in CL:
                    temp_network.remove_vertex(vertex)
                LNPrime = temp_network.get_all_leaves()
            network = temp_network.simplify_network()

            VNPrime = temp_network.vertices

            if VN == VNPrime:
                return temp_network

        return temp_network

        #     while LN != LNPrime:
        #         CL = []
        #         for leaf in LNPrime:
        #             if leaf not in LN:
        #                 CL.append(leaf)
        #         for vertex in CL:
        #             network.arcs[vertex] = []
        #             for reverseArc in network.reverseArcs[vertex]:
        #                 arc = [reverseArc[1], reverseArc[0]]
        #                 temp_network.removeArc(arc)
        #             temp_network.vertices.remove(vertex)
        #         LNPrime = temp_network.getAllLeafsInDegreeIndependant()
        #     network = temp_network.simplifyNetwork()
        #
        #     VNPrime = temp_network.vertices
        #
        #     if VN == VNPrime:
        #         return temp_network
        #
        # return temp_network

    # def treeBasedToTreeChildAlgorithm(self, network):
    #     """
    #
    #     :type network: PhylogeneticNetwork
    #     """
    #
    #     temp_network = deepcopy(network)
    #
    #     while not network.isTreeChild():
    #         VN = temp_network.vertices
    #         LN = temp_network.getAllLeafsInDegreeIndependant()
    #
    #         obpg = network.makeOmnianBipartiteGraph2()
    #         # obpg.displayGraph()
    #         obpg.hopcroftKarp()
    #         M = obpg.returnHKMatching()
    #         # print("MATCHING")
    #         # print(M)
    #
    #         temp_network.applyOmnianOppositeMatchingToGraph(obpg)
    #
    #         obpg = network.makeOmnianBipartiteGraph2()
    #         # obpg.displayGraph()
    #
    #         LNPrime = temp_network.getAllLeafsInDegreeIndependant()
    #
    #         while LN != LNPrime:
    #             CL = []
    #             for leaf in LNPrime:
    #                 if leaf not in LN:
    #                     CL.append(leaf)
    #             for vertex in CL:
    #                 network.arcs[vertex] = []
    #                 for reverseArc in network.reverseArcs[vertex]:
    #                     arc = [reverseArc[1], reverseArc[0]]
    #                     temp_network.removeArc(arc)
    #                 temp_network.vertices.remove(vertex)
    #             LNPrime = temp_network.getAllLeafsInDegreeIndependant()
    #         network = temp_network.simplifyNetwork()
    #
    #         VNPrime = temp_network.vertices
    #
    #         if VN == VNPrime:
    #             return temp_network
    #
    #     return temp_network

    def tree_based_to_tree_child_algorithm(self, network):
        """

        :type network: DAG
        """

        temp_network = deepcopy(network)

        while not network.is_tree_child():
            VN = temp_network.vertices
            LN = temp_network.get_all_leaves()

            ON = temp_network.get_all_omnians()

            for omnian in ON:

                vertices_above = []
                vertices_below = []

                for arc in temp_network.vertex_dict[omnian]["reverseArcs"]:
                    vertices_above.append(arc[1])
                    temp_network.remove_arc([arc[1], arc[0]])

                for arc in temp_network.vertex_dict[omnian]["arcs"]:
                    vertices_below.append(arc[1])
                    temp_network.remove_arc([arc[0], arc[1]])

                # for arc in temp_network.reverseArcs[omnian]:
                #     vertices_above.append(arc[1])
                #     temp_network.removeArc([arc[1], arc[0]])
                #
                # for arc in temp_network.arcs[omnian]:
                #     vertices_below.append(arc[1])
                #     temp_network.removeArc([arc[0], arc[1]])

                temp_network.remove_vertex(omnian)

                for vertex in vertices_above:
                    for vertex2 in vertices_below:
                        temp_network.add_arc([vertex, vertex2])



            # obpg = network.makeOmnianBipartiteGraph2()
            # obpg.hopcroftKarp()
            # M = obpg.returnHKMatching()
            #
            # temp_network.applyOmnianOppositeMatchingToGraph(obpg)

            LNPrime = temp_network.get_all_leaves()

            while LN != LNPrime:
                CL = []
                for leaf in LNPrime:
                    if leaf not in LN:
                        CL.append(leaf)
                for vertex in CL:
                    temp_network.remove_vertex(vertex)
                LNPrime = temp_network.get_all_leaves()
            network = temp_network.simplify_network()

            VNPrime = temp_network.vertices

            if VN == VNPrime:
                return temp_network

        return temp_network

            # while LN != LNPrime:
            #     CL = []
            #     for leaf in LNPrime:
            #         if leaf not in LN:
            #             CL.append(leaf)
            #     for vertex in CL:
            #         network.arcs[vertex] = []
            #         for reverseArc in network.reverseArcs[vertex]:
            #             arc = [reverseArc[1], reverseArc[0]]
            #             temp_network.removeArc(arc)
            #         temp_network.vertices.remove(vertex)
            #     LNPrime = temp_network.getAllLeafsInDegreeIndependant()
            # network = temp_network.simplifyNetwork()
            #
            # VNPrime = temp_network.vertices

        #     if VN == VNPrime:
        #         return temp_network
        #
        # return temp_network

    def TreeChildAlgorithm(self, network):
        """

        :type network: DAG
        """

        while not network.is_tree_child():
            l_n = network.get_all_leaves()
            main_v_n = network.arcs
            bpg = network.make_omnian_bipartite_graph()
            bpg.hopcroftkarp()
            network.apply_omnian_opposite_matching_to_graph(bpg)
            l_n_prime = network.get_all_leaves()
            while l_n != l_n_prime:
                v_n = network.vertices
                for leaf in l_n_prime:
                    if leaf not in l_n:
                        network.remove_vertex(leaf)
                v_n_prime = network.vertices
                if v_n == v_n_prime:
                    break
            network = network.simplify_network()
            main_v_n_prime = network.arcs
            if main_v_n == main_v_n_prime:
                break
        return network

    def reintegration_algorithm2(self, network, component, input_arc_list, output_arc_list, original_leaf_list, vertex_above_component, old_taxa):
        """

        :type component: DAG
        :type network: DAG
        """

        # component.display_graph()

        network_base_tree = network.get_base_tree()
        component_base_tree = component.get_base_tree()

        network_base_tree_vertices = network_base_tree.vertices
        network_base_tree_arcs = network_base_tree.arcs
        component_base_tree_vertices = component_base_tree.vertices
        component_base_tree_arcs = component_base_tree.arcs

        new_network = deepcopy(network)

        new_input_arc_list = []
        other_arc_list = []

        for arc in input_arc_list:
            if arc[0] in network_base_tree_vertices and arc[1] in component_base_tree_vertices:
                new_input_arc_list.append(arc)
            else:
                other_arc_list.append(arc)

        for vertex in component.vertices:
            if vertex not in network.vertices:
                new_network.add_vertex(vertex)

        for vertex in component.vertices:
            for arc in component.vertex_dict[vertex]["arcs"]:
                new_network.add_arc(arc)

        for arc in input_arc_list:
            if arc[0] in new_network.vertices and arc[1] in new_network.vertices:
                new_network.add_arc(arc)

        if vertex_above_component != -1:
            new_network.add_arc([vertex_above_component, component.root])

        new_network_leaves = new_network.get_all_leaves()

        component_leaf_set = component.get_all_leaves()

        # while new_network_leaves != new_network.taxa.keys():
        #     old_vertex_set = new_network.vertices
        #     for leaf in new_network_leaves:
        #         if leaf not in new_network.taxa.keys():
        #             new_network.remove_vertex(leaf)
        #     new_vertex_set = new_network.vertices
        #     new_network_leaves = new_network.get_all_leaves()
        #
        #     if old_vertex_set == new_vertex_set:
        #         break

        while new_network_leaves != original_leaf_list:
            old_vertex_set = new_network.vertices
            for leaf in new_network_leaves:
                if leaf not in original_leaf_list:
                    if leaf not in component_leaf_set:
                        new_network.remove_vertex(leaf)
            new_network_leaves = new_network.get_all_leaves()
            new_vertex_set = new_network.vertices

            if old_vertex_set == new_vertex_set:
                break

        vertices_to_remove = []

        for key, value in new_network.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 1:
                vertices_to_remove.append(key)

        for vertex in vertices_to_remove:
            new_network.remove_vertex(vertex)



        for key, value in component.taxa.items():
            if value in old_taxa.values():
                new_network.taxa[key] = value
                new_network.vertex_dict[key]["tax"] = value

        # print("OLD TAXA")
        # print(old_taxa)
        # print("NEW TAXA")
        # print(new_network.taxa)

        while True:
            removed_vertex = False
            for leaf in new_network.get_all_leaves():
                if leaf not in new_network.taxa.keys():
                    new_network.remove_vertex(leaf)
                    removed_vertex = True
            if removed_vertex == False:
                break



        # for key, value in component.taxa.items():




        # old_dict = []
        # new_dict = []
        #
        # for key, value in new_network.taxa.items():
        #     old_dict.append(key)
        #
        # while old_dict != new_network.get_all_leaves():
        #     old_leaf_set = new_network.get_all_leaves()
        #     for leaf in old_leaf_set:
        #         if leaf not in old_dict:
        #             new_network.remove_vertex(leaf)
        #     if old_leaf_set == new_network.get_all_leaves():
        #         break

        #
        # for arc in new_input_arc_list:
        #     new_network.add_arc(arc)
        #
        # for key in component.taxa.keys():
        #     new_network.taxa[key] = component.taxa.get(key)
        #     new_network.vertex_dict[key]["tax"] = component.taxa.get(key)
        #
        # VN = network.get_all_leaves()
        # VNPrime = new_network.get_all_leaves()
        #
        # while VN != VNPrime:
        #     old_vertex_list = new_network.vertices
        #     for leaf in VNPrime:
        #         if leaf not in VN:
        #             new_network.remove_vertex(leaf)
        #     new_vertex_list = new_network.vertices
        #     if old_vertex_list == new_vertex_list:
        #         return new_network

        return new_network

    def folding_algorithm_new_reintegration(self, network):
            """

            :type network: DAG
            """

            for leaf in network.get_all_leaves():
                if leaf not in network.taxa.keys():
                    network.taxa[leaf] = leaf
                    network.vertex_dict[leaf]["tax"] = leaf

            N = deepcopy(network)
            obpg = network.make_omnian_bipartite_graph()
            cc = obpg.get_connected_components()
            original_network_leaf_set = network.get_all_leaves()

            # print("COMPONENTS")
            # for component in cc:
            #     print(component)

            # ARC LIST TESTS
            for arc in N.get_all_arcs():
                if arc[0] not in N.vertices or arc[1] not in N.vertices:
                    print(arc)
                    raise Exception

            obpg.hopcroftkarp()

            # bpg.displayMatchingGraph()

            pairU, pairV = obpg.return_hk_matching()

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
                # print("COMPONENT")
                # print(component)
                for vertex in component:
                    if vertex not in vertex_set and vertex <= obpg.U:
                        non_tree_based_components.append(component)
                        break

            # obpg.display_graph()
            # print("NONTREEBASED COMPONENTS")
            # print(non_tree_based_components)

            converted_component = []
            converted_component_trees = []
            converted_component_reticulation = []

            ol, rl, cel = self.network.get_connected_omnian_and_reticulation_list()

            # for component in non_tree_based_components:
            #     temp_comp = []
            #     temp_tree = []
            #     temp_reticulation = []
            #     for vertex in component:
            #         if vertex > obpg.U:
            #             temp_comp.append(rl[vertex - obpg.U])
            #             temp_reticulation.append(rl[vertex - obpg.U])
            #         else:
            #             temp_comp.append(ol[vertex])
            #             temp_tree.append(ol[vertex])
            #     converted_component.append(temp_comp)
            #     converted_component_trees.append(temp_tree)
            #     converted_component_reticulation.append(temp_reticulation)

            for component in non_tree_based_components:
                cc, col, crv = network.convert_bp_component_to_edge_list_omnian(obpg, component)
                converted_component.append(cc)
                converted_component_trees.append(col)
                converted_component_reticulation.append(crv)
                # for omnian in col:
                #     converted_component_trees.append(omnian)
                # for reticulation in crv:
                #     converted_component_reticulation.append(reticulation)

            print("CONVERTED COMPONENT")
            print(converted_component)

            temp_leaf_list = self.network.get_all_leaves()

            networkXGraph1 = networkx.DiGraph()
            for key, value in network.vertex_dict.items():
                networkXGraph1.add_node(key)
                for arc in value["arcs"]:
                    networkXGraph1.add_edge(arc[0], arc[1])

            temp_component = converted_component[0]
            for tree_vertex in converted_component_trees[0]:
                for arc in N.vertex_dict[tree_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.vertex_dict[tree_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])

            for reticulation_vertex in converted_component_reticulation[0]:
                for arc in N.vertex_dict[reticulation_vertex]["arcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])
                for arc in N.vertex_dict[reticulation_vertex]["reverseArcs"]:
                    if arc[1] not in temp_component:
                        temp_component.append(arc[1])



            for arc in N.get_all_arcs():
                if arc[0] not in N.vertices or arc[1] not in N.vertices:
                    print(arc)
                    raise Exception

            lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

            component_network = N.get_network_below_vertex_network_x(lca)

            component_vertices = component_network.vertices
            connection_arcs_into = []
            connection_arcs_outto = []

            # component_network.displayGraph()

            for vertex in component_vertices:
                for arc in N.vertex_dict[vertex]["arcs"]:
                    if arc[1] not in component_vertices:
                        connection_arcs_outto.append(arc)
                for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                    if reverseArc[1] not in component_vertices:
                        connection_arcs_into.append([reverseArc[1], reverseArc[0]])

            # for vertex in component_vertices:
            #     for arc in N.arcs[vertex]:
            #         if arc[1] not in component_vertices:
            #             connection_arcs_outto.append(arc)
            #     for reverseArc in N.reverseArcs[vertex]:
            #         if reverseArc[1] not in component_vertices:
            #             connection_arcs_into.append([reverseArc[1], reverseArc[0]])

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

            independant_component = deepcopy(component_network)

            if component_network.root != network.root:
                vertex_above_component = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
            else:
                vertex_above_component = -1

            # component_network.display_graph()
            fa_temp = FoldingFunction3(component_network, network).startAlgorithm(True)
            # fa_temp.display_graph()
            # return fa.startAlgorithm()
            # fa_temp.displayGraph()

            for key, value in independant_component.vertex_dict.items():
                N.remove_vertex(key)

            # print("NEW TAX DICT")
            # print(fa_temp.taxDict)

            # print("FA TEMP VERTICES")
            # print(fa_temp.vertices)

            # if network.root != component_network.root:
            #     vertex_above_old_root = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
            # # vertex_above_old_root = network.reverseArcs[component_network.root][0][1]
            #
            # for vertex in component_network.vertices:
            #     if vertex in N.vertices:
            #         N.vertices.remove(vertex)
            #     for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
            #         N.remove_arc([reverseArc[1], reverseArc[0]])
            #     for arc in N.vertex_dict[vertex]["arcs"]:
            #         N.remove_arc(arc)
            #
            # for key, value in fa_temp.vertex_dict.items():
            #     N.add_vertex(key)
            #
            # for key, value in fa_temp.vertex_dict.items():
            #     for arc in value["arcs"]:
            #         N.add_arc(arc)
            #
            # # for vertex in fa_temp.vertices:
            # #     N.add_vertex(vertex)
            # #
            # # for arc in fa_temp.arcs:
            # #     N.add_arc(arc)
            #
            # for key in fa_temp.taxa.keys():
            #     N.taxa[key] = fa_temp.taxa.get(key)
            #
            # rv_vertices = []
            # leaf_vertices = []
            #
            # for key, value in fa_temp.vertex_dict.items():
            #     if len(value["arcs"]) == 1 and len(value["reverseArcs"]) >= 2:
            #         rv_vertices.append(key)
            #     elif len(value["arcs"]) == 0 and len(value["reverseArcs"]) == 1:
            #         leaf_vertices.append(key)
            #
            # ca_list = []

            # fa_temp.display_graph()

            # print("FA TEMP TAXA")
            # print(fa_temp.taxa)

            if len(N.vertices) == 0:
                N = fa_temp
            else:
                N = self.reintegration_algorithm2(N, fa_temp, connection_arcs_into, connection_arcs_outto, original_network_leaf_set, vertex_above_component, network.taxa)
                N = N.simplify_network()

            for key, value in fa_temp.taxa.items():
                N.taxa[key] = value
                N.vertex_dict[key]["tax"] = value


            # print("N TAX DICT")
            # print(N.taxa)

            return N

    def polyploidy_algorithm_new_reintegration(self, network):
        """

        :type network: DAG
        """

        for leaf in network.get_all_leaves():
            if leaf not in network.taxa.keys():
                network.taxa[leaf] = leaf
                network.vertex_dict[leaf]["tax"] = leaf

        old_dict = deepcopy(network.taxa)
        N = deepcopy(network)
        obpg = network.make_omnian_bipartite_graph()
        cc = obpg.get_connected_components()
        original_network_leaf_set = network.get_all_leaves()

        # print("COMPONENTS")
        # for component in cc:
        #     print(component)

        # ARC LIST TESTS
        for arc in N.get_all_arcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception



        network.taxa = N.taxa

        obpg.hopcroftkarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = obpg.return_hk_matching()

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
            print("COMPONENT")
            print(component)
            for vertex in component:
                if vertex not in vertex_set and vertex <= obpg.U:
                    non_tree_based_components.append(component)
                    break

        # obpg.display_graph()
        # print("NONTREEBASED COMPONENTS")
        # print(non_tree_based_components)

        converted_component = []
        converted_component_trees = []
        converted_component_reticulation = []

        ol, rl, cel = self.network.get_connected_omnian_and_reticulation_list()

        # for component in non_tree_based_components:
        #     temp_comp = []
        #     temp_tree = []
        #     temp_reticulation = []
        #     for vertex in component:
        #         if vertex > obpg.U:
        #             temp_comp.append(rl[vertex - obpg.U])
        #             temp_reticulation.append(rl[vertex - obpg.U])
        #         else:
        #             temp_comp.append(ol[vertex])
        #             temp_tree.append(ol[vertex])
        #     converted_component.append(temp_comp)
        #     converted_component_trees.append(temp_tree)
        #     converted_component_reticulation.append(temp_reticulation)

        for component in non_tree_based_components:
            cc, col, crv = network.convert_bp_component_to_edge_list_omnian(obpg, component)
            converted_component.append(cc)
            converted_component_trees.append(col)
            converted_component_reticulation.append(crv)
            # for omnian in col:
            #     converted_component_trees.append(omnian)
            # for reticulation in crv:
            #     converted_component_reticulation.append(reticulation)

        # print("CONVERTED COMPONENT")
        # print(converted_component)

        temp_leaf_list = self.network.get_all_leaves()

        networkXGraph1 = networkx.DiGraph()
        for key, value in network.vertex_dict.items():
            networkXGraph1.add_node(key)
            for arc in value["arcs"]:
                networkXGraph1.add_edge(arc[0], arc[1])

        temp_component = converted_component[0]
        for tree_vertex in converted_component_trees[0]:
            for arc in N.vertex_dict[tree_vertex]["arcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])
            for arc in N.vertex_dict[tree_vertex]["reverseArcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])

        for reticulation_vertex in converted_component_reticulation[0]:
            for arc in N.vertex_dict[reticulation_vertex]["arcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])
            for arc in N.vertex_dict[reticulation_vertex]["reverseArcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])

        for arc in N.get_all_arcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception

        lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

        component_network = N.get_network_below_vertex_network_x(lca)

        component_vertices = component_network.vertices
        connection_arcs_into = []
        connection_arcs_outto = []

        # component_network.displayGraph()

        for vertex in component_vertices:
            for arc in N.vertex_dict[vertex]["arcs"]:
                if arc[1] not in component_vertices:
                    connection_arcs_outto.append(arc)
            for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                if reverseArc[1] not in component_vertices:
                    connection_arcs_into.append([reverseArc[1], reverseArc[0]])

        # for vertex in component_vertices:
        #     for arc in N.arcs[vertex]:
        #         if arc[1] not in component_vertices:
        #             connection_arcs_outto.append(arc)
        #     for reverseArc in N.reverseArcs[vertex]:
        #         if reverseArc[1] not in component_vertices:
        #             connection_arcs_into.append([reverseArc[1], reverseArc[0]])

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

        independant_component = deepcopy(component_network)

        if component_network.root != network.root:
            vertex_above_component = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
        else:
            vertex_above_component = -1

        # component_network.display_graph()
        fa_temp = PolyPloidy(component_network).startAlgorithm(max(network.vertices), network)
        # fa_temp = FoldingFunction3(component_network, network).startAlgorithm(True)
        # fa_temp.display_graph()
        # return fa.startAlgorithm()
        # fa_temp.displayGraph()

        for key, value in independant_component.vertex_dict.items():
            N.remove_vertex(key)

        # print("NEW TAX DICT")
        # print(fa_temp.taxDict)

        # print("FA TEMP VERTICES")
        # print(fa_temp.vertices)

        # if network.root != component_network.root:
        #     vertex_above_old_root = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
        # # vertex_above_old_root = network.reverseArcs[component_network.root][0][1]
        #
        # for vertex in component_network.vertices:
        #     if vertex in N.vertices:
        #         N.vertices.remove(vertex)
        #     for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
        #         N.remove_arc([reverseArc[1], reverseArc[0]])
        #     for arc in N.vertex_dict[vertex]["arcs"]:
        #         N.remove_arc(arc)
        #
        # for key, value in fa_temp.vertex_dict.items():
        #     N.add_vertex(key)
        #
        # for key, value in fa_temp.vertex_dict.items():
        #     for arc in value["arcs"]:
        #         N.add_arc(arc)
        #
        # # for vertex in fa_temp.vertices:
        # #     N.add_vertex(vertex)
        # #
        # # for arc in fa_temp.arcs:
        # #     N.add_arc(arc)
        #
        # for key in fa_temp.taxa.keys():
        #     N.taxa[key] = fa_temp.taxa.get(key)
        #
        # rv_vertices = []
        # leaf_vertices = []
        #
        # for key, value in fa_temp.vertex_dict.items():
        #     if len(value["arcs"]) == 1 and len(value["reverseArcs"]) >= 2:
        #         rv_vertices.append(key)
        #     elif len(value["arcs"]) == 0 and len(value["reverseArcs"]) == 1:
        #         leaf_vertices.append(key)
        #
        # ca_list = []

        # fa_temp.display_graph()

        # print("FA TEMP TAXA")
        # print(fa_temp.taxa)

        if len(N.vertices) == 0:
            N = fa_temp
            N = N.simplify_network()
        else:



            N = self.reintegration_algorithm2(N, fa_temp, connection_arcs_into, connection_arcs_outto,
                                              original_network_leaf_set, vertex_above_component, old_dict)

            N = N.simplify_network()

        for key, value in fa_temp.taxa.items():
            N.taxa[key] = value
            N.vertex_dict[key]["tax"] = value

        # print("N TAX DICT")
        # print(N.taxa)

        vertices_to_be_removed = []

        for key, value in N.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) == 0:
                if key not in N.vertices:
                    vertices_to_be_removed.append(key)

        for vertex in vertices_to_be_removed:
            N.vertex_dict.pop(vertex)

        # N = N.simplify_network()
        #
        # for leaf in N.get_all_leaves():
        #     if leaf not in N.taxa.keys():
        #         N.remove_vertex(leaf)
        #
        # N = N.simplify_network()

        return N

    def minimised_ployploidy_algorithm(self, network):
        """

        :type network: DAG
        """

        for leaf in network.get_all_leaves():
            if leaf not in network.taxa.keys():
                network.taxa[leaf] = leaf
                network.vertex_dict[leaf]["tax"] = leaf

        N = deepcopy(network)
        obpg = network.make_omnian_bipartite_graph()
        cc = obpg.get_connected_components()
        original_network_leaf_set = network.get_all_leaves()

        # print("COMPONENTS")
        # for component in cc:
        #     print(component)

        # ARC LIST TESTS
        for arc in N.get_all_arcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception

        obpg.hopcroftkarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = obpg.return_hk_matching()

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
            # print("COMPONENT")
            # print(component)
            for vertex in component:
                if vertex not in vertex_set and vertex <= obpg.U:
                    non_tree_based_components.append(component)
                    break

        # obpg.display_graph()
        # print("NONTREEBASED COMPONENTS")
        # print(non_tree_based_components)

        converted_component = []
        converted_component_trees = []
        converted_component_reticulation = []

        ol, rl, cel = self.network.get_connected_omnian_and_reticulation_list()

        # for component in non_tree_based_components:
        #     temp_comp = []
        #     temp_tree = []
        #     temp_reticulation = []
        #     for vertex in component:
        #         if vertex > obpg.U:
        #             temp_comp.append(rl[vertex - obpg.U])
        #             temp_reticulation.append(rl[vertex - obpg.U])
        #         else:
        #             temp_comp.append(ol[vertex])
        #             temp_tree.append(ol[vertex])
        #     converted_component.append(temp_comp)
        #     converted_component_trees.append(temp_tree)
        #     converted_component_reticulation.append(temp_reticulation)

        for component in non_tree_based_components:
            cc, col, crv = network.convert_bp_component_to_edge_list_omnian(obpg, component)
            converted_component.append(cc)
            converted_component_trees.append(col)
            converted_component_reticulation.append(crv)
            # for omnian in col:
            #     converted_component_trees.append(omnian)
            # for reticulation in crv:
            #     converted_component_reticulation.append(reticulation)

        # print("CONVERTED COMPONENT")
        # print(converted_component)

        temp_leaf_list = self.network.get_all_leaves()

        networkXGraph1 = networkx.DiGraph()
        for key, value in network.vertex_dict.items():
            networkXGraph1.add_node(key)
            for arc in value["arcs"]:
                networkXGraph1.add_edge(arc[0], arc[1])

        temp_component = converted_component[0]
        for tree_vertex in converted_component_trees[0]:
            for arc in N.vertex_dict[tree_vertex]["arcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])
            for arc in N.vertex_dict[tree_vertex]["reverseArcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])

        for reticulation_vertex in converted_component_reticulation[0]:
            for arc in N.vertex_dict[reticulation_vertex]["arcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])
            for arc in N.vertex_dict[reticulation_vertex]["reverseArcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])

        for arc in N.get_all_arcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception

        lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

        component_network = N.get_network_between_all_vertices_networkx(lca, temp_component)

        component_vertices = component_network.vertices
        connection_arcs_into = []
        connection_arcs_outto = []

        # component_network.displayGraph()

        for vertex in component_vertices:
            for arc in N.vertex_dict[vertex]["arcs"]:
                if arc[1] not in component_vertices:
                    connection_arcs_outto.append(arc)
            for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                if reverseArc[1] not in component_vertices:
                    connection_arcs_into.append([reverseArc[1], reverseArc[0]])

        independant_component = deepcopy(component_network)

        component_network = component_network.simplify_network()

        if component_network.root != network.root:
            vertex_above_component = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
        else:
            vertex_above_component = -1

        new_roots = []

        for key, value in component_network.vertex_dict.items():
            if len(value["arcs"]) > 0 and len(value["reverseArcs"]) == 0:
                if key != component_network.root:
                    component_network.add_arc([component_network.root, key])

        fa_temp = PolyPloidy(component_network).startAlgorithm(max(network.vertices), network)
        fa_temp = fa_temp.simplify_network()

        while not fa_temp.check_tree_based_non_binary():
            original_vertex_length = len(fa_temp.vertices)
            fa_temp = fa_temp.simplify_network()
            fa_temp = PolyPloidy(fa_temp).startAlgorithm(max(network.vertices), network)
            after_vertex_length = len(fa_temp.vertices)
            if original_vertex_length == after_vertex_length:
                break

        # if not fa_temp.check_tree_based_non_binary():
        #     fa_temp = fa_temp.simplify_network()
        #     fa_temp = PolyPloidy(fa_temp).startAlgorithm(max(network.vertices), network)

        vertices_to_be_removed = []

        for key, value in fa_temp.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) == 0:
                vertices_to_be_removed.append(key)

        for vertex in vertices_to_be_removed:
            if vertex in fa_temp.vertices:
                fa_temp.remove_vertex(vertex)
            elif vertex in fa_temp.vertex_dict.keys():
                fa_temp.vertex_dict.pop(vertex)

        # fa_temp = FoldingFunction3(component_network, network).startAlgorithm(True)

        for key, value in independant_component.vertex_dict.items():
            N.remove_vertex(key)

        if len(N.vertices) == 0:
            N = fa_temp
        else:
            N = self.reintegration_algorithm3(N, fa_temp, connection_arcs_into, connection_arcs_outto, original_network_leaf_set, vertex_above_component, network.taxa)
            N = N.simplify_network()

        for key, value in fa_temp.taxa.items():
            N.taxa[key] = value
            N.vertex_dict[key]["tax"] = value

        return N

    def minimised_folding_algorithm(self, network):
        """

        :type network: DAG
        """

        for leaf in network.get_all_leaves():
            if leaf not in network.taxa.keys():
                network.taxa[leaf] = leaf
                network.vertex_dict[leaf]["tax"] = leaf

        N = deepcopy(network)
        obpg = network.make_omnian_bipartite_graph()
        cc = obpg.get_connected_components()
        original_network_leaf_set = network.get_all_leaves()

        # print("COMPONENTS")
        # for component in cc:
        #     print(component)

        # ARC LIST TESTS
        for arc in N.get_all_arcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception

        obpg.hopcroftkarp()

        # bpg.displayMatchingGraph()

        pairU, pairV = obpg.return_hk_matching()

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
            # print("COMPONENT")
            # print(component)
            for vertex in component:
                if vertex not in vertex_set and vertex <= obpg.U:
                    non_tree_based_components.append(component)
                    break

        # obpg.display_graph()
        # print("NONTREEBASED COMPONENTS")
        # print(non_tree_based_components)

        converted_component = []
        converted_component_trees = []
        converted_component_reticulation = []

        ol, rl, cel = self.network.get_connected_omnian_and_reticulation_list()

        # for component in non_tree_based_components:
        #     temp_comp = []
        #     temp_tree = []
        #     temp_reticulation = []
        #     for vertex in component:
        #         if vertex > obpg.U:
        #             temp_comp.append(rl[vertex - obpg.U])
        #             temp_reticulation.append(rl[vertex - obpg.U])
        #         else:
        #             temp_comp.append(ol[vertex])
        #             temp_tree.append(ol[vertex])
        #     converted_component.append(temp_comp)
        #     converted_component_trees.append(temp_tree)
        #     converted_component_reticulation.append(temp_reticulation)

        for component in non_tree_based_components:
            cc, col, crv = network.convert_bp_component_to_edge_list_omnian(obpg, component)
            converted_component.append(cc)
            converted_component_trees.append(col)
            converted_component_reticulation.append(crv)
            # for omnian in col:
            #     converted_component_trees.append(omnian)
            # for reticulation in crv:
            #     converted_component_reticulation.append(reticulation)

        # print("CONVERTED COMPONENT")
        # print(converted_component)

        temp_leaf_list = self.network.get_all_leaves()

        networkXGraph1 = networkx.DiGraph()
        for key, value in network.vertex_dict.items():
            networkXGraph1.add_node(key)
            for arc in value["arcs"]:
                networkXGraph1.add_edge(arc[0], arc[1])

        temp_component = converted_component[0]
        for tree_vertex in converted_component_trees[0]:
            for arc in N.vertex_dict[tree_vertex]["arcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])
            for arc in N.vertex_dict[tree_vertex]["reverseArcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])

        for reticulation_vertex in converted_component_reticulation[0]:
            for arc in N.vertex_dict[reticulation_vertex]["arcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])
            for arc in N.vertex_dict[reticulation_vertex]["reverseArcs"]:
                if arc[1] not in temp_component:
                    temp_component.append(arc[1])

        for arc in N.get_all_arcs():
            if arc[0] not in N.vertices or arc[1] not in N.vertices:
                print(arc)
                raise Exception

        lca = self.lowest_common_ancestor_multiple(networkXGraph1, temp_component)

        component_network = N.get_network_between_all_vertices_networkx(lca, temp_component)

        component_vertices = component_network.vertices
        connection_arcs_into = []
        connection_arcs_outto = []

        # component_network.displayGraph()

        for vertex in component_vertices:
            for arc in N.vertex_dict[vertex]["arcs"]:
                if arc[1] not in component_vertices:
                    connection_arcs_outto.append(arc)
            for reverseArc in N.vertex_dict[vertex]["reverseArcs"]:
                if reverseArc[1] not in component_vertices:
                    connection_arcs_into.append([reverseArc[1], reverseArc[0]])

        independant_component = deepcopy(component_network)

        if component_network.root != network.root:
            vertex_above_component = network.vertex_dict[component_network.root]["reverseArcs"][0][1]
        else:
            vertex_above_component = -1



        fa_temp = FoldingFunction3(component_network, network).startAlgorithm(True)

        if not fa_temp.check_tree_based_non_binary():
            fa_temp = fa_temp.simplify_network()
            fa_temp = FoldingFunction3(fa_temp, network).startAlgorithm(True)

        for key, value in independant_component.vertex_dict.items():
            N.remove_vertex(key)

        if len(N.vertices) == 0:
            N = fa_temp
        else:
            N = self.reintegration_algorithm3(N, fa_temp, connection_arcs_into, connection_arcs_outto, original_network_leaf_set, vertex_above_component, network.taxa)
            N = N.simplify_network()


        try:
            for key, value in fa_temp.taxa.items():
                N.taxa[key] = value
                N.vertex_dict[key]["tax"] = value
        except KeyError:
            print("KEYERROR")
            print(network.vertices)
            print(network.arcs)
            print(network.root)
            Exception()



        return N

    def reintegration_algorithm3(self, network, component, input_arc_list, output_arc_list, original_leaf_list, vertex_above_component, old_taxa):
        """

        :type component: DAG
        :type network: DAG
        """

        # component.display_graph()

        network_base_tree = network.get_base_tree()
        component_base_tree = component.get_base_tree()

        network_base_tree_vertices = network_base_tree.vertices
        network_base_tree_arcs = network_base_tree.arcs
        component_base_tree_vertices = component_base_tree.vertices
        component_base_tree_arcs = component_base_tree.arcs

        new_network = deepcopy(network)

        new_input_arc_list = []
        other_arc_list = []

        for arc in input_arc_list:
            if arc[0] in network_base_tree_vertices and arc[1] in component_base_tree_vertices:
                new_input_arc_list.append(arc)
            else:
                if arc not in new_network.arcs:
                    other_arc_list.append(arc)

        for vertex in component.vertices:
            if vertex not in network.vertices:
                new_network.add_vertex(vertex)

        for vertex in component.vertices:
            for arc in component.vertex_dict[vertex]["arcs"]:
                new_network.add_arc(arc)

        input_arcs_not_used = []

        for arc in input_arc_list:
            if arc[0] in new_network.vertices and arc[1] in new_network.vertices:
                new_network.add_arc(arc)
            else:
                if arc not in new_network.arcs:
                    input_arcs_not_used.append(arc)

        for arc in output_arc_list:
            if arc[0] in new_network.vertices and arc[1] in new_network.vertices:
                new_network.add_arc(arc)
            else:
                if arc[1] in new_network.vertices:
                    new_network.add_arc([component.root, arc[1]])

        if vertex_above_component != -1:
            new_network.add_arc([vertex_above_component, component.root])

        new_network_leaves = new_network.get_all_leaves()

        component_leaf_set = component.get_all_leaves()

        while new_network_leaves != original_leaf_list:
            old_vertex_set = new_network.vertices
            for leaf in new_network_leaves:
                if leaf not in original_leaf_list:
                    if leaf not in component_leaf_set:
                        new_network.remove_vertex(leaf)
            new_network_leaves = new_network.get_all_leaves()
            new_vertex_set = new_network.vertices

            if old_vertex_set == new_vertex_set:
                break

        vertices_to_remove = []

        for key, value in new_network.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 1:
                vertices_to_remove.append(key)

        for vertex in vertices_to_remove:
            new_network.remove_vertex(vertex)



        for key, value in component.taxa.items():
            if value in old_taxa.values():
                if key in new_network.vertex_dict.keys():
                    new_network.taxa[key] = value
                    new_network.vertex_dict[key]["tax"] = value

        # print("OLD TAXA")
        # print(old_taxa)
        # print("NEW TAXA")
        # print(new_network.taxa)

        while True:
            removed_vertex = False
            for leaf in new_network.get_all_leaves():
                if leaf not in new_network.taxa.keys():
                    new_network.remove_vertex(leaf)
                    removed_vertex = True
            if removed_vertex == False:
                break

        arc_list = []

        if len(input_arcs_not_used) > 0:
            vertex_above_root = new_network.vertex_dict[component.root]["reverseArcs"][0][1]
            new_vertex = max(new_network.vertices) + 1
            new_network.add_vertex_on_edge(max(new_network.vertices) + 1, [vertex_above_root, component.root])
            for arc in input_arcs_not_used:
                new_network.add_arc([arc[0], new_vertex])

        for arc in new_network.get_all_arcs():
            if arc in arc_list:
                new_network.remove_arc(arc)
            else:
                arc_list.append(arc)

        return new_network











