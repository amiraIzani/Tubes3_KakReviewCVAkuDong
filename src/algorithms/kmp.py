class KMP:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.prefix_table = self._compute_prefix_table()

    def _compute_prefix_table(self) -> list[int]:
        m = len(self.pattern)
        prefix_table = [0] * m
        j = 0  # length of previous longest prefix suffix

        for i in range(1, m):
            while j > 0 and self.pattern[i] != self.pattern[j]:
                j = prefix_table[j - 1]

            if self.pattern[i] == self.pattern[j]:
                j += 1
                prefix_table[i] = j
            else:
                prefix_table[i] = 0

        return prefix_table

    def search(self, text: str) -> list[int]:
        n = len(text)
        m = len(self.pattern)
        j = 0  # index for pattern
        occurrences = []

        for i in range(n):
            while j > 0 and text[i] != self.pattern[j]:
                j = self.prefix_table[j - 1]

            if text[i] == self.pattern[j]:
                j += 1

            if j == m:
                occurrences.append(i - m + 1)
                j = self.prefix_table[j - 1]

        return occurrences