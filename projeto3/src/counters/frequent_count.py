def frequent_count(text, threshold=10):
    """
    Identify frequent words with counts exceeding the threshold.

    Args:
        text (str): The preprocessed text.
        threshold (int): The frequency threshold for words to be considered frequent (default: 10).

    Returns:
        dict: A dictionary of words and their counts exceeding the threshold.
    """
    words = text.split()
    word_counts = {}

    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Filter words by threshold
    frequent_words = {word: count for word, count in word_counts.items() if count > threshold}
    return frequent_words
