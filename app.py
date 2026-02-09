import streamlit as st

from utils.summarizer import summarize_text
from utils.loader import load_document
from utils.chunker import chunk_text
from utils.embedding import embed_text, model
from utils.retriever import VectorStore

st.set_page_config(page_title="DocGraph AI")

st.title("DocGraph AI")
st.write("A Retrieval-Augmented Learning Assistant")

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

store = None
chunks = []

if uploaded_file:
    with st.spinner("Processing document..."):
        text = load_document(uploaded_file)
        chunks = chunk_text(text)

        st.write("Chunks created:", len(chunks))

        embeddings = embed_text(chunks)

        if len(embeddings) == 0:
            st.error("No embeddings generated. Try another PDF.")
        else:
            store = VectorStore(dim=len(embeddings[0]))
            store.add(embeddings, chunks)

    st.success("Document processed successfully!")

    query = st.text_input("Ask a question from the document:")

    if query and store:
        query_embedding = model.encode(query)
        context = store.search(query_embedding)

        st.subheader("Retrieved Context")
        for c in context:
            st.write("-", c)

        st.subheader("Answer")
        if "summarize" in query.lower() or "explain" in query.lower():
            summary = summarize_text(context[0])
            st.write(summary)

        else:
          st.write(context[0])
