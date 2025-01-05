# Format all footnotes to not have any \n characters so the whole footnote is on one line.
import os

# Define the directory path
dir_path = "Footnotes"

# Loop through the directory and its subdirectories
for root, dirs, files in os.walk(dir_path):
    # Loop through the files
    for file in files:
        # Get the full file path
        file_name, file_ext = os.path.splitext(file)
        # Check if the file has no extension
        if file_ext == "" and file_name != ".DS_Store":
            file_path = os.path.join(root, file)
            # Open the file in read mode
            with open(file_path, "r") as f:
                # Read the file content
                content = f.read()
                # Remove the newline characters
                #content = content.replace("\n", " ")
                content = content + "\n"
            # Open the file in write mode
            with open(file_path, "w") as f:
                # Write the modified content
                f.write(content)
