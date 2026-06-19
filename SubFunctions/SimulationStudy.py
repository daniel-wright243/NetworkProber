import ast
# import math
import pathlib
import time
from copy import deepcopy

import networkx
import numpy
import numpy as np
import re
import random
import pickle
import csv

import phylox
from phylox.newick_parser import dinetwork_to_extended_newick, extended_newick_to_dinetwork

from SubFunctions.FoldingAlgorithm import FoldingAlgorithm
from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.PloidyAlgorithm import PolyPloidy
# from SubFunctions.MultiLabelledGraph import MultiLabelledGraph
from SubFunctions.TreeSpotterAlgorithm import TreeSpotterAlgorithm
from SubFunctions.Measures import *


class SimulationStudy:

    def __init__(self, percentage_x, percentage_y):
        """

        Parameters
        ----------
        percentage_x : int
        percentage_y : int
        """

        self.percentage_x = percentage_x
        self.percentage_y = percentage_y
        self.subscript_dict = {'0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084', '5': '\u2085','6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089'}


    def runBioSimStudy(self):
        vertices_list = []
        for i in range(1, 7):
            vertices_list.append(i)
        arc_list = [[1, 2], [1, 3], [2, 4], [2, 5], [4, 6], [5, 6], [3, 6], [4, 7], [5, 7], [3, 7]]
        bio_network = PhylogeneticNetwork(vertices_list, arc_list, 1)
        #bio_network.displayGraph()
        # PA = PolyPloidy(bio_network)
        # NPrime = PA.startAlgorithm()
        #NPrime.displayGraph()
        timings = []

        #BIO EXAMPLE 1
        bio_preset1_vertices = [0]
        for i in range(1, 62):
            if i != 32:
                bio_preset1_vertices.append(i)
        bio_preset1_taxDict = {43: "x" + self.subscript_dict.get('1'), 44: "x" + self.subscript_dict.get('2'),
                               45: "x" + self.subscript_dict.get('3'), 46: "x" + self.subscript_dict.get('4'),
                               47: "x" + self.subscript_dict.get('5'), 48: "x" + self.subscript_dict.get('6'),
                               49: "x" + self.subscript_dict.get('7'), 50: "x" + self.subscript_dict.get('8'),
                               51: "x" + self.subscript_dict.get('9'),
                               52: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('0'),
                               53: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('1'),
                               54: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('2'),
                               55: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('3'),
                               56: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('4'),
                               57: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('5'),
                               58: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('6')}
        bio_preset1_arcs = [[0, 1], [1, 2], [1, 43], [2, 3], [2, 42], [3, 59], [3, 4], [4, 5], [4, 41], [5, 8], [5, 6],
                            [6, 7], [6, 12], [7, 9], [7, 11], [8, 9], [8, 61], [9, 10], [10, 41], [10, 37], [11, 34],
                            [11, 35], [12, 29], [12, 13], [13, 14], [13, 29], [14, 15], [14, 30], [15, 27], [15, 25],
                            [15, 24], [15, 23], [15, 22], [15, 21], [15, 20], [16, 18], [16, 17], [17, 58], [18, 19],
                            [19, 57], [19, 17], [20, 16], [21, 18], [22, 56], [23, 55], [24, 54], [25, 26], [26, 31],
                            [26, 53], [27, 28], [28, 33], [28, 52], [29, 30], [30, 31], [31, 50], [33, 51], [34, 20],
                            [34, 21], [34, 22], [34, 23], [34, 24], [34, 25], [34, 27], [34, 31], [34, 60], [35, 36],
                            [36, 38], [37, 36], [37, 39], [38, 47], [38, 48], [39, 45], [40, 39], [41, 40], [42, 44],
                            [59, 42], [59, 40], [60, 49], [60, 33], [61, 35], [61, 46]]
        bio_preset1_network = PhylogeneticNetwork(bio_preset1_vertices, bio_preset1_arcs, 0, bio_preset1_taxDict)

        #BIO EXAMPLE 2
        bio_preset2_vertices = [0]
        for i in range(1, 75):
            if i != 33 and i != 37 and i != 38:
                bio_preset2_vertices.append(i)
        bio_preset2_taxDict = {45: "x" + self.subscript_dict.get('1'), 46: "x" + self.subscript_dict.get('2'),
                               47: "x" + self.subscript_dict.get('3'), 48: "x" + self.subscript_dict.get('4'),
                               49: "x" + self.subscript_dict.get('5'), 50: "x" + self.subscript_dict.get('6'),
                               51: "x" + self.subscript_dict.get('7'), 52: "x" + self.subscript_dict.get('8'),
                               53: "x" + self.subscript_dict.get('9'),
                               54: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('0'),
                               55: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('1'),
                               56: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('2'),
                               57: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('3'),
                               58: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('4'),
                               59: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('5'),
                               60: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('6'),
                               61: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('7'),
                               62: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('8'),
                               63: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('9'),
                               64: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('0'),
                               65: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('1'),
                               66: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('2'),
                               67: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('3'),
                               68: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('4'),
                               69: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('5'),
                               70: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('6'),
                               71: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('7'),
                               72: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('8'),
                               73: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('9'),
                               74: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('0')}
        bio_preset2_arcs = [[0, 1], [1, 45], [1, 9], [1, 2], [2, 49], [2, 3], [3, 8], [3, 20], [4, 5], [4, 19], [5, 52],
                            [5, 6], [6, 53], [6, 7], [7, 11], [7, 12], [8, 50], [8, 51], [9, 10], [9, 48], [10, 47],
                            [10, 46], [11, 54], [12, 55], [13, 11], [13, 12], [13, 14], [13, 15], [13, 17], [14, 57],
                            [15, 58], [16, 59], [17, 16], [17, 43], [17, 44], [17, 41], [18, 14], [18, 15], [18, 28],
                            [19, 56], [19, 21], [20, 4], [20, 24], [21, 13], [21, 22], [21, 25], [22, 18], [22, 16],
                            [22, 23], [22, 28], [22, 29], [22, 30], [22, 31], [22, 32], [22, 39], [22, 40], [22, 41],
                            [23, 11], [23, 12], [24, 73], [24, 34], [25, 26], [25, 32], [25, 72], [26, 27], [26, 31],
                            [27, 28], [27, 29], [27, 30], [28, 60], [29, 61], [30, 62], [31, 63], [32, 64], [34, 74],
                            [34, 35], [35, 36], [35, 71], [36, 43], [36, 44], [36, 39], [36, 40], [36, 41], [36, 42],
                            [39, 67], [40, 68], [41, 69], [42, 70], [43, 65], [44, 66], ]
        bio_preset2_network = PhylogeneticNetwork(bio_preset2_vertices, bio_preset2_arcs, 0, bio_preset2_taxDict)

        #BIO EXAMPLE 3
        bio_preset3_vertices = [0]
        for i in range(1, 91):
            bio_preset3_vertices.append(i)
        bio_preset3_taxDict = {50: "x" + self.subscript_dict.get('1'), 51: "x" + self.subscript_dict.get('2'),
                               53: "x" + self.subscript_dict.get('3'), 54: "x" + self.subscript_dict.get('4'),
                               55: "x" + self.subscript_dict.get('5'),
                               56: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('4'),
                               57: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('5'),
                               58: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('6'),
                               59: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('7'),
                               60: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('8'),
                               61: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('9'),
                               62: "x" + self.subscript_dict.get('4') + self.subscript_dict.get('1'),
                               63: "x" + self.subscript_dict.get('7'), 64: "x" + self.subscript_dict.get('8'),
                               65: "x" + self.subscript_dict.get('9'),
                               66: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('0'),
                               67: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('1'),
                               68: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('2'),
                               69: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('3'),
                               70: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('4'),
                               71: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('5'),
                               72: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('6'),
                               73: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('7'),
                               74: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('8'),
                               75: "x" + self.subscript_dict.get('1') + self.subscript_dict.get('9'),
                               76: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('0'),
                               77: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('1'),
                               78: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('2'),
                               79: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('3'),
                               80: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('0'),
                               81: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('1'),
                               82: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('2'),
                               83: "x" + self.subscript_dict.get('3') + self.subscript_dict.get('3'),
                               84: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('4'),
                               85: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('5'),
                               86: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('6'),
                               87: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('7'),
                               88: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('8'),
                               89: "x" + self.subscript_dict.get('2') + self.subscript_dict.get('9')}
        bio_preset3_arcs = [[0, 1], [1, 2], [1, 10], [2, 50], [2, 3], [2, 4], [3, 51], [3, 52], [4, 5], [4, 53],
                            [5, 54], [5, 6], [6, 55], [6, 15], [7, 15], [7, 56], [8, 7], [8, 57], [9, 8], [9, 58],
                            [10, 9], [10, 11], [10, 12], [11, 90], [11, 62], [12, 13], [12, 21], [13, 14], [13, 61],
                            [14, 59], [14, 60], [15, 16], [16, 17], [16, 18], [17, 63], [17, 64], [18, 19], [18, 20],
                            [19, 23], [19, 37], [20, 21], [20, 22], [21, 24], [22, 67], [22, 68], [23, 65], [23, 66],
                            [24, 25], [24, 27], [24, 28], [25, 26], [25, 32], [26, 82], [26, 83], [27, 29], [27, 34],
                            [28, 30], [28, 33], [29, 80], [29, 81], [30, 43], [30, 31], [31, 44], [31, 32], [32, 47],
                            [33, 34], [33, 36], [34, 35], [35, 76], [35, 77], [36, 37], [36, 38], [37, 49], [38, 84],
                            [38, 39], [39, 40], [39, 41], [40, 85], [40, 86], [41, 42], [41, 89], [42, 87], [42, 88],
                            [43, 48], [44, 45], [44, 43], [45, 71], [45, 46], [46, 72], [46, 73], [47, 74], [47, 75],
                            [48, 69], [48, 70], [49, 78], [49, 79]]
        bio_preset3_network = PhylogeneticNetwork(bio_preset3_vertices, bio_preset3_arcs, 0, bio_preset3_taxDict)

        #RUN TREESPOTTER ON BIO NETWORKS

        input_networks = [bio_preset1_network, bio_preset2_network, bio_preset3_network]
        output_networks_fold = []
        output_networks_pp = []

        for network in input_networks:
            fold_start_time = time.time()
            output_networks_fold.append(TreeSpotterAlgorithm(network).startAlgorithm(False))
            fold_end_time = time.time()
            polyploidy_start_time = time.time()
            output_networks_pp.append(TreeSpotterAlgorithm(network).startAlgorithm(True))
            polyploidy_end_time = time.time()

            fold_total_time = fold_end_time - fold_start_time
            polyploidy_total_time = polyploidy_end_time - polyploidy_start_time
            timings.append([fold_total_time, polyploidy_total_time])



        for vertex in output_networks_fold[1].vertices:
            if vertex not in bio_preset2_network.vertices:
                print("VERTEX NOT IN IS")
                print(vertex)

        # bio1_tsa = TreeSpotterAlgorithm(bio_preset1_network)
        # bio1_output = bio1_tsa.startAlgorithm(False)
        #
        # bio2_tsa = TreeSpotterAlgorithm(bio_preset2_network)
        # bio2_output = bio2_tsa.startAlgorithm(False)
        #
        # bio3_tsa = TreeSpotterAlgorithm(bio_preset3_network)
        # bio3_output = bio3_tsa.startAlgorithm(False)

        measure1_array = []
        measure2_array = []
        measure3_array = []
        measure4_array = []
        measure5_array = []

        for i in range(len(input_networks)):
            measure1_array.append([measure1(output_networks_fold[i], input_networks[i]), measure1(output_networks_pp[i], input_networks[i])])
            measure2_array.append([measure2(output_networks_fold[i], input_networks[i]), measure2(output_networks_pp[i], input_networks[i])])
            measure3_array.append([measure3(output_networks_fold[i], input_networks[i]), measure3(output_networks_pp[i], input_networks[i])])
            measure4_array.append([timings[i][0], timings[i][1]])
            #measure4_array.append([measure4(output_networks_fold[i], input_networks[i]), measure4(output_networks_pp[i], input_networks[i])])
            # measure5_array.append([measure5(output_networks_fold[i], input_networks[i]), measure5(output_networks_pp[i], input_networks[i])])

        measure_data_array = [measure1_array, measure2_array, measure3_array, measure4_array]

        print(output_networks_fold[0].checkTreeBasedNonBinary2())

        self.saveDataToCSV(input_networks, output_networks_pp, output_networks_fold, measure_data_array)

        print("MEASURE5ARRAY")
        print(measure5_array)

        return measure1_array, measure2_array, measure3_array, measure4_array

    def getTreesFromFiles(self):
        root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '\\R files\\'
        # tree_leaves_list = [10, 15, 20, 25, 30, 35]
        tree_leaves_list = [10]
        nexus_tree_array = []
        self.networkArray = []
        self.treeArray = []
        self.treeNEXUSStringArray = []
        self.networkNEXUSStringArray = []
        for leaf_set in tree_leaves_list:
            folder_dir = root_dir + str(leaf_set) + " Leaves\\"
            for i in range(1, 51):
            # for i in range(1, 11):
                file_dir = folder_dir + str(i) + "simTree.nex"
                nexus_tree_array.append(self.SimStudyReadNexusLine(file_dir))
        # print("NEXUS TREE ARRAY")
        # print(self.treeArray)
        # self.treeArray[0][0].displayGraph()
        ## print("SELF.TREEARRAY")
        ## print(self.treeArray)
        # self.treeArray[1][0].displayGraph()

        return self.treeArray

    def runGeneratedSimStudy(self):
        tree_list = self.getTreesFromFiles()
        input_networks = []
        output_networks_fold = []
        output_networks_pp = []
        output_networks_matching = []
        timings = []
        measure1_array = []
        measure2_array = []
        measure3_array = []
        measure4_array = []
        fc_array = [1]
        for fc in fc_array:
            list_of_tree_indices = []
            ntb_indices = []
            for i in range(len(tree_list)):
                list_of_tree_indices.append(i)
            amount_of_tbn = math.ceil(len(tree_list) * 0.3)
            for i in range(amount_of_tbn):
                random_network = random.choice(list_of_tree_indices)
                ntb_indices.append(random_network)
                list_of_tree_indices.remove(random_network)

            for i in range(len(tree_list)):
                tree = tree_list[i][0]
                # tree.displayGraph()
                # print(tree.vertices)
                print(i)
                arc_list = self.getAllArcsFromNetwork(tree)
                #ADD ARCS TO NETWORK
                network = self.addEdges2(tree, arc_list)
                # choice = random.choice(['1', '2'])
                # print("CHOICE")
                # print(choice)
                # if choice != '1' and choice != '2':
                #     raise Exception
                # if i in ntb_indices:
                # network.displayGraph()
                arc_list = self.getAllArcsFromNetwork(network)
                # for repeat in range(int(fc)):
                for j in range(1, 2):
                    network = self.addForbiddenConfigurations(network, arc_list)
                print("FORBIDDEN CONFIGURATION")
                # network.displayGraph()

                #PUT NETWORK INTO TREESPOTTER AND RETURN OUTPUT

                # if fc == 2:
                #     network.displayGraph()

                converted_network = self.readENewickLine(self.networkToENewickLine(network))

                input_networks.append(converted_network)

                input_fold = deepcopy(converted_network)
                input_pp = deepcopy(converted_network)
                input_matching = deepcopy(converted_network)

                fold_start_time = time.time()
                output_networks_fold.append(TreeSpotterAlgorithm(input_fold).startAlgorithm(False))
                fold_end_time = time.time()
                polyploidy_start_time = time.time()
                output_networks_pp.append(TreeSpotterAlgorithm(input_pp).startAlgorithm(True))
                polyploidy_end_time = time.time()
                matching_algorithm_start_time = time.time()
                output_m = TreeSpotterAlgorithm(input_matching).bipartiteGraphAlgorithm(input_matching)
                output_networks_matching.append(output_m)
                matching_algorithm_end_time = time.time()

                fold_total_time = fold_end_time - fold_start_time
                polyploidy_total_time = polyploidy_end_time - polyploidy_start_time
                matching_algorithm_total_time = matching_algorithm_end_time - matching_algorithm_start_time
                timings.append([fold_total_time, polyploidy_total_time, matching_algorithm_total_time])

                print("FOLD TIME")
                print(fold_total_time)
                print("POLYPLOIDY TIME")
                print(polyploidy_total_time)

            for i in range(len(input_networks)):
                measure1_array.append([measure1(output_networks_fold[i], input_networks[i]), measure1(output_networks_pp[i], input_networks[i]), measure1(output_networks_matching[i], input_networks[i])])
                measure2_array.append([measure2(output_networks_fold[i], input_networks[i]), measure2(output_networks_pp[i], input_networks[i])])
                measure3_array.append([measure3(output_networks_fold[i], input_networks[i]), measure3(output_networks_pp[i], input_networks[i])])
                measure4_array.append([timings[i][0], timings[i][1], timings[i][2]])
                #measure4_array.append([measure4(output_networks_fold[i], input_networks[i]), measure4(output_networks_pp[i], input_networks[i])])

        measure_data_array = [measure1_array, measure2_array, measure3_array, measure4_array]

        self.saveDataToCSV(input_networks, output_networks_pp, output_networks_fold, output_networks_matching, measure_data_array)

        return measure1_array, measure2_array, measure3_array, measure4_array

    def runFoldSimStudy(self):
        vertices_list = []
        #for i in range(1, 9):
        #    vertices_list.append(i)
        #arc_list = [[1, 2], [1, 3], [2, 4], [2, 5], [3, 5], [3, 6], [4, 7], [4, 8], [5, 8], [8, 9]]
        for i in range(1, 19):
            vertices_list.append(i)
        arc_list = [[1, 2], [1, 3], [2, 4], [2, 9], [3, 5], [3, 6], [4, 7], [4, 8], [5, 10], [6, 10], [6, 11], [7, 12], [7, 13], [8, 13], [8, 14], [9, 14], [9, 15], [10, 16], [11, 16], [11, 17], [13, 18], [14, 18], [16, 19], [18, 20], [5, 21]]
        test_network = PhylogeneticNetwork(vertices_list, arc_list, 1)

        vertices_list2 = []
        for i in range(1, 12):
            vertices_list2.append(i)
        arc_list2 = [[1, 2], [1, 5], [2, 3], [2, 4], [3, 6], [3, 7], [4, 7], [4, 8], [5, 8], [5, 9], [7, 10], [8, 10], [10, 11]]

        test_network2 = PhylogeneticNetwork(vertices_list2, arc_list2, 1)

        #test_network2.displayGraph()
        #test_network.makeBiPartiteGraph().displayGraph()
        #test_network.getNetworkBelowVertex(8).displayGraph()
        #print("RETICULATION VERTICES")
        #tv, rv = test_network.getTreeAndReticulationVertexArray(True)
        #print(rv)

        FAlgorithm = FoldingAlgorithm(test_network)
        FAlgorithm.runAlgorithm()

        #FAlgorithm.readFromPADREFile()

        #test_network.displayGraph()

        #mlg = MultiLabelledGraph(test_network)
        # print("MULTI-LABELLED VERTICES")
        # print(mlg.multiLabelledVertices)
        #mlg.displayGraph()
        # mlg.writeToPADREFile()

    def runSimStudy(self):
        root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '\\R files\\'
        # tree_leaves_list = [10, 15, 20, 25, 30, 35]
        tree_leaves_list = [10]
        nexus_tree_array = []
        self.networkArray = []
        self.treeArray = []
        self.treeNEXUSStringArray = []
        self.networkNEXUSStringArray = []
        for leaf_set in tree_leaves_list:
            folder_dir = root_dir + str(leaf_set) + " Leaves\\"
            for i in range(1, 99):
                file_dir = folder_dir + str(i) + "simTree.nex"
                nexus_tree_array.append(self.SimStudyReadNexusLine(file_dir))
        #print("NEXUS TREE ARRAY")
        #print(self.treeArray)
        #self.treeArray[0][0].displayGraph()
        network_list = []
        for i in range(len(self.treeArray)):
            for j in range(1, 10):
                tree = self.treeArray[i][0]
                arc_list = self.getAllArcsFromNetwork(tree)
                #print("TREE")
                #print(tree.arcs)
                #print(arc_list)
                random_number = random.choice([1, 10])
                if random_number == 1 or random_number == 2: # ADD FORBIDDEN CONFIGURATION
                    network_list.append(self.addForbiddenConfigurations(tree, arc_list))
                #else: # ADD CERTAIN AMOUNT OF EDGES BASED ON AMOUNT OF EDGES
                #    network_list.append(self.addEdges(tree, arc_list))
                ## print("I")
                ## print(i)
                ## print("J")
                ## print(j)
        #network_list[0].displayGraph()
        for network in network_list:
            if self.checkDirectedCyclicity(network):
                ## print("CYCLE PRESENT")
                #network.displayGraph()
                break
        for network in network_list:
            for vertex in network.vertices:
                if self.checkNotBinary(network, vertex):
                    ## print("VERTEX")
                    ## print(vertex)
                    incoming_arcs = len(network.reverseArcs[vertex])
                    outgoing_arcs = len(network.arcs[vertex])
                    ## print("INCOMING ARCS")
                    ## print(network.reverseArcs[vertex])
                    ## print(incoming_arcs)
                    ## print("OUTGOING ARCS")
                    ## print(network.arcs[vertex])
                    ## print(outgoing_arcs)
                    ## print("NON BINARY")
                    #network.displayGraph()
                    break
            break
        # for network in network_list:
        #     if self.checkMultipleRoots(network):
        #         ## print("MULTIPLE ROOTS FOUND")
        #         #network.displayGraph()
        self.saveDatabase(network_list)
        retrievedDatabase = self.loadDatabase()
        #retrievedDatabase[0].displayGraph()
        #arc_list = self.getAllArcsFromNetwork(self.treeArray[0][0])
        #self.treeArray[0][0].displayGraph()
        #print("LEVELDICT")
        #print(self.treeArray[0][2])
        #network_list.append(self.addEdges(self.treeArray[0][0], arc_list))
        #self.treeArray[0][0].displayGraph()
        #network_list[0].displayGraph()
        #cyclicityCheck = self.checkDirectedCyclicity(network_list[0])
        #print("CYCLICITY")
        #print(cyclicityCheck)

    def saveDatabase(self, database):
        with open('database.pickle', 'wb') as file:
            pickle.dump(database, file)

    def loadDatabase(self):
        with open('database.pickle', 'rb') as file:
            loaded_object = pickle.load(file)
            return loaded_object

    def addForbiddenConfigurations(self, tree, arc_list):
        """

        Parameters
        ----------
        tree : PhylogeneticNetwork
        """
        network = deepcopy(tree)
        leafs = network.getAllLeafs()
        random_number = random.choice(['1', '2'])
        # random_number = '1'
        #random_number = 2
        arcs_used = []
        starting_vertices = max(tree.vertices)
        if random_number == '1': #USE 1ST FORBIDDEN CONFIGURATION
            #PICK 4 RANDOM EDGES FOR THE INPUTS INTO THE FORBIDDEN CONFIGURATION
            amount_of_input_edges = 4
            for i in range(amount_of_input_edges):
                random_arc_index_1 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided_1 = arc_list[random_arc_index_1]
                while arc_to_be_subdivided_1 in arcs_used:
                    random_arc_index_1 = random.randrange(len(arc_list) - 1)
                    arc_to_be_subdivided_1 = arc_list[random_arc_index_1]
                arcs_used.append(arc_to_be_subdivided_1)
            #MAKE THE FORBIDDEN CONFIGURATION
            starting_edges_index = starting_vertices
            for arcs in arcs_used: #ADD THE VERTICES TO THE EDGES
                network.addVertexOnEdge(starting_vertices + 1, arcs)
                starting_vertices = starting_vertices + 1
            #MAKE THE FORBIDDEN CONFIGURATION
            network.createArc([starting_edges_index + 1, starting_vertices + 1])
            network.createArc([starting_edges_index + 2, starting_vertices + 1])
            network.createArc([starting_edges_index + 3, starting_vertices + 2])
            network.createArc([starting_edges_index + 4, starting_vertices + 2])
            network.createVertex(starting_vertices + 3)
            # print(starting_vertices + 3)
            network.createArc([starting_vertices + 1, starting_vertices + 3])
            network.createArc([starting_vertices + 2, starting_vertices + 3])
            bottom_vertex_index = starting_vertices + 3
            starting_vertices = starting_vertices + 3
            amount_of_output_edges = 1
            for i in range(amount_of_output_edges):
                random_arc_index_2 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
                while arc_to_be_subdivided_2 in arcs_used:
                    random_arc_index_2 = random.randrange(len(arc_list) - 1)
                    arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
                #CHECK TO SEE IF NEW EDGE HAS ADDED A CYCLE
                temp_network = deepcopy(network)
                temp_network.addVertexOnEdge(starting_vertices + 1, arc_to_be_subdivided_2)
                temp_network.createArc([bottom_vertex_index, starting_vertices + 1])
                if self.checkDirectedCyclicity(temp_network) or self.checkNotBinary(temp_network, starting_vertices + 1):
                    amount_of_output_edges = amount_of_output_edges + 1
                else:
                    network = temp_network
            return network
        elif random_number == '2': # USE 2ND FORBIDDEN CONFIGURATION
            amount_of_input_edges = 5
            for i in range(amount_of_input_edges):
                random_arc_index_1 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided_1 = arc_list[random_arc_index_1]
                while arc_to_be_subdivided_1 in arcs_used:
                    random_arc_index_1 = random.randrange(len(arc_list) - 1)
                    arc_to_be_subdivided_1 = arc_list[random_arc_index_1]
                arcs_used.append(arc_to_be_subdivided_1)
            # MAKE THE FORBIDDEN CONFIGURATION
            # if len(arcs_used) < 4:
            #     ## print("ARC THRESHOLD NOT ACHIEVED")
            starting_edges_index = starting_vertices
            for arcs in arcs_used:  # ADD THE VERTICES TO THE EDGES
                network.addVertexOnEdge(starting_vertices + 1, arcs)
                starting_vertices = starting_vertices + 1
            fc_starting_edges_index = starting_vertices
            network.createVertex(starting_vertices + 1)
            network.createArc([starting_edges_index + 1, starting_vertices + 1])
            network.createArc([starting_edges_index + 2, starting_vertices + 1])
            network.createVertex(starting_vertices + 2)
            # print("STARTING VERTICES + 2")
            # print(starting_vertices + 2)
            network.createArc([starting_edges_index + 3, starting_vertices + 2])
            network.createVertex(starting_vertices + 3)
            network.createArc([starting_edges_index + 4, starting_vertices + 3])
            network.createArc([starting_edges_index + 5, starting_vertices + 3])
            network.createVertex(starting_vertices + 4)
            # print("STARTING VERTICES + 2")
            # print(starting_vertices + 4)
            network.createArc([starting_vertices + 1, starting_vertices + 4])
            network.createArc([starting_vertices + 2, starting_vertices + 4])
            network.createVertex(starting_vertices + 5)
            # print("STARTING VERTICES + 2")
            # print(starting_vertices + 5)
            network.createArc([starting_vertices + 2, starting_vertices + 5])
            network.createArc([starting_vertices + 3, starting_vertices + 5])
            starting_vertices = starting_vertices + 5
            # print("STARTING VERTICES + 5")
            # print(starting_vertices)
            amount_of_output_edges = 3
            vertex_index = [starting_vertices + 4, starting_vertices + 5]
            #FIRST VERTEX
            random_arc_index_2 = random.randrange(len(arc_list) - 1)
            arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
            while arc_to_be_subdivided_2 in arcs_used:
                random_arc_index_2 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
            temp_network = deepcopy(network)
            temp_network.addVertexOnEdge(starting_vertices + 1, arc_to_be_subdivided_2)
            temp_network.createArc([fc_starting_edges_index + 4, starting_vertices + 1])
            while self.checkDirectedCyclicity(temp_network):
                random_arc_index_2 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
                while arc_to_be_subdivided_2 in arcs_used:
                    random_arc_index_2 = random.randrange(len(arc_list) - 1)
                    arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
                temp_network = deepcopy(network)
                temp_network.addVertexOnEdge(starting_vertices + 1, arc_to_be_subdivided_2)
                temp_network.createArc([fc_starting_edges_index + 4, starting_vertices + 1])
            network = temp_network
            starting_vertices = starting_vertices + 1
            arcs_used.append(arc_to_be_subdivided_2)
            #SECOND VERTEX
            random_arc_index_2 = random.randrange(len(arc_list) - 1)
            arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
            while arc_to_be_subdivided_2 in arcs_used:
                random_arc_index_2 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
            temp_network = deepcopy(network)
            temp_network.addVertexOnEdge(starting_vertices + 1, arc_to_be_subdivided_2)
            temp_network.createArc([fc_starting_edges_index + 5, starting_vertices + 1])
            while self.checkDirectedCyclicity(temp_network):
                random_arc_index_2 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
                while arc_to_be_subdivided_2 in arcs_used:
                    random_arc_index_2 = random.randrange(len(arc_list) - 1)
                    arc_to_be_subdivided_2 = arc_list[random_arc_index_2]
                temp_network = deepcopy(network)
                temp_network.addVertexOnEdge(starting_vertices + 1, arc_to_be_subdivided_2)
                temp_network.createArc([fc_starting_edges_index + 5, starting_vertices + 1])
            network = temp_network
            starting_vertices = starting_vertices + 1
            arcs_used.append(arc_to_be_subdivided_2)
            return network

        #else: # USE 3RD FORBIDDEN CONFIGURATION


    def checkDirectedCyclicity(self, network):
        networkXGraph = networkx.DiGraph()
        for vertex in network.vertices:
            networkXGraph.add_node(vertex)
        for vertex in network.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])
        try:
            cycles = networkx.find_cycle(networkXGraph)
            return True
        except:
            return False

    def checkMultipleRoots(self, network):
        for i in range(len(network.arcs)):
            if len(network.arcs) > 0 and len(network.reverseArcs) == 0:
                return True
        return False

    def addEdges(self, network, arc_list): # ADD 20% MORE EDGES
        network_copy = deepcopy(network)
        """

        Parameters
        ----------
        network : PhylogeneticNetwork
        """
        amount_of_edges_to_be_added = math.ceil(len(arc_list) * 0.2)
        edges_subdivided = []
        starting_amount_of_vertices = max(network_copy.vertices)
        #print("ADDING EDGES")
        for i in range(1, amount_of_edges_to_be_added):
            temp_network = deepcopy(network_copy)
            random_number1 = random.randrange(len(arc_list) - 1)
            arc_to_be_subdivided1 = arc_list[random_number1]
            random_number2 = random.randrange(len(arc_list) - 1)
            while random_number2 == random_number1:
                random_number2 = random.randrange(len(arc_list) - 1)
            #print("ARC LIST")
            #print(arc_list)
            #print("RANDOM NUMBER")
            #print(random_number2)
            #print("STARTING_AMOUNT_OF_VERTICES")
            #print(starting_amount_of_vertices)
            arc_to_be_subdivided2 = arc_list[random_number2]
            while arc_to_be_subdivided1 in edges_subdivided or arc_to_be_subdivided2 in edges_subdivided:
                random_number1 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided1 = arc_list[random_number1]
                random_number2 = random.randrange(len(arc_list) - 1)
                while random_number2 == random_number1:
                    random_number2 = random.randrange(len(arc_list) - 1)
                arc_to_be_subdivided2 = arc_list[random_number2]
            temp_network.addVertexOnEdge(starting_amount_of_vertices + 1, arc_to_be_subdivided1)
            temp_network.addVertexOnEdge(starting_amount_of_vertices + 2, arc_to_be_subdivided2)
            edges_subdivided.append([arc_to_be_subdivided1[0], starting_amount_of_vertices + 1])
            edges_subdivided.append([starting_amount_of_vertices + 1, arc_to_be_subdivided1[1]])
            #CHECK NETWORK CYCLICITY
            temp_network.createArc([starting_amount_of_vertices + 1, starting_amount_of_vertices + 2])
            edges_subdivided.append([starting_amount_of_vertices + 1, starting_amount_of_vertices + 2])
            if self.checkDirectedCyclicity(temp_network):
                temp_network.arcs[starting_amount_of_vertices + 1].remove([starting_amount_of_vertices + 1, starting_amount_of_vertices + 2])
                temp_network.reverseArcs[starting_amount_of_vertices + 2].remove([starting_amount_of_vertices + 2, starting_amount_of_vertices + 1])
                temp_network.createArc([starting_amount_of_vertices + 2, starting_amount_of_vertices + 1])
                edges_subdivided.remove([starting_amount_of_vertices + 1, starting_amount_of_vertices + 2])
                edges_subdivided.append([starting_amount_of_vertices + 2, starting_amount_of_vertices + 1])
                if self.checkDirectedCyclicity(temp_network):
                    edges_subdivided.remove([starting_amount_of_vertices + 2, starting_amount_of_vertices + 1])
                    temp_network.arcs[starting_amount_of_vertices + 2].remove([starting_amount_of_vertices + 2, starting_amount_of_vertices + 1])
                    temp_network.reverseArcs[starting_amount_of_vertices + 1].remove([starting_amount_of_vertices + 1, starting_amount_of_vertices + 2])
                    amount_of_edges_to_be_added = amount_of_edges_to_be_added + 1
            edges_subdivided.append([arc_to_be_subdivided2[0] + starting_amount_of_vertices + 2])
            edges_subdivided.append([starting_amount_of_vertices + 2, arc_to_be_subdivided2[1]])
            non_binary = False
            if not self.checkNotBinary(temp_network, arc_to_be_subdivided1[0]) and not self.checkNotBinary(temp_network, arc_to_be_subdivided1[1]):
                if not self.checkNotBinary(temp_network, arc_to_be_subdivided2[0]) and not self.checkNotBinary(temp_network, arc_to_be_subdivided2[1]):
                    network_copy = temp_network
                    starting_amount_of_vertices = starting_amount_of_vertices + 2
                else:
                    non_binary = True
            else:
                non_binary = True
            if non_binary:
                amount_of_edges_to_be_added = amount_of_edges_to_be_added + 1

        return network_copy

    def addEdges2(self, network, arc_list):
        """

        :type network: PhylogeneticNetwork
        """

        network_copy = deepcopy(network)

        leaf_set = network_copy.getAllLeafs()

        amount_of_edges_to_be_added = math.ceil(len(network_copy.vertices) * 0.3)
        edges_subdivided = []
        starting_amount_of_vertices = max(network_copy.vertices)

        vertex_set = deepcopy(network_copy.vertices)
        vertex_set.remove(network.root)

        # print(vertex_set)

        for vertex in leaf_set:
            vertex_set.remove(vertex)

        for i in range(1, amount_of_edges_to_be_added):
            random_number1 = vertex_set[random.randrange(len(vertex_set) - 1)]
            # print("RN1")
            # print(random_number1)
            random_number2 = vertex_set[random.randrange(len(vertex_set) - 1)]
            # print("RN2")
            # print(random_number2)
            while random_number2 == random_number1:
                random_number2 = vertex_set[random.randrange(len(vertex_set) - 1)]

            #FIND ARCS THAT ARE GOING TO BE SUBDIVIDED
            arc_subdivide1 = network_copy.reverseArcs[random_number1][0]
            arc_subdivide2 = network_copy.reverseArcs[random_number2][0]

            #ADD TWO NEW VERTICES
            network_copy.vertices.append(starting_amount_of_vertices + 1)
            network_copy.vertices.append(starting_amount_of_vertices + 2)

            #REMOVE SUBDIVIDED ARCS
            network_copy.removeArc([arc_subdivide1[1], arc_subdivide1[0]])
            network_copy.removeArc([arc_subdivide2[1], arc_subdivide2[0]])

            #CREATE ARCS FROM ARC SUBDIVIDED TO NEW VERTICES
            network_copy.createArc([arc_subdivide1[1], starting_amount_of_vertices + 1])
            network_copy.createArc([arc_subdivide2[1], starting_amount_of_vertices + 2])

            #CREATE ARCS FROM NEW VERTICES TO ARC SUBDIVIDED
            network_copy.createArc([starting_amount_of_vertices + 1, arc_subdivide1[0]])
            network_copy.createArc([starting_amount_of_vertices + 2, arc_subdivide2[0]])

            #CREATE ARC BETWEEN NEW VERTICES
            if arc_subdivide1[0] > arc_subdivide2[0]:
                network_copy.createArc([starting_amount_of_vertices + 2, starting_amount_of_vertices + 1])
            else:
                network_copy.createArc([starting_amount_of_vertices + 1, starting_amount_of_vertices + 2])

            starting_amount_of_vertices = starting_amount_of_vertices + 2

        # network_copy.displayGraph()
        return network_copy

    def checkNotBinary(self, network, vertex):
        """

        Parameters
        ----------
        network : PhylogeneticNetwork
        """
        if type(network.reverseArcs[vertex]) == list:
            incoming_arcs = len(network.reverseArcs[vertex])
        else:
            incoming_arcs = 1
        if type(network.arcs[vertex]) == list:
            outgoing_arcs = len(network.arcs[vertex])
        else:
            outgoing_arcs = 1
        #incoming_arcs = len(network.reverseArcs[vertex])
        #outgoing_arcs = len(network.arcs[vertex])
        total_arcs = incoming_arcs + outgoing_arcs
        if total_arcs > 3:
            return True
        else:
            return False

    #def addForbiddenConfigurations(self, network, arc_list):
    #    print("ADDING FORBIDDEN CONFIGURATION")

    def getAllArcsFromNetwork(self, network):
        """

        Parameters
        ----------
        network : PhylogeneticNetwork
        """
        arc_list = []
        for vertex in network.arcs:
            if len(vertex) > 0:
                for arc in vertex:
                    arc_list.append(arc)
        return arc_list
        
    def InputFromNEXUSFile2(self, filepath):
        #root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '/NEXUS Files'
        #window_filename = askopenfilename(initialdir=root_dir)
        # filename = 'testFile'
        # concatFileName = 'NEXUS Files/' + filename + '.NEXUS'
        #print(window_filename)
        openedNexusFile = open(filepath)
        # print(openedNexusFile.read())
        NEXUSFileReadLines = openedNexusFile.readlines()
        begin_datapoints = []
        begin_trees_datapoints = []
        begin_translate_datapoints = []
        end_translate_datapoints = []
        end_datapoints = []
        #print(NEXUSFileReadLines)
        for i in range(len(NEXUSFileReadLines)):
            #print(NEXUSFileReadLines[i])
            if 'BEGIN TREES' in NEXUSFileReadLines[i]:
                begin_datapoints.append(i)
            elif 'END;' in NEXUSFileReadLines[i]:
                end_datapoints.append(i)
            elif NEXUSFileReadLines[i] == "[TREES]\n":
                begin_trees_datapoints.append(i)
            if "TREE" in NEXUSFileReadLines[i] and 'BEGIN TREES' not in NEXUSFileReadLines[i]:
                begin_trees_datapoints.append(i)
                # for i in range(len(begin_trees_datapoints)):
                    ## print("BEGIN TREES DATAPOINTS")
                    #print(NEXUSFileReadLines[begin_trees_datapoints[i]])
            elif NEXUSFileReadLines[i] == "TRANSLATE\n":
                begin_translate_datapoints.append(i)
                for j in range(i, len(NEXUSFileReadLines)):
                    if NEXUSFileReadLines[j] == ";\n":
                        end_translate_datapoints.append(j)
                        break
            elif "TRANSLATE" in NEXUSFileReadLines[i]:
                begin_translate_datapoints.append(i)
                for j in range(i, len(NEXUSFileReadLines)):
                    if ";" in NEXUSFileReadLines[j]:
                        end_translate_datapoints.append(j)
                        break

        #print(begin_datapoints)
        #print(begin_trees_datapoints)
        #print(begin_translate_datapoints)
        #print(end_translate_datapoints)
        #print("END DATAPOINTS")
        #print(end_datapoints)

        # begin_Datapoints to end_datapoints holds all the information
        # begin_trees_datapoints to end_datapoints holds all of the network data
        names_dict_list = []
        for i in range(len(begin_datapoints)):
            # print(begin_datapoints[i])
            # print(begin_trees_datapoints[i])
            names_dict = {}
            # print(end_datapoints[i])
            #print("BEGIN DATAPOINTS")
            #print(begin_datapoints)
            #print("BEGIN TREE DATAPOINTS")
            #print(begin_trees_datapoints)
            for j in range(begin_datapoints[i], begin_trees_datapoints[i]):  # get all the tree information
                #print("NEW TREE")
                #print(begin_datapoints[i])
                #print("BEGIN DATAPOINT")
                #print(NEXUSFileReadLines[begin_datapoints[i]])
                #print("BEGIN TREES DATAPOINTS")
                #print(NEXUSFileReadLines[begin_trees_datapoints[i]])
                #print(begin_trees_datapoints[i])
                if "TITLE" in NEXUSFileReadLines[j]:
                    # print(NEXUSFileReadLines[j])
                    title = NEXUSFileReadLines[j].replace("TITLE", "").strip()
                    title = title.replace("'", "")
                    title = title.replace(";", "")
                    # print(title)
                if "Number of trees" in NEXUSFileReadLines[j]:
                    # print(NEXUSFileReadLines[j])
                    number_of_trees = NEXUSFileReadLines[j].replace("Number of trees: ", "").strip()
                    number_of_trees = number_of_trees.replace("[", "")
                    number_of_trees = number_of_trees.replace("]", "")
                    number_of_trees = int(number_of_trees)
                    # print(number_of_trees)
            #print("BEGIN TRANSLATE DATAPOINTS")
            #print(begin_translate_datapoints)
            #print("END TRANSLATE DATAPOINTS")
            #print(end_translate_datapoints)
            for j in range(begin_translate_datapoints[i] + 1, end_translate_datapoints[i]):
                # print("TRANSLATE FROM PROGRAM")
                # print(NEXUSFileReadLines[j])
                line = NEXUSFileReadLines[j].replace(",", "").strip()
                line = line.replace("'", "")
                split_line = line.split()
                # print(split_line)
                number = int(split_line[0])
                name = split_line[1]
                names_dict[number] = name
            names_dict_list.append(names_dict)
            for j in range(begin_trees_datapoints[i] + 1, end_datapoints[i]):
                #print("TREES START")
                #print(NEXUSFileReadLines[j])
                line = NEXUSFileReadLines[j].split("[&R]", 1)[1]
                line = line.replace(";", "")
                #print(line)
                self.readNexusLine(line)
        #print("SELF.TREENEXUSSTRINGARRAY")
        #print(self.treeNEXUSStringArray)
        return self.treeNEXUSStringArray
        # print(names_dict_list)

    def SimStudyReadNexusLine(self, filepath):
        # root_dir = str(pathlib.Path(__file__).parent.parent.resolve()) + '/NEXUS Files'
        # window_filename = askopenfilename(initialdir=root_dir)
        # filename = 'testFile'
        # concatFileName = 'NEXUS Files/' + filename + '.NEXUS'
        # print(window_filename)
        openedNexusFile = open(filepath)
        # print(openedNexusFile.read())
        NEXUSFileReadLines = openedNexusFile.readlines()
        #find lines with trees
        trees_datapoints = []
        begin_translate_datapoints = []
        end_translate_datapoints = []
        for i in range(len(NEXUSFileReadLines)):
            #print(NEXUSFileReadLines)
            if "TREE" in NEXUSFileReadLines[i] and "BEGIN TREES" not in NEXUSFileReadLines[i]:
                trees_datapoints.append(i)
            elif "TRANSLATE" in NEXUSFileReadLines[i]:
                begin_translate_datapoints.append(i)
                for j in range(i, len(NEXUSFileReadLines)):
                    if ";" in NEXUSFileReadLines[j]:
                        end_translate_datapoints.append(j)
                        break
        #print("TREES DATAPOINTS")
        #print(trees_datapoints)
        #TRANSLATE DATA
        #print("TRANSLATION")
        translate_lines = []
        for i in range(begin_translate_datapoints[0], end_translate_datapoints[0]):
            translate_lines.append(NEXUSFileReadLines[i])
        #TREE DATA
        #print("TREE DATA")
        for i in range(len(trees_datapoints)):
            ## print(NEXUSFileReadLines[trees_datapoints[i]])
            line = NEXUSFileReadLines[trees_datapoints[i]].replace(",", "").strip()
            line = line.replace("'", "")
            split_line = line.split()
            # print(split_line)
            #print(split_line)
            #number = int(split_line[0])
            name = split_line[2]
            # print("TREES START")
            # print(NEXUSFileReadLines[j])
            line = NEXUSFileReadLines[trees_datapoints[i]].split("[&R]", 1)[1]
            line = line.replace(";", "")
            # print(line)
            self.readNexusLine(line)
        return self.treeNEXUSStringArray

    def readNexusLine(self, nexusString):
        #INPUT NEXUS STRING
        #OUTPUT PHYLOGENETIC NETWORK
        temp_list = list(nexusString)
        #print(temp_list)
        for j in range(len(temp_list)):
            temp_list[j] = temp_list[j].replace("(", "[")
            temp_list[j] = temp_list[j].replace(")", "]")
        #print("TEMP LIST")
        #print(temp_list)
        temp_string = ''.join(temp_list).strip()
        #print("TEMP STRING")
        #print(temp_string)
        if "#" in nexusString: #PHYLOGENETIC NETWORK
            pattern = re.sub(r'#H\d+', self.add_quotes, temp_string)
            #print("PATTERN")
            #print(pattern)
            temp_string = pattern
            temp_string = temp_string.replace(",'#", ",'")
            temp_string = temp_string.replace("'#", ",'")

            #print("TEMP STRING")
            #print(temp_string)
            network_list = ast.literal_eval(temp_string.strip())

            #print("NETWORK LIST")
            #print(network_list)

            vertex_list = []

            temp_network = network_list
            dims = []
            while isinstance(temp_network, list) and network_list is not None:
                dims.append(len(network_list))
                temp_network = temp_network[0]
            num_of_dimensions = len(dims)

            vertices_on_each_level = [[] for _ in range(num_of_dimensions + 2)]
            counter = 0

            numpyArray = np.array(network_list, dtype=object)

            self.leaf_counter = 0

            self.NEXUSGetAmountOfLeaves(numpyArray)

            # print("LEAF COUNTER")
            # print(self.leaf_counter)

            vertex_required = self.leaf_counter + (self.leaf_counter - 1)

            for i in range(1, vertex_required + 1):
                vertex_list.append(i)

            ConstructedNetwork = PhylogeneticNetwork(vertex_list, [], 1)

            self.currentVertex = 1
            self.leafDict = {}
            self.PhyVertex = {}
            self.levelDict = {}

            self.NexusNetworkFrameRecursiveSearch(numpyArray, vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork)

            #print("VERTICES ON EACH LEVEL")
            #print(vertices_on_each_level)

            #ConstructedNetwork.displayGraph()

            #print("SELF PHYVERTEX")
            #print(self.PhyVertex)

            #print("NETWORK LIST")
            #print(network_list)
            #print("TEST")

            for list_values in self.PhyVertex.values():
                #FROM CHATGPT
                flattened_item = [item for sublist in list_values for item in (sublist if isinstance(sublist[0], list) else [sublist])]
                #
                #print(flattened_item)
                lowest_value = 100
                lowest_vertex = 0
                for value in flattened_item:
                    if value[1] < lowest_value:
                        lowest_value = value[1]
                        lowest_vertex = value[0]
                flattened_item.remove([lowest_vertex, lowest_value])
                for value in flattened_item:
                    ConstructedNetwork.createArc([value[0], lowest_vertex])

            #ConstructedNetwork.displayGraph()


            if [ConstructedNetwork, self.leafDict] not in self.networkArray:
                self.networkArray.append([ConstructedNetwork, self.leafDict])
                self.networkNEXUSStringArray.append(nexusString)


        else: #TREE
            network_list = ast.literal_eval(temp_string.strip())
            #print("NETWORK LIST")
            #print(network_list)
            #print(len(network_list))
            # length of network list is amount of new vertices that need to be added +1
            vertex_required = int(len(network_list)) + int(1)
            #print(vertex_required)
            # print(network_list.shape)
            #print("NETWORK LIST TEST")
            dims = []
            temp_network = network_list
            while isinstance(temp_network, list) and network_list is not None:
                dims.append(len(network_list))
                temp_network = temp_network[0]
            num_of_dimensions = len(dims)
            #print(num_of_dimensions)
            #for n in range(1, num_of_dimensions + 1):
            #    print(n)
            # numpyArray = np.array(network_list)
            # numpyArray = np.array(nexusString)
            numpyArray = np.array(network_list, dtype=object)
            #print(numpyArray.shape)
            # dtype="object"

            #print("NEXUSSTRING")
            #print(numpyArray)

            #print(numpyArray[0])

            values = np.take(numpyArray, indices=0, axis=0)
            #print(values)

            finished = False

            vertices_on_each_level = [[] for _ in range(num_of_dimensions + 100)]
            counter = 0

            #print("INPUT NEXUSSTRING")
            #print(nexusString)

            vertex_list = [0]

            self.leaf_counter = 0

            self.NEXUSGetAmountOfLeaves(numpyArray)

            # print("LEAF COUNTER")
            # print(self.leaf_counter)

            vertex_required = self.leaf_counter + (self.leaf_counter - 1)

            for i in range(1, vertex_required + 1):
                vertex_list.append(i)

            # print("VERTEX LIST")
            # print(vertex_list)

            ConstructedNetwork = PhylogeneticNetwork(vertex_list, [[0, 1]], 0)

            # print("CONSTRUCTED NETWORK VERTEX LIST")
            # print(ConstructedNetwork.vertices)

            self.currentVertex = 1
            self.leafDict = {}
            self.levelDict = [[] for _ in range(num_of_dimensions + 100)]
            current_level = 0

            self.NexusTreeFrameRecursiveSearch(numpyArray, vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork, current_level)
            #ConstructedNetwork.displayGraph()

            #print("VERTICES ON EACH LEVEL")
            #print(vertices_on_each_level)


            #print(self.leafDict)

            #ConstructedNetwork.displayGraph()



            if [ConstructedNetwork, self.leafDict] not in self.treeArray:
                self.treeArray.append([ConstructedNetwork, self.leafDict, self.levelDict])
                self.treeNEXUSStringArray.append(nexusString)

    def NexusNetworkFrameRecursiveSearch(self, frame, vertices_on_each_level, previousVertex, counter, ConstructedNetwork):
        for i in range(len(frame)):
            #self.levelDict[counter] = previousVertex
            ConstructedNetwork.createArc([previousVertex, self.currentVertex + 1])
            self.currentVertex = self.currentVertex + 1
            if type(frame[i]) == str:
                data = [self.currentVertex, counter]
                #self.PhyVertex.update({frame[i]: data})
                if frame[i] in self.PhyVertex:
                    self.PhyVertex[frame[i]] = [self.PhyVertex[frame[i]], data]
                else:
                    self.PhyVertex[frame[i]] = data

                #self.PhyVertex[self.currentVertex] = [frame[i], counter]
            elif type(frame[i]) != list and not isinstance(frame[i], numpy.ndarray):
                self.leafDict[(frame[i])] = self.currentVertex
                vertices_on_each_level[counter].append(frame[i])
            else:
                counter = counter + 1
                self.NexusNetworkFrameRecursiveSearch(frame[i], vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork)

    # FROM CHATGPT
    def add_quotes(self, match):
        return f"'{match.group(0)}'"
    #

    def NexusTreeFrameRecursiveSearch(self, frame, vertices_on_each_level, previousVertex, counter, ConstructedNetwork, current_level):
        #print("VERTEX ON EACH LEVEL")
        #print(vertices_on_each_level)
        #print("FRAME")
        #print(frame)
        for i in range(len(frame)):
            #print("FRAME")
            #print(i)
            #print(frame[i])
            #print("SELF.CURRENTVERTEX")
            #print(self.currentVertex)
            #print("SELF.LEAFDICT")
            #print(self.leafDict)
            #print("VERTICES ON EACH LEVEL")
            #print(vertices_on_each_level)
            ConstructedNetwork.createArc([previousVertex, self.currentVertex + 1])
            self.currentVertex = self.currentVertex + 1
            if type(frame[i]) != list and type(frame[i]) != numpy.ndarray:
                self.leafDict[frame[i]] = self.currentVertex
                vertices_on_each_level[counter].append(frame[i])
                self.levelDict[current_level].append(frame[i] + 1)
            else:
                counter = counter + 1
                self.levelDict[current_level].append(self.currentVertex)
                current_level = current_level + 1
                self.NexusTreeFrameRecursiveSearch(frame[i], vertices_on_each_level, self.currentVertex, counter, ConstructedNetwork, current_level)

    def NEXUSGetAmountOfLeaves(self, nexus_string):
        for item in nexus_string:
            if isinstance(item, list) or isinstance(item, np.ndarray):
                self.NEXUSGetAmountOfLeaves(item)
            else:
                self.leaf_counter = self.leaf_counter + 1

    def saveDataToCSV(self, input_network_array, output_network_array_pp, output_network_array_fold, output_network_array_matching, measure_data):
        database = [input_network_array, output_network_array_pp, output_network_array_fold, output_network_array_matching, measure_data]
        self.saveDatabase(database)
        with open('SimStudyDataTemp4.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            # csv_writer.writerow(["NETWORK NUMBER", "V(N)", "A(N)", "L(N)", "isBinary", "isTreeBased",
            #                      "V(PN)", "A(PN)", "L(PN)", "isBinary", "isTreeBased",
            #                      "V(FN)", "A(FN)", "L(FN)", "isBinary", "isTreeBased",
            #                      "Measure1 FOLD", "Measure1 PP", "Measure2 FOLD", "Measure2 PP",
            #                      "Measure3 FOLD", "Measure3 PP", "RV Input", "RV PN", "RV FN",
            #                      "PL Input", "PL PN", "PL FN"])
            csv_writer.writerow(["NETWORK NUMBER", "V(N)", "A(N)", "L(N)", "isBinary", "isTreeBased",
                                 "V(PN)", "A(PN)", "L(PN)", "isBinary", "isTreeBased",
                                 "V(FN)", "A(FN)", "L(FN)", "isBinary", "isTreeBased",
                                 "V(MN)", "A(MN)", "L(MN)", "isBinary", "isTreeBased",
                                 "Measure1 FOLD", "Measure1 PP", "Measure1 Matching", "RV Input", "RV PN", "RV FN",
                                 "TV Input", "TV PN", "TV FN",
                                 "PL Input", "PL PN", "PL FN",
                                 "HN Input", "HN PN", "HN FN",
                                 "FOLD TIME", "PP TIME"])
            for i in range(len(input_network_array)):
                # if len(output_network_array_fold[i].getAllLeafs()) != len(input_network_array[i].getAllLeafs()):
                #     print("INPUT NETWORK VERTICES")
                #     print(input_network_array[i].vertices)
                #     print("INPUT NETWORK ARCS")
                #     print(input_network_array[i].getAllArcs())
                #     input_network_array[i].displayGraph()
                #     time.sleep(2)
                #     output_network_array_fold[i].displayGraph()
                #     break
                line = []
                line.append(i) # NETWORK NUM
                line.append(len(input_network_array[i].vertices)) # NUMBER OF VERTICES IN NETWORK
                line.append(len(self.getAllArcsFromNetwork(input_network_array[i]))) # NUMBER OF ARCS IN NETWORK
                line.append(len(input_network_array[i].getAllLeafs())) # AMOUNT OF LEAVES IN NETWORK
                isBinaryInput = input_network_array[i].isBinary()
                line.append(isBinaryInput) # IF INPUT NETWORK IS BINARY
                if isBinaryInput:
                    line.append(input_network_array[i].checkTreeBasedNonBinary2()) # IF INPUT NETWORK IS TREEBASED
                else:
                    line.append(input_network_array[i].checkTreeBasedNonBinary2()) # IF OUTPUT NETWORK IS TREEBASED
                line.append(len(output_network_array_pp[i].vertices))  # NUMBER OF VERTICES IN NETWORK
                line.append(len(self.getAllArcsFromNetwork(output_network_array_pp[i])))  # NUMBER OF ARCS IN NETWORK
                line.append(len(output_network_array_pp[i].getAllLeafs()))  # AMOUNT OF LEAVES IN NETWORK
                isBinaryInput = output_network_array_pp[i].isBinary()
                line.append(isBinaryInput)  # IF INPUT NETWORK IS BINARY
                if isBinaryInput:
                    line.append(output_network_array_pp[i].checkTreeBasedBinary())  # IF OUTPUT NETWORK IS TREEBASED
                else:
                    line.append(output_network_array_pp[i].checkTreeBasedNonBinary2())  # IF OUTPUT NETWORK IS TREEBASED
                line.append(len(output_network_array_fold[i].vertices))  # NUMBER OF VERTICES IN NETWORK
                line.append(len(self.getAllArcsFromNetwork(output_network_array_fold[i])))  # NUMBER OF ARCS IN NETWORK
                line.append(len(output_network_array_fold[i].getAllLeafs()))  # AMOUNT OF LEAVES IN NETWORK
                isBinaryInput = output_network_array_fold[i].isBinary()
                line.append(isBinaryInput)  # IF INPUT NETWORK IS BINARY
                if isBinaryInput:
                    line.append(output_network_array_fold[i].checkTreeBasedBinary())  # IF OUTPUT NETWORK IS TREEBASED
                else:
                    line.append(output_network_array_fold[i].checkTreeBasedNonBinary2())  # IF OUTPUT NETWORK IS TREEBASED
                line.append(len(output_network_array_matching[i].vertices))
                line.append(len(self.getAllArcsFromNetwork(output_network_array_matching[i])))
                line.append(len(output_network_array_matching[i].getAllLeafs()))
                line.append(output_network_array_matching[i].isBinary())
                line.append(output_network_array_matching[i].checkTreeBasedNonBinary2())
                line.append(measure_data[0][i][0]) # MEASURE 1 FOLD NETWORK
                line.append(measure_data[0][i][1]) # MEASURE 1 PP NETWORK
                line.append(measure_data[0][i][2]) # MEASURE 1 MATCHING NETWORK
                # line.append(measure_data[1][i][0]) # MEASURE 2 FOLD NETWORK
                # line.append(measure_data[1][i][1]) # MEASURE 2 PP NETWORK
                # line.append(measure_data[2][i][0]) # MEASURE 3 FOLD NETWORK
                # line.append(measure_data[2][i][1]) # MEASURE 3 PP NETWORK
                line.append(len(input_network_array[i].getReticulationVertices()))
                line.append(len(output_network_array_pp[i].getReticulationVertices()))
                line.append(len(output_network_array_fold[i].getReticulationVertices()))
                line.append(len(input_network_array[i].getTreeVertices()))
                line.append(len(output_network_array_pp[i].getTreeVertices()))
                line.append(len(output_network_array_fold[i].getTreeVertices()))
                line.append(str(input_network_array[i].getPloidyLevels()[1]))
                line.append(str(output_network_array_pp[i].getPloidyLevels()[1]))
                line.append(str(output_network_array_fold[i].getPloidyLevels()[1]))
                line.append(hybrid_number_measure(input_network_array[i]))
                line.append(hybrid_number_measure(output_network_array_pp[i]))
                line.append(hybrid_number_measure(output_network_array_fold[i]))
                line.append(measure_data[3][i][0]) #FOLDING TIMING DATA
                line.append(measure_data[3][i][1]) # PLOYPLOIDY TIMING DATA
                # line.append(measure_data[3][i][0]) # MEASURE 4 FOLD NETWORK
                # line.append(measure_data[3][i][1]) # MEASURE 4 PP NETWORK
                # if len(input_network_array[i].getAllLeafs()) != len(output_network_array_fold[i].getAllLeafs()):
                #     print("ENEWICK OF BROKEN NETwORK")
                #     print(self.networkToENewickLine(input_network_array[i]))
                if not output_network_array_matching[i].checkTreeBasedNonBinary2():
                    print("ENEWICK OF BROKEN NETWORK")
                    print(self.networkToENewickLine(input_network_array[i]))
                    print(self.networkToENewickLine(output_network_array_matching[i]))
                    print(input_network_array[i].vertices)
                    print(input_network_array[i].getAllArcs())
                    print(input_network_array[i].root)
                csv_writer.writerow(line)
            print("SAVED DATA TO SimStudyDava.csv")


    def networkToENewickLine(self, network):
        """

        :type network: PhylogeneticNetwork
        """

        # network.displayGraph()

        if 0 in network.vertices:
            network.vertices.remove(0)

        label_array = []
        for key, value in network.taxDict.items():
            tup = (int(key), value)
            label_array.append(tup)

        # arc_array = []
        # for arc in network.getAllArcs():
        #     temp_arc = (arc[0], arc[1])
        #     arc_array.append(temp_arc)

        leaf_set = network.getAllLeafs()

        phyx_network = phylox.DiNetwork(labels=label_array)
        for vertex in network.vertices:
            # if vertex in leaf_set:
            #     phyx_network.add_node(vertex, label=str(network.taxDict[vertex]))
            # else:
            phyx_network.add_node(vertex)
        for arc in network.getAllArcs():
            phyx_network.add_edge(arc[0], arc[1])

        # for key, value in network.taxDict.items():
        #     phyx_network.nodes[key]["label"] = str(value)
        #     # phyx_network.nodes[key][LABEL_ATTR] = str(value)
        #     # phyx_network.labels[key] = value

        # print(phyx_network.labels)

        output_line = dinetwork_to_extended_newick(phyx_network)

        return output_line

    def readENewickLine(self, line):
        temp_network = extended_newick_to_dinetwork(line)

        # print(temp_network.labels)

        vertex_list = []
        vertex_dict = {}
        i = 1
        for node in temp_network.nodes:
            vertex_list.append(i)
            vertex_dict[str(node)] = str(i)
            i = i + 1

        # for i in range(len(temp_network.nodes)):
        #     vertex_list.append(i+1)
        #     print(temp_network.nodes)
        #     vertex_dict[temp_network.nodes[i]] = str(i + 1)


        arc_list = []
        for arc in temp_network.edges:
            arc_0 = vertex_dict.get(str(arc[0]))
            arc_1 = vertex_dict.get(str(arc[1]))
            arc_list.append([int(arc_0), int(arc_1)])


        reverse_labels = {}
        for key, value in temp_network.labels.items():
            reverse_labels[value[0]] = key


        tax_dict = {}

        for key, value in reverse_labels.items():
            if key in temp_network.leaves:
                converted_key = vertex_dict.get(str(key))
                tax_dict[converted_key] = value


        finished_network = PhylogeneticNetwork(vertex_list, arc_list, 1, tax_dict)

        return finished_network



