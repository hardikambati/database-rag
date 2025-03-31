import os

import requests
from dotenv import load_dotenv

import chromadb
from google import genai
from chromadb import (
    Documents,
    Embeddings,
    EmbeddingFunction,
)

from database import Database


load_dotenv()
API_KEY = os.getenv("API_KEY")
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")


class GenUtility:
    """
    Calls Gemini API for generating content (model : gemini-2.0-flash)
    """

    def __init__(self):
        self.model_client = genai.Client(api_key=API_KEY)

    def generate_response(self, query: str, context: str):
        prompt = f"""
        You are an SQL assistant. Generate an SQL query **exactly as a human would type it**.

        ### Context:  
        {context}  

        ### User Query:  
        {query}  

        ### Output:  
        (Output starts here—no code blocks, no formatting, just plain text)

        SELECT ...
        """
        response = self.model_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        print(f"{response.text}\n")
        return response.text


class EmbeddingUtility:
    """
    Token embedding utility.
    Calls hugging face API for embedding tokens.
    [Heavylifting done on upstream server :) ]
    """

    def __init__(self):
        self.embedding_model_id = "sentence-transformers/all-MiniLM-L6-v2"

    def get_embedding(self, text: str):
        api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{self.embedding_model_id}"
        headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
        data = {"inputs": text, "options": {"wait_for_model": True}}
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()
    
    
class CustomEmbedding(EmbeddingFunction):

    def __init__(self):
        self.embedding_model = EmbeddingUtility()

    def __call__(self, input: Documents) -> Embeddings:
        return self.embedding_model.get_embedding(text=input)[0]


class ChromaDBUtility:
    """
    Stores content (vector embeddings) in Chroma DB.
    Creates local file (.sqlite3) for storing data temporarily.
    """

    def __init__(self):
        self.embedding = EmbeddingUtility()
        self.chroma_client = chromadb.PersistentClient(path="db")
        self.collection = self.chroma_client.get_or_create_collection(
            name="test-vector",
            embedding_function=CustomEmbedding()
        )

    def write(self, ids: list, query: list):
        embedding_list = []
        for text in query:
            embedding = self.embedding.get_embedding(
                text=[text]
            )[0]
            embedding_list.append(embedding)
        self.collection.add(
            ids=ids,
            embeddings=embedding_list,
            documents=query
        )
        print(f"[Chroma] Stored data to chromaDB.")

    def read(self, query):
        res = self.collection.query(
            query_texts=[query],
            n_results=1,
        )
        document = res["documents"][0]
        return document

    def load_data(self):
        """
        Helper method
        """
        db_instance = Database()
        schema_dict = db_instance.get_db_schema()
        
        ids = []
        columns = []
        for key, value in schema_dict.items():
            text = f"table: {key}, columns : {','.join(value)}"
            
            ids.append(key)
            columns.append(text)

        print(ids)
        print(columns)

        chromadb_instance = ChromaDBUtility()
        chromadb_instance.write(ids=ids, query=columns)
        chromadb_instance.read(
            query="customers data schema, orders data schema"
        )


if __name__ == "__main__":

    gen_instance = GenUtility()
    sql_db_instance = Database()
    chroma_db_instance = ChromaDBUtility()

    query = "give all product titles and their amount"
    context = chroma_db_instance.read(query=query)

    sql_query = gen_instance.generate_response(
        query=query,
        context=context
    )

    results = sql_db_instance.execute(
        sql_query=sql_query
    )
    print(results)

