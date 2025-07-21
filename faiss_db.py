import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAISS index file
INDEX_FILE = "faiss_index.pkl"
DATA_FILE = "faiss_data.pkl"

# Load or create FAISS index
def load_faiss_index():
    if os.path.exists(INDEX_FILE) and os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            data = pickle.load(f)
        index = faiss.read_index(INDEX_FILE)
        return index, data
    else:
        index = faiss.IndexFlatL2(384)
        return index, []

def save_faiss_index(index, data):
    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

# Add new content
def add_to_faiss(text, metadata):
    index, data = load_faiss_index()
    vector = model.encode([text])[0]
    index.add(np.array([vector]).astype("float32"))
    data.append((text, metadata))
    save_faiss_index(index, data)

# Search
def search_faiss(query, k=5):
    index, data = load_faiss_index()
    if len(data) == 0:
        return []
    query_vector = model.encode([query])[0]
    D, I = index.search(np.array([query_vector]).astype("float32"), k)
    return [data[i] for i in I[0]]

