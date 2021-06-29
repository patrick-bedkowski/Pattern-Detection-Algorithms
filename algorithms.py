from typing import List, Iterator, Tuple

# Knuth-Morris-Pratt Algorithm

def find_kmp(string: str, text: str) -> List[int]:
    """
    Parameters:
        substring: substring to be found
        text: text to be searched
    Returns:
        List of positions in ascending order of the beginnings of
        ``substring`` in ``text``
    """
    N: int = len(string)  # length of substring
    M: int = len(text)  # length of text

    if M == 0 or N == 0 or M < N:
        return []

    def lps_table(string: str) -> List[int]:
        lenght = len(string)
        result = [0 for _ in range(lenght)]
        k = 0
        for q in range(1, lenght):
            while k > 0 and string[k] != string[q]:
                k = result[k]
            if string[k] == string[q]:
                k += 1
            result[q] = k
        return result

    result = list()
    lps = lps_table(string)
    b = 0
    for i in range(M):
        while (b > 0 and string[b] != text[i]):
            b = lps[b-1]
        if string[b] == text[i]:
            b = b + 1
        if b == N:
            result.append(i - N + 1)
            b = lps[b-1]
    return result

# Karp-Rabin Algorithm

KR_HASH_ALPHABET_SIZE = 512
KR_HASH_MODULUS = 104729


def kr_initial_hash(word: str) -> int:
    """Calculates a rolling hash of a string.

    This rolling hash is caluclated using the following formula, all modulo KR_HASH_MODULUS:
    ```
       c[0]  * alphabet_size**(n-1)
    +  c[1]  * alphabet_size**(n-2)
    + ...
    +  c[-2] * alphabet_size
    +  c[-1] * 1
    ```
    """
    hash = 0
    for char in map(ord, word):
        hash = (hash * KR_HASH_ALPHABET_SIZE + char) % KR_HASH_MODULUS
    return hash


def kr_rolling_hash(text: str, window_size: int) -> Iterator[Tuple[int, int, str]]:
    """An iterator over all substrings of text of size window_size.

    Yields 3-element tuples:
    1. Index of generated substring in text
    2. The hash (as defined in kr_initial_hash)
    3. The substring itself

    This generator exploits the rolling hash, and should be faster then
    ```
    for i, substr in generate_substrings(text, window_size):
        subst_hash = kr_initial_hash(substr)
    ```
    """
    first_char_factor = KR_HASH_ALPHABET_SIZE**(window_size-1) % KR_HASH_MODULUS

    hash = kr_initial_hash(text[:window_size])
    max_start_idx = len(text)-window_size

    for i in range(max_start_idx+1):
        yield i, hash, text[i:i+window_size]

        if i != max_start_idx:
            # Updating the rolling hash (see definition in kr_initial_hash) takes 3 steps
            # 1. Removing the term corresponding to the char being shifted-out:
            #     hash -= old_char * alphabet^(n-1)
            # 2. Multiplying all terms by alphabet
            #     hash *= alphabet
            # 3. Adding the value for new char
            #     hash += new_char
            hash = (
                (hash - ord(text[i])*first_char_factor) * KR_HASH_ALPHABET_SIZE
                + ord(text[i+window_size])
            ) % KR_HASH_MODULUS


def find_kr(substring: str, text: str) -> List[int]:
    """
    Finds all occurrences of ``substring`` in ``text``
    using the Karp-Rabin algorithm.

    Parameters:
        substring: substring to be found
        text: text to be searched

    Returns:
        List of positions in ascending order of the beginnings of
        ``substring`` in``text``.
    """
    if not substring:
        return list(range(len(text)+1))

    substr_hash = kr_initial_hash(substring)

    return [
        i for (i, text_hash, possible_match) in kr_rolling_hash(text, len(substring))
        if text_hash == substr_hash and possible_match == substring
    ]

# Naive Algorithm

def find_n(substring: str, text: str) -> List[int]:
    """
    Parameters:
        substring: substring to be found
        text: text to be searched
    Returns:
        List of positions in ascending order of the beginnings of
        ``substring`` in ``text``
    """

    N: int = len(substring)  # length of substring
    M: int = len(text)  # length of text

    indecies: List = []

    for i in range(0, M-N+1):  # iterate as many times as the length difference between text and substring + 1
        if substring == text[i:i+N]:  # if the substring has been found
            indecies.append(i+1)  # save current index of a word in the list
    return indecies  # return list with found indecies
