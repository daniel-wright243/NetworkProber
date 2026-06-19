from SubFunctions.MultiLabelledGraph import MultiLabelledGraph
from SubFunctions.PADREAlgorithm import PADREAlgorithm


class Vertex:
    def __init__(self, code, previousVertex):
        self.code = code
        self.previousVertex = previousVertex

def runAlgorithm(mul_tree):
    """

    :type mul_tree: MultiLabelledGraph
    """

    pa = PADREAlgorithm(mul_tree)

    n = len(mul_tree.vertices)

    # GET H_MAX
    path_list = mul_tree.path_list
    max_value = 0
    for path in path_list:
        if max(path) > max_value:
            max_value = max(path)

    h_max = max_value

    #ASSIGN TO EVERY NODE V IN T A CODE C(V) BETWEEN 1 AND N

    vertex_list = []

    for i in range(len(mul_tree.vertices)):
        vertex_list.append(Vertex(pa.computeIsomorpthismCode(mul_tree.vertices[i]), mul_tree.vertices[i]))
        # print(vertex_list[i].code)

    #INITIALIZE A LIST H OF H_MAX LISTS, IN WHICH EACH LIST WILL CONTAON NODES V ORDERED BY THEIR CODE C(V) SO THAT THE LAST LIST CONTAINS p(T) AND ALL REMAINING LISTS ARE EMPTY

    h_max_list = []




