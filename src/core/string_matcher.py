# KMP ALGORITHM
def kmp_search():
    pass

# BOOYER-MOORE ALGORITHM
def build_bad_char_table(pattern:str) -> dict[str, int]:
    table = {}
    for i, char in enumerate(pattern):
        table[char] = i
    return table

def boyer_moore_search(text: str, pattern: str) -> list[int]:
    if not text or not pattern or len(pattern) > len(text):
        return []

    n = len(text)
    m = len(pattern)
    bad_char_table = build_bad_char_table(pattern)
    occurrences = []

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            occurrences.append(s)
            s += m - bad_char_table.get(text[s + m], -1) if s + m < n else 1
        else:
            bad_char = text[s + j]
            shift = j - bad_char_table.get(bad_char, -1)
            s += max(1, shift)

    return occurrences

# LEVENSTHEIN DISTANCE ALGORITHM
def levenshtein_distance(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)

    # initialize dp matrix of size (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,    # deletion
                dp[i][j - 1] + 1,    # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
    return dp[m][n]