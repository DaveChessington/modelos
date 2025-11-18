from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import logging


# Silenciar logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

# Cargar variables de entorno
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class ChatMemoria:
    def __init__(self,input_inicial="Eres un asistente útil y recuerdas la conversación anterior."):  
        # Modelo
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

        # Prompt con espacio para el historial
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",input_inicial),
            ("placeholder", "{history}"),
            ("human", "{input}")
        ])

        # Crear la memoria
        self.memory = ConversationBufferMemory(return_messages=True)
    
    def ejecutar_con_memoria(self,texto):
        """Ejecuta el modelo conservando la memoria entre llamadas."""
        # Cargar historial previo desde la memoria
        self.history = self.memory.load_memory_variables({}).get("history", [])
        
        # Crear el chain moderno (RunnableSequence)
        chain = self.prompt | self.llm
        
        # Invocar el modelo con historial e input actual
        response = chain.invoke({"history": self.history, "input": texto})
        
        # Guardar el intercambio actual en la memoria
        self.memory.save_context({"input": texto}, {"output": response.content})
        
        # Retornar texto limpio
        return response.content.strip()

    def chat(self):
        while True:
            prompt=input("Tú: ")
            if prompt.strip().lower()=="salir":
                break
            print("IA: ",self.ejecutar_con_memoria(prompt))

ChatMemoria().chat()
