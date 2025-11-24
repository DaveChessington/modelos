#pip uninstall -y langchain langchain-core langchain-community langchain-google-genai
#pip cache purge
#pip install langchain==0.2.17 langchain-core==0.2.43 langchain-community==0.2.17 langchain-google-genai==1.0.7 faiss-cpu pypdf python-dotenv
#pip install sentence-transformers

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# --- Cargar API Key de Gemini (solo para el modelo generativo) ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class Rag:
    def __init__(self,
                 input_inicial='''Usa el siguiente contexto para responder la pregunta del usuario.
Si no hay suficiente información, responde: "No tengo información suficiente en el documento."
''',
documento=r"documentos\reglamento_interno.pdf",ai="google"):
        # --- 4. Modelo LLM (Gemini solo para generación, no embeddings) ---
        # Modelo
        if ai.strip().lower()=="google":
            os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
            self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        else:
            os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            self.llm = ChatOpenAI(
            model="gpt-4.1",   # o el que quieras: gpt-4.1, gpt-4.1-preview, o3-mini...
            temperature=0.7
            )
        # --- 5. Prompt ---
        template = """
        {input}
        Contexto:
        {context}
        Pregunta:
        {question}
        """
        self.prompt = ChatPromptTemplate.from_template(template)

        self.procesar_documento(documento)

        # --- 6. Construir el RAG Chain moderno ---
        self.rag_chain = (
            {"input":RunnableLambda(lambda _: input_inicial),"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )

    # --- 7. Función para preguntar ---
    def preguntar(self,pregunta: str):
        respuesta = self.rag_chain.invoke(pregunta)
        #print(respuesta.content)
        return "Respuesta IA:"+respuesta.content.strip()

    def procesar_documento(self,pdf_path):
        # --- 1. Cargar documento ---
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        print(f"Documento cargado con {len(pages)} páginas")

        # --- 2. Dividir texto ---
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(pages)
        print(f"Texto dividido en {len(docs)} fragmentos")

        # --- 3. Crear embeddings locales ---
        print("Generando embeddings locales con HuggingFace (esto puede tardar unos segundos la primera vez)...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Crear o cargar índice FAISS (para no recalcular embeddings cada vez)
        INDEX_PATH = "faiss_local_index"

        if os.path.exists(INDEX_PATH):
            print("Cargando índice FAISS existente...")
            vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        else:
            print("Creando índice FAISS nuevo...")
            vectorstore = FAISS.from_documents(docs, embedding=embeddings)
            vectorstore.save_local(INDEX_PATH)

        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def chat(self):
        while True:
            prompt=input("Tú: ")
            if prompt.strip().lower()=="salir":
                break
            print(self.preguntar(prompt))

# --- Ejemplo de uso ---
"""
if __name__ == "__main__":
    chat=Rag()
    chat.chat()"""
 