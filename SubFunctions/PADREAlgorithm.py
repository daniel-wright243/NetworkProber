from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork

class PADREAlgorithm:


    def __init__(self, network):
        self.isomorpthismCodeArray = [[] for _ in range(max(network.vertices))]
        self.network = network


    def runAlgorithm(self):
        """

        :type network: PhylogeneticNetwork
        """

        var3 = True

        if self.network.root == None:
            return None

        var4 = []
        self.computeIsomorpthismCode(self.network.root)


    def computeIsomorpthismCode(self, vertex):
        if self.isLeaf(vertex):
            isomorphismCode = []
            isomorphismCode[0] = vertex
        else:
            var1 = []
            var2 = 1

            var3 = 0
            for i in range(var3, self.getOutDegree(vertex), 1):
                var4 = self.getChildVertexAt(vertex, i)
                var1.append(var4)
                self.isomorpthismCodeArray[var4] = self.computeIsomorpthismCode(var4)
                var2 = var2 + len(self.isomorpthismCodeArray[var4])

            isomorphismCode = []
            var10 = 1
            isomorphismCode.append(str(var2))

            while len(var1) != 0:
                var11 = var1[0]
                var5 = self.isomorpthismCodeArray[var11]

                var6 = 1
                for i in range(var6, len(var1), 1):
                    var7 = var1[i]
                    var8 = self.isomorpthismCodeArray[var7]
                    if len(var8) < len(var5):
                        var11 = var7
                        var5 = var8
                    elif len(var8) == len(var5):
                        var9 = 0
                        for j in range(var9, len(var8), 1):
                            if var8[j] > var5[j]:
                                var11 = var7
                                var5 = var8
                                j = len(var8)

                var12 = 0
                for i in range(var12, len(var5), 1):
                    self.isomorpthismCodeArray[var10 + 1] = var5[i]

                var1.remove(var11)


    def isLeaf(self, vertex):
        input_arcs = len(self.network.reverseArcs[vertex])
        output_arcs = len(self.network.arcs[vertex])

        if input_arcs == 1 and output_arcs == 0:
            return True
        else:
            return False

    def getOutDegree(self, vertex):
        return len(self.network.arcs[vertex])

    def getChildVertexAt(self, vertex, var1):
        vertices_above = []

        for arc in self.network.reverseArcs[vertex]:
            vertices_above.append(arc[1])

        if len(vertices_above) >= var1:
            return vertices_above[var1]
        else:
            return None


