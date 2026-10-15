from copy import deepcopy

from TreeSpotter.DAG import DAG
from TreeSpotter.BiPartiteGraph import BiPartiteGraph


class leaf_algorithm:
    def __init__(self, network):
        """

        :type network: DAG
        """

        self.network = network

    def start_algorithm(self, network):
        """

        :type network: DAG
        """

        obpg = network.make_omnian_bipartite_graph()

        obpg.hopcroftkarp()

        pair_u, pair_v = obpg.return_hk_matching()

        edge_list = []

        for i in range(len(pair_v)):
            if pair_v[i] != 0:
                edge_list.append([pair_v[i], i])

        ct, cv, cel = network.get_connected_omnian_and_reticulation_list()

        ct.append(0)
        ct.sort()
        cv.append(0)
        cv.sort()

        converted_edge_list = []

        for edge in edge_list:
            converted_edge_list.append([ct[edge[0]], cv[edge[1]]])

        omnian_list = deepcopy(ct)
        omnian_list.remove(0)

        for edge in converted_edge_list:
            if edge[0] in omnian_list:
                omnian_list.remove(edge[0])

        max_vertex = max(network.vertices)

        new_leaves = []

        for omnian in omnian_list:
            for edge in cel:
                if edge[0] == omnian:
                    network.add_vertex_on_edge(max_vertex + 1, edge)
                    network.add_vertex(max_vertex + 2)
                    network.add_arc([max_vertex + 1, max_vertex + 2])
                    network.remove_arc([max_vertex + 1, edge[1]])
                    new_leaves.append(max_vertex + 2)
                    max_vertex = max_vertex + 2
                    network = network.simplify_network()
                    break
        i = 1
        for leaf in new_leaves:
            network.taxa[leaf] = i
            network.vertex_dict[leaf]["tax"] = i
            i = i + 1

        return network

