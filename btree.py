class BTreeNode:
    def __init__(self, block_id, parent_id=0):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_pairs = 0
        self.keys = [0] * 19
        self.values = [0] * 19
        self.children = [0] * 20

    def is_full(self):
        return self.num_pairs == 19

class BTree:
    def __init__(self, degree=10):
        self.degree = degree
        self.root = BTreeNode(1)
        self.nodes = {1: self.root}

    def insert(self, key, value):
        node = self.root
        while True:
            if node.is_full():
                self.split_node(node)
                node = self.find_root()
                continue
            if node.children[0] == 0:  # Leaf node
                self.insert_into_leaf(node, key, value)
                break
            for i in range(node.num_pairs):
                if key < node.keys[i]:
                    node = self.nodes[node.children[i]]
                    break
            else:
                node = self.nodes[node.children[node.num_pairs]]

    def search(self, key):
        node = self.root
        while node:
            for i in range(node.num_pairs):
                if key == node.keys[i]:
                    return node.values[i]
                if key < node.keys[i]:
                    node = self.nodes.get(node.children[i])
                    break
            else:
                node = self.nodes.get(node.children[node.num_pairs])
        return None

    def insert_into_leaf(self, node, key, value):
        if key in node.keys[:node.num_pairs]:
            print(f"Key {key} already exists in the B-Tree.")
            return
        index = 0
        while index < node.num_pairs and node.keys[index] < key:
            index += 1
        node.keys.insert(index, key)
        node.values.insert(index, value)
        node.num_pairs += 1
        node.keys = node.keys[:19]
        node.values = node.values[:19]

    def split_node(self, node):
        mid_index = len(node.keys) // 2
        new_node = BTreeNode(len(self.nodes) + 1, node.parent_id)
        new_node.keys = node.keys[mid_index:]
        new_node.values = node.values[mid_index:]
        new_node.children = node.children[mid_index + 1:]
        new_node.num_pairs = len(new_node.keys)
        node.keys = node.keys[:mid_index]
        node.values = node.values[:mid_index]
        node.children = node.children[:mid_index + 1]
        node.num_pairs = len(node.keys)
        self.nodes[new_node.block_id] = new_node
        if node == self.root:
            new_root = BTreeNode(len(self.nodes) + 1)
            new_root.keys[0] = new_node.keys[0]
            new_root.children[0] = node.block_id
            new_root.children[1] = new_node.block_id
            new_root.num_pairs = 1
            self.root = new_root
            self.nodes[new_root.block_id] = new_root

    def find_root(self):
        for node in self.nodes.values():
            if node.parent_id == 0:
                return node

    def print_tree(self):
        print("\nB-Tree Contents:")
        for node_id, node in self.nodes.items():
            print(f"Node {node_id}:")
            for i in range(node.num_pairs):
                print(f"  Key: {node.keys[i]}, Value: {node.values[i]}")
        print("\n")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    try:
                        key, value = map(int, line.strip().split(','))
                        self.insert(key, value)
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
            print(f"Data loaded successfully from {filename}.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError as e:
            print(f"Error reading file '{filename}': {e}")

    def extract_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                for node in self.nodes.values():
                    for i in range(node.num_pairs):
                        file.write(f"{node.keys[i]},{node.values[i]}\n")
            print(f"Data extracted to {filename}.")
        except IOError as e:
            print(f"Error writing to file: {e}")
