import ast
import math
from copy import deepcopy

import graphviz
import networkx
from TreeSpotter.DAG import DAG
# import TreeSpotter.DAG as DAG
import TreeSpotter.BiPartiteGraph as BiPartiteGraph

from PIL import ImageTk, Image

from SubFunctions import SPRINTIntegration


class PolyPloidy:
    def __init__(self, PhyloNetwork):
        """

        Parameters
        ----------
        PhyloNetwork : DAG
        """
        self.PhyloNetwork = PhyloNetwork

    def startAlgorithm(self, max_vertex, main_network):
        N = self.PhyloNetwork
        # N.simplifyNetwork()
        # N.displayGraph()
        GN = N.make_bipartite_graph()
        GN.hopcroftkarp()
        NPrime = deepcopy(N)
        # PloidyIndex, PloidyProfile = self.getInitialPloidyProfile()
        PloidyProfile, PloidyIndex = self.getPloidyProfile(NPrime)
        # print("PLOIDY INDEX")
        # print(PloidyIndex)
        # print("PLOIDY PROFILE")
        # print(PloidyProfile)
        # print("PLOIDY PROFILE")
        # print(PloidyProfile)
        # print("PLOIDY INDEX")
        # print(PloidyIndex)
        NPrimeLeafs = NPrime.get_all_leaves()
        G, labels = SPRINTIntegration.runSPRINTImplementation(PloidyProfile, PloidyIndex, 'binary', len(NPrimeLeafs))
        # print("G")
        # print(G)
        # print(G.nodes)
        new_tax_dict = {}
        for key in labels.keys():
            value = labels[key]
            recovered_i = ord(value) - ord('@')
            # print("RECOVERED I")
            # print(recovered_i)
            # print("TAX DICT")
            # print(N.taxDict)
            if PloidyIndex[recovered_i - 1] in N.taxa.keys():
                old_index = N.taxa[PloidyIndex[recovered_i - 1]]
                new_tax_dict[key] = old_index
        # print(new_tax_dict)
        # edge_string = str(G.edges)
        #
        # edge_string = edge_string.replace('(', '[')
        # edge_string = edge_string.replace(')', ']')
        #
        # edge_list = ast.literal_eval(edge_string)
        #
        # trimmed_edge_list = []
        #
        # for edge in edge_list:
        #     trimmed_edge_list.append([edge[0], edge[1]])
        #
        # vertex_list = G.nodes

        ploidyNetwork = networkx.to_dict_of_lists(G)
        vertex_list = []
        edge_list = []
        for vertex in ploidyNetwork:
            vertex_list.append(vertex)
            for item in ploidyNetwork[vertex]:
                edge_list.append([vertex, item])
        root = 0
        PloidyNetwork = DAG(vertex_list, edge_list, new_tax_dict, root)
        # PloidyNetwork.display_graph()
        temp_network = deepcopy(PloidyNetwork)

        for vertex in PloidyNetwork.vertices:
            # PloidyNetwork.convertVertex(vertex, max_vertex + 1)
            temp_network = self.convertVertex(temp_network, vertex, max_vertex + 1, main_network)
            max_vertex = max_vertex + 1

        # temp_network.display_graph()

        # print("TAXDICT")
        # print(temp_network.taxa)

        return temp_network


    # def startAlgorithm(self):
    #     N = self.PhyloNetwork
    #     NPrime = deepcopy(N)
    #     networkXGraph = networkx.Graph()
    #     for vertex in NPrime.vertices:
    #         networkXGraph.add_node(vertex)
    #     for vertex in NPrime.arcs:
    #         for arc in vertex:
    #             networkXGraph.add_edge(arc[0], arc[1])
    #     cycles = networkx.cycle_basis(networkXGraph, NPrime.root)
    #     if len(cycles) > 0:
    #         PloidyIndex, PloidyProfile = self.getInitialPloidyProfile()
    #         NPrimeLeafs = NPrime.getAllLeafs()
    #         G = SPRINTIntegration.runSPRINTImplementation(PloidyProfile, PloidyIndex, 'binary', len(NPrimeLeafs))
    #         ploidyNetwork = networkx.to_dict_of_lists(G)
    #         vertex_list = []
    #         edge_list = []
    #         for vertex in ploidyNetwork:
    #             vertex_list.append(vertex)
    #             for item in ploidyNetwork[vertex]:
    #                 edge_list.append([vertex, item])
    #         root = min(vertex_list)
    #         PloidyNetwork = PhylogeneticNetwork(vertex_list, edge_list, root)
    #         return PloidyNetwork
    #     else:
    #         return NPrime



    def FindAllPaths(self):
        networkXGraph = networkx.DiGraph()
        for key, value in self.PhyloNetwork.vertex_dict.items():
            networkXGraph.add_node(key)
            for arc in value["arcs"]:
                networkXGraph.add_edge(arc[0], arc[1])
        # for vertex in self.PhyloNetwork.vertices:
        #     networkXGraph.add_node(vertex)
        # for vertex in self.PhyloNetwork.arcs:
        #     for arc in vertex:
        #         networkXGraph.add_edge(arc[0], arc[1])
        # makes networkx graph
        leafs = []
        leafs = self.PhyloNetwork.get_all_leaves()
        # for i in range(len(self.PhyloNetwork.arcs)):
        #     if len(self.PhyloNetwork.arcs[i]) == 0 and len(self.PhyloNetwork.reverseArcs[i]) > 0:
        #         leafs.append(i)
        # print("Leafs from FindAllPaths2")
        # print(leafs)
        path_list = []
        for leaf in leafs:
            networkx_path_list = networkx.all_simple_paths(networkXGraph, self.PhyloNetwork.root, leaf)
            for path in networkx_path_list:
                path_list.append(path)
        # print(path_list)
        return path_list

    def getInitialPloidyProfile(self):
        PloidyCounter = []
        paths = self.FindAllPaths()
        for path in paths:
            PloidyCounter.append(path[len(path) - 1])
        PloidyIndex = []
        PloidyProfile = []
        highest_number = 0
        highest_number_index = 0
        for counter in PloidyCounter:
            if counter not in PloidyIndex:
                PloidyIndex.append(counter)
                PloidyProfile.append(1)
            else:
                index = PloidyIndex.index(counter)
                PloidyProfile[index] = PloidyProfile[index] + 1
        self.bubbleSort(PloidyProfile, PloidyIndex)
        return PloidyIndex, PloidyProfile

    def getSimplificationSequence(self, PloidyIndex, PloidyProfile):
        PloidyAlphaList = []
        repeat = True
        #iteration of simplification
        while repeat == True:
            ## print(PloidyProfile)
            m1 = PloidyProfile[0]
            m2 = PloidyProfile[1]

            #terminating sequences
            first_check = True
            current_value = m1
            for item in PloidyProfile:
                if item != current_value:
                    first_check = False
                    break
            if first_check:
                return PloidyProfile, PloidyIndex, PloidyAlphaList

            second_check = True
            for i in range(len(PloidyProfile) - 1):
                if PloidyProfile[i + 1] != 1:
                    second_check = False
            if second_check:
                return PloidyProfile, PloidyIndex, PloidyAlphaList

            #iteration sequence
            alpha = m1 - m2
            if alpha > m2:
                PloidyProfile[0] = alpha
                PloidyIndex[0] = [PloidyIndex[0], PloidyIndex[1]]
                PloidyProfile[1] = 0
                self.bubbleSort(PloidyProfile, PloidyIndex)
                index_of_0 = PloidyProfile.index(0)
                PloidyIndex.pop(index_of_0)
                PloidyProfile.pop(index_of_0)
            elif alpha <= m2:
                PloidyProfile[0] = 0
                PloidyIndex[1] = [PloidyIndex[0], PloidyIndex[1]]
                self.bubbleSort(PloidyProfile, PloidyIndex)
                index_of_0 = PloidyProfile.index(0)
                PloidyIndex.pop(index_of_0)
                PloidyProfile.pop(index_of_0)
            elif alpha == 0:
                PloidyProfile[0] = m2
                PloidyIndex[0] = [PloidyIndex[0], PloidyIndex[1]]
                PloidyProfile[1] = 0
                self.bubbleSort(PloidyProfile, PloidyIndex)
                index_of_0 = PloidyProfile.index(0)
                PloidyIndex.pop(index_of_0)
                PloidyProfile.pop(index_of_0)
            PloidyAlphaList.append(alpha)

    def generateNetwork(self, terminal_element):
        #equation log2(max value of terminal element) and round down to find amount of ploidy elements we need
        amount_of_ploidy_required = math.floor(math.log(max(terminal_element), 2))
        vertices_list = []
        for i in range((amount_of_ploidy_required * 4) + len(terminal_element)):
            vertices_list.append(i+1)
        generatedNetwork = DAG(vertices_list, [], {}, 1)

        amount_of_leaves = 0

        # generate ploidy elements
        for i in range(amount_of_ploidy_required):
            ## print("i")
            ## print(i)
            start = (4*(i)+1)
            ## print("Start")
            ## print(start)
            generatedNetwork.add_arc([start, start+1])
            generatedNetwork.add_arc([start, start+2])
            generatedNetwork.add_arc([start+1, start+3])
            generatedNetwork.add_arc([start+2, start+3])

            #add arcs from simplification matrix to generatedNetwork

            for item in terminal_element:
                ## print("Terminal element loop")
                ## print(item)
                ## print(pow(2, i+1))
                ## print(pow(2, i))

                if pow(2, i+1) > item >= pow(2, i):
                    ## print("Top Argument")
                    ## print("Making arc")
                    ## print([start+1, (amount_of_ploidy_required * 4) + amount_of_leaves + 1])
                    if len(generatedNetwork.vertex_dict[start+1]["arcs"]) == 2:
                    # if len(generatedNetwork.arcs[start+1]) == 2:
                        generatedNetwork.add_arc([start+2, (amount_of_ploidy_required * 4) + amount_of_leaves + 1])
                    elif len(generatedNetwork.vertex_dict[start+1]["arcs"]) == 1:
                    # elif len(generatedNetwork.arcs[start+1]) == 1:
                        generatedNetwork.add_arc([start+1, (amount_of_ploidy_required * 4) + amount_of_leaves + 1])

                    amount_of_leaves = amount_of_leaves + 1
                elif item == pow(2, i+1):
                    ## print("Bottom Argument")
                    ## print("Making arc")
                    ## print([start+3, (amount_of_ploidy_required * 4) + amount_of_leaves + 1])
                    generatedNetwork.add_arc([start+3, (amount_of_ploidy_required * 4) + amount_of_leaves + 1])
                    amount_of_leaves = amount_of_leaves + 1

        #generatedNetwork.displayGraph()
        return generatedNetwork

    def createNetworkFromSimplificationSequence(self, simplification_sequence, PloidyIndex, PloidyAlphaList):
        generatedNetwork = self.generateNetwork(simplification_sequence)
        ## print("PloidyIndex")
        ## print(PloidyIndex)
        ## print("Simplification sequence")
        ## print(simplification_sequence)
        ## print("PloidyAlphaList")
        ## print(PloidyAlphaList)
        reversed_ploidy_alpha_list = PloidyAlphaList[::-1]
        ## print("Reversed list")
        ## print(reversed_ploidy_alpha_list)

        for alpha in reversed_ploidy_alpha_list:
            x1Prime = simplification_sequence[0]
            ## print("x1Prime")
            ## print(x1Prime)
            x2Prime = simplification_sequence[1]
            ## print("x2Prime")
            ## print(x2Prime)
            x1PrimeIndex = PloidyIndex[0]
            ## print("x1PrimeIndex")
            ## print(x1PrimeIndex)
            x2PrimeIndex = PloidyIndex[1]
            ## print("x2PrimeIndex")
            ## print(x2PrimeIndex)
            #if alpha == 0:
                #get edge connected to x1Prime
                #x1PrimeEdge = generatedNetwork.reverseArcs(x1Prime)

            #elif alpha > simplification_sequence[1]:


    def bubbleSort(self, arr, arr2): # bubble sort from https://www.geeksforgeeks.org/sorting-algorithms-in-python/
        # with modification for both arrays to be changed instead of one
        n = len(arr)

        # For loop to traverse through all
        # element in an array
        for i in range(n):
            for j in range(0, n - i - 1):

                # Range of the array is from 0 to n-i-1
                # Swap the elements if the element found
                # is greater than the adjacent element
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    arr2[j], arr2[j + 1] = arr2[j + 1], arr2[j]

    def convertVertex(self, network, vertex1, vertex2, main_network):
        """

        :type network: DAG
        """
        #AIM TO CONVERT VERTEX 1 INDEX TO VERTEX 2 INDEX
        network.add_vertex(vertex2)
        #GET ALL ARCS GOING AWAY FROM VERTEX 1
        outgoing_arcs = []
        for arc in network.vertex_dict[vertex1]["arcs"]:
        # for arc in network.arcs[vertex1]:
            outgoing_arcs.append(arc)
        incoming_arcs = []
        for arc in network.vertex_dict[vertex1]["reverseArcs"]:
        # for arc in network.reverseArcs[vertex1]:
            incoming_arcs.append(arc)

        for arc in outgoing_arcs:
            network.add_arc([vertex2, arc[1]])

        for reverse_arc in incoming_arcs:
            network.add_arc([reverse_arc[1], vertex2])

        for arc in outgoing_arcs:
            network.remove_arc(arc)

        for reverse_arc in incoming_arcs:
            network.remove_arc([reverse_arc[1], reverse_arc[0]])

        if vertex1 == network.root:
            network.root = vertex2

        network.vertices.remove(vertex1)

        if vertex1 in network.taxa.keys():
            value = network.taxa.get(vertex1)
            network.taxa[vertex2] = value
            network.taxa.pop(vertex1)

        # taxDict_remove = []
        # taxDict_add = []
        #
        # if str(vertex1) in main_network.taxDict.keys():
        #     print("GOT INTO LOOP")
        #     value = main_network.taxDict.get(vertex1)
        #     taxDict_remove.append([vertex1, value])
        #     taxDict_add.append([vertex2, value])

        # print("VERTEX 1")
        # print(vertex1)
        # print("VERTEX 2")
        # print(vertex2)

        # print(main_network.taxDict)
        # for key in main_network.taxDict.keys():
        #     print(key)
        # for value in main_network.taxDict.values():
        #     print(value)



        return network

    def getPloidyProfile(self, network):
        """

        :type network: DAG
        """

        all_paths = network.get_all_paths()

        ploidy_profile = []
        ploidy_index = []

        for path in all_paths:
            print(path)
            end_vertex = path[len(path) - 1]
            if end_vertex not in ploidy_index:
                ploidy_index.append(end_vertex)
                ploidy_profile.append(1)
            else:
                index = ploidy_index.index(end_vertex)
                ploidy_profile[index] = ploidy_profile[index] + 1

        self.bubbleSort(ploidy_profile, ploidy_index)

        return ploidy_profile, ploidy_index


