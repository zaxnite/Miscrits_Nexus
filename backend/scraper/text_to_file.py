import os

def append_list_to_file(data_list: list, filename: str, directory: str = None):
    """
    Appends each item from a list to a text file, each on a new line.
    This version allows saving to a specific directory.
    It avoids explicit error checks and print statements for brevity.

    Args:
        data_list (list): The list of items (e.g., strings, numbers) to append.
        filename (str): The base name of the text file (e.g., 'log.txt').
        directory (str, optional): The directory where the file should be saved.
                                   If None, the file is saved in the current working directory.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  

    if directory:
        full_dir = os.path.join(project_root, directory)
        os.makedirs(full_dir, exist_ok=True)
        full_path = os.path.join(full_dir, filename)
    else:
        full_path = os.path.join(project_root, filename)


    # Open the file in append mode ('a') with UTF-8 encoding
    with open(full_path, 'a', encoding='utf-8') as f:
        for item in data_list:
            f.write(f"{item},") # Write each item followed by a newline

def write_list_to_file(full_page_content, filename: str, directory: str = None):
    if directory:
        os.makedirs(directory, exist_ok=True)
        full_path = os.path.join(directory, filename)
    else:
        full_path = filename
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(full_page_content)