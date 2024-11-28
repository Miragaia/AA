import random
from math import comb

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


def dynamic_randomized_mweds(
    G, 
    max_iterations=10000, 
    initial_search_size=2, 
    base_threshold=0.25, 
    refine_threshold=0.5
):
    """
    Dynamic randomized heuristic for MWEDS with adjustable search size and thresholds.
    Parameters:
    - G: The input graph.
    - max_iterations: Maximum iterations to run the algorithm.
    - initial_search_size: Initial size of the subset of edges to search.
    - base_threshold: Progress threshold to increase search size.
    - refine_threshold: Progress threshold to decrease search size for refinement.
    """
    edges = list(G.edges(data="weight"))
    num_edges = len(edges)
    best_solution = edges  # Initialize with all edges as a fallback
    min_weight = sum(w for _, _, w in edges)  # Total weight of all edges
    basic_operations = 0
    num_configurations = 0

    # Start with a small subset size
    search_size = initial_search_size

    # Use the total number of edges as a measure of graph size
    max_possible_configurations = num_edges

    for iteration in range(max_iterations):
        num_configurations += 1

        progress = iteration / max_possible_configurations

        # Adjust search size dynamically based on progress
        if progress > base_threshold and best_solution == edges:
            # If no valid solution yet, increase search size
            search_size = min(search_size + 1, num_edges)
        elif progress > refine_threshold and best_solution != edges:
            # If solution exists and progress is beyond refine_threshold, refine by decreasing size
            search_size = max(search_size - 1, 1)

        # Randomly select a subset of edges of the current search size
        candidate_set = random.sample(edges, random.randint(1, min(search_size, num_edges)))
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
                search_size = max(2, search_size - 1)  # Shrink search size for refinement

    return best_solution, min_weight, basic_operations, num_configurations
