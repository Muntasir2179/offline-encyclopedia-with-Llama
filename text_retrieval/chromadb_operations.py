import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from dashboard.settings import BASE_DIR
import os


class ChromadbOperations:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(BASE_DIR / 'database'))
        self.collection = self.client.get_or_create_collection(name="text_collection",
                                                               embedding_function=ONNXMiniLM_L6_V2())
    
    def create_vector_storage(self):
        if len(self.client.list_collections()) == 0:
            self.collection = self.client.get_or_create_collection(name="text_collection",
                                                                   embedding_function=ONNXMiniLM_L6_V2())


    def insert_data(self, texts_chunks):
        ids = [str(i) for i in range(1, len(texts_chunks)+1)]
        self.collection.add(documents=texts_chunks, ids=ids)
    
    
    def query(self, query_text):
        response = self.collection.query(query_texts=[query_text], n_results=1)
        return response['documents'][0]
    
    def delete_vector_storage(self):
        if len(self.client.list_collections()) != 0:
            self.client.delete_collection(name="text_collection")