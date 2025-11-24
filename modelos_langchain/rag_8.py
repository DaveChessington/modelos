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
                documento=r"documentos\reglamento_interno.pdf",
                input_inicial='''Usa el siguiente contexto para responder la pregunta del usuario.
Si no hay suficiente información, responde: "No tengo información suficiente en el documento."
''',ai="google"):
        # --- 4. Modelo LLM (Gemini solo para generación, no embeddings) ---
        # Modelo
        print(documento)
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
        print("precesando documento")
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
        return respuesta.content.strip()

    def procesar_documento(self, pdf_path):
        print("PDF:", pdf_path)

        # Crear carpeta de índices si no existe
        INDEX_DIR = "indices"
        os.makedirs(INDEX_DIR, exist_ok=True)

        # 1. Cargar PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        print(f"Documento cargado con {len(pages)} páginas")

        # 2. Dividir en fragmentos
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = splitter.split_documents(pages)
        print(f"Texto dividido en {len(docs)} fragmentos")

        # 3. Embeddings
        print("Generando embeddings locales...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # 4. Nombre del índice basado en el PDF
        base = os.path.splitext(os.path.basename(pdf_path))[0]

        # --- AQUÍ LE INDICAS LA CARPETA ---
        INDEX_PATH = os.path.join(INDEX_DIR, f"faiss_index_{base}")

        # 5. Crear o cargar FAISS
        if os.path.isdir(INDEX_PATH) and \
   os.path.exists(os.path.join(INDEX_PATH, "index.faiss")) and \
   os.path.exists(os.path.join(INDEX_PATH, "index.pkl")):
            print("Cargando índice FAISS existente...")
            vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        else:
            print("Creando índice FAISS nuevo...")
            vectorstore = FAISS.from_documents(docs, embedding=embeddings)
            vectorstore.save_local(INDEX_PATH)

        # 6. Crear el retriever
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def chat(self):
        while True:
            prompt=input("Tú: ")
            if prompt.strip().lower()=="salir":
                break
            print("respuesta IA: "+self.preguntar(prompt))

# --- Ejemplo de uso ---

if __name__ == "__main__":
    chat=Rag(documento="C:/Users/David-PC/Downloads/Becas Excelencia.pdf")
    chat.chat()
 