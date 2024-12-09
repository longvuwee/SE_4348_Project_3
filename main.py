from fileHandler import create_index_file, open_index_file
from btree import BTree

def display_menu():
    print("\nMenu:")
    print("create  - Create a new index file")
    print("open    - Open an existing index file")
    print("insert  - Insert a key-value pair")
    print("search  - Search for a key")
    print("load    - Load from a file")
    print("print   - Print all key-value pairs")
    print("extract - Extract to a file")
    print("quit    - Exit the program")

def main():
    global current_file, btree
    current_file = None
    btree = None

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip().lower()

        if choice == "create":
            filename = input("Enter the filename to create: ").strip()
            if create_index_file(filename):
                current_file = filename
                btree = BTree()
                btree.set_current_file(current_file)  # Set the current file for the BTree

        elif choice == "open":
            filename = input("Enter the filename to open: ").strip()
            if open_index_file(filename):
                current_file = filename
                btree = BTree()
                btree.set_current_file(current_file)
                btree.read_from_idx_file(current_file)

        elif choice == "insert":
            if not current_file:
                print("No index file is open. Please create or open a file first.")
                continue
            try:
                key = int(input("Enter the key: ").strip())
                value = int(input("Enter the value: ").strip())
                btree.insert(key, value)
            except ValueError:
                print("Invalid input. Please enter integers only.")

        elif choice == "search":
            if not current_file:
                print("No index file is open. Please create or open a file first.")
                continue
            try:
                key = int(input("Enter the key to search for: ").strip())
                value = btree.search(key)
                if value is not None:
                    print(f"Key: {key}, Value: {value}")
                else:
                    print("Key not found.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == "load":
            if not current_file:
                print("No index file is open. Please create or open an index file first.")
                continue
            filename = input("Enter the filename to load keys and values from: ").strip()
            try:
                print(f"Key-value pairs loaded from {filename}.")
                btree.load_from_file(filename)
            except IOError as e:
                print(f"Error loading from file: {e}")

        elif choice == "print":
            if not btree:
                print("No index file is open. Please create or open an index file first.")
                continue
            btree.print_tree()

        elif choice == "extract":
            if not btree:
                print("No index file is open. Please create or open an index file first.")
                continue
            filename = input("Enter the filename: ").strip()
            try:
                btree.extract_to_file(filename)
                print(f"Key-value pairs extracted to {filename}.")
            except IOError as e:
                print(f"Error extracting to file: {e}")

        elif choice == "quit":
            print("Exiting the program.")
            break
        else:
            print("Option invalid. Please try again.")

    exit()
if __name__ == "__main__":
    main()
