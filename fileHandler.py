import os #for directory use

def create_index_file(filename):
    MAGIC_NUMBER = b"4337PRJ3"
    HEADER_SIZE = 512

    if os.path.exists(filename):
        overwrite = input(f"File '{filename}' already exists. Do you want to overwrite? (yes/no): ").strip().lower
        if overwrite == "no":
            print("File creation aborted.")
            return False
    
    try:
        with open(filename, "wb") as f:
            # create the header
            header = MAGIC_NUMBER 
            header += (0).to_bytes(8, 'big') # root node block ID
            header += (1).to_bytes(8, 'big') # next block ID
            header += b"\x00" * (HEADER_SIZE - len(header)) # fill in the remaining unused space of the block
            f.write(header)
        return True
    except IOError as e:
        print(f"Error opening file '{filename}': {e}")
        return False


def open_index_file(filename):
    MAGIC_NUMBER = b"4337PRJ3"

    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        return False
    
    try:
        with open(filename, "rb") as f:
            # validate the magic number
            magic_number = f.read(8)
            if magic_number != MAGIC_NUMBER:
                print(f"File '{filename}' is not a valid index file.")
                return False
        return True
    except IOError as e:
        print(f"Error opening file '{filename}': {e}")
        return False