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

        elif choice == "open":
            filename = input("Enter the filename to open: ").strip()
            if open_index_file(filename):
                current_file = filename
                btree = BTree()

        elif choice == "insert":
            if not current_file:
                print("No index file is open. Please create or open a file first.")
                continue
            try:
                key = int(input("Enter the key (unsigned integer): ").strip())
                value = int(input("Enter the value (unsigned integer): ").strip())
                btree.insert(key, value)
                print("Key-value pair inserted.")
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
            if not filename:
                print("No index file is open. Please create or open an index file first.")
                continue
            filename = input("Enter the filename to load from: ").strip()
            try:
                btree.load_from_file(filename)
                print(f"Key-value pairs loaded from {filename}.")
            except IOError as e:
                print(f"Error loading from file: {e}")

        elif choice == "print":
            if not btree:
                print("No index file is open. Please create or open an index file first.")
                continue
            btree.print_tree()

        elif choice == "extract":
            if not btree:
                print("No index file is currently open. Please create or open an index file first.")
                continue
            filename = input("Enter filename to extract to: ").strip()
            try:
                try:
                    with open(filename, 'rb'):
                        overwrite = input("File exists. Overwrite? (y/n): ").strip().lower()
                        if overwrite != 'y':
                            print("Extraction canceled.")
                            continue
                except FileNotFoundError:
                    pass

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
