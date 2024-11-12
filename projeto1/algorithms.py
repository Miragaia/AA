from itertools import combinations
from functools import lru_cache

def precompute_edge_dict(G):
    edge_dict = {node: set(G.edges(node)) for node in G.nodes}
    return edge_dict

def is_edge_dominating_set(edge_dict, edge_set, all_edges):
    covered_edges = set()

    for u, v, _ in edge_set:
        covered_edges |= edge_dict[u]
        covered_edges |= edge_dict[v]

    return len(covered_edges) == all_edges

def exhaustive_search_mweds(G):
    min_weight = float('inf')
    min_weight_set = []
    
    edges = list(G.edges(data=True))  # Includes edge weights
    all_edges = G.number_of_edges()
    edge_dict = precompute_edge_dict(G)

    for r in range(1, all_edges + 1):
        for edge_subset in combinations(edges, r):
            if is_edge_dominating_set(edge_dict, edge_subset, all_edges):
                weight = sum(w['weight'] for u, v, w in edge_subset)
                if weight < min_weight:
                    min_weight = weight
                    min_weight_set = edge_subset

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
