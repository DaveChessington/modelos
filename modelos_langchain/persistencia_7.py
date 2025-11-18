import os, json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# --- Configuración ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class ChatMemoriaArchivo:
    def __init__(self,archivo_memoria="modelos_langchain\memoria.json",input_inicial="Eres un asistente amable que recuerda toda la conversación anterior."):
        
        # Modelo
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

        # Prompt con memoria
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", input_inicial),
            ("placeholder", "{history}"),
            ("human", "{input}")
        ])

        # Archivo donde se guardará la memoria
        self.MEMORY_FILE = archivo_memoria

        # Crear memoria
        self.memory = ConversationBufferMemory(return_messages=True)

        # Cargar memoria previa
        self.cargar_memoria()

    # --- Funciones de persistencia ---
    def guardar_memoria(self):
        """Guarda el historial en JSON serializando solo texto."""
        data = self.memory.load_memory_variables({})
        # Convertir los mensajes en texto plano
        history_text = []
        for msg in data.get("history", []):
            if hasattr(msg, "type") and hasattr(msg, "content"):
                history_text.append({"type": msg.type, "content": msg.content})
        with open(self.MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"history": history_text}, f, ensure_ascii=False, indent=2)

    def cargar_memoria(self):
        """Carga la memoria desde el archivo JSON si existe."""
        if os.path.exists(self.MEMORY_FILE):
            with open(self.MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for msg in data.get("history", []):
                    if msg["type"] == "human":
                        self.memory.chat_memory.add_user_message(msg["content"])
                    elif msg["type"] == "ai":
                        self.memory.chat_memory.add_ai_message(msg["content"])


    # --- Ejecutar con memoria persistente ---
    def ejecutar_con_memoria(self,texto):
        """Ejecuta el modelo conservando memoria entre sesiones."""
        history = self.memory.load_memory_variables({}).get("history", [])
        chain = self.prompt | self.llm
        response = chain.invoke({"history": history, "input": texto})
        self.memory.save_context({"input": texto}, {"output": response.content})
        self.guardar_memoria()  # 🔄 Guarda después de cada interacción
        return response.content.strip()
    

    def chat(self):
        while True:
            prompt=input("Tú: ")
            if prompt.strip().lower()=="salir":
                break
            print("IA: ",self.ejecutar_con_memoria(prompt))

# --- Prueba ---
ChatMemoriaArchivo().chat()
