from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging


# Silenciar mensajes de gRPC / Google
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)

# Cargar API Key de Gemini desde .env
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class AsistenteTematico():
    def __init__(self,contexto):

        # Inicializar Google Gemini
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.7
        )
        # Crear el prompt
        self.prompt = PromptTemplate(
            input_variables=["tema"],
            template=contexto+"{tema}."
        )

        # Nueva forma (con tubería)
        self.chain = self.prompt | self.llm

    def preguntar_tema(self,tema):
        # Ejecutar
        respuesta = self.chain.invoke({"tema": tema})
        print(respuesta.content)
        return respuesta.content
