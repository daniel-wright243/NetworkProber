from copy import deepcopy

from TreeSpotter.DAG import DAG
from TreeSpotter.LeafAlgorithm import leaf_algorithm

class leaf_tree_child_algorithm:
    def __init__(self, network):
        """

        :type network: DAG
        """
        self.network = network

    def start_algorithm(self, network):
        """

        :type network: DAG
        """

        network = leaf_algorithm(network).start_algorithm(network)

        ct, cv, cel = network.get_connected_omnian_and_reticulation_list()

        max_vertex = max(network.vertices)

        new_leaves = []

        for omnian in ct:
            for edge in cel:
                if edge[0] == omnian:
                    network.add_vertex_on_edge(max_vertex + 1, edge)
                    network.add_vertex(max_vertex + 2)
                    network.add_arc([max_vertex + 1, max_vertex + 2])
                    # network.remove_arc([max_vertex + 1, edge[1]])
                    new_leaves.append(max_vertex + 2)
                    max_vertex = max_vertex + 2
                    network = network.simplify_network()
                    break

        i = 1
        for leaf in new_leaves:
            while i in network.taxa.values():
                i = i + 1
            network.taxa[leaf] = i
            network.vertex_dict[leaf]["tax"] = i
            i = i + 1

        return network