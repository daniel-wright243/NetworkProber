import os
import pathlib
from copy import deepcopy

import graphviz
import networkx
import networkx as nx

from TreeSpotter.BiPartiteGraph import BiPartiteGraph

os.environ["PATH"] += os.pathsep + str(pathlib.Path(__file__).parent.parent.resolve()) + '/venv/Lib/site-packages/graphviz/Graphviz/bin'
class DAG:
    def __init__(self, vertices: list = None, arcs = None, taxa: dict = None, root: int = None):
        if arcs is None:
            arcs = []
        if taxa is None:
            taxa = {}
        if vertices is None:
            vertices = []
        self.vertex_dict = {}
        self.vertices = []
        self.reverse_arcs = []
        for vertex in vertices:
            self.add_vertex(vertex)
        self.arcs = []
        for arc in arcs:
            self.add_arc(arc)
        # for arc in arcs:
        #     reversed_arc = [arc[1], arc[0]]
        #     self.reverse_arcs.append(reversed_arc)
        self.taxa = taxa
        for key, value in self.taxa.items():
            self.vertex_dict[key]["tax"] = value
        self.root = root

    def add_arc(self, arc):

        if arc[0] in self.vertices and arc[1] in self.vertices:
            self.vertex_dict[arc[0]]["arcs"].append(arc)
            self.vertex_dict[arc[1]]["reverseArcs"].append([arc[1], arc[0]])
            self.arcs.append(arc)
            self.reverse_arcs.append([arc[1], arc[0]])

    def remove_arc(self, arc):

        if arc in self.arcs:
            if arc[0] in self.vertices and arc[1] in self.vertices:
                if arc in self.vertex_dict[arc[0]]["arcs"]:
                    self.vertex_dict[arc[0]]["arcs"].remove(arc)
                if [arc[1], arc[0]] in self.vertex_dict[arc[1]]["reverseArcs"]:
                    self.vertex_dict[arc[1]]["reverseArcs"].remove([arc[1], arc[0]])
                if arc in self.arcs:
                    self.arcs.remove(arc)
                if [arc[1], arc[0]] in self.reverse_arcs:
                    self.reverse_arcs.remove([arc[1], arc[0]])

    def add_vertex(self, vertex):
        self.vertex_dict[vertex] = {"arcs": [], "reverseArcs": [], "tax": None}
        # self.vertex_dict[vertex]["arcs"] = []
        # self.vertex_dict[vertex]["reverseArcs"] = []
        # self.vertex_dict[vertex]["tax"] = None
        self.vertices.append(vertex)

    def remove_vertex(self, vertex):
        arcs = deepcopy(self.vertex_dict[vertex]["arcs"])
        reverse_arcs = deepcopy(self.vertex_dict[vertex]["reverseArcs"])

        # REMOVE ARCS GOING FROM VERTEX

        for arc in arcs:
            self.remove_arc(arc)
            # arcs = self.vertex_dict[vertex]["arcs"]


        #REMOVE ARCS GOING TO VERTEX

        for reverse_arc in reverse_arcs:
            arc = [reverse_arc[1], reverse_arc[0]]
            self.remove_arc(arc)





        # for arc in arcs:
        #     reversed_arc = [arc[1], arc[0]]
        #     self.reverse_arcs.remove(reversed_arc)
        #     self.vertex_dict[arc[1]]["reverseArcs"].remove(reversed_arc)
        #     self.vertex_dict[arc[0]]["arcs"].remove(arc)
        # for reverse_arc in reverse_arcs:
        #     arc = [reverse_arc[1], reverse_arc[0]]
        #     self.reverse_arcs.remove(reverse_arc)
        #     self.arcs.remove(arc)
        #     self.vertex_dict[arc[1]]["reverseArcs"].remove(reverse_arc)
        #     self.vertex_dict[arc[0]]["arcs"].remove(arc)
        self.vertices.remove(vertex)
        self.vertex_dict.pop(vertex)
        if vertex in self.taxa.keys():
            self.taxa.pop(vertex)

    def change_root(self, new_root):

        if new_root in self.vertices:
            self.root = new_root

    def get_all_paths(self):
        network_x_graph = networkx.DiGraph()
        leafs = []
        for key, value in self.vertex_dict.items():
            network_x_graph.add_node(key)
            for arc in value["arcs"]:
                network_x_graph.add_edge(arc[0], arc[1])
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 0:
                leafs.append(key)
        path_list = []
        for leaf in leafs:
            network_x_path_list = networkx.all_simple_paths(network_x_graph, self.root, leaf)
            for path in network_x_path_list:
                path_list.append(path)
        return path_list

    def check_cyclicity(self):
        network_x_graph = networkx.Graph()
        for key, value in self.vertex_dict.items():
            network_x_graph.add_node(key)
            for arc in value["arcs"]:
                network_x_graph.add_edge(arc[0], arc[1])
        cycles = networkx.cycle_basis(network_x_graph, self.root)
        if len(cycles) > 0:
            return True
        else:
            return False

    def get_tree_and_reticulation_vertices(self):
        tree_vertex_array = []
        reticulation_vertex_array = []
        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) == 1 and len(value["reverseArcs"]) > 1:
                reticulation_vertex_array.append(key)
            elif len(value["arcs"]) > 1 and len(value["reverseArcs"]) == 1:
                tree_vertex_array.append(key)
        return tree_vertex_array, reticulation_vertex_array

    def get_tree_vertices(self):
        tree_vertex_array = []
        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) > 1 and len(value["reverseArcs"]) == 1:
                tree_vertex_array.append(key)
        return tree_vertex_array

    def get_reticulation_vertices(self):
        reticulation_vertex_array = []
        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) == 1 and len(value["reverseArcs"]) > 1:
                reticulation_vertex_array.append(key)
        return reticulation_vertex_array

    def get_connected_tree_and_reticulation_vertices(self):
        ctv = []
        crv = []
        cel = []
        tv, rv = self.get_tree_and_reticulation_vertices()
        for tree_vertex in tv:
            for reticulation_vertex in rv:
                if [tree_vertex, reticulation_vertex] in self.vertex_dict[tree_vertex]["arcs"]:
                    if tree_vertex not in ctv:
                        ctv.append(tree_vertex)
                    if reticulation_vertex not in crv:
                        crv.append(reticulation_vertex)
                    cel.append([tree_vertex, reticulation_vertex])

        ctv.sort()
        crv.sort()

        return ctv, crv, cel

    def make_bipartite_graph(self):
        ctv, crv, cel = self.get_connected_tree_and_reticulation_vertices()

        ctv.append(0)
        crv.append(0)

        ctv.sort()
        crv.sort()

        bip_graph = BiPartiteGraph(len(ctv) - 1, len(crv) - 1)

        for edge in cel:
            bip_graph.add_edge(ctv.index(edge[0]), crv.index(edge[1]))

        return bip_graph

    def display_graph(self):
        dot = graphviz.Digraph()
        for key, value in self.vertex_dict.items():
            dot.node(str(key))
            for arc in value["arcs"]:
                dot.edge(str(arc[0]), str(arc[1]))
        dot.view()

    def display_graph_no_interior_vertices(self):
        dot = graphviz.Digraph()
        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 0:
                dot.node(str(key), label='')
            else:
                dot.node(str(key))
            for arc in value["arcs"]:
                dot.edge(str(arc[0]), str(arc[1]))
        dot.view()

    def create_graph_image(self):
        digraph_image = graphviz.Digraph('Images/Phylogenetic Network', comment='Phylogenetic Network')

        digraph_image.attr(labelloc="b")

        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 0:
                if key in self.taxa:
                    digraph_image.node(str(key), shape="point", xlabel=str(value["tax"]), labelloc="b")
                else:
                    digraph_image.node(str(key), shape="point", xlabel=str(key))
            else:
                digraph_image.node(str(key), label='', shape="point")
            for arc in value["arcs"]:
                digraph_image.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))

        digraph_image.render('Images/PhylogeneticNetworkImage', format='png', view=False)

    def apply_matching_to_graph(self, matching_graph: BiPartiteGraph):
        pair_u, pair_v = matching_graph.return_hk_matching()

        edge_list = []

        for i in range(len(pair_v)):
            if pair_v[i] != 0:
                edge_list.append([pair_v[i], i])

        ct, cv, cel = self.get_connected_tree_and_reticulation_vertices()

        ct.append(0)
        ct.sort()
        cv.append(0)
        cv.sort()

        converted_edge_list = []

        for edge in edge_list:
            converted_edge_list.append([ct[edge[0]], cv[edge[1]]])

        for edge in cel:
            if edge not in converted_edge_list:
                self.remove_arc(edge)

    def apply_opposite_matching_to_graph(self, matching_graph: BiPartiteGraph):
        pair_u, pair_v = matching_graph.return_hk_matching()

        edge_list = []

        for i in range(len(pair_v)):
            if pair_v[i] != 0:
                edge_list.append([pair_v[i], i])

        ct, cv, cel = self.get_connected_tree_and_reticulation_vertices()

        ct.append(0)
        ct.sort()
        cv.append(0)
        cv.sort()

        converted_edge_list = []

        for edge in edge_list:
            converted_edge_list.append([ct[edge[0]], cv[edge[1]]])

        for edge in converted_edge_list:
            self.remove_arc(edge)

    def simplify_network(self):
        simplified_network = deepcopy(self)
        vertices_to_be_simplified = []
        for key, value in simplified_network.vertex_dict.items():
            if len(value["arcs"]) == 1 and len(value["reverseArcs"]) == 1:
                vertices_to_be_simplified.append(key)

        for vertex in vertices_to_be_simplified:
            vertex_above = simplified_network.vertex_dict[vertex]["reverseArcs"][0][1]
            vertex_below = simplified_network.vertex_dict[vertex]["arcs"][0][1]

            simplified_network.remove_arc([vertex_above, vertex])
            simplified_network.remove_arc([vertex, vertex_below])
            simplified_network.add_arc([vertex_above, vertex_below])
            simplified_network.remove_vertex(vertex)

        return simplified_network

        # one_to_one_exists = True
        #
        # while one_to_one_exists:
        #     for key, value in simplified_network.vertex_dict.items():
        #         if len(value["arcs"]) == 1 and len(value["reverseArcs"]) == 1:
        #             vertices_to_be_simplified.append(key)
        #
        #     if len(vertices_to_be_simplified) > 0:
        #         vertex_above = simplified_network.vertex_dict[vertices_to_be_simplified[0]]["reverseArcs"][0][1]
        #         vertex_below = simplified_network.vertex_dict[vertices_to_be_simplified[0]]["arcs"][0][1]
        #
        #         simplified_network.remove_arc([vertex_above, vertices_to_be_simplified[0]])
        #         simplified_network.remove_arc([vertices_to_be_simplified[0], vertex_below])
        #         simplified_network.add_arc([vertex_above, vertex_below])
        #         simplified_network.remove_vertex(vertices_to_be_simplified[0])
        #     else:
        #         return simplified_network

    def get_all_leaves(self):
        leaf_array = []
        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 0:
                leaf_array.append(key)
        return leaf_array

    def add_vertex_on_edge(self, vertex_num, edge):
        self.add_vertex(vertex_num)
        self.remove_arc([edge[0], edge[1]])
        self.add_arc([edge[0], vertex_num])
        self.add_arc([vertex_num, edge[1]])

    def get_cycle_basis(self):
        network_x_graph = networkx.Graph()
        for key, value in self.vertex_dict.items():
            network_x_graph.add_node(key)
            for arc in value["arcs"]:
                network_x_graph.add_edge(arc[0], arc[1])
        cycles = networkx.cycle_basis(network_x_graph, self.root)
        return cycles

    def get_connected_component_of_graph_from_bp_graph(self):
        bp_graph = self.make_bipartite_graph()

        connected_components = bp_graph.get_connected_components()

        ct, cv, cel = self.get_connected_tree_and_reticulation_vertices()

        ct.append(0)
        ct.sort()
        cv.append(0)
        cv.sort()

        resolved_comps = []

        for component in connected_components:
            temp_comp = []
            for vertex in component:
                if vertex > bp_graph.U:
                    temp_comp.append(cv[vertex - bp_graph.U])
                else:
                    temp_comp.append(ct[vertex])
            if temp_comp not in resolved_comps:
                resolved_comps.append(temp_comp)

        return resolved_comps

    def get_all_omnians(self):
        tv, rv = self.get_tree_and_reticulation_vertices()

        omnian_list = []

        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) > 0:
                omnian_check = True

                for arc in value["arcs"]:
                    if arc[1] not in rv:
                        omnian_check = False

                if omnian_check:
                    omnian_list.append(key)

        return omnian_list

    def get_connected_omnian_and_reticulation_list(self):
        ol = self.get_all_omnians()

        tv, rv = self.get_tree_and_reticulation_vertices()

        col = []
        crv = []
        cel = []

        for omnian in ol:
            for reticulation in rv:
                if [omnian, reticulation] in self.arcs:
                    if omnian not in col:
                        col.append(omnian)
                    if reticulation not in crv:
                        crv.append(reticulation)
                    cel.append([omnian, reticulation])

        col.sort()
        crv.sort()

        return col, crv, cel


    def make_omnian_bipartite_graph(self):
        col, crv, cel = self.get_connected_omnian_and_reticulation_list()

        col.append(0)
        crv.append(0)

        col.sort()
        crv.sort()

        bip_graph = BiPartiteGraph(len(col) - 1, len(crv) - 1)

        for edge in cel:
            bip_graph.add_edge(col.index(edge[0]), crv.index(edge[1]))

        return bip_graph

    def has_reticulations(self):
        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) == 1 and len(value["reverseArcs"]) > 1:
                return True
        return False

    def display_graph_highlight_edges(self, edge_list, vertex_list):
        dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')

        dot.attr(labelloc="b")

        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 0:
                if key in self.taxa:
                    dot.node(str(key), shape="point", xlabel=str(value["tax"]), labelloc="b")
                else:
                    if key in vertex_list:
                        dot.node(str(key), shape="point", xlabel=str(key), color='blue', penwidth='2')
                    else:
                        dot.node(str(key), shape="point")
            else:
                if key in vertex_list:
                    dot.node(str(key), label='', shape="point", color='blue', penwidth='2')
                else:
                    dot.node(str(key), label='', shape="point")
            for arc in value["arcs"]:
                if arc in edge_list:
                    dot.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2), color='blue', penwidth='2')
                else:
                    dot.edge(str(arc[0]), str(arc[1]), arrowsize=str(0.2))

        dot.view()

    def compare_two_sub_graphs(self, vertex_list1, edge_list1, vertex_list2, edge_list2):
        network_x_graph1 = networkx.DiGraph()
        for vertex in vertex_list1:
            network_x_graph1.add_node(vertex)
        for arc in edge_list1:
            network_x_graph1.add_edge(arc[0], arc[1])

        network_x_graph2 = networkx.DiGraph()
        for vertex in vertex_list2:
            network_x_graph2.add_node(vertex)
        for arc in edge_list2:
            network_x_graph2.add_edge(arc[0], arc[1])

        is_isomorphic = networkx.is_isomorphic(network_x_graph1, network_x_graph2)

        return is_isomorphic

    def is_binary(self):
        for key, value in self.vertex_dict.items():
            if len(value["arcs"]) > 2:
                return False
            if len(value["reverseArcs"]) > 2:
                return False

        return True

    def check_tree_based_binary(self):
        ct, cr, cel = self.get_connected_tree_and_reticulation_vertices()

        bip_graph = self.make_bipartite_graph()

        bip_graph.hopcroftkarp()

        pair_u, pair_v = bip_graph.return_hk_matching()

        if len(ct) == len(pair_u) and len(cr) == len(pair_v):
            return True
        else:
            return False

    def check_tree_based_non_binary(self):
        bip_graph = self.make_omnian_bipartite_graph()

        bip_graph.hopcroftkarp()

        pair_u, pair_v = bip_graph.return_hk_matching()

        while 0 in pair_u:
            pair_u.remove(0)

        while 0 in pair_v:
            pair_v.remove(0)

        # print("PAIRU")
        # print(pair_u)
        # print("PAIRV")
        # print(pair_v)

        ol, rl, cel = self.get_connected_omnian_and_reticulation_list()

        # print("OL")
        # print(ol)

        if len(ol) == 0:
            return True

        if len(pair_u) == len(ol):
            return True
        else:
            return False

    def get_all_arcs(self):
        return self.arcs

    def get_ploidy_levels(self):
        network_x_graph = networkx.DiGraph()
        leafs = []
        ploidy_dict = {}
        ploidy_array = []
        for key, value in self.vertex_dict.items():
            network_x_graph.add_node(key)
            for arc in value["arcs"]:
                network_x_graph.add_edge(arc[0], arc[1])
            if len(value["arcs"]) == 0 and len(value["reverseArcs"]) > 0:
                leafs.append(key)

        for leaf in leafs:
            paths = networkx.all_simple_paths(network_x_graph, source=self.root, target=leaf)
            i = 0
            for path in paths:
                i = i + 1
            ploidy_dict[leaf] = i
            ploidy_array.append(i)

        return ploidy_dict, ploidy_array

    def get_leafs_below_vertex(self, vertex):
        leafs_below = []
        paths = self.get_all_paths()
        for path in paths:
            if vertex in path:
                leaf = path[len(path) - 1]
                if leaf not in leafs_below:
                    leafs_below.append(leaf)
        return leafs_below

    def get_ploidy_level_of_each_vertex_and_connections(self):
        ploidy_dict, ploidy_array = self.get_ploidy_levels()

        level_dict = {}
        leafs_below_dict = {}

        for key, value in ploidy_dict.items():
            leafs_below = self.get_leafs_below_vertex(key)
            level_dict[key] = ploidy_dict[key]
            leafs_below_dict[key] = leafs_below

        return level_dict, leafs_below_dict

    def is_tree_child(self):
        if len(self.get_all_omnians()) == 0:
            return True
        else:
            return False

    def is_normal(self):
        if self.is_tree_child():
            network_x_graph = networkx.DiGraph()
            for key, value in self.vertex_dict.items():
                network_x_graph.add_node(key)
                for arc in value["arcs"]:
                    network_x_graph.add_edge(arc[0], arc[1])

            for vertex1 in self.vertices:
                for vertex2 in self.vertices:
                    simple_paths = networkx.all_simple_paths(network_x_graph, vertex1, vertex2)
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

    def apply_omnian_opposite_matching_to_graph(self, matching_graph: BiPartiteGraph):
        pair_u, pair_v = matching_graph.return_hk_matching()

        edge_list = []

        for i in range(len(pair_v)):
            if pair_v[i] != 0:
                edge_list.append([pair_v[i], i])

        col, crv, cel = self.get_connected_omnian_and_reticulation_list()

        col.append(0)
        crv.append(0)

        col.sort()
        crv.sort()

        edges_to_be_removed = []

        for edge in edge_list:
            edges_to_be_removed.append([col[edge[0]], crv[edge[1]]])

        # for i in range(len(pair_u)):
        #     edges_to_be_removed.append([col[pair_u[i]], crv[pair_v[i]]])

        for edge in edges_to_be_removed:
            if edge[0] != 0 and edge[1] != 0:
                self.remove_arc(edge)

    def get_network_below_vertex_network_x(self, input_vertex):
        networkXGraph = networkx.DiGraph()
        for key, value in self.vertex_dict.items():
            networkXGraph.add_node(key)
            for arc in value["arcs"]:
                networkXGraph.add_edge(arc[0], arc[1])
        # for vertex in self.vertices:
        #     networkXGraph.add_node(vertex)
        # for vertex in self.arcs:
        #     if type(vertex) == list:
        #         for arc in vertex:
        #             networkXGraph.add_edge(arc[0], arc[1])
        #     else:
        #         networkXGraph.add_edge(vertex[0], vertex[1])
        vertices_below = networkx.descendants(networkXGraph, input_vertex)
        vertex_list = []
        arcList = []
        temp_tax_dict = {}

        vertex_list.append(input_vertex)

        for arc in self.vertex_dict[input_vertex]["arcs"]:
            arcList.append(arc)

        for vertex in vertices_below:
            vertex_list.append(vertex)
            for arc in self.vertex_dict[vertex]["arcs"]:
                arcList.append(arc)
            if vertex in self.taxa.keys():
                temp_tax_dict[vertex] = self.taxa.get(vertex)

        # for vertex in vertices_below:
        #     vertex_list.append(vertex)
        #     for arc in self.arcs[vertex]:
        #         arcList.append(arc)
        #     if vertex in self.taxDict.keys():
        #         temp_tax_dict[vertex] = self.taxDict.get(vertex)

        return DAG(vertex_list, arcList, temp_tax_dict, input_vertex)

    def get_network_between_all_vertices_networkx(self, top_vertex, component_vertex_array):
        networkXGraph = networkx.DiGraph()
        for key, value in self.vertex_dict.items():
            networkXGraph.add_node(key)
            for arc in value["arcs"]:
                networkXGraph.add_edge(arc[0], arc[1])

        vertex_array = []
        arc_array = []

        for vertex in component_vertex_array:
            paths = nx.all_simple_paths(networkXGraph, top_vertex, vertex)
            for path in paths:
                for vertex in path:
                    if vertex not in vertex_array:
                        vertex_array.append(vertex)
                arc_list = [[a, b] for a, b in zip(path, path[1:])] # FROM COPILOT
                for arc in arc_list:
                    if arc not in arc_array:
                        arc_array.append(arc)

        tax_dict = {}

        vertices_to_add = []
        arcs_to_add = []

        for vertex in vertex_array:
            for arc in self.vertex_dict[vertex]["arcs"]:
                if arc[1] in self.taxa.keys():
                    if arc not in self.arcs:
                        vertices_to_add.append(arc[1])
                        arcs_to_add.append(arc)

        for vertex in vertices_to_add:
            vertex_array.append(vertex)

        for arc in arcs_to_add:
            arc_array.append(arc)

        for vertex in vertex_array:
            if vertex in self.taxa.keys():
                tax_dict[vertex] = self.taxa.get(vertex)

        return DAG(vertex_array, arc_array, tax_dict, top_vertex)

    def get_base_tree(self):
        bpg = self.make_bipartite_graph()
        bpg.hopcroftkarp()
        network = deepcopy(self)
        network.apply_matching_to_graph(bpg)

        return network

    def convert_hk_matching_to_edge_list_binary(self, bpg):
        """

        :type bpg: BiPartiteGraph
        """
        pair_u, pair_v = bpg.return_hk_matching()

        edge_list = []

        for i in range(len(pair_v)):
            if pair_v[i] != 0:
                edge_list.append([pair_v[i], i])

        ct, cv, cel = self.get_connected_tree_and_reticulation_vertices()

        ct.append(0)
        ct.sort()
        cv.append(0)
        cv.sort()

        converted_edge_list = []

        for edge in edge_list:
            converted_edge_list.append([ct[edge[0]], cv[edge[1]]])

        return converted_edge_list

    def convert_hk_matching_to_edge_list_non_binary(self, bpg):
        """

        :type bpg: BiPartiteGraph
        """
        pair_u, pair_v = bpg.return_hk_matching()

        edge_list = []

        for i in range(len(pair_v)):
            if pair_v[i] != 0:
                edge_list.append([pair_v[i], i])

        ct, cv, cel = self.get_connected_omnian_and_reticulation_list()

        ct.append(0)
        ct.sort()
        cv.append(0)
        cv.sort()

        converted_edge_list = []

        for edge in edge_list:
            converted_edge_list.append([ct[edge[0]], cv[edge[1]]])

        # print(converted_edge_list)

        return converted_edge_list

    def convert_bp_component_to_edge_list(self, bpg, component):
        """

        :type bpg: BiPartiteGraph
        """
        ct, cv, cel = self.get_connected_tree_and_reticulation_vertices()

        converted_component = []

        # print("NEW COMPONENT")
        # print(component)
        # print(ct)
        # print(cv)
        # print(cel)

        for vertex in component:
            if vertex > bpg.U:
                converted_component.append(cv[vertex - bpg.U - 1])
            else:
                converted_component.append(ct[vertex - 1])

        # print(converted_component)

        return converted_component

    def convert_bp_component_to_edge_list_omnian(self, bpg, component):
        """

        :type bpg: BiPartiteGraph
        """
        ct, cv, cel = self.get_connected_omnian_and_reticulation_list()

        converted_component = []
        converted_omnians = []
        converted_reticulations = []

        # print("NEW COMPONENT")
        # print(component)
        # print(ct)
        # print(cv)
        # print(cel)

        for vertex in component:
            if vertex > bpg.U:
                converted_component.append(cv[vertex - bpg.U - 1])
                converted_reticulations.append(cv[vertex - bpg.U - 1])
            else:
                converted_component.append(ct[vertex - 1])
                converted_omnians.append(ct[vertex - 1])

        # print(converted_component)

        return converted_component, converted_omnians, converted_reticulations

    def convertVertex(self, old, new):

        arcs = deepcopy(self.vertex_dict[old]["arcs"])
        reverseArcs = deepcopy(self.vertex_dict[old]["reverseArcs"])

        print("REMOVING OLD")
        print(old)
        print(arcs)
        print(reverseArcs)
        self.remove_vertex(old)
        self.add_vertex(new)
        for arc in arcs:
            self.add_arc([new, arc[1]])
        for arc in reverseArcs:
            self.add_arc([arc[1], new])
        if old == self.root:
            self.root = new

