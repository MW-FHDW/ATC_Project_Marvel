import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# Setup
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="vektordatenbank", embedding_function=embedding)
llm = OllamaLLM(model="llama3.2")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever(), return_source_documents=True)

# Streamlit UI
st.title("🧠 Lokaler KI-Chat mit deinen Dokumenten")
frage = st.text_input("Stelle eine Frage:")

if frage:
    try:
        antwort = qa_chain(frage)
        st.write("**Antwort:**", antwort["result"])
        with st.expander("📄 Quellen anzeigen"):
            if antwort.get("source_documents"):
                for doc in antwort["source_documents"]:
                    st.markdown(f"- {doc.metadata}")
            else:
                st.write("Keine Quellen gefunden.")
    except Exception as e:
        st.error(f"Fehler bei der Anfrage: {e}")