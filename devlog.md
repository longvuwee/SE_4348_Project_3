# 12-2-24 1:58 AM
# Purpose:

This project involves creating an interactive program to manage index files containing a B-Tree structure.
The program must allow users to create, insert into, search, load, print, and extract data from index files.

# Implementation Details:
- Interactive using a menu approach to handle user commands.
- Index files must adhere to specific size and structure requirements (512-byte blocks).

# Main Components:
### Header Block:
Contains metadata such as a magic number, root node ID, and next block ID.

### Node Blocks:
Stores keys, values, child pointers, and metadata about parent and current block IDs.

### B-Tree Characteristics:
- Minimum degree of 10.
- Each node fits within a 512-byte block.
- Up to 19 key-value pairs and 20 child pointers per node.

### Program Commands:

- create: Create a new index file.
- open: Open an existing index file.
- insert: Add key-value pairs to the B-Tree.
- search: Find a key in the index and print its value.
- load: Insert multiple key-value pairs from a file.
- print: Display all key-value pairs in the index.
- extract: Save all key-value pairs to a file.
- quit: Exit the program.

### Extra Notes

- Numbers must be stored as 8-byte integers in big-endian format.
- Only 3 nodes may be in memory at any time.
- Error handling is required for all user inputs and file operations.


# Start of project

I'll first create a main file that will be running the program and it will display the menu.

# 12-7-24 4:40PM

make another python file called fileHandler to work with file handling. create 2 functions, one for creating a file and one for opening a file.


for the file creation function, the header should use the <code>n.to_bytes(8, 'big')</code> to convert the integers into bytes as big endian


# 12-7-24 7:30 PM

work on BTree algorithm in another python file.

create a class for the BTree nodes and a class for the BTree.
added a insert, print, and search method

# 12-8-24 12:40 AM

added a load_from_file method and input.csv file to test the load option and check if the keys and values are inserted correctly to the BTree