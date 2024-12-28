from collections import Counter

def exact_counter(text):
    """
    Count exact word frequencies in the text.

    Args:
        text (str): The preprocessed text.

    Returns:
        dict: A dictionary with words as keys and their counts as values.
    """
    words = text.split()
    word_counts = Counter(words)
    return word_counts
