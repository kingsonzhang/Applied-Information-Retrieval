import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import zipfile
import os

# nltk.download('punkt_tab')
# nltk.download('stopwords')
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

# sampleString = "Document will describe marketing strategies carried out by U.S. companies for their agricultural chemicals, report predictions for market share of such chemicals, or report market statistics for agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, stimulate demand, price cut, volume of sales."

def transformBook(book):
    tokens = word_tokenize(book)
    filteredTokens = [word for word in tokens if word.isalpha() and not word.lower() in stop_words]
    stemmedTokens = [stemmer.stem(token) for token in filteredTokens]
    return stemmedTokens

rootDirectory = './input-files/aleph.gutenberg.org'
outputDir = './input-transform'
targetExtension = '.txt'

for dirpath, dirnames, filenames in os.walk(rootDirectory):
    for fileName in filenames:
        if fileName.endswith('.zip'):
            zipFilePath = os.path.join(dirpath, fileName)
            try:
                with zipfile.ZipFile(zipFilePath, 'r') as zipRef:
                    # Look at ALL files listed by the zip file
                    for innerFullPath in zipRef.namelist(): # <-- THIS IS THE KEY LIST
                        
                        # 1. Check if the file name ends with the target extension
                        # This works regardless of how deep the file is nested inside the zip.
                        if innerFullPath.endswith(targetExtension):
                            print(f"Processing file inside zip: {innerFullPath}")
                            
                            # 2. Read and Process the content
                            with zipRef.open(innerFullPath) as file:
                                textContent = file.read().decode('utf-8', errors='ignore')
                            
                            processedTokens = transformBook(textContent)

                            # 3. Writing to text file
                            output_path = os.path.join(outputDir, fileName.replace(".zip", "transformed.txt"))
                            with open(output_path, 'w', encoding='utf-8') as outfile:
                                # Write each token followed by a newline character
                                outfile.write('\n'.join(processedTokens))

            except FileNotFoundError:
                print(f"Error: Zip file not found at '{zipFilePath}'")
            except Exception as e:
                print(f"An error occurred: {e}")