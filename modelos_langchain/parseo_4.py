from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import os
import logging

# Silenciar logs
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_CPP_VERBOSITY"] = "NONE"
logging.getLogger("absl").setLevel(logging.ERROR)
logging.getLogger("grpc").setLevel(logging.ERROR)



load_dotenv()

class Parse:
    def __init__(self,ai="google"):
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

    def parse_prompt(self,input_inicial,prompt):
        # Prompt
        self.prompt = PromptTemplate.from_template(
            prompt+" {input}"
        )

        # Parser para obtener texto limpio
        parser = StrOutputParser()

        # Encadenamiento moderno (RunnableSequence)
        self.chain = self.prompt | self.llm | parser

        # Ejecutar
        self.resultado = self.chain.invoke(input_inicial)

        return self.resultado

#print(Parse().parse_prompt("traduce al inglés","""Las ciencias de la computación son un campo de estudio que se enfoca en las bases teóricas de la información y la computación, así como en su aplicación para diseñar y desarrollar sistemas computacionales. El estudio abarca desde los algoritmos y la teoría de la computación hasta la inteligencia artificial, el hardware y el software, con el objetivo de resolver problemas complejos. """))