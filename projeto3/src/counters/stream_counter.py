from ..utils import save_results

def stream_counter(text, n=10):
    """
    Identify the n most frequent items using a data stream algorithm.

    Args:
        text (str): The preprocessed text.
        n (int): Number of most frequent items to track.

    Returns:
        dict: A dictionary of the n most frequent items.
    """
    words = text.split()
    counter = {}

    for word in words:
        if word in counter:
            counter[word] += 1
        elif len(counter) < n:
            counter[word] = 1
        else:
            # Evict the least frequent item
            min_word = min(counter, key=counter.get)
            del counter[min_word]
            counter[word] = 1

    # Sort by frequency in descending order
    return dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))

def stream_counter_with_save(text, filename, n=10):
    """
    Run the stream counter and save results.

    Args:
        text (str): The preprocessed text.
        filename (str): The name of the output file (without extension).
        n (int): Number of most frequent items to track.
    """
    results = stream_counter(text, n)
    save_results(results, filename, "./data/results/stream/")
    return results
