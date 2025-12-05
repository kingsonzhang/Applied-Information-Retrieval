import zipfile
import os
import nltk
from Tokenize import transformBook

nltk.download('punkt_tab')
nltk.download('stopwords')

# sampleString = "Document will describe marketing strategies carried out by U.S. companies for their agricultural chemicals, report predictions for market share of such chemicals, or report market statistics for agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, stimulate demand, price cut, volume of sales."

rootDirectory = './input-files/aleph.gutenberg.org'
outputDir = './input-transform'
targetExtension = '.txt'

for dirpath, dirnames, filenames in os.walk(rootDirectory):
    for fileName in filenames:
        if fileName.endswith('.zip'):
            zipFilePath = os.path.join(dirpath, fileName)
            try:
                with zipfile.ZipFile(zipFilePath, 'r') as zipRef:
                    for innerFullPath in zipRef.namelist():
                        if innerFullPath.endswith(targetExtension):
                            print(f"Processing file inside zip: {innerFullPath}")
                            with zipRef.open(innerFullPath) as file:
                                textContent = file.read().decode('utf-8', errors='ignore')
                            processedTokens = transformBook(textContent)
                            output_path = os.path.join(outputDir, fileName.replace(".zip", "transformed.txt"))
                            with open(output_path, 'w', encoding='utf-8') as outfile:
                                outfile.write(' '.join(processedTokens))
            except FileNotFoundError:
                print(f"Error: Zip file not found at '{zipFilePath}'")
            except Exception as e:
                print(f"An error occurred: {e}")