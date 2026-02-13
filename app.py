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

st.markdown(
    """
    <h1 style='text-align: center;'>DocGraph AI</h1>
    <h4 style='text-align: center; color: gray;'>
    A Retreival-Augmented Learning Assistant</h4>

    """,
    unsafe_allow_html=True
)
st.write("")

# ---------------- ANIMATED UI STYLE ---------------- #

st.markdown("""
<style>

/* Smooth Fade In */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Animated Gradient Background */
.stApp {
    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c1c1c);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Center Header Glow */
h1 {
    text-align: center;
    animation: fadeIn 1.2s ease-in-out;
    text-shadow: 0px 0px 15px rgba(0,255,255,0.5);
}

h4 {
    text-align: center;
    color: #cfcfcf;
    animation: fadeIn 1.5s ease-in-out;
}

/* Button Styling */
div.stButton > button {
    border-radius: 12px;
    padding: 10px 20px;
    transition: 0.3s;
    animation: fadeIn 1.5s ease-in-out;
}

div.stButton > button:hover {
    background-color: #00c6ff;
    color: black;
    transform: scale(1.05);
}

/* Upload box animation */
section[data-testid="stFileUploader"] {
    animation: fadeIn 1.2s ease-in-out;
}

/* Input box */
input[type="text"] {
    border-radius: 10px !important;
    transition: 0.3s;
}

input[type="text"]:focus {
    box-shadow: 0 0 10px #00c6ff;
}

</style>
""", unsafe_allow_html=True)


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
