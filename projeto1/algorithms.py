from itertools import combinations

def is_edge_dominating_set(G, edge_set):
    covered_edges = set(edge_set)
    for u, v in edge_set:
        covered_edges.update(G.edges(u))
        covered_edges.update(G.edges(v))
    return len(covered_edges) == len(G.edges)


def is_edge_dominating_set_optimized(G, edge_set, all_edges):
    # Create a set to track covered edges
    covered_edges = set(edge_set)
    for u, v in edge_set:
        covered_edges.update(G.edges(u))
        covered_edges.update(G.edges(v))
        if len(covered_edges) == all_edges:
            return True
    return False

def exhaustive_search_mweds(G):
    min_weight = float('inf')
    min_weight_set = []
    edges = list(G.edges(data='weight'))
    all_edges = len(G.edges)
    
    for r in range(1, len(edges) + 1):
        for edge_subset in combinations(edges, r):
            weight = sum(w for u, v, w in edge_subset)
            if weight >= min_weight:
                continue  # Prune subsets with weight >= current minimum

            edge_set = [(u, v) for u, v, w in edge_subset]
            if is_edge_dominating_set_optimized(G, edge_set, all_edges):
                min_weight = weight
                min_weight_set = edge_subset
                break  # Break early if a solution of this size is found
        if min_weight_set:  # Stop if we found a dominating set of minimum weight
            break

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
