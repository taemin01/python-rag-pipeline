from dotenv import load_dotenv
from hugging_face_embeddings import get_embeddings
import os
import chromadb

#.env file load
load_dotenv('../RAG_Pipeline/.env')

class chromaDB:
    def load_client():
        client = chromadb.HttpClient(host=os.getenv('CHROMADB_HOST'), port=os.getenv('CHROMADB_PORT'))
        # collection = client.get_or_create_collection(os.getenv('CHROMADB_COLLECTION'))
        return client

    def collection_add_embedding(chunks):
        collection = load_collction()
        embeddings = get_embeddings(chunks)
        collection.add(
            embeddings=embeddings,
            documents=chunks  # 원본 텍스트만 저장
        )

client = chromadb.HttpClient(host=os.getenv('CHROMADB_HOST'), port=os.getenv('CHROMADB_PORT'))
collection = client.get_or_create_collection(os.getenv('CHROMADB_COLLECTION'))
print(collection.get())