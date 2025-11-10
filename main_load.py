from PyQt5 import QtWidgets,uic
from load.load_ventana_principal import Load_ventana_principal
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ventana = Load_ventana_principal()
    ventana.show()
    sys.exit(app.exec_())