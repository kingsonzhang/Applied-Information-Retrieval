import os
from collections import defaultdict

def create_inverted_index(directory):
    # 26 dictionaries for each letter of the alphabet
    inverted_index = {chr(i): defaultdict(str) for i in range(ord('a'), ord('z')+1)}

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Only process .txt files
            file_path = os.path.join(directory, filename)

            # Extract the location from the first 5 digits of the filename
            location = filename[:5]

            with open(file_path, 'r', encoding='utf-8') as file:
                print("Processing: " + filename)
                # Read the words from the file
                words = file.read().splitlines()

                # Dictionary to track occurrences of words in the current file
                word_positions = defaultdict(list)

                # Collect word positions
                for index, word in enumerate(words):
                    first_letter = word[0].lower()  # Get the first letter (case-insensitive)
                    word_positions[word].append(index)  # Track the index of the word

                # Now build the inverted index for this file's words
                for word, positions in word_positions.items():
                    # Count of occurrences of the word
                    count = len(positions)

                    # Format the positions list as a comma-separated string
                    positions_str = ','.join(map(str, positions))

                    # Construct the entry for this word
                    entry = f"{location}:{count}:{positions_str}"

                    # Get the first letter of the word
                    first_letter = word[0].lower()

                    # Append this entry to the appropriate dictionary
                    if inverted_index[first_letter][word]:
                        # If word already exists, append with semicolon separator
                        inverted_index[first_letter][word] += ";" + entry
                    else:
                        # Otherwise, create a new entry
                        inverted_index[first_letter][word] = entry
    return inverted_index

def write_inverted_index_to_files(inverted_index, output_directory):
    # Make sure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Loop through each letter of the alphabet
    for letter, word_dict in inverted_index.items():
        # Skip empty dictionaries
        if word_dict:
            # Sort the dictionary by the word (alphabetical order)
            sorted_items = sorted(word_dict.items())

            # Create a file for the current letter
            output_file_path = os.path.join(output_directory, f"{letter}-inverted-index.txt")

            with open(output_file_path, 'w', encoding='utf-8') as f:
                for word, data in sorted_items:
                    # Write the word and its inverted index data to the file
                    f.write(f"{word}: {data}\n")
            print(f"Written {letter}-inverted-index.txt")

def mergeFiles(directory):
    output_file_path = os.path.join("./inv-index/mergedIndex.txt")
    for filename in os.listdir("./inv-index"):
        if filename.endswith(".txt"):  # Only process .txt files
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                words = file.read()
                with open(output_file_path, 'a', encoding='utf-8') as f:
                    f.write(words)

# Example usage
directory_path = "./input-transform"
output_directory = "./inv-index"

inverted_index = create_inverted_index(directory_path)

# Write the inverted index to files
write_inverted_index_to_files(inverted_index, output_directory)

mergeFiles("./inv-index")