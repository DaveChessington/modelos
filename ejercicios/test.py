import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# --- Forzar CPU para embeddings HuggingFace ---
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["FORCE_CUDA"] = "0"

# --- Cargar API Key de Gemini ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# --- 1. Cargar documento ---
pdf_path = r"C:\Users\David-PC\Documents\Python projects\AI\modelos-langchain\modelos\documentos\reglamento_interno.pdf"
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"No se encontró el PDF en la ruta: {pdf_path}")

print("📄 Cargando documento...")
loader = PyPDFLoader(pdf_path)
pages = loader.load()
print(f"✅ Documento cargado con {len(pages)} páginas")

# --- 2. Dividir texto ---
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = splitter.split_documents(pages)
print(f"🧩 Texto dividido en {len(docs)} fragmentos")

# --- 3. Crear embeddings locales ---
print("⚙️ Generando embeddings locales con HuggingFace (CPU)...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

INDEX_PATH = "faiss_local_index"

if os.path.exists(INDEX_PATH):
    print("📦 Cargando índice FAISS existente...")
    vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
else:
    print("🆕 Creando índice FAISS nuevo...")
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    vectorstore.save_local(INDEX_PATH)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- 4. Modelo LLM (Gemini) ---
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)

# --- 5. Prompt personalizado ---
template = """
Usa el siguiente contexto para responder la pregunta del usuario.
Si no hay suficiente información, responde: "No tengo información suficiente en el documento."

Contexto:
{context}

Pregunta:
{question}
"""
prompt = ChatPromptTemplate.from_template(template)

# --- 6. Crear RAG Chain moderno ---
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# --- 7. Función para preguntar ---
def preguntar(pregunta: str):
    print(f"\n🧠 Pregunta: {pregunta}")
    respuesta = rag_chain.invoke(pregunta)
    print("💬 Respuesta:", respuesta.content.strip())

# --- 8. Ejemplo de uso ---
if __name__ == "__main__":
    preguntar("¿De qué trata el documento?")
    preguntar("¿Qué conclusiones se mencionan?")
