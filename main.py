# Nota functions
from models.nota_model import NotaModel
from controllers.nota_controller import NotaController

nota_model = NotaModel()
nota_controller = NotaController( nota_model )

#nota_model.last_nota = "Necesito uno de esos"
#nota_model.text = "Yo necesito unos tecates y aguacate."
#nota_controller.save()

print( nota_model.last_nota )
print( nota_model.text )
print( nota_controller.list_nota() )


# GUI
from config.paths import ICON_FILE, MYAPP_UI_FILE
import sys, os
from functools import partial
from PyQt6.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog

)
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt



def get_text(text):
    return text.replace(' ', '-').replace('_', '-').lower()




class MyApp(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle( get_text('CM Notas') )
        self.setWindowIcon( QIcon( str(ICON_FILE) ) )
        self.resize( 256, 256 )
        uic.loadUi( MYAPP_UI_FILE, self )
        
        # Contenedor principal
        self.textedit.setText( nota_model.text )
        '''
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones verticales - Botones - Notas; Editar nuevo y remover
        list_option = ['new_note', 'edit_note', 'remove_note']
        for option in list_option:
            button = QPushButton( get_text(option) )
            vbox_main.addWidget( button )
        
        # Seccion vertical boton cambiar directorio de nota
        button = QPushButton( get_text('change_main_dir') )
        vbox_main.addWidget( button)
        '''


# Bucle del programa
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec())
