from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import os
import json

# 📄 Nur die gewünschte JSON-Datei laden
json_file = r"Beispieldaten\275.json"

documents = []
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            doc_text = json.dumps(data, ensure_ascii=False)
            documents.append(Document(page_content=doc_text, metadata={"source": os.path.basename(json_file)}))
        except Exception as e:
            print(f"Fehler beim Laden von {json_file}: {e}")
else:
    print(f"Datei nicht gefunden: {json_file}")

# 📚 Dokumente in Chunks aufteilen
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# 🔤 Embeddings vorbereiten
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 💾 Chroma Vektordatenbank initialisieren
vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embedding_function,
    persist_directory="vektordatenbank"
)

# 🤖 Lokales Modell über Ollama
llm = OllamaLLM(model="llama3.2")

# 🔄 RetrievalQA-Kette
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)

# ❓ Beispiel-Frage
# frage = "Wer sind die Avengers?"
# antwort = qa_chain(frage)

# print("Antwort:", antwort["result"])
# print("Quellen:", [doc.metadata for doc in antwort["source_documents"]])