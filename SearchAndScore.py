import os
from Tokenize import transformBook

keepSearching = True
while (keepSearching):
    searchQuery = transformBook(input("Search Query: ").lower())
    if not searchQuery:
        print("Error: Input text is empty.")
    else:
        invertedIndex = []
        for word in searchQuery:
            filename = f"{word.lower()[0]}-inverted-index.txt"
            folderName = ".\\inv-index"
            filePath = os.path.join(folderName, filename)
            print(filePath)
            try:
                with open(filePath, 'r') as file:
                    for line in file:
                        if line.lower().startswith(f"{word}:"):
                            invertedIndex.append(line[len(word) + 2:].rstrip())
                            continue
            except FileNotFoundError:
                print(f"Error: The file '{filePath}' was not found.")
            except Exception as e:
                print(f"An unexpected error occurred during file processing: {e}")
        

    keepSearching = input("Search again? [Y/N]: ")
    keepSearching = True if keepSearching.lower() == "y" else False