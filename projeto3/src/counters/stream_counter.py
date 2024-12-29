import random
from ..utils import save_results

def misra_gries_counter(text, k=2):
    """
    Estimate frequent word counts using the Misra-Gries algorithm.

    Args:
        text (str): The preprocessed text.
        k (int): Parameter to determine the threshold (find items with frequency > 1/k).

    Returns:
        dict: A dictionary of words and their approximate counts.
    """
    words = text.split()
    counters = {}

    # Process each word in the text
    for word in words:
        if word in counters:
            counters[word] += 1
        elif len(counters) < k - 1:
            counters[word] = 1
        else:
            # Decrement all counters
            for key in list(counters.keys()):
                counters[key] -= 1
                if counters[key] == 0:
                    del counters[key]

    return counters


def verify_frequent_items(text, counters, k=2):
    """
    Verify which words exceed the 1/k threshold.

    Args:
        text (str): The preprocessed text.
        counters (dict): Output of the Misra-Gries algorithm.
        k (int): Threshold parameter.

    Returns:
        dict: Verified frequent words with their actual counts.
    """
    words = text.split()
    true_counts = {}

    # Count all words in the text
    for word in words:
        true_counts[word] = true_counts.get(word, 0) + 1

    # Threshold for frequency
    threshold = len(words) / k

    # Filter words that meet the threshold
    frequent_items = {word: count for word, count in true_counts.items() if count > threshold}
    return frequent_items


def misra_gries_counter_with_save(text, filename, k=800):
    """
    Run the Misra-Gries counter and save results.

    Args:
        text (str): The preprocessed text.
        filename (str): The name of the output file (without extension).
        k (int): Parameter to determine the threshold (find items with frequency > 1/k).

    Returns:
        dict: A dictionary of words and their approximate counts.
    """
    results = misra_gries_counter(text, k)
    save_results(results, filename, "./data/results/stream/")
    return results
