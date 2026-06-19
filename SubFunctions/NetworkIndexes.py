import functools
import math
import networkx as nx

from SubFunctions.PhyloGeneticNetwork import PhylogeneticNetwork
from SubFunctions.MultiLabelledGraph import MultiLabelledGraph

# RANDIC INDEX FUNCTION IS GOTTEN FROM GRIMPY https://github.com/somacdivad/grinpy

def GetRandicIndex(network):
    """

    :type network: PhylogeneticNetwork
    """
    networkXGraph = nx.DiGraph()
    for vertex in network.vertices:
        networkXGraph.add_node(vertex)
    for vertex in network.arcs:
        for arc in vertex:
            networkXGraph.add_edge(arc[0], arc[1])
    return randic_index(networkXGraph)

def GetRandicIndexMLG(mlg):
    """

    :type mlg: MultiLabelledGraph
    """

    networkXGraph = nx.DiGraph()
    for vertex in mlg.vertices:
        networkXGraph.add_node(vertex)
    for vertex in mlg.arcs:
        for arc in vertex:
            networkXGraph.add_edge(arc[0], arc[1])
    return randic_index(networkXGraph)

def GetWienerIndex(network):
    """

    :type network: PhylogeneticNetwork
    """
    networkXGraph = nx.DiGraph()
    for vertex in network.vertices:
        networkXGraph.add_node(vertex)
    for vertex in network.arcs:
        for arc in vertex:
            networkXGraph.add_edge(arc[0], arc[1])
    return nx.wiener_index(networkXGraph)



def _topological_index(G, func):
    """Return the topological index of ``G`` determined by ``func``"""

    return math.fsum(func(*edge) for edge in G.edges())

def randic_index(G):
    r"""Returns the Randić Index of the graph ``G``.

    The *Randić index* of a graph *G* with edge set *E* is defined as the
    following sum:

    .. math::
        \sum_{vw \in E} \frac{1}{\sqrt{d_G(v) \times d_G(w)}}

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph.

    Returns
    -------
    float
        The Randić Index of a ``G``.

    References
    ----------

    Ivan Gutman, Degree-Based Topological Indices, Croat. Chem. Acta 86 (4)
    (2013) 351–361. http://dx.doi.org/10.5562/cca2294
    """
    _degree = functools.partial(nx.degree, G)
    return _topological_index(G, func=lambda x, y: 1 / math.sqrt(_degree(x) * _degree(y)))
