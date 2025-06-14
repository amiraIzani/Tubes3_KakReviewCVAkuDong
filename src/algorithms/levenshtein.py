# --- Levenshtein Distance and Similarity Utilities ---
def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates the Levenshtein distance between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for j in range(n + 1): dp[0][j] = j
    for i in range(m + 1): dp[i][0] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,       # Deletion
                           dp[i][j - 1] + 1,       # Insertion
                           dp[i - 1][j - 1] + cost)  # Substitution
    return dp[m][n]

def calculate_levenshtein_similarity(s1: str, s2: str) -> float:
    # Calculates a similarity score (0.0 to 1.0) based on Levenshtein distance.
    if not s1 and not s2: return 1.0
    if not s1 or not s2: return 0.0
    max_len = max(len(s1), len(s2))
    if max_len == 0: return 1.0
    distance = levenshtein_distance(s1, s2)
    return 1.0 - (distance / max_len)