import random

def csuros_counter(text, sampling_rate=0.1):
    """
    Approximate word frequencies using Csuros' sampling-based method.

    Args:
        text (str): The preprocessed text.
        sampling_rate (float): The proportion of words to sample (default: 0.1).

    Returns:
        dict: A dictionary with sampled words as keys and estimated counts as values.
    """
    words = text.split()
    total_words = len(words)
    sampled_counts = {}

    # Sample words based on the sampling rate
    for word in words:
        if random.random() < sampling_rate:
            if word in sampled_counts:
                sampled_counts[word] += 1
            else:
                sampled_counts[word] = 1

    # Scale counts to estimate true frequencies
    scaling_factor = 1 / sampling_rate
    estimated_counts = {word: int(count * scaling_factor) for word, count in sampled_counts.items()}

    return estimated_counts
