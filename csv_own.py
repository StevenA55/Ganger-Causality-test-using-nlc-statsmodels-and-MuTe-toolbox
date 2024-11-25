import csv
import os

def save(data_lists, file_name, folder_path=''):
    """
    Saves multiple lists as columns in a CSV file.

    Parameters:
    - data_lists: a list of lists where each inner list represents a column.
    - file_name: the name of the file (without the extension).
    - folder_path: (optional) the path of the folder where the file will be saved.
    """
    # Create the full file name
    full_file_name = f"{file_name}.csv"
    
    # If a folder is specified, add it to the file name
    if folder_path:
        full_file_name = os.path.join(folder_path, full_file_name)
    
    # Ensure all lists have the same length
    max_len = max(len(lst) for lst in data_lists)
    
    # Pad shorter lists with empty values so all have the same length
    data_lists = [lst + [None] * (max_len - len(lst)) for lst in data_lists]
    
    # Save the lists to the CSV file
    with open(full_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Transpose the data so it is saved by columns
        for row in zip(*data_lists):
            writer.writerow(row)
    
    print(f"File saved as: {full_file_name}")