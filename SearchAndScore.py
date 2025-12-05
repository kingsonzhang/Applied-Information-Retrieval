import math
import os
from Tokenize import transformBook

def badScoring(bookInfo1, bookInfo2):
    score = bookInfo1[0] + bookInfo2[0]
    minDistance = float('inf')
    for index1 in bookInfo1[1]:
        for index2 in bookInfo2[1]:
            minDistance = min(minDistance, abs(index1 - index2))
    return score + 1 / minDistance if minDistance != float('inf') else 0

def processQuery(query):
    queryWords = transformBook(query)
    commonBooks = None
    wordInfo = []
    
    for word in queryWords:
        filePath = f"inv-index/{word[0]}-inverted-index.txt"
        if not os.path.exists(filePath):
            print(f"File for word '{word}' not found: {filePath}")
            return
        
        with open(filePath, 'r') as file:
            for line in file:
                if line.startswith(word + ":"):
                    splitWordData = [bookData.split(":") for bookData in line.split(": ")[1].split(";")]

                    booksFound = set(int(bookData[0]) for bookData in splitWordData)
                    if commonBooks is None:
                        commonBooks = booksFound
                    else:
                        commonBooks = commonBooks.intersection(booksFound)
                    
                    wordInfoDictionary = {}
                    for bookData in splitWordData:
                        wordInfoDictionary[bookData[0]] = (int(bookData[1]), [int(indexes) for indexes in bookData[2].split(",")])
                    wordInfo.append(wordInfoDictionary)

                    continue
    
    if commonBooks:
        for book in commonBooks:
            print (str(book) + ": " + str(badScoring(wordInfo[0][str(book)], wordInfo[1][str(book)])))
    else:
        print("No common books found containing all the words in your query.")
    
query = "y"
while (query == "y"):
    query = input("Search query: ").strip()
    processQuery(query)
    query = input ("Search again? (y/n): ")[0].lower()