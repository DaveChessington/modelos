from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging


from langchain_openai import ChatOpenAI

# Silenciar logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)


# Cargar API Key
load_dotenv()
#os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class CadenaSecuencial():
    def __init__(self):
        # Modelo
        #self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",   # o el que quieras: gpt-4.1, gpt-4.1-preview, o3-mini...
            temperature=0.7
        )

    def encadenar(self,input_inicial,prompt1,prompt2):
        self.prompt1=PromptTemplate.from_template(prompt1+" {input}")
        self.prompt2=PromptTemplate.from_template(prompt2+" {input}")

        chain1=self.prompt1 | self.llm
        chain2=self.prompt2 | self.llm
        self.chain= chain1 | chain2
        self.resultado=self.chain.invoke(input_inicial)     

        return self.resultado.content if hasattr(self.resultado, "content") else str(self.resultado)      

input_inicial="Eres un profesor univesitario"
prompt1="Explica el tema de langchain a un grupo de la materia de IA considerando"
prompt2="Resume en una frase"

print(CadenaSecuencial().encadenar(input_inicial,prompt1,prompt2))