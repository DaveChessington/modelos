from openai import OpenAI
from google import genai

from dotenv import load_dotenv
import os

load_dotenv()

class ModeloOpenAI:
    def __init__(self):
        key=os.getenv("OPENAI_API_KEY")
        print(key)
        self.cliente=OpenAI(api_key=key)

    def modeloSimple(self,pregunta):
        respuesta=self.cliente.chat.completions.create(model="gpt-4o-mini",
                            messages=[{'role':'user',
                             'content':pregunta}])
        print(respuesta.choices[0].message.content)

class ModeloGemini:
    def __init__(self):
        self.cliente=genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def modeloSimple(self,pregunta):
        print("Pregunta: "+pregunta)
        respuesta=self.cliente.models.generate_content(model="gemini-2.5-flash",contents=pregunta)
        print("respuesta: "+respuesta.candidates[0].content.parts[0].text)
        return respuesta.candidates[0].content.parts[0].text

