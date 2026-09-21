import unittest
from TreeSpotter.DAG import DAG

class MyTestCase(unittest.TestCase):
    def test_init(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        self.assertEqual(dag.vertices, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "DAG vertex set initialisation is broken")
        self.assertEqual(dag.arcs, [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]], "DAG arc set initialisation is broken")
        self.assertEqual(dag.vertex_dict[1]["arcs"], [[1, 2], [1, 3]], "DAG vertex dict arcs broken")
        self.assertEqual(dag.vertex_dict[2]["reverseArcs"], [[2, 1]], "DAG vertex dict reverseArcs broken")
        self.assertEqual(dag.vertex_dict[10]["tax"], "X1", "DAG vertex dict tax broken")
        self.assertEqual(dag.reverse_arcs, [[2, 1], [3, 1], [5, 2], [6, 2], [4, 3], [5, 3], [6, 4], [7, 4], [8, 5], [9, 6], [8, 7], [9, 7], [10, 8], [11, 9]], "DAG reverse_arcs initialisation is broken")
        self.assertEqual(dag.taxa, {10: "X1", 11: "X2"})

    def test_add_arc(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        dag.add_arc([2, 4])
        self.assertEqual(dag.arcs, [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8], [7, 9], [8, 10], [9, 11], [2, 4]], "DAG add_arc arc list broken")
        self.assertEqual(dag.reverse_arcs, [[2, 1], [3, 1], [5, 2], [6, 2], [4, 3], [5, 3], [6, 4], [7, 4], [8, 5], [9, 6], [8, 7], [9, 7], [10, 8], [11, 9], [4, 2]], "DAG add_arc reverseArc list broken")
        self.assertEqual(dag.vertex_dict[2]["arcs"], [[2, 5], [2, 6], [2, 4]], "DAG add_arc vertex_dict arc list broken")
        self.assertEqual(dag.vertex_dict[4]["reverseArcs"], [[4, 3], [4, 2]])

    def test_remove_arc(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        dag.remove_arc([1, 3])
        self.assertEqual(dag.arcs, [[1, 2], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]], "DAG remove_arc arcs broken")
        self.assertEqual(dag.reverse_arcs, [[2, 1], [5, 2], [6, 2], [4, 3], [5, 3], [6, 4], [7, 4], [8, 5], [9, 6], [8, 7], [9, 7], [10, 8], [11, 9]])
        self.assertEqual(dag.vertex_dict[1]["arcs"], [[1, 2]], "DAG remove_arc vertex_dict arc list broken")
        self.assertEqual(dag.vertex_dict[3]["reverseArcs"], [], "DAG remove_arc vertex_dict reverseArcs list broken")

    def test_add_vertex(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        dag.add_vertex(12)
        self.assertEqual(dag.vertices, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "DAG add_vertex vertex list broken")
        self.assertEqual(dag.vertex_dict[12]["arcs"], [], "DAG add_vertex vertex_dict broken")

    def test_remove_vertex(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        dag.remove_vertex(3)
        self.assertEqual(dag.vertices, [1,2,4,5,6,7,8,9,10,11], "DAG remove_vertex vertex list broken")
        self.assertEqual(dag.arcs, [[1, 2], [2, 5], [2, 6], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]])
        self.assertEqual(dag.reverse_arcs, [[2, 1], [5, 2], [6, 2], [6, 4], [7, 4], [8, 5], [9, 6], [8, 7], [9, 7], [10, 8], [11, 9]])
        self.assertEqual(dag.vertex_dict[1]["arcs"], [[1, 2]], "DAG remove_vertex arcs broken")
        self.assertEqual(dag.vertex_dict[4]["reverseArcs"], [], "DAG remove_vertex reverseArcs broken")

    def test_change_root(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        dag.change_root(2)
        self.assertEqual(dag.root, 2, "DAG change_root broken")

    def test_get_all_paths(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        self.assertEqual(dag.get_all_paths(), [[1, 2, 5, 8, 10], [1, 3, 4, 7, 8, 10], [1, 3, 5, 8, 10], [1, 2, 6, 9, 11], [1, 3, 4, 6, 9, 11], [1, 3, 4, 7, 9, 11]], "DAG get_all_paths broken")

    def test_check_cyclicity(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        self.assertEqual(dag.check_cyclicity(), True, "DAG check_cyclicity broken")

    def test_get_tree_and_reticulation_vertices(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        tv, rv = dag.get_tree_and_reticulation_vertices()
        self.assertEqual(tv, [2, 3, 4, 7], "DAG get_tree_and_reticulation_vertices wrong tree vertices")
        self.assertEqual(rv, [5, 6, 8, 9], "DAG get_tree_and_reticulation_vertices wrong reticulation vertices")

    def test_get_connected_tree_and_reticulation_vertices(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        ctv, crv, cel = dag.get_connected_tree_and_reticulation_vertices()
        self.assertEqual(ctv, [2, 3, 4, 7], "DAG get_connected_tree_and_reticulation_vertices wrong connected tree vertices")
        self.assertEqual(crv, [5, 6, 8, 9], "DAG get_connected_tree_and_reticulation_vertices wrong connected reticulation vertices")
        self.assertEqual(cel, [[2, 5], [2, 6], [3, 5], [4, 6], [7, 8], [7, 9]], "DAG get_connected_tree_and_reticulation_vertices wrong connected edge list")

    def test_make_bipartite_graph(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        self.assertEqual(bpg.U, 4, "DAG make_bipartite_graph U broken")
        self.assertEqual(bpg.V, 4, "DAG make_bipartite_graph V broken")
        self.assertEqual(bpg.edges, [[], [1, 2], [1], [2], [3, 4]], "DAG make_bipartite_graph edges broken")

    def test_apply_matching_to_graph(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        dag.display_graph()
        bpg = dag.make_bipartite_graph()
        bpg.hopcroftkarp()
        dag.apply_matching_to_graph(bpg)
        self.assertEqual(dag.arcs, [[1, 2], [1, 3], [2, 5], [3, 4], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8], [8, 10], [9, 11]], "DAG apply_matching_to_graph arcs broken")
        self.assertEqual(dag.vertices, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "DAG apply_matching_to_graph vertices broken")
        self.assertEqual(dag.vertex_dict[7]["arcs"], [[7, 8]], "DAG apply_matching_to_graph vertex_dict arcs broken")
        self.assertEqual(dag.vertex_dict[9]["reverseArcs"], [[9, 6]], "DAG apply_matching_to_graph vertex_dict reverseArcs broken")
        # dag.display_graph()

    def test_apply_opposite_matching_to_graph(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.hopcroftkarp()
        dag.apply_opposite_matching_to_graph(bpg)
        self.assertEqual(dag.arcs, [[1, 2], [1, 3], [2, 6], [3, 4], [3, 5], [4, 7], [5, 8], [6, 9], [7, 9], [8, 10], [9, 11]], "DAG apply_opposite_matching_to_graph arcs broken")
        self.assertEqual(dag.vertices, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "DAG apply_opposite_matching_to_graph vertices broken")
        self.assertEqual(dag.vertex_dict[2]["arcs"], [[2, 6]], "DAG apply_opposite_matching_to_graph vertex_dict broken")

    def test_simplify_network(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.hopcroftkarp()
        dag.apply_opposite_matching_to_graph(bpg)
        dag = dag.simplify_network()
        self.assertEqual(dag.vertices, [1, 3, 9, 10, 11], "DAG simplify_network vertices broken")
        self.assertEqual(dag.arcs, [[1, 3], [9, 11], [1, 9], [3, 9], [3, 10]], "DAG simplify_network arcs broken")
        self.assertEqual(dag.vertex_dict[1]["arcs"], [[1, 3], [1, 9]], "DAG simplify_network vertex_dict broken")

    def test_get_all_leaves(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        leafs = dag.get_all_leaves()
        self.assertEqual(leafs, [10, 11], "DAG get_all_leaves broken")

    def test_add_vertex_on_edge(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        dag.add_vertex_on_edge(12, [2, 6])
        self.assertEqual(dag.vertices, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "DAG add_vertex_on_edge vertices broken")
        self.assertEqual(dag.arcs, [[1, 2], [1, 3], [2, 5], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8], [7, 9], [8, 10], [9, 11], [2, 12], [12, 6]], "DAG add_vertex_on_edge arcs broken")
        self.assertEqual(dag.vertex_dict[2]["arcs"], [[2, 5], [2, 12]], "DAG add_vertex_on_edge vertex_dict broken")

    def test_get_cycle_basis(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        cycle_basis = dag.get_cycle_basis()
        self.assertEqual(cycle_basis, [[2, 5, 3, 1], [4, 7, 8, 5, 3], [2, 6, 9, 7, 8, 5], [4, 6, 9, 7]], "DAG get_cycle_basis broken")

    def test_get_all_omnians(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        omnian_list = dag.get_all_omnians()
        self.assertEqual(omnian_list, [2, 5, 6, 7], "DAG get_all_omnians broken")

    def test_get_connected_omnian_and_reticulation_list(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        col, crv, cel = dag.get_connected_omnian_and_reticulation_list()
        self.assertEqual(col, [2, 5, 6, 7], "DAG get_connected_omnian_and_reticulation_list omnian list broken")
        self.assertEqual(crv, [5, 6, 8, 9], "DAG get_connected_omnian_and_reticulation_list reticulation list broken")
        self.assertEqual(cel, [[2, 5], [2, 6], [5, 8], [6, 9], [7, 8], [7, 9]], "DAG get_connected_omnian_and_reticulation_list edge list broken")

    def test_make_omnian_bipartite_graph(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        obpg = dag.make_omnian_bipartite_graph()
        self.assertEqual(obpg.U, 4, "DAG make_omnian_bipartite_graph U broken")
        self.assertEqual(obpg.V, 4, "DAG make_omnian_bipartite_graph V broken")
        self.assertEqual(obpg.edges, [[], [1, 2], [3], [4], [3, 4]], "DAG make_omnian_bipartite_graph edges broken")

    def test_has_reticulations(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        hr = dag.has_reticulations()
        self.assertEqual(hr, True, "DAG has_reticulations broken")

    def test_is_binary(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        ib = dag.is_binary()
        self.assertEqual(ib, True, "DAG is_binary broken")

    def test_check_tree_based_binary(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        is_tree_based = dag.check_tree_based_binary()
        self.assertEqual(is_tree_based, False, "DAG check_tree_based_binary broken")

    def test_check_tree_based_non_binary(self):
        bio_preset1_vertices = []
        for i in range(1, 61):
            bio_preset1_vertices.append(i)
        bio_preset1_arcs = [[1, 2], [1, 42], [2, 3], [2, 41], [3, 58], [3, 4], [4, 5], [4, 40], [5, 8], [5, 6],
                            [6, 7], [6, 12], [7, 9], [7, 11], [8, 9], [8, 60], [9, 10], [10, 40], [10, 36],
                            [11, 33], [11, 34], [12, 29], [12, 13], [13, 14], [13, 29], [14, 15], [14, 30],
                            [15, 27], [15, 25], [15, 24], [15, 23], [15, 22], [15, 21], [15, 20], [16, 18],
                            [16, 17], [17, 57], [18, 19], [19, 56], [19, 17], [20, 16], [21, 18], [22, 55],
                            [23, 54], [24, 53], [25, 26], [26, 31], [26, 52], [27, 28], [28, 32], [28, 51],
                            [29, 30], [30, 31], [31, 49], [32, 50], [33, 20], [33, 21], [33, 22], [33, 23],
                            [33, 24], [33, 25], [33, 27], [33, 31], [33, 59], [34, 35], [35, 37], [36, 35],
                            [36, 38], [37, 46], [37, 47], [38, 44], [39, 38], [40, 39], [41, 43], [58, 41],
                            [58, 39], [59, 48], [59, 32], [60, 34], [60, 45]]
        dag = DAG(bio_preset1_vertices, bio_preset1_arcs, {}, 1)
        is_tree_based = dag.check_tree_based_non_binary()
        self.assertEqual(is_tree_based, False, "DAG check_tree_based_non_binary broken")

    def test_get_all_arcs(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        all_arcs = dag.get_all_arcs()
        self.assertEqual(all_arcs, [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8], [7, 9], [8, 10], [9, 11]], "DAG get_all_arcs broken")

    def test_get_ploidy_levels(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        ploidy_dict, ploidy_array = dag.get_ploidy_levels()
        self.assertEqual(ploidy_dict, {10: 3, 11: 3}, "DAG get_ploidy_levels ploidy_dict broken")
        self.assertEqual(ploidy_array, [3, 3], "DAG get_ploidy_levels ploidy_array broken")

    def test_get_leafs_below_vertex(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        leafs_below = dag.get_leafs_below_vertex(5)
        self.assertEqual(leafs_below, [10], "DAG get_leafs_below_vertex broken")

    def test_get_ploidy_level_of_each_vertex_and_connections(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        level_dict, leafs_below_dict = dag.get_ploidy_level_of_each_vertex_and_connections()

        #THIS NEEDS MORE WORK AS IT DOES NOT SEEM TO BE WORKING CORRECTLY

    def test_is_tree_child(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.hopcroftkarp()
        dag.apply_opposite_matching_to_graph(bpg)
        dag = dag.simplify_network()
        self.assertEqual(dag.is_tree_child(), True, "DAG is_tree_child broken")

    def test_is_normal(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.hopcroftkarp()
        dag.apply_opposite_matching_to_graph(bpg)
        dag = dag.simplify_network()
        self.assertEqual(dag.is_normal(), True, "DAG is_normal broken")

    def test_apply_omnian_opposite_matching_to_graph(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        obpg = dag.make_omnian_bipartite_graph()
        obpg.hopcroftkarp()
        dag.apply_omnian_opposite_matching_to_graph(obpg)
        self.assertEqual(dag.vertices, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "DAG apply_omnian_opposite_matching_to_graph vertices broken")
        self.assertEqual(dag.arcs, [[1, 2], [1, 3], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [7, 8], [7, 9], [8, 10], [9, 11]] , "DAG apply_omnian_opposite_matching_to_graph arcs broken")

    def test_bipartite_graph_init(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        self.assertEqual(bpg.U, 4, "bipartite_graph init U broken")
        self.assertEqual(bpg.V, 4, "bipartite_graph init V broken")
        self.assertEqual(bpg.edges, [[], [1, 2], [1], [2], [3, 4]], "bipartite_graph init edges broken")

    def test_bipartite_graph_add_edge(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.add_edge(1, 3)
        self.assertEqual(bpg.edges, [[], [1, 2, 3], [1], [2], [3, 4]], "bipartite_graph add_edge broken")

    def test_bipartite_graph_remove_edge(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.remove_edge(1, 1)
        self.assertEqual(bpg.edges, [[], [2], [1], [2], [3, 4]], "bipartite_graph remove_edge broken")

    def test_bipartite_graph_hopcroft_karp(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.hopcroftkarp()
        pair_u, pair_v = bpg.return_hk_matching()
        self.assertEqual(pair_u, [0, 1, 0, 2, 3], "bipartite_graph hopcroft_karp pair_u broken")
        self.assertEqual(pair_v, [0, 1, 3, 4, 0], "bipartite_graph hopcroft_karp pair_v broken")

    def test_bipartite_graph_perfect_matching(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        bpg.hopcroftkarp()
        self.assertEqual(bpg.check_perfect_matching(), False, "bipartite_graph check_perfect_matching broken")

    def test_bipartite_graph_get_connected_components(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        components = []
        cc = bpg.get_connected_components()
        for component in cc:
            components.append(component)
        self.assertEqual(components, [{1, 2, 3, 5, 6}, {8, 4, 7}], "bipartite_graph get_connected_components broken")

    def test_convert_hk_matching_to_edge_list_binary(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        converted_edges = dag.convert_hk_matching_to_edge_list_binary(bpg)
        self.assertEqual(converted_edges, [[2, 5], [4, 6], [7, 8]], "DAG convert_hk_matching_to_edge_list_binary edge list broken")

    def test_convert_hk_matching_to_edge_list_non_binary(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_omnian_bipartite_graph()
        converted_edges = dag.convert_hk_matching_to_edge_list_non_binary(bpg)
        self.assertEqual(converted_edges, [[2, 5], [5, 8], [6, 9]], "DAG convert_hk_matching_to_edge_list_non_binary edge list broken")

    def test_convert_bp_component_to_edge_list(self):
        preset1_vertices = []
        for i in range(1, 12):
            preset1_vertices.append(i)
        preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8],
                        [7, 9], [8, 10], [9, 11]]
        preset1_taxa = {10: "X1", 11: "X2"}
        dag = DAG(preset1_vertices, preset1_arcs, preset1_taxa, 1)
        bpg = dag.make_bipartite_graph()
        cc = bpg.get_connected_components()
        converted_list = []
        for component in cc:
            converted_list.append(dag.convert_bp_component_to_edge_list(bpg, component))
        self.assertEqual(converted_list, [[2, 3, 4, 5, 6], [9, 7, 8]], "DAG convert_bp_component_to_edge_list broken")



if __name__ == '__main__':
    unittest.main()
