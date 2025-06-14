import collections

class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.failure_link = None
        self.output = []

class AhoCorasick:
    def __init__(self, keywords = list[str]):
        self.root = TrieNode()
        self.keywords = keywords
        self._build_trie()
        self._build_failure_links()
    
    def _build_trie(self):
        for keyword in self.keywords:
            node = self.root
            for char in keyword:
                node = node.children[char]
            node.output.append(keyword)
    
    def _build_failure_links(self):
        queue = collections.deque()
        
        for char, node in self.root.children.items():
            node.failure_link = self.root
            queue.append(node)
        
        while queue:
            current_node = queue.popleft()
            
            for char, next_node in current_node.children.items():
                fail_node = current_node.failure_link

                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.failure_link
                
                if fail_node:
                    next_node.failure_link = fail_node.children[char]
                else:
                    next_node.failure_link = self.root
                
                if next_node.failure_link:
                    next_node.output.extend(next_node.failure_link.output)
                
                queue.append(next_node)
    
    def search(self, text: str) -> dict[str, list[int]]:
        results = collections.defaultdict(list)
        current_node = self.root

        for i, char in enumerate(text):
            while current_node is not None and char not in current_node.children:
                current_node = current_node.failure_link

            if current_node is None:
                current_node = self.root
                continue

            current_node = current_node.children[char]

            if current_node.output:
                for keyword in current_node.output:
                    start_index = i - len(keyword) + 1
                    results[keyword].append(start_index)
        
        return dict(results)    