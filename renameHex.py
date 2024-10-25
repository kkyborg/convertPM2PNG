import os
import re

def rename_files_in_folder(folder_path):
    # Regular expression to match files with the format "TmbpABCD.png"
    pattern = re.compile(r"Tbmp([A-Fa-f0-9]{4})\.png")
    
    for filename in os.listdir(folder_path):
        print(filename)
        match = pattern.match(filename)
        
        if match:
            # Extract hexadecimal part (ABCD) and convert it to decimal
            hex_value = match.group(1)
            decimal_value = int(hex_value, 16)
            
            # Generate new filename
            new_filename = f"blob{decimal_value}.png"
            
            # Get full paths
            old_filepath = os.path.join(folder_path, filename)
            new_filepath = os.path.join(folder_path, new_filename)
            
            # Rename file
            os.rename(old_filepath, new_filepath)
            print(f'Renamed "{filename}" to "{new_filename}"')

# Usage
folder_path = './toRename'
rename_files_in_folder(folder_path)
