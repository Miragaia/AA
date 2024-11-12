from itertools import combinations
from functools import lru_cache
import networkx as nx

def is_edge_dominating_set(G, edge_set):
    for u, v in G.edges:
        if not any((u in (u1, v1) or v in (u1, v1)) for u1, v1, w in edge_set):
            return False
    return True

def exhaustive_search_mweds(G):
    min_weight = float('inf')
    min_weight_set = []
    

    edges = G.edges(data= "weight")
    all_edges = G.number_of_edges()

    for r in range(1, all_edges + 1):
        for edge_subset in combinations(edges, r):
            edge_set = set((u, v, w) for u, v, w in edge_subset)
            if is_edge_dominating_set(G, edge_set):
                weight = sum(w for u, v, w in edge_set)
                if weight < min_weight:
                    min_weight = weight
                    min_weight_set = edge_set
            else:
                continue
            
    return min_weight_set, min_weight

def greedy_mweds(G):
    edge_list = sorted(G.edges(data='weight'), key=lambda x: x[2])
    dominating_set = []
    covered_edges = set()

    for u, v, weight in edge_list:
        if (u, v) not in covered_edges:
            dominating_set.append((u, v, weight))
            covered_edges.update(G.edges(u))
            covered_edges.update(G.edges(v))

            # Stop once all edges are covered
            if len(covered_edges) >= len(G.edges):
                break

    total_weight = sum(weight for u, v, weight in dominating_set)
    return dominating_set, total_weight

import networkx as nx

def greedy_mweds(G):
    edge_list = sorted(G.edges(data='weight'), key=lambda x: x[2])
    dominating_set = []
    covered_edges = set()

    for u, v, weight in edge_list:
        if (u, v) not in covered_edges:
            dominating_set.append((u, v, weight))
            covered_edges.update(G.edges(u))
            covered_edges.update(G.edges(v))

            if all(any((u in (u1, v1) or v in (u1, v1)) for u1, v1, w in dominating_set) for u, v in G.edges):
                break 

    total_weight = sum(weight for u, v, weight in dominating_set)
    return dominating_set, total_weight
