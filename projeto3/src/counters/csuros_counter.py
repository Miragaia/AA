import random
from ..utils import save_results

def csuros_counter(text, sampling_rate=0.1):
    """
    Estimate word frequencies using Csuros' algorithm with sampling.

    Args:
        text (str): The preprocessed text.
        sampling_rate (float): The fraction of words to sample (0 < sampling_rate <= 1).

    Returns:
        dict: A dictionary of words and their estimated counts.
    """
    if not (0 < sampling_rate <= 1):
        raise ValueError("Sampling rate must be between 0 and 1.")
    
    words = text.split()
    sample = [word for word in words if random.random() < sampling_rate]
    sampled_counts = {}
    
    for word in sample:
        sampled_counts[word] = sampled_counts.get(word, 0) + 1

    # Scale up the counts to estimate total occurrences
    estimated_counts = {word: int(count / sampling_rate) for word, count in sampled_counts.items()}
    return estimated_counts

def csuros_counter_with_save(text, filename, sampling_rate=0.1):
    """
    Run Csuros' counter and save results.

    Args:
        text (str): The preprocessed text.
        filename (str): The name of the output file (without extension).
        sampling_rate (float): The fraction of words to sample (0 < sampling_rate <= 1).
    """
    results = csuros_counter(text, sampling_rate)
    save_results(results, filename, "./data/results/csuros/")
    return results
