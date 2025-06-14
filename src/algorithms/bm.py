class BoyerMoore:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self.m = len(pattern)
        self.last_occurence_table = self._build_last_occurrence_table()

    def _build_last_occurrence_table(self) -> dict[str, int]:
        table = {}
        for i, char in enumerate(self.pattern):
            table[char] = i
        return table
    
    def search(self, text: str) -> list[int]:
        pattern = self.pattern
        m = self.m
        last_occurence_table = self.last_occurence_table

        n = len(text)
        occurences = []

        if not text or not pattern or m > n:
            return []
        
        s = 0
        while s <= n - m:
            j = m - 1

            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1
            
            if j < 0:
                occurences.append(s)
                s += m - last_occurence_table.get(text[s + m], -1) if s + m < n else 1
            
            else:
                bad_char = text[s + j]
                shift = j - last_occurence_table.get(bad_char, -1)
                s += max(1, shift)
        
        return occurences