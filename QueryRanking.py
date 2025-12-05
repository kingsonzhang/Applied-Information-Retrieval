import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Tokenize import transformBook

# --- Configuration ---
folder_path = 'input-transform'

def document_generator(folder):
    """
    A generator function that yields the content of one text file at a time.
    This reads the documents efficiently without loading all content into a list.
    """
    document_names = []
    
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder, filename)
            document_names.append(filename)
            
            # Read the entire single-line, space-separated token string
            with open(file_path, 'r', encoding='utf-8') as f:
                yield f.read().strip()
                
    return document_names # Note: Generators can't directly return values like this 
                         # easily when used in fit_transform. We'll handle doc names 
                         # separately below.

# 1. Get the list of filenames (for labeling the output)
document_names = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
if not document_names:
    print(f"⚠️ Error: No text files found in the folder '{folder_path}'.")
else:
    # 2. Initialize the vectorizer
    # We'll use the default settings since your text is pre-tokenized.
    vectorizer = TfidfVectorizer()

    # 3. Fit and Transform the corpus using the generator
    print(f"Starting vectorization for {len(document_names)} documents...")
    # We call the generator function and pass the resulting iterable to fit_transform
    tfidf_matrix = vectorizer.fit_transform(document_generator(folder_path))

    print("\n✅ TF-IDF Vectorization Complete.")
    print(f"Shape of the resulting matrix: {tfidf_matrix.shape}")

# Assuming 'vectorizer' is the TfidfVectorizer object you previously fit.
# Assuming 'tfidf_matrix' is the sparse matrix of your documents.

query = "y"
while (query == "y"):
    # 1. Define your query
    query = input("Enter search query: ")
    query = " ".join(transformBook(query))

    # 2. Transform the query using the *fitted* vectorizer
    query_vector = vectorizer.transform([query]) 

    print(f"Query vector shape: {query_vector.shape}")
    # The shape should be (1, N_features) where N_features is the size of your vocabulary.

    # Calculate the similarity between the single query vector and all document vectors
    # The result will be a sparse matrix of shape (1, N_documents).
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)

    # Convert the result to a flat NumPy array for easier indexing
    similarity_scores = similarity_scores.flatten() 

    print(f"Total scores calculated: {len(similarity_scores)}")

    # Assuming 'document_names' is the list of filenames/document titles created earlier.

    # 1. Get the indices that would sort the scores in descending order (highest score first)
    ranked_indices = np.argsort(similarity_scores)[::-1]

    # 2. Define how many top results you want to see
    top_n = 5
    top_results_indices = ranked_indices[:top_n]

    print("\n--- Top Search Results ---")

    # 3. Print the top results
    for i, doc_index in enumerate(top_results_indices):
        score = similarity_scores[doc_index]
        doc_name = document_names[doc_index] 
        
        # We round the score for cleaner output
        print(f"#{i+1}: Document '{doc_name}' | Similarity Score: {score:.4f}")

    query = input ("Search again? (y/n): ")[0].lower()