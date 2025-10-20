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

# Inicializar Google Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.7
)
# Crear el prompt
prompt = PromptTemplate(
    input_variables=["tema"],
    template="Explícale a un estudiante universitario el tema {tema}."
)

# Nueva forma (con tubería)
chain = prompt | llm

# Ejecutar
respuesta = chain.invoke({"tema": "el aprendizaje automático"})
print(respuesta.content)
