# Database RAG LLM implementation (Gemini API, Chroma DB and Hugging Face embedding model)

## Description
This pipeline generates database queries with contextual knowledge of existing database schemas.

- Store database schema in Chroma DB (vector storage).
- Consume user queries and extract knowledge from Chroma DB.
- Build prompt template using raw user query and extracted knowledge (as base).
- Cater response.


## How to run

1. Install requirements.
   ```
   pip install -r requirements.txt
   ```
2. Setup env file (.env)
   ```
   API_KEY=<API_KEY>
   HUGGING_FACE_TOKEN=<HF_TOKEN>
   ```
3. Load sample data to Sqlite3 DB.
    ```
    db = Database()
    db.load_data()
    ```
4. Load schemas to Chroma DB.
   ```
   chroma_db = ChromaDBUtility()
   chroma_db.load_data()
   ```
4. Run file.
   ```
   python3 utility/gen.py
   ```

## Documentation & Reference

[Chroma DB](https://www.trychroma.com/)
<br>
[Hugging Face Embedding Model](https://huggingface.co/blog/getting-started-with-embeddings)
<br>
[Gemini API](https://ai.google.dev/gemini-api/docs?authuser=2)
