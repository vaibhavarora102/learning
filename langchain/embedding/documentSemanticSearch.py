from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


load_dotenv()

embedding = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=300,
)

documents = [
    "Paris is the capital of France.",
    "Berlin is the capital of Germany.",
    "Madrid is the capital of Spain.",
    "Rome is the capital of Italy.",
    "London is the capital of the United Kingdom."
]

query = "tell me about Spain"


# Embed the documents and the query
doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)  

# Calculate cosine similarity between the query and each document
similarities = cosine_similarity([query_embedding], doc_embeddings)[0]

print("Cosine Similarities:", similarities)

# Get the index of the most similar document
most_similar_index = np.argmax(similarities)
print("Most similar document index:", most_similar_index)   
print("Most similar document:", documents[most_similar_index])
