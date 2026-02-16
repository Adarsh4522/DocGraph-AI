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


st.set_page_config(page_title="DocGraph AI", layout="wide")

# =====================================================
# 🌌 ANIMATED UI STYLE
# =====================================================

st.markdown("""
<style>

body {
    background-color: #0d1117;
}

/* Neon Glow Title */
.glow {
    font-size: 60px;
    color: #00f7ff;
    text-align: center;
    text-shadow: 0 0 5px #00f7ff,
                 0 0 10px #00f7ff,
                 0 0 20px #00f7ff,
                 0 0 40px #00f7ff;
    animation: flicker 2s infinite alternate;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #bbbbbb;
    font-size: 20px;
    margin-bottom: 40px;
}

@keyframes flicker {
    from { opacity: 0.8; }
    to { opacity: 1; }
}

/* Floating particles */
.particles {
    position: fixed;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 20% 30%, #00f7ff33 2px, transparent 3px),
                radial-gradient(circle at 70% 60%, #00f7ff33 2px, transparent 3px),
                radial-gradient(circle at 50% 80%, #00f7ff33 2px, transparent 3px);
    background-size: 200px 200px;
    animation: moveParticles 20s linear infinite;
    z-index: -1;
}

@keyframes moveParticles {
    from { background-position: 0 0, 0 0, 0 0; }
    to { background-position: 200px 200px, -200px 200px, 200px -200px; }
}

</style>

<div class="particles"></div>
<div class="glow">DocGraph AI</div>
<div class="subtitle">A Retrieval-Augmented Learning Assistant</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# 📂 FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if uploaded_file is None:
    st.stop()

if "last_uploaded" not in st.session_state:
   st.session_state.last_uploaded = None

if uploaded_file != st.session_state.last_uploaded:
    st.session_state.clear()
    st.session_state.last_uploaded = uploaded_file
    
# =====================================================
# 📄 DOCUMENT PROCESSING
# =====================================================

if "store" not in st.session_state:

    text = load_document(uploaded_file)
    chunks = chunk_text(text)

    st.write("Chunks created:", len(chunks))

    if len(chunks) == 0:
        st.error("No chunks generated.")
        st.stop()

    embeddings = embed_text(chunks)

    store = VectorStore(dim=len(embeddings[0]))
    store.add(embeddings, chunks)

    st.session_state.store = store
    st.session_state.chunks = chunks

    st.success("Document processed successfully!")

store = st.session_state.store
chunks = st.session_state.chunks

# =====================================================
# 💬 QUERY SECTION
# =====================================================

query = st.text_input("Ask a question from the document:")

if query:
    query_lower = query.lower()

    # 🔹 Summarize
   if "summarize" in query_lower or "summary" in query_lower:

    full_text = " ".join([c["text"] for c in chunks])

    st.write("Text length:", len(full_text))  # Debug

    summary = summarize_text(full_text)

    st.write("Raw summary output:", summary)  # Debug

    st.subheader("Summary")

    if summary:
        st.write(summary)
    else:
        st.warning("Summary returned empty output.")

    # 🔹 MCQ
    elif "mcq" in query_lower:
        st.session_state.mcqs = generate_mcqs(chunks)

    # 🔹 Mindmap
    elif "mindmap" in query_lower or "mind map" in query_lower:
        st.session_state.graph = build_mindmap(chunks)

    # 🔹 Normal RAG
    else:
        context = store.search(query)
        answer = generate_answer(query, context)

        st.subheader("Answer")
        st.write(answer)

        with st.expander("Show Source Context"):
            for c in context:
                highlighted = highlight_keywords(c["text"], query)
                st.markdown(f"**Page {c['page']}:** {highlighted}")

# =====================================================
# 🎯 BUTTON SECTION
# =====================================================

st.markdown("---")
col1, col2 = st.columns(2)

# Initialize session state flags
if "mcqs" not in st.session_state:
    st.session_state.mcqs = None

if "graph" not in st.session_state:
    st.session_state.graph = None

# ==========================
# MCQ BUTTON
# ==========================
with col1:
    if st.button("Generate MCQs"):
        st.session_state.mcqs = generate_mcqs(chunks)
        st.session_state.graph = None   # clear mindmap

# Display MCQs ONLY if button was pressed
if st.session_state.mcqs is not None:

    st.subheader("Assessment")

    for i, mcq in enumerate(st.session_state.mcqs):

        st.markdown(
            f"<p style='font-size:20px; font-weight:600;'>"
            f"Q{i+1}: {mcq['question']}</p>",
            unsafe_allow_html=True
        )

        selected = st.radio(
            "Select answer:",
            mcq["options"],
            index=None,
            key=f"mcq_{i}"
        )

        if st.button(f"Show Answer {i+1}", key=f"show_{i}"):
            st.success(f"Correct Answer: {mcq['answer']}")

        st.markdown("<br>", unsafe_allow_html=True)


# -----------------------
# MIND MAP BUTTON
# -----------------------
with col2:
    if st.button("Generate Mind Map"):
        st.session_state.graph = build_mindmap(chunks)

# Only display if graph exists
if "graph" in st.session_state and st.session_state.graph is not None:
    st.subheader("Concept Mind Map")
    st.write("Nodes:", list(st.session_state.graph.nodes()))
    st.write("Connections:", list(st.session_state.graph.edges()))
