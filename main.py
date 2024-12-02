from file_handler import create_index_file, open_index_file
from btree import BTree

current_file = None  # Tracks the currently open index file
btree = None         # Instance of the BTree class

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
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            filename = input("Enter the filename to create: ").strip()
            if create_index_file(filename):
                current_file = filename
                btree = BTree()

        elif choice == "2":
            filename = input("Enter the filename to open: ").strip()
            if open_index_file(filename):
                current_file = filename
                btree = BTree()

        elif choice == "3":
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

        elif choice == "4":
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

        elif choice == "8":
            print("Exiting the program.")
            break

        else:
            print("Option not implemented or invalid. Please try again.")

if __name__ == "__main__":
    main()
