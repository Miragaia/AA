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
    Randomized algorithm to find a Minimum Weight Edge Dominating Set,
    avoiding duplicate subsets of edges.
    """
    edges = list(G.edges(data="weight"))
    num_edges = len(edges)
    best_solution = None
    min_weight = float('inf')
    basic_operations = 0
    num_configurations = 0

    # Use a set to keep track of already seen subsets
    seen_subsets = set()

    for _ in range(max_iterations):
        num_configurations += 1

        # Generate a random subset
        candidate_set = random.sample(edges, random.randint(1, num_edges))
        candidate_set_key = tuple(sorted(candidate_set))  # Sort and convert to tuple for hashing

        # Skip if this subset has already been processed
        if candidate_set_key in seen_subsets:
            continue

        # Mark this subset as processed
        seen_subsets.add(candidate_set_key)
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
    base_threshold=0.125, 
    refine_threshold=0.25
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
    best_solution = edges
    min_weight = sum(w for _, _, w in edges)
    basic_operations = 0
    num_configurations = 0

    search_size = initial_search_size
    max_possible_configurations = num_edges

    # Use a set to track unique subsets
    seen_subsets = set()

    for iteration in range(max_iterations):
        num_configurations += 1

        progress = iteration / max_possible_configurations

        if progress > base_threshold and best_solution == edges:
            search_size = min(search_size + 1, num_edges)
        elif progress > refine_threshold and best_solution != edges:
            search_size = max(search_size - 1, 1)

        # Generate a candidate set and check if it has been seen before
        candidate_set = random.sample(edges, random.randint(1, min(search_size, num_edges)))
        candidate_set_key = tuple(sorted(candidate_set))
        
        if candidate_set_key in seen_subsets:
            continue  # Skip if already processed
        
        # Mark this subset as processed
        seen_subsets.add(candidate_set_key)
        basic_operations += len(candidate_set)

        is_dominating, operations = is_edge_dominating_set(G, candidate_set)
        basic_operations += operations

        if is_dominating:
            weight = sum(w for u, v, w in candidate_set)
            basic_operations += len(candidate_set)

            if weight < min_weight:
                min_weight = weight
                best_solution = candidate_set
                search_size = max(2, search_size - 1)

    return best_solution, min_weight, basic_operations, num_configurations

def dynamic_combined_mweds(
    G, 
    max_iterations=10000, 
    initial_search_size=2, 
    base_explore_interval=500, 
    base_threshold=0.125, 
    refine_threshold=0.25,
    min_subset_size=2,
    max_subset_fraction=0.3
):
    edges = sorted(G.edges(data="weight"), key=lambda x: x[2])  # Sort by weight
    num_edges = len(edges)
    num_nodes = G.number_of_nodes()
    edge_density = num_edges / (num_nodes * (num_nodes - 1) / 2)

    best_solution = edges
    min_weight = sum(w for _, _, w in edges)
    basic_operations = 0
    num_configurations = 0

    max_subset_size = max(min_subset_size, int(edge_density * num_edges))
    fixed_size = initial_search_size
    explore_interval = max(base_explore_interval, int(base_explore_interval * (1 / edge_density)))
    seen_subsets = set()

    for iteration in range(max_iterations):
        num_configurations += 1
        progress = iteration / max_iterations
        candidate_size = max(min_subset_size, min(max_subset_size, int(progress * max_subset_size)))

        if iteration % explore_interval == 0 and iteration > 0:
            candidate_size = random.randint(
                max(min_subset_size, candidate_size - int(candidate_size * 0.1)),
                min(max_subset_size, candidate_size + int(candidate_size * 0.1))
            )

        try:
            candidate_set = random.sample(edges, candidate_size)
        except ValueError:
            candidate_set = edges

        candidate_set_key = tuple(sorted(candidate_set))
        if candidate_set_key in seen_subsets:
            continue

        seen_subsets.add(candidate_set_key)
        basic_operations += len(candidate_set)

        # Debug: Print candidate subset
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Progress = {progress:.2f}, Candidate size = {len(candidate_set)}")
            print(f"Subset example: {candidate_set[:5]}...")

        is_dominating, operations = is_edge_dominating_set(G, candidate_set)
        basic_operations += operations

        if not is_dominating:
            uncovered = [(u, v) for u, v in G.edges() if (u, v) not in candidate_set and (v, u) not in candidate_set]
        else:
            weight = sum(w for u, v, w in candidate_set)
            print(f"Iteration {iteration}: Dominating set found. Weight = {weight:.2f}, Current best = {min_weight:.2f}")

            if weight < min_weight:
                min_weight = weight
                best_solution = candidate_set

            if min_weight < edge_density * sum(w for _, _, w in edges):
                print(f"Early termination at iteration {iteration}: Solution with weight = {min_weight:.2f}")
                break


    return best_solution, min_weight, basic_operations, num_configurations




