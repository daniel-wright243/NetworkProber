import ast
import math
import subprocess
import time
from copy import deepcopy

import graphviz
import networkx

from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.MultiLabelledGraph import MultiLabelledGraph


class FoldingAlgorithm:

    def __init__(self, network):
        """

        Parameters
        ----------
        network : PhylogeneticNetwork
        """
        self.network = network
        self.networkXGraph = networkx.DiGraph()
        for vertex in self.network.vertices:
            self.networkXGraph.add_node(vertex)
        for vertex in self.network.arcs:
            for arc in vertex:
                self.networkXGraph.add_edge(arc[0], arc[1])

    def runAlgorithm(self):

        #self.network.displayGraph()

        connected_components = self.network.getConnectedComponentOfGraphFromBPGraph()
        # print("CONNECTED COMPONENTS")
        # print(connected_components)

        connected_components_extended = connected_components

        # for item in connected_components:
        #     if type(item) == list:
        #         for vertex in item:
        #             for arc in self.network.reverseArcs[vertex]:
        #                 print(self.network.reverseArcs[vertex])
        #                 item.append(arc[1])

        for i in range(len(connected_components)):
            for j in range(len(connected_components[i])):
                for arc in self.network.reverseArcs[connected_components[i][j]]:
                    if arc[1] not in connected_components_extended[i]:
                        connected_components_extended[i].append(arc[1])
        # print("CONNECTED COMPONENTS EXTENDED")
        # print(connected_components_extended)

        cc_networks = []
        cc_before_networks = []
        #CHECK IF COMPONENTS ARE CONNECTED
        connected_sets = []
        connected_folded_networks = []
        reattached_network = self.network
        # print("CONNECTED COMPONENTS")
        # print(connected_components)
        for cc1 in connected_components_extended:
            for cc2 in connected_components_extended:
                if cc1 is not cc2:
                    connected = any(networkx.has_path(self.networkXGraph, u, v) for u in cc1 for v in cc2)
                    if connected:
                        connected_sets.append([cc1, cc2])
        # print("CONNECTED SET")
        # print(connected_sets)

        # for set in connected_sets:
        #     temp_set = []
        #     for i in range(len(set)):
        #         print("SET[I}")
        #         print(set)
        #         print(i)
        #         print(set[i])
        #         print("CONNECTED COMPONENTS")
        #         print(connected_components)
        #         if set[i] in connected_components:
        #             connected_components.remove(set[i])
        #             temp_set.append(set[i])
        #     #connected_components.remove(set[0])
        #     #connected_components.remove(set[1])
        #     if len(temp_set) > 0:
        #         connected_components.append(temp_set)
        #     #connected_components.append(set[0] + set[1])
        if len(connected_components) == 0:
            connected_network = self.network
        else:
            for component in connected_components:
                # print("CONNECTED COMPONENT")
                # print(component)
                connected_network = self.getNetworkConnectedToConnectedComponent(component)
                cc_before_networks.append(connected_network)
        #cc_before_networks[0].displayGraph()
        # for component in cc_before_networks:
        #     reattached_network = self.removeComponentFromNetwork(component, reattached_network)
        #     #reattached_network.displayGraph()
        #     cc_networks.append(reattached_network)
        uf_array = []
        f_array = []
        #cc_before_networks[0].displayGraph()
        if len(cc_before_networks) == 0:
            unfolded_network = MultiLabelledGraph(self.network)
            # unfolded_network.displayGraph()
            uf_array.append(unfolded_network)
            unfolded_network.writeToPADREFile()
            # unfolded_network.displayGraph()
            # subprocess.run("java -jar PADRE_Files/PADRE_DECOMPILED.jar PADRE_Files/PADREInputFile.tre PADRE_Files/outputFile.txt")
            subprocess.run("java -jar PADRE_Files/PADRE_DECOMPILED.jar PADRE_Files/PADREInputFile.tre PADRE_Files/outputFile.txt",check=True)
            # time.sleep(1)
            folded_network = self.readFromPADREFile()
            return folded_network
        else:
            # print("CC BEFORE NETWORKS")
            # print(cc_before_networks)
            for network in cc_before_networks:
                none_check = False
                if network == None:
                    unfolded_network = MultiLabelledGraph(self.network)
                    none_check = True
                else:
                    unfolded_network = MultiLabelledGraph(network)
                #unfolded_network.displayGraph()
                uf_array.append(unfolded_network)
                unfolded_network.writeToPADREFile()
                #unfolded_network.displayGraph()
                #subprocess.run("java -jar PADRE_Files/PADRE_DECOMPILED.jar PADRE_Files/PADREInputFile.tre PADRE_Files/outputFile.txt")
                subprocess.run("java -jar PADRE_Files/PADRE_DECOMPILED.jar PADRE_Files/PADREInputFile.tre PADRE_Files/outputFile.txt", check=True)
                #time.sleep(1)
                folded_network = self.readFromPADREFile()
                f_array.append(folded_network)
                if none_check:
                    break
                #folded_network.displayGraph()
                reattached_network = self.reattachNetwork(folded_network, network.root, reattached_network)
        #uf_array[0].displayGraph()
        #f_array[0].displayGraph()


        #for vertex in reattached_network.vertices:
        #    if [vertex, vertex] in reattached_network.arcs[vertex]:
        #        reattached_network.arcs[vertex].remove([vertex, vertex])
        #reattached_network.displayGraph()

    def reattachNetwork(self, component, vertex, network):
        """

        Parameters
        ----------
        network : PhylogeneticNetwork
        component : PhylogeneticNetwork
        """
        vertex_dict = {}
        vertex_list = []
        edge_list = []
        vertex_max = max(network.vertices)
        print("VERTEX MAX")
        print(vertex_max)
        for i in range(len(component.vertices)):
            #vertex_max[vertex_max + 1] = component.vertices[i]
            vertex_dict[component.vertices[i]] = vertex_max + 1
            vertex_list.append(vertex_max + 1)
        for vertex in component.arcs:
            for arc in vertex:
                edge_tail = vertex_dict[arc[0]]
                edge_head = vertex_dict[arc[1]]
                edge_list.append([edge_tail, edge_head])
        for vertex in vertex_list:
            network.vertices.append(vertex)
        for edge in edge_list:
            if edge not in network.arcs[edge[0]]:
                network.createArc(edge)
        print("VERTEX MAX AFTER")
        print(vertex_max)

        return network

    def removeComponentFromNetwork(self, component, network):
        """

        Parameters
        ----------
        network : PhylogeneticNetwork
        component : PhylogeneticNetwork
        """

        if component.root != network.root:
            for vertex in component.vertices:
                if vertex in network.vertices:
                    network.vertices.remove(vertex)
                    network.arcs[vertex] = []
                    network.reverseArcs[vertex] = []

        return network


    def readFromPADREFile(self):
        file = open("PADRE_Files\\outputFile.txt", "r")
        lines = file.readlines()
        # leafs = lines[2]
        edges = lines[1]
        vertices = lines[0]
        # edges = edges.rsplit(',', 1)[0]
        # edges = edges + "]"
        edge_list = ast.literal_eval(edges)
        vertex_list = ast.literal_eval(vertices)
        # leaf_list = ast.literal_eval(leafs)

        ## print("EDGE LIST")
        ## print(edge_list)

        ## print("VERTEX LIST")
        ## print(vertex_list)

        # print("LEAF LIST")
        # print(leaf_list)

        # for vertex in vertex_list:
        #     if str(vertex) not in edges:
        #         vertex_list.remove(vertex)

        phy_network = PhylogeneticNetwork(vertex_list, edge_list, 0)

        # self.new_display_graph(phy_network.simplifyNetwork(), leaf_list)

        already_swapped_list = []

        # for leaf in leaf_list:
        #     old_index = leaf[0]
        #     new_index = leaf[1]

            # if old_index not in already_swapped_list:
            #     for arc in phy_network.arcs[old_index]:
            #

        # for vertex in phy_network.vertices:
        #     if len(phy_network.arcs[vertex]) == 0 and len(phy_network.reverseArcs[vertex]) == 0:
        #         phy_network.vertices.remove(vertex)
        #     elif vertex is not phy_network.root and len(phy_network.reverseArcs[vertex]) == 0:
        #         phy_network.vertices.remove(vertex)
        #         phy_network.arcs[vertex] = []

        ## print("VERTICES")
        ## print(phy_network.vertices)
        ## print("EDGES")
        ## print(phy_network.arcs)
        ## print("REVERSE EDGES")
        ## print(phy_network.reverseArcs)
        #phy_network.displayGraph()

        return phy_network

    def getNetworkConnectedToConnectedComponent(self, connected_component):
        flattened_connected_component = []
        for component in connected_component:
            if type(component) == list:
                for vertex in component:
                    flattened_connected_component.append(vertex)
            else:
                flattened_connected_component.append(component)
        ## print("CONNECTED COMPONENT")
        ## print(connected_component)
        networkXGraph = networkx.DiGraph()
        for vertex in self.network.vertices:
            if vertex != None:
                networkXGraph.add_node(vertex)
        for vertex in self.network.arcs:
            for arc in vertex:
                if arc[0] != None and arc[1] != None:
                    networkXGraph.add_edge(arc[0], arc[1])
        ## print("CONNECTED COMPONENT")
        ## print(connected_component)
        #self.network.displayGraph()
        lca = self.lowest_common_ancestor_multiple(networkXGraph, flattened_connected_component)
        if lca == None:
            self.network.getNetworkBelowVertexNetworkX(self.network.root)
        else:
            return self.network.getNetworkBelowVertexNetworkX(lca)

    #GOTTEN FROM COPILOT
    def lowest_common_ancestor_multiple(self, G, nodes):
        if not nodes:
            return None
        lca = nodes[0]
        for node in nodes[1:]:
            lca = networkx.lowest_common_ancestor(G, lca, node)
            if lca is None:
                break
        return lca

    def runAlgorithm2(self):
        N = deepcopy(self.network)
        ## print("NETWORK VERTICES ALGORITHM")
        ## print(self.network.vertices)
        cc = N.getConnectedComponentOfGraphFromBPGraph()
        ## print(cc)
        #N.displayGraph()
        root_connections = [[] for _ in range(len(cc))]

        unfolded_network = MultiLabelledGraph(self.network)
        #unfolded_network.simplifyNetwork().displayGraph()
        unfolded_network.simplifyNetwork().writeToPADREFile()
        #print("UNFOLDED NETWORK MULTIVERTEX")
        #print(unfolded_network.reverseMultiLabelledVertices[26])
        leaf_set = self.getAllLeafs(self.network)
        sp = subprocess.Popen("java -jar PADRE_Files/PADRE_DECOMPILED.jar PADRE_Files/PADREInputFile.tre PADRE_Files/outputFile.txt" + " " + str(leaf_set))
        sp.wait()
        folded_network = self.readFromPADREFile()
        ## print("OUTPUT LEAF COUNT")
        ## print(len(folded_network.getAllLeafs()))
        #folded_network.simplifyNetwork().displayGraph()
        #folded_network.simplifyNetwork().displayGraph()
        #folded_network.displayGraph()

        # for i in range(len(cc)):
        #     connected_network = self.getNetworkConnectedToConnectedComponent(cc[i])
        #     N = self.removeComponentFromNetwork(connected_network, N)
        #     for arc in N.reverseArcs[connected_network.root]:
        #         root_connections[i].append(arc[1])
        #     unfolded_network = MultiLabelledGraph(connected_network)
        #     unfolded_network.writeToPADREFile()
        #     subprocess.run("java -jar PADRE_Files/PADRE_DECOMPILED.jar PADRE_Files/PADREInputFile.tre PADRE_Files/outputFile.txt", check=True)
        #     folded_network = self.readFromPADREFile()
        #     folded_network.displayGraph()

    def getAllLeafs(self, network):
        """

        :type network: PhylogeneticNetwork
        """
        input_arcs = []
        output_arcs = []
        for i in range(len(network.arcs)):
            output_arcs.append(len(network.arcs[i]))
        for i in range(len(network.reverseArcs)):
            input_arcs.append(len(network.reverseArcs[i]))

        leaf_set = []

        for i in range(len(input_arcs)):
            if input_arcs[i] == 1 and output_arcs[i] == 0:
                leaf_set.append(i)

        return leaf_set

    def new_display_graph(self, network, leaf_list):
        """

        :type network: PhylogeneticNetwork
        """
        label_array = [0 for _ in range(5000)]
        labelDict = {}

        multiLabelledVertices = [[] for _ in range(5000)]

        for leaf in leaf_list:
            multiLabelledVertices[leaf[0]].append(leaf[1])

        dot = graphviz.Digraph('Phylogenetic Network', comment='Phylogenetic Network')
        for i in network.vertices:
            if len(multiLabelledVertices[i]) > 0:
                dot.node(str(i), str(multiLabelledVertices[i][0]))
            else:
                dot.node(str(i))
        for vertex in network.arcs:
            for arc in vertex:
                dot.edge(str(arc[0]), str(arc[1]))
        dot.view()


