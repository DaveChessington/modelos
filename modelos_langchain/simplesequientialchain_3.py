from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging

# Silenciar logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

# Cargar API Key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class SimpleSequentialChain:
    def __init__(self):
        # Modelo
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    def encadenar(self,input_inicial,prompt_1,prompt_2):
        # Prompts (usar {input}, no {texto})
        self.prompt_1 = PromptTemplate.from_template(prompt_1+" {input}")
        self.prompt_2 = PromptTemplate.from_template(prompt_2+" {input}")

        # Encadenamiento moderno con Runnables (sin LLMChain)
        self.chain = self.prompt_1 | self.llm | self.prompt_2 | self.llm

        # Ejecutar pasando directamente texto (no diccionario)
        self.resultado = self.chain.invoke(input_inicial)

        # Obtener texto limpio
        texto_final = self.resultado.content if hasattr(self.resultado, "content") else str(self.resultado)

        return texto_final.strip()

input_inicial="Serie de One punch man"
prompt1="resume la primera temporada"
prompt2="traduce al japones con subtitulos en inglés"

print(SimpleSequentialChain().encadenar(input_inicial,prompt1,prompt2))