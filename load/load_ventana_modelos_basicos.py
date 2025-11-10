#pip install pyqt5 o pysite
from PyQt5 import QtWidgets,uic,QtCore
from PyQt5.QtCore import QPropertyAnimation
import modelos_basicos.modeloBasico as model
import modelos_basicos.modeloHistorial as hist

class Load_ventana_modelos_basicos(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        #Cargar la interfaz
        uic.loadUi(r"interfaces\ventana_modelos_basicos.ui",self)
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
        self.boton_prompt.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_prompt))
        self.boton_enviar.clicked.connect(self.chat_prompt)
        self.boton_memoria.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_memoria))
        memoria=hist.ModeloHistorialOpenAI()
        self.boton_enviar_2.clicked.connect(lambda:self.chat_memoria(memoria))
        self.boton_chat.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_chat))
        historial=hist.ModeloHistorialOpenAI(n_historial=2)
        self.boton_enviar_3.clicked.connect(lambda:self.chat_historial(historial))
    
    def chat_prompt(self): 
        self.pregunta=self.input_prompt.text()
        modelo=model.ModeloGemini()
        respuesta=modelo.modeloSimple(self.pregunta)
        self.output_response.setText(respuesta)
        
    def chat_memoria(self,modelo):
        self.pregunta=self.input_prompt_2.text()
        self.output_response_2.append(
        f"<p style='color:#B85D28;'><b>Tú:</b> {self.pregunta}</p>"
        )
        if self.pregunta=="salir":
            self.output_response_2.setText("")
            return
        respuesta=modelo.memoria(self.pregunta)
        self.output_response_2.append(
        f"<p style='color:#5E618C;'><b>Chatbot:</b> {respuesta}</p>"
        )

    def chat_historial(self,modelo:hist.ModeloHistorialOpenAI):
        self.output_response_3.append(f"<br>{'Quedan '+ str(modelo.restantes)+' pregunta(s) para que se borre el historial'}")
        self.pregunta=self.input_prompt_3.text()
        self.output_response_3.append(
        f"<p style='color:#B85D28;'><b>{modelo.n_pregunta}.- Tú:</b> {self.pregunta}</p>"
        )
        if self.pregunta=="salir":
            self.output_response_3.setText("")
            return
        respuesta=modelo.memoria(self.pregunta)
        
        self.output_response_3.append(
        f"<p style='color:#5E618C;'><b>Chatbot:</b> {respuesta}</p>"
        )

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

