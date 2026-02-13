import streamlit as st

from utils.highlighter import highlight_keywords
from utils.loader import load_document
from utils.chunker import chunk_text
from utils.embedding import embed_text, model
from utils.retriever import VectorStore
from utils.mcq import generate_mcqs
from utils.mindmap import build_mindmap
from utils.answer import generate_answer
from utils.summarizer import summarize_text

st.set_page_config(page_title="DocGraph AI")

st.title("DocGraph AI")
st.write("A Retrieval-Augmented Learning Assistant")

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if uploaded_file is None:
    st.session_state.mcqs = []
    st.session_state.chunks = []
    st.session_state.vector_store = None
store = None
chunks = []

# ---------------- DOCUMENT PROCESSING ---------------- #

if uploaded_file:
    with st.spinner("Processing document..."):
        pages = load_document(uploaded_file)

        if not pages or len(pages) == 0:
            st.error("No readable text found. Try another file.")
        else:
            chunks = chunk_text(pages)
            st.write("Chunks created:", len(chunks))

            embeddings = embed_text(chunks)

            if len(embeddings) == 0:
                st.error("No embeddings generated.")
            else:
                store = VectorStore(dim=len(embeddings[0]))
                store.add(embeddings, chunks)

    st.success("Document processed successfully!")

# ---------------- QUESTION ANSWERING ---------------- #

query = st.text_input("Ask a question from the document:")

if query and store:
    query_embedding = model.encode(query)
    context = store.search(query_embedding)

    # Extract only text for answer generation
    context_texts = [c["text"] for c in context]

    st.subheader("Answer")

    if "summarize" in query.lower() or "explain" in query.lower():
        answer = summarize_text(context_texts[0])
    else:
        answer = generate_answer(query, context_texts)

    st.write(answer)

    # -------- SOURCE CITATION (Page Reference) -------- #

    with st.expander("Show Source Context"):
        for c in context:
            st.write(f"Page {c['page']}: {c['text']}")

# ---------------- MCQ GENERATOR ---------------- #

st.subheader("Assessment")

# Initialize session state
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

# Generate MCQs and store
if st.button("Generate MCQs") and chunks:
    chunk_texts = [c["text"] for c in chunks]
    st.session_state.mcqs = generate_mcqs(chunk_texts)

# Display MCQs if available
if st.session_state.mcqs:
    for i, mcq in enumerate(st.session_state.mcqs):
        st.write(f"Q{i+1}: {mcq['question']}")

        selected = st.radio(
            f"Select answer for Q{i+1}",
            mcq["options"],
            index=None,
            key=f"mcq_{i}"
        )

        if st.button(f"Show Answer for Q{i+1}", key=f"btn_{i}"):
            st.success(f"Correct Answer: {mcq['answer']}")

        st.write("---")




# ---------------- MIND MAP ---------------- #

st.subheader("Concept Mind Map")

if st.button("Generate Mind Map") and chunks:
    chunk_texts = [c["text"] for c in chunks]
    graph = build_mindmap(chunk_texts)

    st.write("Nodes:", list(graph.nodes()))
    st.write("Connections:", list(graph.edges()))
