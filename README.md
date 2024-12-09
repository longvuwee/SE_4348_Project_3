# Project 3
 
Author: Long Vu 

This project uses 3 program to create a BTree index file manager. The system allows creating, opening, and managing index files, along with operations like inserting, searching, loading, and extracting key-value pairs.

# Files Included
### 1. main.py
This is the main entry point of the program. It provides a menu-driven interface for interacting with the B-Tree. Operations include:
- Creating a new index file.
- Opening an existing index file.
- Inserting key-value pairs.
- Searching for a specific key.
- Loading key-value pairs from a file into the B-Tree.
- Printing the B-Tree contents.
- Extracting key-value pairs to a file.
- Exiting the program.

### 2. btree.py
This file contains the implementation of the `BTree` and `BTreeNode` classes and its functionalities are:
- Inserting key-value pairs into the B-Tree.
- Searching for keys in the B-Tree.
- Reading from and writing to `.idx` files.
- Splitting nodes when they exceed capacity.
- Loading data into the B-Tree and extracting it to a file.

### 3. fileHandler.py
This file handles operations on index files, including:
- Creating a new `.idx` file with a predefined header.
- Validating and opening existing `.idx` files.

# How to Run the Project
### Step by Step Instructions:
1. Using the terminal, type "python main.py" to execute the program
2. The program will print out the menu in the terminal
		
