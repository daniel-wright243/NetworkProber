import math

from TreeSpotter.DAG import DAG
from TreeSpotter.MultiLabelledGraph import MultiLabelledGraph
from TreeSpotter.NetworkIndexes import GetRandicIndex, GetRandicIndexMLG


# def measure1(replaced_network, original_network):
#
#     if replaced_network is PhylogeneticNetwork:
#         network1_randic_index = GetRandicIndex(replaced_network)
#     else:
#         network1_randic_index = GetRandicIndexMLG(replaced_network)
#
#     if original_network is PhylogeneticNetwork:
#         network2_randic_index = GetRandicIndex(original_network)
#     else:
#         network2_randic_index = GetRandicIndexMLG(original_network)
#
#     # network1_randic_index = GetRandicIndex(replaced_network)
#     # network2_randic_index = GetRandicIndex(original_network)
#
#     first_index = network1_randic_index/network2_randic_index
#     second_index = network2_randic_index/network1_randic_index
#
#     if first_index > second_index:
#         return first_index
#     else:
#         return second_index
#
#     # return network1_randic_index / network2_randic_index


# def measure2(network1, network2):
#     """
#
#         :type network1: PhylogeneticNetwork
#         :type network2: PhylogeneticNetwork
#     """
#
#     network1_randic_index = GetRandicIndex(network1)
#     network2_randic_index = GetRandicIndex(network2)
#
#     if len(network1.vertices) > len(network2.vertices):
#         max_network_randic = network1_randic_index
#     elif len(network2.vertices) > len(network1.vertices):
#         max_network_randic = network2_randic_index
#     else:
#         max_network_randic = network1_randic_index
#
#     measure_output = abs(network1_randic_index * network2_randic_index)/max_network_randic
#
#     return measure_output

def measure2(network1, network2):
    """

    :type network2: DAG
    :type network1: DAG
    """

    #JACCARD INDEX MEASURE WITH VERTICES

    vertex_counter = 0
    vertex_array = []

    for vertex in network1.vertices:
        vertex_array.append(vertex)
        if vertex in network2.vertices:
            vertex_counter = vertex_counter + 1

    for vertex in network2.vertices:
        if vertex not in vertex_array:
            vertex_array.append(vertex)

    measure_output = 1 - abs(vertex_counter)/abs(len(vertex_array))

    return measure_output


def measure3(network1, network2):
    """

    :type network2: DAG
    :type network1: DAG
    """

    arc_counter = 0
    arc_array = []

    arc_array1 = network1.get_all_arcs()
    arc_array2 = network2.get_all_arcs()

    for arc in arc_array1:
        if arc in arc_array2:
            arc_counter = arc_counter + 1
        else:
            arc_array.append(arc)

    for arc in arc_array2:
        if arc not in arc_array:
            arc_array.append(arc)

    # for vertex in network1.vertices:
    #     for arc in network1.arcs[vertex]:
    #         arc_array.append(arc)
    #         if arc in network2.arcs[vertex]:
    #             arc_counter = arc_counter + 1
    #
    # for vertex in network2.vertices:
    #     for arc in network2.arcs[vertex]:
    #         if arc not in arc_array:
    #             arc_array.append(arc)

    measure_output = 1 - abs(arc_counter)/abs(len(arc_array))

    return measure_output

def measure1(network1, network2):
    """

    :type network2: DAG
    :type network1: DAG
    """

    network1_randic_index = GetRandicIndex(network1)
    network2_randic_index = GetRandicIndex(network2)

    # if len(network1.vertices) > len(network2.vertices):
    #     max_network_randic = network1_randic_index
    # elif len(network2.vertices) > len(network1.vertices):
    #     max_network_randic = network2_randic_index
    # else:
    #     max_network_randic = network1_randic_index

    if network1_randic_index > network2_randic_index:
        max_network_randic = network1_randic_index
    elif network2_randic_index > network1_randic_index:
        max_network_randic = network2_randic_index
    else:
        max_network_randic = network1_randic_index

    output_measure = 1 - (math.sqrt(network1_randic_index*network2_randic_index))/max_network_randic

    return output_measure

def measure1_MLG(network1, network2):
    """

    :type network2: DAG
    :type network1: MultiLabelledGraph
    """

    network1_randic_index = GetRandicIndexMLG(network1)
    network2_randic_index = GetRandicIndex(network2)

    # if len(network1.vertices) > len(network2.vertices):
    #     max_network_randic = network1_randic_index
    # elif len(network2.vertices) > len(network1.vertices):
    #     max_network_randic = network2_randic_index
    # else:
    #     max_network_randic = network1_randic_index

    if network1_randic_index > network2_randic_index:
        max_network_randic = network1_randic_index
    elif network2_randic_index > network1_randic_index:
        max_network_randic = network2_randic_index
    else:
        max_network_randic = network1_randic_index

    output_measure = 1 - (math.sqrt(network1_randic_index * network2_randic_index)) / max_network_randic

    return output_measure


def hybrid_number_measure(network1):
    """

    :type network1: DAG
    """

    tv, rv = network1.get_tree_and_reticulation_vertices()
    # rv = network1.getReticulationVertices()
    total = 0
    for vertex in rv:
        in_degree = len(network1.vertex_dict[vertex]["reverseArcs"])
        # len(network1.reverse_arcs[vertex])
        total = total + in_degree - 1

    return total
