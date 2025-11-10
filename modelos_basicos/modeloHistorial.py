from openai import OpenAI
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

class ModeloHistorialOpenAI:
    def __init__(self,n_historial=None):
        key=os.getenv("OPENAI_API_KEY")
        self.cliente=OpenAI(api_key=key)
        self.historial=[{"role":"system","content":
                "Eres un sistema util y amigable"}]
        self.n_pregunta=1
        self.n_historial=n_historial
        self.restantes=n_historial

    def memoria(self,pregunta):

        if pregunta.lower()=="salir":
            return ("chatbot terminado")
        
        self.historial.append({"role":"user","content":pregunta})

        respuesta=self.cliente.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.historial
        )
        respuesta_chatbot=respuesta.choices[0].message.content
        
        self.historial.append({"role":"assistant", "content": respuesta_chatbot})

        if self.restantes==0:
            self.historial=[]
            self.n_pregunta=1
            self.restantes=self.n_historial
            return(f"{respuesta_chatbot}<br> <p style='color:#B85D28;'> <p>Se borró el historial</p>")
        
        else:
            self.n_pregunta+=1
            try:
                self.restantes-=1
            except:
                pass
            return (f"{respuesta_chatbot}")
            
            

   

