from itertools import combinations

def is_edge_dominating_set(G, edge_set):
    operations = 0 
    for u, v in G.edges:
        operations += 1
        if not any((u in (u1, v1) or v in (u1, v1)) for u1, v1, w in edge_set):
            operations += 1
            return False, operations
    return True, operations

def exhaustive_search_mweds(G):
    min_weight = float('inf')
    min_weight_set = []
    basic_operations = 0    

    edges = G.edges(data= "weight")
    all_edges = G.number_of_edges()
    basic_operations += all_edges

    for r in range(1, all_edges + 1):
        for edge_set in combinations(edges, r):
            basic_operations += 1

            is_dominating, operations = is_edge_dominating_set(G, edge_set)
            basic_operations += operations

            if is_dominating:
                weight = sum(w for u, v, w in edge_set)
                basic_operations += len(edge_set)

                if weight < min_weight:
                    min_weight = weight
                    min_weight_set = edge_set
                    basic_operations += 1
            else:
                continue
            
    print(basic_operations)
    return min_weight_set, min_weight, basic_operations

def greedy_mweds(G):
    edge_list = sorted(G.edges(data='weight'), key=lambda x: x[2])
    dominating_set = []
    covered_edges = set()
    basic_operations = 0 

    for u, v, weight in edge_list:
        if (u, v) not in covered_edges:
            dominating_set.append((u, v, weight))
            covered_edges.update(G.edges(u))
            covered_edges.update(G.edges(v))
            basic_operations += len(G.edges(u)) + len(G.edges(v))

            if all(any((u in (u1, v1) or v in (u1, v1)) for u1, v1, w in dominating_set) for u, v in G.edges):
                basic_operations += len(G.edges)
                break 

    total_weight = sum(weight for u, v, weight in dominating_set)
    return dominating_set, total_weight, basic_operations
