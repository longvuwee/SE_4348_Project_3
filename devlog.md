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
