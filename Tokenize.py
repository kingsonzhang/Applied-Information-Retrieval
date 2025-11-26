from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

# sampleString = "Document will describe marketing strategies carried out by U.S. companies for their agricultural chemicals, report predictions for market share of such chemicals, or report market statistics for agrochemicals, pesticide, herbicide, fungicide, insecticide, fertilizer, predicted sales, market share, stimulate demand, price cut, volume of sales."

def transformBook(book):
    tokens = word_tokenize(book)
    filteredTokens = [word for word in tokens if word.isalpha() and not word.lower() in stop_words]
    stemmedTokens = [stemmer.stem(token) for token in filteredTokens]
    return stemmedTokens