import random

def is_edge_dominating_set(G, edge_set):
    operations = 0
    for u, v in G.edges:
        operations += 1
        if not any((u in (u1, v1) or v in (u1, v1)) for u1, v1, w in edge_set):
            operations += 1
            return False, operations
    return True, operations


def randomized_mweds(G, max_iterations=1000):
    """
    Randomized algorithm to find a Minimum Weight Edge Dominating Set.
    """
    edges = list(G.edges(data="weight"))
    num_edges = len(edges)
    best_solution = None
    min_weight = float('inf')
    basic_operations = 0
    num_configurations = 0

    for _ in range(max_iterations):
        num_configurations += 1

        # Randomly select a subset of edges
        candidate_set = random.sample(edges, random.randint(1, num_edges))
        basic_operations += len(candidate_set)

        # Check if it is a dominating set
        is_dominating, operations = is_edge_dominating_set(G, candidate_set)
        basic_operations += operations

        if is_dominating:
            weight = sum(w for u, v, w in candidate_set)
            basic_operations += len(candidate_set)

            # Update the best solution if the current one is better
            if weight < min_weight:
                min_weight = weight
                best_solution = candidate_set
                basic_operations += 1

    return best_solution, min_weight, basic_operations, num_configurations


def randomized_heuristic_mweds(G, max_iterations=1000):
    """
    Randomized heuristic for finding a Minimum Weight Edge Dominating Set.
    Combines random selection with a heuristic to greedily minimize weight.
    """
    edges = list(G.edges(data="weight"))
    best_solution = None
    min_weight = float('inf')
    basic_operations = 0
    num_configurations = 0

    for _ in range(max_iterations):
        num_configurations += 1

        # Shuffle edges randomly and sort by weight
        random.shuffle(edges)
        sorted_edges = sorted(edges, key=lambda x: x[2])
        basic_operations += len(sorted_edges)

        # Build a dominating set greedily from the sorted edges
        dominating_set = []
        covered_edges = set()

        for u, v, weight in sorted_edges:
            if (u, v) not in covered_edges:
                dominating_set.append((u, v, weight))
                covered_edges.update(G.edges(u))
                covered_edges.update(G.edges(v))
                basic_operations += len(G.edges(u)) + len(G.edges(v))

                # Check if all edges are covered
                if all(any((u in (u1, v1) or v in (u1, v1)) for u1, v1, w in dominating_set) for u, v in G.edges):
                    basic_operations += len(G.edges)
                    break

        # Calculate the total weight of the dominating set
        weight = sum(weight for u, v, weight in dominating_set)
        basic_operations += len(dominating_set)

        # Update the best solution if the current one is better
        if weight < min_weight:
            min_weight = weight
            best_solution = dominating_set
            basic_operations += 1

    return best_solution, min_weight, basic_operations, num_configurations
