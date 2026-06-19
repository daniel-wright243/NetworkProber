import networkx

class SoftlyTreeBasedAlgorithm:

    def __init__(self, network):
        self.PhyloNetwork = network

    def startAlgorithm(self):
        #GET PLOIDY PROFILE OF NETWORK
        ploidy_index, ploidy_profile = self.getInitialPloidyProfile()
        ## print("PLOIDY PROFILE")
        ## print(ploidy_profile)
        # CHECK IF ANY VALUE IS ABOVE 4 IN THE PLOIDY PROFILE
        for level in ploidy_profile:
            if level > 4:
                return False
        return True

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

    def FindAllPaths(self):
        networkXGraph = networkx.DiGraph()
        for vertex in self.PhyloNetwork.vertices:
            networkXGraph.add_node(vertex)
        for vertex in self.PhyloNetwork.arcs:
            for arc in vertex:
                networkXGraph.add_edge(arc[0], arc[1])
        # makes networkx graph
        leafs = []
        for i in range(len(self.PhyloNetwork.arcs)):
            if len(self.PhyloNetwork.arcs[i]) == 0 and len(self.PhyloNetwork.reverseArcs[i]) > 0:
                leafs.append(i)
        ## print("Leafs from FindAllPaths2")
        ## print(leafs)
        path_list = []
        for leaf in leafs:
            networkx_path_list = networkx.all_simple_paths(networkXGraph, 1, leaf)
            for path in networkx_path_list:
                path_list.append(path)
        ## print(path_list)
        return path_list

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

