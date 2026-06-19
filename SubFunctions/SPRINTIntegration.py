import Sprint.SPRINT as SPRINT
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from collections import Counter
from itertools import chain
from itertools import product
from itertools import starmap
from functools import partial
chaini = chain.from_iterable

def runSPRINTImplementation(ploidy_list, species_list, core_choice, leaf_count):
    # print("LEAF COUNT")
    # print(leaf_count)
    species_list = []
    for i in range(1, leaf_count + 2):
        species_list.append(chr(ord('@')+i))
    # print("SPECIES LIST")
    # print(species_list)
    #species_list = ['a', 'b', 'c', 'd', 'e']
    i=1
    tuples = list(zip(species_list, ploidy_list))
    G, tot_hybrids, text_to_write = SPRINT.SPLINTER([int(i[1]) for i in tuples], core_choice)
    species = [i[0] for i in tuples]

    # assign the species taxon to correct vertex by equating the number of paths from root to leaf with
    # the ploidy levels of the species
    leaves = list(v for v, d in G.out_degree() if d == 0)
    roots = (v for v, d in G.in_degree() if d == 0)
    leaves = list(v for v, d in G.out_degree() if d == 0)
    all_paths = partial(nx.all_simple_paths, G)
    leaf_paths = list(chaini(starmap(all_paths, product(roots, leaves))))
    new_list = list([sublist[-1] for sublist in leaf_paths])
    c = Counter(new_list)
    c.most_common()
    count_tuples = list(Counter(c).items())
    remove_dupes = set(item[1] for item in count_tuples)
    distinct_count = [tup for tup in count_tuples if tup[1] in remove_dupes]
    from operator import itemgetter
    def unique_by_key(elements, key=None):
        if key is None:
            # no key: the whole element must be unique
            key = lambda e: e
        return {key(el): el for el in elements}.values()
    distinct_count = list(unique_by_key(count_tuples, key = itemgetter(1)))
    L3 = [(x1, y1) for (x1, x2) in tuples for (y1, y2) in count_tuples if int(x2) == int(y2)]
    # print("L3")
    # print(L3)
    leaf_list = list(dict.fromkeys([i[0] for i in L3]))
    vertex_list = list(dict.fromkeys([i[1] for i in L3]))

    label= {}

    for item in vertex_list:
        pos_leaf = [i for i,x in enumerate(vertex_list) if x == item]
        label[item] = leaf_list[pos_leaf[0]]

    print("LABEL")
    print(label)


    # gives arcs contained in a bead curvature so visible in networkx
    leftbead = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 1.01]
    rightbead = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 5]
    rest = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 1]

    # print("LEFTBEAD")
    # print(leftbead)
    # print("RIGHTBEAD")
    # print(rightbead)
    # print("REST")
    # print(rest)

    return G, label
