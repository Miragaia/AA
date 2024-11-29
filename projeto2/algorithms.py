import random
from collections import deque
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
    base_threshold=0.125, 
    refine_threshold=0.25,
    early_stopping_threshold=0.1,  # Early stopping if improvement is under threshold
    min_subset_size=2,
    max_subset_size=None
):
    """
    Upgraded Dynamic randomized heuristic for MWEDS with adjustable search size and thresholds.
    Parameters:
    - G: The input graph.
    - max_iterations: Maximum iterations to run the algorithm.
    - initial_search_size: Initial size of the subset of edges to search.
    - base_threshold: Progress threshold to increase search size.
    - refine_threshold: Progress threshold to decrease search size for refinement.
    - early_stopping_threshold: Threshold to stop early if the improvement is low.
    - min_subset_size: Minimum subset size to search for.
    - max_subset_size: Maximum subset size to search for (defaults to number of edges).
    """
    edges = list(G.edges(data="weight"))
    num_edges = len(edges)
    best_solution = edges
    min_weight = sum(w for _, _, w in edges)
    basic_operations = 0
    num_configurations = 0

    # Initialize search size
    search_size = initial_search_size
    max_subset_size = max_subset_size or num_edges  # Default to all edges if not specified

    # Use a deque for more efficient removal of old subsets
    seen_subsets = deque(maxlen=500)

    # Early stopping tracking
    last_improvement = float('inf')
    improvement_count = 0

    for iteration in range(max_iterations):
        num_configurations += 1
        progress = iteration / max_iterations

        # Dynamically adjust search size based on progress
        if progress > base_threshold and best_solution == edges:
            search_size = min(search_size + 1, max_subset_size)
        elif progress > refine_threshold and best_solution != edges:
            search_size = max(search_size - 1, min_subset_size)

        # Generate a candidate set and check if it has been seen before
        # Ensure valid range for candidate size
        upper_bound = min(search_size, max_subset_size) - 1
        candidate_size = random.randint(min_subset_size, upper_bound) if upper_bound >= min_subset_size else min_subset_size

        # Ensure that candidate_size does not exceed the number of available edges
        candidate_size = min(candidate_size, num_edges)

        # Ensure candidate_size is not negative
        if candidate_size < 0:
            candidate_size = min_subset_size

        # Generate the candidate set
        candidate_set = random.sample(edges, candidate_size)
        candidate_set_key = tuple(sorted(candidate_set))
        
        if candidate_set_key in seen_subsets:
            continue  # Skip if already processed
        
        # Mark this subset as processed
        seen_subsets.append(candidate_set_key)
        basic_operations += len(candidate_set)

        # Evaluate the candidate set
        is_dominating, operations = is_edge_dominating_set(G, candidate_set)
        basic_operations += operations

        if is_dominating:
            weight = sum(w for u, v, w in candidate_set)

            if weight < min_weight:
                min_weight = weight
                best_solution = candidate_set
                search_size = max(min_subset_size, search_size - 1)

                # Track the improvement and manage early stopping
                if last_improvement - min_weight < early_stopping_threshold:
                    improvement_count += 1
                    if improvement_count > 5:  # Stop early after a few iterations with low improvement
                        print(f"Early stopping at iteration {iteration} due to low improvement.")
                        break
                else:
                    improvement_count = 0

                last_improvement = min_weight
                
    return best_solution, min_weight, basic_operations, num_configurations
