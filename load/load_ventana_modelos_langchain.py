#pip install pyqt5 o pysite
from PyQt5 import QtWidgets,uic,QtCore
from PyQt5.QtCore import QPropertyAnimation
from modelos_langchain.llmchain_1 import AsistenteTematico
from modelos_langchain.sequientialchain_2 import CadenaSecuencial
from modelos_langchain.simplesequientialchain_3 import SimpleSequentialChain
from modelos_langchain.parseo_4 import Parse
from modelos_langchain.varios_pasos_5 import ParseSteps
from modelos_langchain.memoria_6 import ChatMemoria
from modelos_langchain.persistencia_7 import ChatMemoriaArchivo
from modelos_langchain.rag_8 import Rag

class Load_ventana_modelos_Langchain(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        #Cargar la interfaz
        uic.loadUi(r"interfaces\ventana_modelos_langchain.ui",self)


        #lista de prompts para ej 5
        self.prompts=[]
        #Maximizar VEntana
        
        #self.showMaximized()
        
        #self.actionSalir.triggered.connect(self.cerrarVentana)

        #3.- Configurar contenedores
        
        #eliminar barra y de titulo - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Cerrar ventana
        self.boton_cerrar.clicked.connect(lambda: self.close())
        # mover ventana
        self.frame_superior.mouseMoveEvent = self.mover_ventana
        #menu lateral
        self.boton_menu.clicked.connect(self.mover_menu)
    
        #Botones para cambiar de página
        self.boton_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.llmchain1))
        self.boton_enviar.clicked.connect(lambda: self.llmchain())
        self.boton_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.sequentialchain2))
        self.boton_enviar_2.clicked.connect(lambda: self.sequentialchain())
        self.boton_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.simplesequentialchain3))
        self.boton_enviar_3.clicked.connect(lambda: self.simplesequentialchain())
        self.boton_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.parseo4))
        self.boton_enviar_4.clicked.connect(lambda: self.parse())
        self.boton_5.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.varios_pasos5))
        self.agregar_prompt.clicked.connect(lambda: self.agregar_prompts())
        self.boton_enviar_5.clicked.connect(lambda: self.varios())
        self.boton_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.memoria6))
        ia=ChatMemoria()
        self.boton_enviar_6.clicked.connect(lambda: self.memoria_chat(ia))
        self.boton_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.persistencia7))
        
        self.cargar_archivo.clicked.connect(lambda: self.browse_file())
        self.boton_enviar_7.clicked.connect(lambda: self.memoria_archivo())
        
        self.boton_8.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.rag8))
        self.load_file.clicked.connect(lambda: self.browse_pdf())
        self.boton_enviar_8.clicked.connect(lambda: self.rag())

    def llmchain(self):
        contexto=self.input_contexto.text()
        tema=self.input_tema.text()
        ia=AsistenteTematico(contexto)
        respuesta=ia.preguntar_tema(tema)
        self.output_response.setText(respuesta)

    def sequentialchain(self):
        contexto=self.input_contexto_2.text()
        prompt_1=self.input_instruccion_1.text()
        prompt_2=self.input_instruccion_2.text()
        ia=CadenaSecuencial()
        respuesta=ia.encadenar(contexto,prompt_1,prompt_2)
        self.output_response_2.setText(respuesta)

    def simplesequentialchain(self):
        contexto=self.input_contexto_3.text()
        prompt_1=self.input_prompt_1.text()
        prompt_2=self.input_prompt_2.text()
        ia=SimpleSequentialChain()
        respuesta=ia.encadenar(contexto,prompt_1,prompt_2)
        self.output_response_3.setText(respuesta)

    def parse(self):
        input_inicial=self.input_inicial_4.text()
        prompt=self.input_prompt_4.text()
        ia=Parse()
        respuesta=ia.parse_prompt(input_inicial,prompt)
        self.output_response_4.setText(respuesta)

    def agregar_prompts(self):
        prompt=self.new_prompt.text()
        self.prompts.append(prompt)
        self.show_prompts.append(f"<p style='color=#0d4599;'>{len(self.prompts)}.-{prompt}</p>")

    def varios(self):
        input_inicial=self.input_inicial_5.text()
        ia=ParseSteps()
        respuesta=ia.parse_prompts(input_inicial,self.prompts)
        self.output_response_5.setText(respuesta)
        self.show_prompts.setText("")
        self.prompts=[]

    def memoria_chat(self,modelo:ChatMemoria):
        pregunta=self.input_mensaje.text()
        self.output_response_6.append(
        f"<p style='color:#B85D28;'><b>Tú:</b> {pregunta}</p>"
        )
        if pregunta=="salir":
            self.output_response_6.setText("")
            return
        respuesta=modelo.ejecutar_con_memoria(pregunta)
        self.output_response_6.append(
        f"<p style='color:#5E618C;'><b>Chatbot:</b> {respuesta}</p>"
        )

    def browse_file(self):
        # This is where the dialog is created and shown dynamically
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.', 'All Files (*.*)')
        
        if filename:
            # Update the QLineEdit designed in Qt Designer
            self.lineEditPath.setText(filename)
            print(filename)
            self.memoria_file=ChatMemoriaArchivo(filename)
            """self.memoria_file.MEMORY_FILE=filename
            print(self.memoria_file.MEMORY_FILE)
            self.memoria_file.cargar_memoria()"""

    def memoria_archivo(self):
        print("sent")
        mensaje=self.input_mensaje_7.text()
        self.output_response_7.append(f"<p style='color:#B85D28;'><b>Tú:</b> {mensaje}</p>"
        )
        respuesta=self.memoria_file.ejecutar_con_memoria(mensaje)
        self.output_response_7.append(f"<p style='color:#5E618C;'><b>Chatbot:</b> {respuesta}</p>")

    def browse_pdf(self):
        # This is where the dialog is created and shown dynamically
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.', 'All Files (*.*)')
        
        if filename:
            # Update the QLineEdit designed in Qt Designer
            self.pdf_path.setText(filename)
            print(filename)
            self.ia_pdf=Rag(documento=filename)

    def rag(self):
        print("sent")
        mensaje=self.input_pregunta_pdf.text()
        self.output_response_8.append(f"<p style='color:#B85D28;'><b>Tú:</b> {mensaje}</p>"
        )
        respuesta=self.ia_pdf.preguntar(mensaje)
        self.output_response_8.append(f"<p style='color:#5E618C;'><b>Chatbot:</b> {respuesta}</p>")

    # 6.- mover ventana
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def mover_ventana(self, event):
        if self.isMaximized() == False:			
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <=20:
            self.showMaximized()
        else:
            self.showNormal()
    
    #7.- Mover menú
    def mover_menu(self):
        if True:			
            width = self.frame_lateral.width()
            widthb = self.boton_menu.width()
            normal = 0
            if width==0:
                extender = 200
                self.boton_menu.setText("Menú")
            else:
                extender = normal
                self.boton_menu.setText("")
                
            self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()
            
            self.animacionb = QPropertyAnimation(self.boton_menu, b'minimumWidth')
            self.animacionb.setStartValue(width)
            self.animacionb.setEndValue(extender)
            self.animacionb.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacionb.start()

