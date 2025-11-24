from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
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

class ParseSteps:
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

    def parse_prompts(self,input_inicial,prompts:list[str]):
        self.prompts=[]
        self.chain=RunnablePassthrough()
        for prompt in prompts:
            template=PromptTemplate.from_template(prompt+" {input}")
            self.prompts.append(template)
            self.chain=self.chain | template | self.llm
        self.chain= self.chain | StrOutputParser()
    

        self.resultado=self.chain.invoke(input_inicial)

        return self.resultado

input_inicial="""Las ciencias de la computación, también denominadas ciencias de la informática, son un conjunto de ciencias formales que estudian los fundamentos teóricos de la información y de la computación, así como sus aplicaciones prácticas en los sistemas de información y en los sistemas informáticos.[1]​[2]​[3]​
El cuerpo de conocimiento de las ciencias de la computación suele describirse como el estudio sistemático de los procesos algorítmicos que describen, transforman y representan información: su teoría, análisis, diseño, eficiencia, implementación y aplicación.[4]​
En un sentido más específico, la disciplina aborda el estudio formal de la factibilidad, la estructura, la expresión y la automatización de procedimientos metódicos (o algoritmos) que intervienen en la adquisición, representación, procesamiento, almacenamiento, comunicación y acceso a la información.
La información puede estar codificada en forma de bits dentro de la memoria de una computadora o representada en otros sistemas físicos o biológicos, como los genes y las proteínas en una célula.[5]​
Existen diversas ramas o disciplinas dentro de las ciencias de la computación; algunos resaltan los resultados específicos del cómputo (como los gráficos por computadora), mientras que otros (como la teoría de la complejidad computacional) se relacionan con propiedades de los algoritmos usados al realizar cómputo; y otros se enfocan en los problemas que requieren la implementación de sistemas informáticos. Por ejemplo, los estudios de la teoría de lenguajes de programación describen un cómputo, mientras que la programación de computadoras aplica lenguajes de programación específicos para desarrollar una solución a un problema computacional específico. Un computólogo se especializa en teoría de la computación y en el diseño e implementación de sistemas computacionales.[6]​
Según Peter J. Denning, la cuestión fundamental en que se basa la ciencia de la computación es: «¿Qué puede ser (eficientemente) automatizado?».[7]​"""

prompts=[
    "Resume este texto:",
    "Convierte el resumen en una lista:",
    "Traduce la lista al inglés:"
]

#print(ParseSteps().parse_prompts(input_inicial,prompts))