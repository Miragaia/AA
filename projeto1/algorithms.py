from itertools import combinations

def is_edge_dominating_set(G, edge_set):
    covered_edges = set(edge_set)
    for u, v in edge_set:
        covered_edges.update(G.edges(u))
        covered_edges.update(G.edges(v))
    return len(covered_edges) == len(G.edges)

def exhaustive_search_mweds(G):
    min_weight = float('inf')
    min_weight_set = None

    edges = list(G.edges(data='weight'))
    for r in range(1, len(edges) + 1):
        for edge_subset in combinations(edges, r):
            if is_edge_dominating_set(G, [(u, v) for u, v, w in edge_subset]):
                weight = sum(w for u, v, w in edge_subset)
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

            if len(covered_edges) >= len(G.edges):
                break

    total_weight = sum(weight for u, v, weight in dominating_set)
    return dominating_set, total_weight
