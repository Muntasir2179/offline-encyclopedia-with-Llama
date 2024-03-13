import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from dashboard.settings import BASE_DIR
from .text_processor import get_document_chunks
import os


class ChromadbOperations:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(BASE_DIR / 'database'))

        # collection for user
        self.collection = self.client.get_or_create_collection(name="text_collection",
                                                               embedding_function=ONNXMiniLM_L6_V2())
        # collection for custom knowledge base
        # it will be used in case user is not satisfied with the result generated from the uploaded document
        self.custom_collection = self.client.get_or_create_collection(name="custom_knowledge_base",
                                                                      embedding_function=ONNXMiniLM_L6_V2())
        
        # if there is no items in the custom knowledge base then insert all the documents from the "local_knowledge_base" directory
        if self.custom_collection.count() == 0:
            text_chunks = get_document_chunks(path=BASE_DIR / "local_knowledge_base")
            ids = [str(i) for i in range(1, len(text_chunks)+1)]
            self.custom_collection.add(documents=text_chunks, ids=ids)
    

    def create_vector_storage(self):
        if 'text_collection' not in self.client.list_collections():
            self.collection = self.client.get_or_create_collection(name="text_collection",
                                                                   embedding_function=ONNXMiniLM_L6_V2())


    def insert_data(self, texts_chunks):
        ids = [str(i) for i in range(1, len(texts_chunks)+1)]
        self.collection.add(documents=texts_chunks, ids=ids)
    
    
    def query(self, query_text):
        response = self.collection.query(query_texts=[query_text], n_results=1)
        return response['documents'][0]
    
    def query_on_custom_knowledge_base(self, query_text):
        response = self.custom_collection.query(query_texts=[query_text], n_results=1)
        return response['documents'][0]
    
    def delete_vector_storage(self):
        if len(self.client.list_collections()) != 0:
            self.client.delete_collection(name="text_collection")