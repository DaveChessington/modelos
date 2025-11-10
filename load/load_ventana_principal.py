#pip install pyqt5 o pysite
from PyQt5 import QtWidgets,uic
from load.load_ventana_modelos_basicos import Load_ventana_modelos_basicos
from load.load_ventana_modelos_langchain import Load_ventana_modelos_Langchain

class Load_ventana_principal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #Cargar la interfaz
        uic.loadUi(r"interfaces\ventana_principal.ui",self)
        #Maximizar VEntana
        self.showMaximized()
        
        self.actionSalir.triggered.connect(self.cerrarVentana)
        self.actionBasicos.triggered.connect(self.abrirVentanaBasico)
        self.actionLangchain.triggered.connect(self.abrirVentanaLangchain)
    
    def cerrarVentana(self):
        self.close()

    def abrirVentanaBasico(self):
        self.basicos=Load_ventana_modelos_basicos()
        self.basicos.exec_()

    def abrirVentanaLangchain(self):
        self.langchain=Load_ventana_modelos_Langchain()
        self.langchain.exec_()







