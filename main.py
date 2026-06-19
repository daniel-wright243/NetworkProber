import io

import SubFunctions.PADRE
import networkx

from SubFunctions import SPRINTIntegration
from SubFunctions.MainGUI import ProgramGUI
from SubFunctions.MultiLabelledGraph import MultiLabelledGraph
from SubFunctions.NewGUI import TreeSpotterGUI
from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.FoldingAlgorithm import FoldingAlgorithm
from SubFunctions.PloidyAlgorithm import PolyPloidy
from SubFunctions.SimulationStudy import SimulationStudy
from SubFunctions.TreeSpotterFoldingFunction import FoldingFunction
from SubFunctions.NetworkIndexes import GetRandicIndex, GetWienerIndex
from SubFunctions.TreeSpotterFoldingFunction2 import FoldingFunction2
from SubFunctions.TreeSpotterAlgorithm import TreeSpotterAlgorithm
from SubFunctions.TreeSpotterFoldingFunction2 import FoldingFunction2
from SubFunctions.SoftlyTreeBasedFunction import SoftlyTreeBasedAlgorithm
from SubFunctions.GUIPyQt import GUIPyQt
import phylox
from phylox.newick_parser import extended_newick_to_dinetwork, dinetwork_to_extended_newick

if __name__ == '__main__':
    # vertices_list = []
    # for i in range(1, 19):
    #     vertices_list.append(i)
    # arc_list = [[1, 2], [1, 3], [2, 4], [2, 9], [3, 5], [3, 6], [4, 7], [4, 8], [5, 10], [6, 10], [6, 11], [7, 12],
    #             [7, 13], [8, 13], [8, 14], [9, 14], [9, 15], [10, 16], [11, 16], [11, 17], [13, 18], [14, 18], [16, 19],
    #             [18, 20], [5, 21]]
    # test_network = PhylogeneticNetwork(vertices_list, arc_list, 1)
    #
    # fa = FoldingAlgorithm(test_network)
    # fa.runAlgorithm()
    #
    # test_BipGraph = test_network.makeBiPartiteGraph()

    test_example_vertices = [0]
    for i in range(1, 60):
        if i != 39:
            test_example_vertices.append(i)
    test_example_arcs = [[0,1],[1,2],[1,43],[2,3],[2,42],[3,59],[3,4],[4,5],[4,41],[5,8],[5,6],[6,7],[6,12],[7,9],[7,11],[8,9],[8,61],[9,10],[10,41],[10,37],[11,34],[11,35],[12,29],[12,13],[13,14],[13,29],[14,15],[14,30],[15,27],[15,25],[15,24],[15,23],[15,22],[15,21],[15,20],[16,18],[16,17],[17,58],[18,19],[19,57],[19,17],[20,16],[21,18],[22,56],[23,55],[24,54],[25,26],[26,31],[26,53],[27,28],[28,33],[28,52],[29,30],[30,31],[31,50],[32,33],[33,51],[34,20],[34,21],[34,22],[34,23],[34,24],[34,25],[34,27],[34,31],[34,60],[35,36],[36,38],[37,36],[37,39],[38,47],[38,48],[39,45],[40,39],[41,40],[42,44],[59,42],[59,40],[60,49],[60,32],[61,35],[61,46]]
    test_example_network = PhylogeneticNetwork(test_example_vertices,test_example_arcs, 0)
    # test_example_network.displayGraphNetworkX()
    # test_example_network.displayGraph()
    # print(test_example_network.simplifyNetwork().checkTreeBasedOmnian())
    # test_example_network.displayGraph()
    # test_example_network_ff = FoldingFunction2(test_example_network)
    # graph1 = MultiLabelledGraph(test_example_network_ff.network)
    # graph1_below = test_example_network_ff.getNetworkBelowVertex(graph1, 14)
    # test_example_network_ff.displayNetworkXGraph(graph1_below)
    # graph2_below = test_example_network_ff.getNetworkBelowVertex(graph1 , 15)
    # print(test_example_network_ff.checkIfTwoGraphsAreIsomorphic(graph1_below, graph2_below))
    # print(test_example_network_ff.checkIfTwoNetworksShareSameLeafToRootLength(graph1_below, graph2_below, graph1))

    # test_example_network_ff.startAlgorithm()
    # test_example_multigraph = MultiLabelledGraph(test_example_network)
    # test_example_multigraph.displayGraph()
    #test_example_network.simplifyNetwork()

    #t1_pp = PolyPloidy(test_example_network)
    #temp = t1_pp.startAlgorithm()
    #temp.displayGraph()

    # t1_fa = FoldingAlgorithm(test_example_network)
    # t1_fa.runAlgorithm2()

    #test_example_network.makeBiPartiteGraph().displayGraph()

    test_example2_vertices = [0]
    for i in range(1, 74):
        if i != 33 and i != 37 and i != 38:
            test_example2_vertices.append(i)
    #test_example2_arcs = [[0, 1],[1, 2],[2, 3],[3, 4],[4, 5],[5, 6],[7, 8],[8, 9],[2, 10],[10, 11],[11, 12],[12, 13],[13, 14],[15, 16],[16, 17],[17, 18],[18, 19],[19, 20],[19, 21],[22, 23],[23, 24],[24, 25],[25, 26],[26, 27],[27, 28],[25, 17],[24, 29],[29, 30],[30, 31],[31, 26],[11, 32],[32, 33],[33, 22],[33, 34],[34, 35],[36, 37],[37, 38],[35, 39],[39, 40],[39, 41],[41, 43],[43, 44],[45, 46],[46, 47],[47, 48],[48, 49],[49, 50],[47, 51],[51, 52],[52, 53],[53, 54],[53, 48],[55, 56],[56, 51],[57, 58],[58, 59],[60, 61],[61, 62],[63, 64],[64, 65],[66, 67],[67, 68],[68, 69],[68, 36],[70, 71],[71, 72],[72, 73],[72, 41],[34, 15],[32, 74],[75, 76],[76, 77],[77, 78],[78, 36],[74, 79],[79, 80],[80, 81],[81, 45],[81, 55],[81, 66],[81, 70],[81, 57],[81, 60],[81, 63],[80, 77],[79, 75],[10, 29],[1, 7],[0, 82]]
    test_example2_arcs = [[0,1],[1,45],[1,9],[1,2],[2,49],[2,3],[3,8],[3,20],[4,5],[4,19],[5,52],[5,6],[6,53],[6,7],[7,11],[7,12],[8,50],[8,51],[9,10],[9,48],[10,47],[10,46],[11,54],[12,55],[13,11],[13,12],[13,14],[13,15],[13,17],[14,57],[15,58],[16,59],[17,16],[17,43],[17,44],[17,41],[18,14],[18,15],[18,28],[19,56],[19,21],[20,4],[20,24],[21,13],[21,22],[21,25],[22,18],[22,16],[22,23],[22,28],[22,29],[22,30],[22,31],[22,32],[22,39],[22,40],[22,41],[23,11],[23,12],[24,73],[24,34],[25,26],[25,32],[25,72],[26,27],[26,31],[27,28],[27,29],[27,30],[28,60],[29,61],[30,62],[31,63],[32,64],[34,74],[34,35],[35,36],[35,71],[36,43],[36,44],[36,39],[36,40],[36,41],[36,42],[39,67],[40,68],[41,69],[42,70],[43,65],[44,66],]
    test_example2_network = PhylogeneticNetwork(test_example2_vertices, test_example2_arcs, 0)
    # test_example2_network_ff = FoldingFunction2(test_example2_network)
    # print(test_example2_network.checkTreeBasedOmnian())
    # test_example2_network.displayGraph()
    # test_example2_network_ff.startAlgorithm()
    # test_example2_network.displayGraph()
    #test_example_multigraph = MultiLabelledGraph(test_example2_network)
    #test_example_multigraph.displayGraph()
    # test_example2_network.displayGraph()

    #omnian_bp = test_example2_network.makeOmnianBipartiteGraph()
    #omnian_bp.displayGraph()

    #print(test_example2_network.checkTreeBasedOmnian())

    # t2_pp = PolyPloidy(test_example2_network)
    # t2_pp.startAlgorithm().displayGraph()

    #test_example2_network.makeBiPartiteGraph().displayGraph()
    # print("CONNECTED COMPONENTS")
    # print(test_example2_network.getConnectedComponentOfGraphFromBPGraph())
    #
    # t2_fa = FoldingAlgorithm(test_example2_network)
    # t2_fa.runAlgorithm2()

    # t2_tsa = TreeSpotterAlgorithm(test_example2_network)
    # output = t2_tsa.startAlgorithm()
    # output.displayGraph()
    # output.makeBiPartiteGraph().displayGraph()

    #padre_test_arcs = [[0, 1],[1, 2],[2, 3],[3, 4],[4, 5],[5, 6],[7, 8],[8, 9],[2, 10],[10, 11],[11, 12],[12, 13],[13, 14],[15, 16],[16, 17],[17, 18],[18, 19],[19, 20],[19, 21],[22, 23],[23, 24],[24, 25],[25, 26],[26, 27],[27, 28],[25, 17],[24, 29],[29, 30],[30, 31],[31, 26],[11, 32],[32, 33],[33, 22],[33, 34],[34, 35],[36, 37],[37, 38],[35, 39],[39, 40],[39, 41],[41, 43],[43, 44],[45, 46],[46, 47],[47, 48],[48, 49],[49, 50],[47, 51],[51, 52],[52, 53],[53, 54],[53, 48],[55, 56],[56, 51],[57, 58],[58, 59],[60, 61],[61, 62],[63, 64],[64, 65],[66, 67],[67, 68],[68, 69],[68, 36],[70, 71],[71, 72],[72, 73],[72, 41],[34, 15],[32, 74],[75, 76],[76, 77],[77, 78],[78, 36],[74, 79],[79, 80],[80, 81],[81, 45],[81, 55],[81, 66],[81, 70],[81, 57],[81, 60],[81, 63],[80, 77],[79, 75],[10, 29],[1, 7],[0, 82]]
    #padre_test_arcs = [[1, 0],[2, 1],[3, 2],[4, 3],[5, 4],[6, 5],[0, 3],[8, 7],[9, 8],[10, 2],[11, 10],[12, 11],[13, 12],[14, 13],[0, 13],[16, 15],[17, 16],[18, 17],[19, 18],[20, 19],[21, 19],[0, 12],[23, 22],[24, 23],[25, 24],[26, 25],[27, 26],[28, 27],[17, 25],[29, 24],[30, 29],[31, 30],[26, 31],[32, 11],[33, 32],[22, 33],[34, 33],[35, 34],[0, 35],[37, 36],[38, 37],[39, 35],[40, 39],[41, 39],[0, 41],[43, 41],[44, 43],[0, 35],[46, 45],[47, 46],[48, 47],[49, 48],[50, 49],[51, 47],[52, 51],[53, 52],[54, 53],[48, 53],[0, 35],[56, 55],[51, 56],[0, 35],[58, 57],[59, 58],[0, 35],[61, 60],[62, 61],[0, 35],[64, 63],[65, 64],[0, 35],[67, 66],[68, 67],[69, 68],[36, 68],[0, 35],[71, 70],[72, 71],[73, 72],[41, 72],[15, 34],[74, 32],[0, 74],[76, 75],[77, 76],[78, 77],[36, 78],[79, 74],[80, 79],[81, 80],[45, 81],[55, 81],[66, 81],[70, 81],[57, 81],[60, 81],[63, 81],[77, 80],[75, 79],[29, 10],[7, 1],[82, 0]]
    #padre_test_vertices = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82]
    #padre_test_network = PhylogeneticNetwork(padre_test_vertices, padre_test_arcs, 0)
    #padre_test_network.displayGraph()

    #test_example2_network.makeBiPartiteGraph().displayGraph()

    #test_example2_network.makeBiPartiteGraph().displayGraph()

    #print(test_example2_network.checkTreeBased())
    #test_example2_network.displayGraph()

    # t2_fa = FoldingAlgorithm(test_example2_network)
    # t2_fa.runAlgorithm()

    test_example3_vertices = [0]
    for i in range(1, 90):
        test_example3_vertices.append(i)
    test_example3_arcs = [[0,1],[1,2],[1,10],[2,50],[2,3],[2,4],[3,51],[3,52],[4,5],[4,53],[5,54],[5,6],[6,55],[6,15],[7,15],[7,56],[8,7],[8,57],[9,8],[9,58],[10,9],[10,11],[10,12],[11,90],[11,62],[12,13],[12,21],[13,14],[13,61],[14,59],[14,60],[15,16],[16,17],[16,18],[17,63],[17,64],[18,19],[18,20],[19,23],[19,37],[20,21],[20,22],[21,24],[22,67],[22,68],[23,65],[23,66],[24,25],[24,27],[24,28],[25,26],[25,32],[26,82],[26,83],[27,29],[27,34],[28,30],[28,33],[29,80],[29,81],[30,43],[30,31],[31,44],[31,32],[32,47],[33,34],[33,36],[34,35],[35,76],[35,77],[36,37],[36,38],[37,49],[38,84],[38,39],[39,40],[39,41],[40,85],[40,86],[41,42],[41,89],[42,87],[42,88],[43,48],[44,45],[44,43],[45,71],[45,46],[46,72],[46,73],[47,74],[47,75],[48,69],[48,70],[49,78],[49,79]]
    test_example3_network = PhylogeneticNetwork(test_example3_vertices, test_example3_arcs, 0)
    # test_example3_network.displayGraph()
    # test_example3_tsa = TreeSpotterAlgorithm(test_example3_network)
    # # print(test_example3_network.checkTreeBasedOmnian())
    # test_example3_tsa.startAlgorithm().displayGraph()
    # print("INPUT LEAF COUNT")
    # print(len(test_example3_network.getAllLeafs()))
    # test_example3_mlg = MultiLabelledGraph(test_example3_network)
    # test_example3_mlg.simplifyNetwork().displayGraph()
    # test_example3_mlg.displayGraph()
    # test_example3_network.displayGraph()
    # #
    # # t3_pa = PolyPloidy(test_example3_network)
    # # t3_pa.startAlgorithm().displayGraph()
    #
    # t3_fa = FoldingAlgorithm(test_example3_network)
    # t3_fa.runAlgorithm2()

    working_padre_vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153]
    working_padre_arcs = [[0, 1], [0, 85], [0, 88], [1, 2], [1, 84], [2, 3], [2, 83], [3, 4], [3, 82], [4, 5], [5, 6], [5, 9], [6, 7], [6, 8], [9, 10], [9, 18], [10, 11], [10, 14], [11, 12], [11, 13], [14, 15], [15, 16], [15, 17], [18, 19], [18, 22], [19, 20], [19, 21], [22, 23], [23, 24], [23, 32], [23, 40], [24, 25], [24, 28], [25, 26], [25, 27], [28, 29], [29, 30], [29, 31], [32, 33], [32, 36], [33, 34], [33, 35], [36, 37], [37, 38], [37, 39], [40, 41], [40, 61], [41, 42], [41, 46], [42, 43], [43, 44], [43, 45], [46, 47], [46, 57], [47, 48], [47, 53], [48, 49], [48, 50], [50, 51], [50, 52], [53, 54], [54, 55], [54, 56], [57, 58], [58, 59], [58, 60], [61, 62], [61, 66], [62, 63], [63, 64], [63, 65], [66, 67], [66, 71], [67, 68], [68, 69], [68, 70], [71, 72], [71, 73], [73, 74], [73, 77], [74, 75], [74, 76], [77, 78], [77, 81], [78, 79], [78, 80], [85, 86], [85, 87], [88, 89], [88, 94], [89, 90], [89, 93], [90, 91], [90, 92], [94, 95], [95, 96], [95, 104], [95, 112], [96, 97], [96, 100], [97, 98], [97, 99], [100, 101], [101, 102], [101, 103], [104, 105], [104, 108], [105, 106], [105, 107], [108, 109], [109, 110], [109, 111], [112, 113], [112, 133], [113, 114], [113, 118], [114, 115], [115, 116], [115, 117], [118, 119], [118, 129], [119, 120], [119, 125], [120, 121], [120, 122], [122, 123], [122, 124], [125, 126], [126, 127], [126, 128], [129, 130], [130, 131], [130, 132], [133, 134], [133, 150], [134, 135], [134, 146], [135, 136], [135, 137], [137, 138], [137, 141], [138, 139], [138, 140], [141, 142], [141, 145], [142, 143], [142, 144], [146, 147], [147, 148], [147, 149], [150, 151], [151, 152], [151, 153]]
    working_padre_network = PhylogeneticNetwork(working_padre_vertices, working_padre_arcs, 0)
    #working_padre_network.displayGraph()

    # test_1_vertices = [1,2,3,4,5,6,7,8,9,10,11]
    # test_1_arcs = [[1,2],[2,3],[2,4],[4,5],[4,6],[7,8],[7,11],[8,9],[8,10]]
    # test_1_network = PhylogeneticNetwork(test_1_vertices, test_1_arcs, 1)
    # test_1_fa = FoldingAlgorithm(test_1_network)
    # test_1_fa.runAlgorithm2()
    # t3_fa = FoldingAlgorithm(test_example3_network)
    # t3_fa.runAlgorithm()

    #test_example3_network.displayGraph()

    #t3_bp = test_example3_network.makeBiPartiteGraph()
    # t3_bp.hopcroftKarp()
    #t3_bp.displayGraph()
    # print(test_example3_network.checkTreeBased())

    #print(test_BipGraph.getConnectedComponents())
    # for component in test_BipGraph.getConnectedComponents():
    #     print(component)
    # print(test_BipGraph.edges)
    # print(test_BipGraph.U)
    # print(test_BipGraph.V)
    # #test_BipGraph.displayGraph()
    # test_BipGraph.hopcroftKarp()
    # print(test_BipGraph.returnHKMatching())
    # #test_BipGraph.displayMatchingGraph()
    # #test_network.displayGraph()
    #
    # vertices_list2 = []
    # for i in range(1, 12):
    #     vertices_list2.append(i)
    # arc_list2 = [[1, 2], [1, 5], [2, 3], [2, 4], [3, 6], [3, 7], [4, 7], [4, 8], [5, 8], [5, 9], [7, 10], [8, 10], [10, 11]]
    # test_network2 = PhylogeneticNetwork(vertices_list2, arc_list2, 1)
    # #test_network2.displayGraph()
    # test_BipGraph2 = test_network2.makeBiPartiteGraph()
    # #test_BipGraph2.displayGraph()
    # test_BipGraph2.hopcroftKarp()
    # test_BipGraph2.displayMatchingGraph()


    # kathi_test_vertices = []
    # for i in range(1,13):
    #     if i != 11:
    #         kathi_test_vertices.append(i)
    # kathi_test_arcs = [[1,2],[1,3],[2,5],[2,8],[3,4],[4,5],[4,6],[5,7],[6,12],[6,13],[7,9],[7,10]]
    # kathi_test_network = PhylogeneticNetwork(kathi_test_vertices, kathi_test_arcs, 1)
    # #kathi_test_network.displayGraph()
    # #kathi_test_mlg = MultiLabelledGraph(kathi_test_network)
    # #kathi_test_mlg.displayGraph()
    # kathi_test_fa = FoldingAlgorithm(kathi_test_network)
    # kathi_test_fa.runAlgorithm2()

    kathi_test_2_vertices = []
    for i in range(1, 13):
        kathi_test_2_vertices.append(i)
    kathi_test_2_arcs = [[1,2],[1,10],[2,5],[2,4],[3,4],[3,12],[4,8],[8,6],[8,9],[10,3],[10,4],[12,11],[12,7],[12,13]]
    kathi_test_2_network = PhylogeneticNetwork(kathi_test_2_vertices, kathi_test_2_arcs, 1)
    # kathi_test_2_network.displayGraph()
    # kathi_test_2_fa = FoldingAlgorithm(kathi_test_2_network)
    # kathi_test_2_fa.runAlgorithm2()

    kathi_test_3_vertices = [0]
    for i in range(1, 17):
        kathi_test_3_vertices.append(i)
    kathi_test3_arcs = [[0,1],[1,2],[1,12],[2,3],[2,4],[3,5],[3,6],[4,7],[4,8],[5,13],[5,9],[6,9],[6,14],[7,15],[7,10],[8,10],[8,16],[9,11],[10,11],[11,17]]
    kathi_test_3_network = PhylogeneticNetwork(kathi_test_3_vertices, kathi_test3_arcs, 0)
    # kathi_test_3_network.displayGraph()
    # kathi_test3_fa = FoldingAlgorithm(kathi_test_3_network)
    # kathi_test3_fa.runAlgorithm2()

    kathi_test_4_vertices = [0]
    for i in range(1,13):
        kathi_test_4_vertices.append(i)
    kathi_test4_arcs = [[0,1],[1,2],[1,3],[2,9],[2,4],[3,4],[3,10],[4,5],[5,6],[5,7],[6,11],[6,8],[7,8],[7,13],[8,12]]
    kathi_test_4_network = PhylogeneticNetwork(kathi_test_4_vertices, kathi_test4_arcs, 0)
    #kathi_test_4_network.displayGraph()
    # kathi_test4_fa = FoldingAlgorithm(kathi_test_4_network)
    # kathi_test4_fa.runAlgorithm2()

    kathi_test_5_vertices = [0]
    for i in range(18, 89):
        if i < 49 or i > 65:
            kathi_test_5_vertices.append(i)
    kathi_test5_arcs = [[0,18],[18,19],[18,20],[19,23],[19,37],[20,21],[20,22],[21,24],[22,67],[22,68],[23,65],[23,66],[24,25],[24,27],[24,28],[25,26],[25,32],[26,82],[26,83],[27,29],[27,34],[28,30],[28,33],[29,80],[29,81],[30,43],[30,31],[31,44],[31,32],[32,47],[33,34],[33,36],[34,35],[35,76],[35,77],[36,37],[36,38],[37,49],[38,84],[38,39],[39,40],[39,41],[40,85],[40,86],[41,42],[41,89],[42,87],[42,88],[43,48],[44,45],[44,43],[45,71],[45,46],[46,72],[46,73],[47,74],[47,75],[48,69],[48,70],[49,78],[49,79]]
    kathi_test_5_network = PhylogeneticNetwork(kathi_test_5_vertices, kathi_test5_arcs, 0)
    # kathi_test_5_network.displayGraph()
    #kathi_test_5_network.displayGraph()
    # kathi_test5_fa = FoldingAlgorithm(kathi_test_5_network)
    # kathi_test5_fa.runAlgorithm2()

    kathi_test_6_vertices = [0]
    for i in range(1,30):
        kathi_test_6_vertices.append(i)
    kathi_test6_arcs = [[0,1],[1,2],[1,3],[2,4],[2,5],[2,6],[3,7],[3,8],[3,9],[4,10],[4,11],[5,12],[5,13],[7,14],[7,15],[8,16],[8,17],[9,18],[12,19],[12,20],[14,21],[14,22],[18,23],[18,24],[20,25],[20,26],[22,26],[22,27],[24,28],[24,29],[26,30]]
    kathi_test_6_network = PhylogeneticNetwork(kathi_test_6_vertices, kathi_test6_arcs, 0)
    #kathi_test_6_network.displayGraph()
    # kathi_test6_fa = FoldingAlgorithm(kathi_test_6_network)
    # kathi_test6_fa.runAlgorithm2()

    kathi_test_7_vertices = [0]
    for i in range(1, 31):
        if i != 4 and i != 20:
            kathi_test_7_vertices.append(i)
    kathi_test7_arcs = [[0,1],[1,2],[1,6],[2,5],[2,3],[2,31],[3,22],[3,8],[5,6],[5,21],[6,7],[7,8],[7,9],[8,10],[9,23],[9,19],[10,11],[10,12],[10,13],[11,24],[11,30],[12,14],[12,15],[13,17],[13,28],[14,30],[14,19],[15,16],[15,18],[16,18],[16,17],[17,27],[18,26],[19,29],[30,25]]
    kathi_test_7_network = PhylogeneticNetwork(kathi_test_7_vertices, kathi_test7_arcs, 0)
    # kathi_test_7_network.displayGraph()
    # kathi_test7_fa = FoldingAlgorithm(kathi_test_7_network)
    # kathi_test7_fa.runAlgorithm2()

    kathi_test_8_vertices = [0]
    for i in range(1, 13):
        kathi_test_8_vertices.append(i)
    kathi_test8_arcs = [[0,1],[1,2],[1,3],[2,4],[2,5],[3,8],[3,11],[4,9],[4,6],[5,6],[5,10],[6,7],[7,12],[7,8],[8,13]]
    kathi_test_8_network = PhylogeneticNetwork(kathi_test_8_vertices, kathi_test8_arcs, 0)
    # kathi_test_8_network.displayGraph()
    # kathi_test_8_fa = FoldingAlgorithm(kathi_test_8_network)
    # kathi_test_8_fa.runAlgorithm2()

    kathi_test_9_vertices = [0]
    for i in range(1, 9):
        kathi_test_9_vertices.append(i)
    kathi_test9_arcs = [[0,1],[1,2],[1,8],[2,5],[2,3],[3,4],[4,6],[4,7],[8,9],[8,3]]
    kathi_test_9_network = PhylogeneticNetwork(kathi_test_9_vertices, kathi_test9_arcs, 0)
    # kathi_test_9_network.displayGraph()
    # kathi_test_9_fa = FoldingAlgorithm(kathi_test_9_network)
    # kathi_test_9_fa.runAlgorithm2()

    # kathi_test_10_vertices = [0,1,2,3,4,5,6,7,8,9,10]
    # kathi_test_10_arcs = [[0, 1],[1, 2],[2, 3],[2, 4],[4, 5],[5, 6],[6, 7],[6, 8],[1, 9],[9, 10],[9, 4]]
    # kathi_test_10_network = PhylogeneticNetwork(kathi_test_10_vertices, kathi_test_10_arcs, 0)
    # kathi_test_10_network.displayGraph()

    kathi_test_11_vertices = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132]
    kathi_test_11_arcs = [[0, 1],[1, 2],[2, 3],[2, 4],[4, 5],[4, 6],[2, 7],[7, 8],[7, 9],[9, 10],[9, 11],[11, 12],[11, 13],[13, 14],[14, 15],[15, 16],[16, 17],[16, 18],[14, 19],[19, 20],[20, 21],[21, 22],[22, 23],[22, 24],[20, 25],[25, 26],[26, 27],[27, 28],[27, 29],[29, 30],[19, 31],[31, 32],[32, 33],[33, 34],[33, 35],[31, 36],[36, 37],[37, 38],[38, 39],[39, 40],[40, 41],[41, 42],[42, 43],[43, 44],[42, 29],[40, 45],[45, 46],[46, 47],[46, 48],[48, 49],[49, 50],[49, 51],[48, 52],[52, 53],[53, 54],[53, 55],[52, 56],[39, 57],[57, 58],[58, 59],[59, 60],[59, 61],[61, 62],[38, 63],[63, 64],[64, 65],[65, 66],[66, 67],[67, 68],[68, 69],[69, 70],[69, 71],[66, 72],[72, 73],[72, 74],[74, 75],[74, 76],[65, 77],[77, 78],[78, 79],[79, 80],[79, 43],[64, 67],[37, 81],[81, 82],[82, 57],[82, 83],[83, 84],[84, 85],[84, 86],[37, 87],[87, 88],[88, 89],[89, 90],[89, 91],[88, 77],[1, 92],[92, 93],[93, 94],[94, 95],[95, 96],[95, 97],[97, 98],[98, 99],[99, 100],[100, 101],[101, 102],[102, 103],[103, 104],[102, 29],[100, 21],[99, 105],[105, 106],[106, 107],[107, 108],[108, 109],[109, 110],[110, 111],[111, 45],[111, 25],[109, 57],[108, 63],[107, 87],[107, 81],[105, 32],[98, 15],[94, 112],[93, 113],[92, 114],[114, 115],[115, 116],[116, 117],[116, 118],[115, 119],[114, 120],[120, 121],[121, 122],[122, 63],[122, 123],[123, 124],[124, 125],[125, 61],[125, 103],[123, 110],[121, 87],[121, 126],[126, 127],[127, 128],[128, 129],[128, 61],[126, 83],[92, 130],[130, 131],[130, 132]]
    kathi_test_11_network = PhylogeneticNetwork(kathi_test_11_vertices, kathi_test_11_arcs, 0)
    # kathi_test_11_network.displayGraph()
    # print("OUTPUT LEAF COUNT")
    # print(len(kathi_test_11_network.getAllLeafs()))

    kathi_test_12_vertices = []
    for i in range(1, 11):
        kathi_test_12_vertices.append(i)
    kathi_test12_arcs = [[1,11],[1,8],[2,4],[2,5],[3,4],[3,5],[4,6],[5,7],[8,3],[8,9],[11,2],[11,10]]
    kathi_test_12_network = PhylogeneticNetwork(kathi_test_12_vertices, kathi_test12_arcs, 1)
    # kathi_test_12_network.displayGraph()
    # kathi_test_12_fa = FoldingAlgorithm(kathi_test_12_network)
    # kathi_test_12_fa.runAlgorithm2()

    kathi_test_13_vertices = []
    for i in range(1, 9):
        kathi_test_13_vertices.append(i)
    kathi_test_13_arcs = [[1,2],[1,3],[2,4],[2,7],[3,7],[3,6],[7,8],[8,9],[8,5]]
    kathi_test_13_network = PhylogeneticNetwork(kathi_test_13_vertices, kathi_test_13_arcs, 1)
    # kathi_test_13_network.displayGraph()
    # kathi_test_13_fa = FoldingAlgorithm(kathi_test_13_network)
    # kathi_test_13_fa.runAlgorithm2()

    kathi_test_14_vertices = [1]
    for i in range(1, 15):
        kathi_test_14_vertices.append(i)
    kathi_test_14_arcs = [[1,2],[2,3],[2,4],[3,5],[3,6],[4,7],[4,8],[5,11],[5,9],[6,9],[7,6],[7,10],[8,10],[8,13],[9,14],[10,14],[14,12]]
    kathi_test_14_network = PhylogeneticNetwork(kathi_test_14_vertices, kathi_test_14_arcs, 1)
    # kathi_test_14_network.displayGraphHighlightEdges([[3,6],[7,6],[6,9],[8,10],[5,9],[9,14]], [6, 9])

    kathi_test_15_vertices = [0]
    for i in range(1,10):
        kathi_test_15_vertices.append(i)
    kathi_test_15_arcs = [[0,1],[1,2],[1,3],[2,6],[2,4],[3,4],[3,9],[4,5],[5,7],[5,8]]
    kathi_test_15_network = PhylogeneticNetwork(kathi_test_15_vertices, kathi_test_15_arcs, 0)
    # kathi_test_15_network.displayGraphHighlightEdges([[3, 4]], [])
    # print(kathi_test_15_network.compareTwoSubGraphs([2,3,4],[[2,3],[2,4]],[5,6,4], [[5,6],[5,4]]))
    # kathi_test_15_mlg = MultiLabelledGraph(kathi_test_15_network)
    # kathi_test_15_pa = SubFunctions.PADRE.runAlgorithm(kathi_test_15_mlg)

    kathi_test_16_vertices = [0]
    for i in range(1, 16):
        kathi_test_16_vertices.append(i)
    kathi_test_16_arcs = [[0,1],[1,2],[1,3],[2,4],[2,5],[3,4],[3,6],[4,14],[5,7],[5,8],[6,8],[6,9],[8,10],[10,11],[10,12],[12,13],[12,14],[14,15]]
    kathi_test_16_network = PhylogeneticNetwork(kathi_test_16_vertices, kathi_test_16_arcs, 1)
    # kathi_test_16_network.applyMatchingToGraph(kathi_test_16_network.makeBiPartiteGraph())
    # kathi_test_16_network.displayGraph()
    # print(kathi_test_16_network.checkTreeBasedBinary())
    # kathi_test_16_network.displayGraphHighlightEdges([[3,4],[5,8],[12,14]],[])

    kathi_test_17_vertices = [0]
    for i in range(1, 8):
        kathi_test_17_vertices.append(i)
    kathi_test_17_arcs = [[0,1],[1,2],[1,3],[2,4],[2,5],[3,4],[3,5],[4,6],[5,7]]
    kathi_test_17_network = PhylogeneticNetwork(kathi_test_17_vertices, kathi_test_17_arcs, 0)
    # kathi_test_17_ff = FoldingFunction2(kathi_test_17_network)
    # kathi_test_17_ff.startAlgorithm()
    # kathi_test_17_network.displayGraph()
    # TSFF = FoldingFunction(kathi_test_17_network)
    # TSFF.runAlgorithm()
    # print(GetRandicIndex(kathi_test_17_network))
    # print(GetWienerIndex(kathi_test_17_network))

    kathi_test_18_vertices = [0]
    for i in range(1, 7):
        kathi_test_18_vertices.append(i)
    kathi_test_18_arcs = [[0,1],[1,2],[1,3],[2,4],[2,5],[3,4],[3,5],[4,6],[5,6]]
    kathi_test_18_network = PhylogeneticNetwork(kathi_test_18_vertices, kathi_test_18_arcs, 0)
    # kathi_test_18_ff = FoldingFunction2(kathi_test_18_network)
    #kathi_test_18_ff.startAlgorithm()
    # kathi_test_18_network.displayGraph()
    # print(kathi_test_18_network.checkTreeBasedBinary())
    # kathi_test_18_network.makeBiPartiteGraph().displayGraph()
    # # print(GetRandicIndex(kathi_test_18_network))
    # print(GetWienerIndex(kathi_test_18_network))

    kathi_test_19_vertices = [0]
    for i in range(1, 10):
        kathi_test_19_vertices.append(i)
    kathi_test_19_arcs = [[0,1],[1,2],[1,3],[2,4],[2,5],[3,6],[3,7],[4,6],[4,7],[5,6],[5,7],[6,8],[7,9]]
    kathi_test_19_network = PhylogeneticNetwork(kathi_test_19_vertices, kathi_test_19_arcs, 0)
    # kathi_test_19_network.displayGraph()
    # kathi_test_19_network_tsa = TreeSpotterAlgorithm(kathi_test_19_network)
    # kathi_test_19_network_tsa.startAlgorithm().displayGraph()
    # kathi_test_19_ff = FoldingFunction2(kathi_test_19_network)
    # kathi_test_19_ff.startAlgorithm()

    kathi_test_20_vertices = [0]
    for i in range(1, 10):
        kathi_test_20_vertices.append(i)
    kathi_test_20_arcs = [[0,1],[1,2],[1,3],[2,4],[2,5],[3,6],[3,7],[4,6],[4,7],[5,6],[5,7],[6,8],[7,8],[8,9]]
    kathi_test_20_network = PhylogeneticNetwork(kathi_test_20_vertices, kathi_test_20_arcs, 0)
    # kathi_test_20_network.displayGraph()
    # print(kathi_test_20_network.checkTreeBasedNonBinary())
    # kathi_test_20_mlg = MultiLabelledGraph(kathi_test_20_network)
    # kathi_test_20_mlg.displayGraph()
    # print(kathi_test_20_mlg.getVerticesBelowVertex(2, 2))
    # MultiLabelledGraph(kathi_test_20_network).displayGraph()
    # kathi_test_20_ff = FoldingFunction2(kathi_test_20_network)
    # kathi_test_20_ff.startAlgorithm()
    # kathi_test_20_tsa = TreeSpotterAlgorithm(kathi_test_20_network)
    # kathi_test_20_tsa.startAlgorithm().displayGraph()

    kathi_test_21_vertices = []
    for i in range(0, 12):
        kathi_test_21_vertices.append(i)
    kathi_test_21_arcs = [[0,1],[1,2],[1,3],[2,5],[2,6],[3,4],[3,5],[4,6],[4,7],[5,8],[6,9],[7,8],[7,9],[8,10],[9,11]]
    kathi_test_21_network = PhylogeneticNetwork(kathi_test_21_vertices, kathi_test_21_arcs, 0)
    # stba = SoftlyTreeBasedAlgorithm(kathi_test_21_network)
    # stba.startAlgorithm()
    # kathi_test_21_network.displayGraph()
    # kathi_test_21_network.makeBiPartiteGraph().displayMatchingGraph()
    # print(kathi_test_21_network.checkTreeBasedBinary())
    # kathi_test_21_network.makeBiPartiteGraph().displayGraph()
    # print(kathi_test_21_network.checkIfNetworkIsTreeBasedBaseTree())
    # kathi_test_21_network.displayGraph()
    # kathi_test_21_tsa = TreeSpotterAlgorithm(kathi_test_21_network)
    # output = kathi_test_21_tsa.startAlgorithm(False)
    # output.displayGraph()
    # # output.displayGraph()
    # output_bpg = output.makeBiPartiteGraph()
    # output_bpg.displayGraph()
    # output_bpg.hopcroftKarp()
    # output_bpg.displayMatchingGraph()

    # vertex_list1 = [2,10,11]
    # edge_list1 = [[2,10],[2,11]]
    #
    # networkXGraph1 = networkx.DiGraph()
    # for vertex in vertex_list1:
    #     networkXGraph1.add_node(vertex)
    # for arc in edge_list1:
    #     networkXGraph1.add_edge(arc[0], arc[1])
    #
    # vertex_list2 = [7, 14, 22]
    # edge_list2 = [[7, 14], [7, 22]]
    #
    # networkXGraph2 = networkx.DiGraph()
    # for vertex in vertex_list2:
    #     networkXGraph2.add_node(vertex)
    # for arc in edge_list2:
    #     networkXGraph2.add_edge(arc[0], arc[1])
    #
    # temp_tsa = FoldingFunction2(kathi_test_21_network)
    # print(temp_tsa.checkIfTwoGraphsAreIsomorphic(networkXGraph1, networkXGraph2))
    #
    # temp_mlg = MultiLabelledGraph(kathi_test_21_network)
    # temp_mlg = temp_mlg.simplifyNetwork()
    #
    # print(temp_tsa.checkIfTwoNetworksShareSameLeafToRootLength(networkXGraph1, networkXGraph2, temp_mlg))

    # forbidden_configuration1_vertices = []
    # for i in range(1, 9):
    #     forbidden_configuration1_vertices.append(i)
    # forbidden_configuration1_arcs = [[1,5],[2,5],[3,6],[4,6],[5,7],[6,7],[7,8]]
    # forbidden_configuration1_taxDict = {8: "x" + "\u2081"}
    # forbidden_configuration1_network = PhylogeneticNetwork(forbidden_configuration1_vertices, forbidden_configuration1_arcs, 1, forbidden_configuration1_taxDict)
    # # forbidden_configuration1_network.createGraphImage()
    #
    # forbidden_configuration2_vertices = []
    # for i in range(1, 13):
    #     forbidden_configuration2_vertices.append(i)
    # forbidden_configuration2_arcs = [[1,3],[2,3],[3,4],[4,5],[6,4],[6,8],[7,6],[8,9],[10,8],[10,12],[11,10]]
    # forbidden_configuration2_taxDict = {5: "x" + "\u2081", 9: "x" + "\u2082", 12: "x" + "\u2083"}
    # forbidden_configuration2_network = PhylogeneticNetwork(forbidden_configuration2_vertices, forbidden_configuration2_arcs, 1, forbidden_configuration2_taxDict)
    # forbidden_configuration2_network.createGraphImage()
    #
    # weakly_displayed_graph_vertices = []
    # for i in range(1, 14):
    #     weakly_displayed_graph_vertices.append(i)15
    # weakly_displayed_graph_arcs = [[1, 2], [1, 3], [2, 4], [2, 5], [3, 5], [3, 6], [5, 7], [7, 8], [7, 9], [8, 10], [8, 11], [9, 12], [9, 13]]
    # weakly_displayed_taxDict = {10: "x" + "\u2081", 11: "x" + "\u2082", 12: "x" + "\u2083", 13: "x" + "\u2084", 6: "x" + "\u2085", 4: "x" + "\u2086"}
    # weakly_displayed_network = PhylogeneticNetwork(weakly_displayed_graph_vertices, weakly_displayed_graph_arcs, 1, weakly_displayed_taxDict)
    # weakly_displayed_network.createGraphImage()

    # breadwheat_example_vertices = []
    # for i in range(1, 16):
    #     breadwheat_example_vertices.append(i)
    # breadwheat_example_arcs = [[1, 2], [1, 3], [2, 5], [2, 4], [3, 4], [3, 6], [4, 14], [5, 7], [5, 8], [6, 8], [6, 9], [8, 10], [10, 11], [10, 12], [12, 13], [12, 14], [14, 15]]
    # breadwheat_example_taxDict = {7: "x" + "\u2081", 9: "x" + "\u2082", 11: "x" + "\u2083", 13: "x" + "\u2084", 15: "x" + "\u2085"}
    # breadwheat_example_network = PhylogeneticNetwork(breadwheat_example_vertices, breadwheat_example_arcs, 1, breadwheat_example_taxDict)
    # breadwheat_example_network.displayBaseTree()
    # breadwheat_example_network.createGraphImage()

    # weakly_displayed_graph_vertices2 = []
    # for i in range(1, 12):
    #     weakly_displayed_graph_vertices2.append(i)
    # weakly_displayed_graph_arcs2 = [[1, 2], [1, 4], [2, 3], [2, 8], [3, 6], [3, 7], [4, 9], [4, 5], [5, 10], [5, 11]]
    # weakly_displayed_taxDict2 = {6: "x" + "\u2081", 7: "x" + "\u2082", 10: "x" + "\u2083", 11: "x" + "\u2084", 9: "x" + "\u2085", 8: "x" + "\u2086"}
    # weakly_displayed_network = PhylogeneticNetwork(weakly_displayed_graph_vertices2, weakly_displayed_graph_arcs2, 1, weakly_displayed_taxDict2)
    # weakly_displayed_network.createGraphImage()

    # omnian_example_vertices = []
    # for i in range(0, 7):
    #     omnian_example_vertices.append(i)
    # omnian_example_arcs = [[0, 2], [1, 2], [2, 3], [3, 6], [4, 3], [5, 3]]
    # omnian_example_taxDict = {6: "x" + "\u2081"}
    # omnian_example_network = PhylogeneticNetwork(omnian_example_vertices, omnian_example_arcs, 0, omnian_example_taxDict)
    # omnian_example_network.createGraphImage()

    # omnian_example_vertices2 = []
    # for i in range(0, 16):
    #     omnian_example_vertices2.append(i)
    # omnian_example_arcs2 = [[0, 1], [1, 5], [1, 9], [1, 14], [2, 5], [3, 5], [4, 5], [5, 6], [7, 9], [8, 9], [9, 10], [11, 14], [12, 14], [13, 14], [14, 15]]
    # omnian_example_taxDict2 = {6: "x" + "\u2081", 10: "x" + "\u2082", 15: "x" + "\u2096"}
    # omnian_example_network2 = PhylogeneticNetwork(omnian_example_vertices2, omnian_example_arcs2, 0, omnian_example_taxDict2)
    # omnian_example_network2.createGraphImage()

    # fc_example_vertices = []
    # for i in range(0, 8):
    #     fc_example_vertices.append(i)
    # fc_example_arcs = [[0, 4], [1, 4], [2, 5], [3, 5], [4, 6], [5, 6], [6, 7]]
    # fc_example_taxDict = {7: "x" + "\u2081"}
    # fc_example_network = PhylogeneticNetwork(fc_example_vertices, fc_example_arcs, 0, fc_example_taxDict)
    # # fc_example_network.displayGraph()
    # fc_example_network.displayGraphFigure([0, 1, 2, 3], [7])
    # fc_example_network.createGraphImage()

    # fc_example_vertices2 = []
    # for i in range(0, 15):
    #     fc_example_vertices2.append(i)
    # fc_example_arcs2 = [[0, 2], [1, 2], [2, 5], [3, 5], [4, 5], [5, 6], [7, 5], [7, 11], [8, 7], [9, 11], [10, 11], [11, 12], [13, 11], [14, 13]]
    # fc_example_taxDict2 = {6: "x" + "\u2081", 12: "x" + "\u2082"}
    # fc_example_network2 = PhylogeneticNetwork(fc_example_vertices2, fc_example_arcs2, 0, fc_example_taxDict2)
    # # fc_example_network2.displayGraph()
    # fc_example_network2.displayGraphFigure([3, 4, 0, 1, 8, 10, 14, 9], [6, 12])
    # fc_example_network2.createGraphImage()

    # fc_example_vertices3 = []
    # for i in range(0, 9):
    #     fc_example_vertices3.append(i)
    # fc_example_arcs3 = [[0, 2], [1, 2], [2, 3], [3, 4], [5, 3], [5, 7], [6, 5], [7, 8]]
    # fc_example_taxDict3 = {8: "x" + "\u2083", 4: "x" + "\u2084"}
    # fc_example_network3 = PhylogeneticNetwork(fc_example_vertices3, fc_example_arcs3, 0, fc_example_taxDict3)
    # # fc_example_network3.displayGraph()
    # fc_example_network3.displayGraphFigure([0, 1, 6], [4, 8])
    # fc_example_network3.createGraphImage()

    # polyploidy_vertices = []
    # for i in range(1, 8):
    #     polyploidy_vertices.append(i)
    # polyploidy_arcs = [[1, 2], [1, 3], [2, 3], [2, 4], [3, 4], [4, 5], [5, 6], [5, 7]]
    # polyploidy_taxDict = {6: "x" + "\u2081", 7: "x" + "\u2082"}
    # polyploidy_network = PhylogeneticNetwork(polyploidy_vertices, polyploidy_arcs, 1, polyploidy_taxDict)
    # polyploidy_network.createGraphImage()

    # pp = PolyPloidy(polyploidy_network)
    # pp.

    # broken_vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
    # broken_arcs = [[0, 21], [1, 23], [1, 27], [3, 24], [3, 30], [4, 5], [4, 6], [6, 20], [6, 37], [8, 9], [8, 10], [10, 11], [10, 26], [11, 15], [11, 22], [12, 28], [12, 36], [15, 16], [15, 29], [20, 25], [21, 1], [21, 20], [22, 12], [23, 3], [23, 22], [24, 4], [24, 25], [25, 8], [26, 18], [26, 31], [27, 2], [27, 31], [28, 14], [28, 32], [29, 17], [29, 33], [30, 19], [30, 33], [31, 34], [32, 34], [32, 35], [33, 35], [34, 36], [35, 37], [36, 13], [37, 7]]
    # broken_network = PhylogeneticNetwork(broken_vertices, broken_arcs, 0)
    # broken_network.displayGraph()
    # print(len(broken_network.getAllLeafs()))
    # output_graph = TreeSpotterAlgorithm(broken_network).startAlgorithm(False)
    # print(len(output_graph.getAllLeafs()))
    # output_graph.displayGraph()

    # broken_vertices2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
    # broken_arcs2 = [[0, 21], [1, 2], [1, 30], [3, 4], [3, 19], [4, 5], [4, 6], [6, 7], [6, 8], [8, 9], [8, 29], [9, 10], [9, 36], [12, 13], [12, 22], [14, 16], [14, 27], [16, 17], [16, 37], [20, 23], [21, 20], [21, 28], [22, 24], [23, 25], [23, 26], [24, 14], [25, 12], [25, 24], [26, 22], [26, 31], [27, 15], [27, 31], [28, 1], [28, 32], [29, 20], [29, 33], [30, 3], [30, 33], [31, 34], [32, 34], [32, 35], [33, 35], [34, 36], [35, 37], [36, 11], [37, 18]]
    # broken_network2 = PhylogeneticNetwork(broken_vertices2, broken_arcs2, 0)
    # # broken_network2.displayGraph()
    # output_graph2 = TreeSpotterAlgorithm(broken_network2).startAlgorithm(False)
    # # output_graph2.displayGraph()

    # print(len(broken_network2.getAllLeafs()))
    # print(len(output_graph2.getAllLeafs()))
    #
    # PloidyProfile = [2, 2]
    # PloidyIndex = [10, 11]
    # NPrimeLeafs = [10, 11]
    #
    # G, labels = SPRINTIntegration.runSPRINTImplementation(PloidyProfile, PloidyIndex, 'binary', len(NPrimeLeafs))
    # ploidyNetwork = networkx.to_dict_of_lists(G)
    # print(ploidyNetwork)
    # vertex_list = []
    # edge_list = []
    # for vertex in ploidyNetwork:
    #     vertex_list.append(vertex)
    #     for item in ploidyNetwork[vertex]:
    #         edge_list.append([vertex, item])
    # root = min(vertex_list)
    # PloidyNetwork = PhylogeneticNetwork(vertex_list, edge_list, root)
    # # PloidyNetwork.displayGraph()

    subscript_dict = {'0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084', '5': '\u2085',
                           '6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089'}
    #
    # preset1_vertices = []
    # for i in range(1, 12):
    #     preset1_vertices.append(i)
    # preset1_taxDict = {10: "x" + subscript_dict.get('2'), 11: "x" + subscript_dict.get('1')}
    # preset1_arcs = [[1, 2], [1, 3], [2, 5], [2, 6], [3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8], [7, 9], [8, 10], [9, 11]]
    # temp_phylo_network = PhylogeneticNetwork(preset1_vertices, preset1_arcs, 1, preset1_taxDict)
    # temp_phylo_network.displayGraphHighlightEdges([[6, 9], [7, 9], [7, 8], [5, 8]], [5,6,7,8,9])
    # # temp_phylo_network.displayGraphHighlightEdges([[3, 4], [3, 5], [4, 6], [4, 7], [5, 8], [6, 9], [7, 8], [7, 9], [8, 10], [9, 11]], [3,4,5,6,7,8,9,10,11])
    #
    # breadwheat_example_vertices = []
    # for i in range(1, 16):
    #     breadwheat_example_vertices.append(i)
    # breadwheat_example_arcs = [[1, 2], [1, 3], [2, 5], [2, 4], [3, 4], [3, 6], [4, 14], [5, 7], [5, 8], [6, 8], [6, 9], [8, 10], [10, 11], [10, 12], [12, 13], [12, 14], [14, 15]]
    # breadwheat_example_taxDict = {7: "x" + "\u2081", 9: "x" + "\u2082", 11: "x" + "\u2083", 13: "x" + "\u2084", 15: "x" + "\u2085"}
    # breadwheat_example_network = PhylogeneticNetwork(breadwheat_example_vertices, breadwheat_example_arcs, 1, breadwheat_example_taxDict)
    # breadwheat_example_network.displayGraph()
    # breadwheat_example_network.displayGraphHighlightEdges([[1, 2], [2, 5], [5, 7], [1, 3], [3, 6], [6, 9], [6, 8], [8, 10], [10, 11], [10, 12], [12, 13], [2, 4], [4, 14], [14, 15]], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])



    # network = extended_newick_to_dinetwork("(A,B,((C,(Y)x#H1)c,(x#H1,D)d)e)f;")
    #
    # print("G VERTICES")
    # print(network.nodes)
    #
    # for node in network.nodes:
    #     print(node)
    #
    # print("G ARCS")
    # print(network.edges)
    #
    # for arc in network.edges:
    #     print(arc)
    #
    # test_string = dinetwork_to_extended_newick(network)
    # print(test_string)

    tsGUI = TreeSpotterGUI(100, 100)
    tsGUI.mainGUI()

    # mainGUI = ProgramGUI(100, 100)
    # mainGUI.InputPage()

    # mainGUI = GUIPyQt(500, 500)