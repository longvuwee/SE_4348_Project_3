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

    def to_bytes(self):
        data = self.block_id.to_bytes(8, 'big')
        data += self.parent_id.to_bytes(8, 'big')
        data += self.num_pairs.to_bytes(8, 'big')

        for key in self.keys:
            data += key.to_bytes(8, 'big')

        for value in self.values:
            data += value.to_bytes(8, 'big')

        for child in self.children:
            data += child.to_bytes(8, 'big')
        return data

class BTree:
    def __init__(self, degree=10):
        self.degree = degree
        self.root = BTreeNode(1)
        self.nodes = {1: self.root}
        self.current_file = None  # Store current file path

    def set_current_file(self, filename):
        self.current_file = filename

    def insert(self, key, value):
        node = self.root
        while True:
            if node.is_full():
                self.split_node(node)
                node = self.find_root()
                continue
            if node.children[0] == 0:  # Leaf node
                self.insert_into_leaf(node, key, value)
                self.write_to_idx_file()
                print("Key-value pair inserted.")
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
        print(f"Inserted '{value}' at key '{key}'")

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

    def read_from_idx_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                # Skip the header (512 bytes)
                file.seek(512)
                
                # Clear current nodes to avoid conflicts
                self.nodes = {}

                while True:
                    # Read one node (512 bytes per node)
                    node_data = file.read(512)
                    if not node_data:
                        break  # End of file

                    # Deserialize the node
                    block_id = int.from_bytes(node_data[0:8], 'big')
                    parent_id = int.from_bytes(node_data[8:16], 'big')
                    num_pairs = int.from_bytes(node_data[16:24], 'big')

                    # Extract keys, values, and child pointers
                    keys = [
                        int.from_bytes(node_data[24 + i * 8:32 + i * 8], 'big')
                        for i in range(19)
                    ]
                    values = [
                        int.from_bytes(node_data[176 + i * 8:184 + i * 8], 'big')
                        for i in range(19)
                    ]
                    children = [
                        int.from_bytes(node_data[328 + i * 8:336 + i * 8], 'big')
                        for i in range(20)
                    ]

                    # Recreate the node and add it to the tree
                    node = BTreeNode(block_id, parent_id)
                    node.num_pairs = num_pairs
                    node.keys = keys
                    node.values = values
                    node.children = children
                    self.nodes[block_id] = node

                # Set the root node based on the node with parent_id == 0
                self.root = next(node for node in self.nodes.values() if node.parent_id == 0)
                print("B-Tree loaded successfully from .idx file.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred while reading the .idx file: {e}")

    def write_to_idx_file(self):
        if not self.current_file:
            print("No file is set. Cannot write to file.")
            return
        try:
            HEADER_SIZE = 512  # Ensure we do not overwrite the header
            with open(self.current_file, 'r+b') as file:  # Open in read+binary mode
                file.seek(HEADER_SIZE)  # Move the file pointer past the header
                for node in self.nodes.values():
                    file.write(node.to_bytes())  # Write the node as bytes
        except IOError as e:
            print(f"Error writing to .idx file: {e}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    try:
                        key, value = map(int, line.strip().split(','))
                        self.insert(key, value)
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                for node in self.nodes.values():
                    for i in range(node.num_pairs):
                        file.write(f"{node.keys[i]},{node.values[i]}\n")
            print(f"Data extracted to {filename}.")
        except IOError as e:
            print(f"Error writing to file: {e}")
