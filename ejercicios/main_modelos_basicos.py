from modelos_basicos.modeloBasico import ModeloOpenAI,ModeloGemini
from modelos_basicos.modeloHistorial import ModeloHistorialOpenAI,ModeloHistorialGemini


def main():
    #ModeloOpenAI().modeloSimple(pregunta=input("Pregunta a open ai:"))
    #ModeloGemini().modeloSimple(pregunta=input("Pregunta a gemini:"))
    #odeloHistorialOpenAI().modeloHistorial(3)
    #ModeloHistorialGemini().modeloHistorial(3)
    #ModeloHistorialGemini().historial(input("Pregunta a gemini:"),n_historial=4)
    ModeloHistorialOpenAI().historial_2(input("Pregunta a gemini:"),n_historial=4)
    

if "__main__"==__name__:
    main()


