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

class CadenaSecuencial():
    def __init__(self):

        # Cargar API Key
        load_dotenv()
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        # Modelo
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    def encadenar(self,prompt1,prompt2):
        prompt1=PromptTemplate.from_template(prompt1)
        prompt2=PromptTemplate.from_template(prompt2)

        chain1=prompt1 | self.llm
        chain2=prompt2 | self.llm
        self.chain= chain1 | chain2
        resultado=self.chain.invoke()     

        return resultado.content if hasattr(resultado, "content") else str(resultado)      
