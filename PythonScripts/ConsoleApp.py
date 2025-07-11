import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# Absoluter Pfad zum Projektverzeichnis
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
persist_directory = os.path.join(project_dir, "vektordatenbank")

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(
    embedding_function=embedding_function,
    persist_directory=persist_directory
)

# Ollama LLM initialisieren (Modellname ggf. anpassen)
llm = OllamaLLM(model="llama3.2")

# RetrievalQA-Kette
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)

# Interaktive Frageschleife
print("Stelle Fragen zu deinem Dokument (oder tippe 'exit' zum Beenden):")
while True:
    frage = input("Frage: ")
    if frage.lower() in ["exit", "quit", "q"]:
        break
    antwort = qa_chain(frage)
    print("Antwort:", antwort["result"])
    print("Quellen:", [doc.metadata for doc in antwort["source_documents"]])