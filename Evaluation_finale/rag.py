"""
rag.py
------
Construction de la base documentaire (RAG).

"""

import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore


def get_it_vector_store():

    documents = []

    # Charger tous les PDF
    for file in glob.glob("data/*.pdf"):

        loader = PyPDFLoader(file)

        documents.extend(loader.load())

    print(f"{len(documents)} pages chargées.")

    # Découpage
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    all_splits = text_splitter.split_documents(documents)

    print(f"{len(all_splits)} morceaux créés.")

    # Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Base vectorielle
    vector_store = InMemoryVectorStore(embeddings)

    vector_store.add_documents(all_splits)

    print("Base documentaire créée.")

    return vector_store

def search_with_relevance(vector_store, query, k=3):

    results = vector_store.similarity_search(query, k=k)

    sufficient = len(results) > 0

    return results, sufficient