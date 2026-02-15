# 🚀 DocGraph AI  
### A Retrieval-Augmented Learning Assistant

DocGraph AI is an intelligent document analysis system that transforms static academic PDFs and TXT files into interactive AI-powered learning tools.

Built using **Retrieval-Augmented Generation (RAG)**, **Transformer-based embeddings**, and **Natural Language Processing (NLP)** techniques, this system enables:

- 📄 Semantic Question Answering  
- 📝 Automatic MCQ Generation  
- 🗺️ Concept-Based Mind Map Creation  
- 📚 Intelligent Document Summarization  

---

## 🧠 Project Objective

The objective of this project is to convert unstructured academic documents into structured, interactive learning resources using applied Artificial Intelligence techniques.

---

## ✨ Key Features

- Upload PDF or TXT documents  
- Automatic text extraction and chunking  
- Transformer-based semantic embeddings  
- FAISS vector similarity search  
- Context-aware Question Answering (RAG pipeline)  
- Minimum 5 auto-generated MCQs  
- Concept-based Mind Map generation  
- Interactive and animated Streamlit UI  

---

## 🛠️ Tech Stack

### 👨‍💻 Programming Language
- Python 3.10+

### 🤖 AI & NLP
- Sentence Transformers (MiniLM)
- NLTK
- TF-IDF
- POS Tagging

### 🔎 Vector Database
- FAISS (Facebook AI Similarity Search)

### 📊 Graph Processing
- NetworkX

### 🌐 Frontend
- Streamlit

---

## 🏗️ System Architecture

The system follows a modular Retrieval-Augmented Generation (RAG) pipeline.

User
    ↓
Document Upload (PDF/TXT)
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embedding Generation (MiniLM - 384 Dimensional Vectors)
    ↓
FAISS Vector Store
    ↓
Semantic Retrieval
    ↓
AI Output
      • Context-Aware Answers
      • MCQ Generation
      • Concept Mind Map


The architecture separates:

- Document processing  
- Semantic indexing  
- Retrieval logic  
- Learning output generation  

This modular design ensures scalability and maintainability.

---

## 🧩 Module Overview

### 📄 1. Document Loader
- Extracts text from PDF using PyPDF2  
- Reads TXT files directly  
- Cleans and prepares raw content  

### ✂️ 2. Chunking Module
- Splits large documents into semantic blocks  
- Improves retrieval accuracy  
- Enables efficient embedding  

### 🧠 3. Embedding Module
- Uses `all-MiniLM-L6-v2` model  
- Converts text into 384-dimensional vectors  
- Enables semantic similarity search  

### 🔎 4. Vector Store (FAISS)
- Stores embeddings  
- Performs fast cosine similarity search  
- Retrieves contextually relevant chunks  

### ❓ 5. Question Answering (RAG)
- Embeds user query  
- Retrieves relevant chunks  
- Generates summarized answer  

### 📝 6. MCQ Generator
- Extracts meaningful sentences  
- Identifies key concepts  
- Generates minimum 5 questions  
- Creates distractor options  
- Interactive selection UI  

### 🗺️ 7. Concept Mind Map
- Extracts nouns using POS tagging  
- Applies TF-IDF scoring  
- Builds concept graph using NetworkX  
- Visualizes structured knowledge  

---
### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/DocGraph-AI.git
cd DocGraph-AI

```

---

## 📊 Example Use Case

1. Upload an academic PDF  
2. Ask a conceptual question  
3. Generate summary  
4. Generate MCQs  
5. Generate concept mind map  

The system converts static content into an interactive learning experience by applying Retrieval-Augmented Generation (RAG) and semantic search techniques.

---

## 🚀 Future Enhancements

- GPT-based generative responses  
- OCR support for scanned PDFs  
- Export MCQs as PDF  
- Mind map visualization improvements  
- Multi-document semantic comparison  
- Quiz scoring and analytics dashboard  

---

## 🧪 Challenges Faced

- Handling large transformer model downloads  
- Managing Streamlit session state effectively  
- Optimizing PDF text extraction  
- Implementing TF-IDF-based concept filtering  
- Debugging NLTK resource dependencies  
- Ensuring smooth vector similarity retrieval  

---

## 📌 Conclusion

DocGraph AI demonstrates the practical implementation of **Retrieval-Augmented Artificial Intelligence systems** in educational technology.

By integrating:

- Natural Language Processing (NLP)  
- Transformer-based Embeddings  
- Vector Databases (FAISS)  
- Graph-Based Knowledge Representation  

The system successfully transforms unstructured documents into intelligent, interactive learning tools.

---

## 👨‍💻 Author

**Adarsh**  
Artificial Intelligence Project  
  

---
