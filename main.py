# Nota functions
from models.nota_model import NotaModel
from controllers.nota_controller import NotaController

nota_model = NotaModel()
nota_controller = NotaController( nota_model )

print(nota_model.text)

print( nota_controller.list_nota() )


# GUI
from config.paths import ICON_FILE
import sys, os
from functools import partial
from PyQt6.QtWidgets import(
    QApplication,
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
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt



def get_text(text):
    return text.replace(' ', '-').replace('_', '-').lower()




class WindowMain(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle( get_text('CM Notas') )
        self.setWindowIcon( QIcon( str(ICON_FILE) ) )
        self.resize( 256, 256 )
        
        # Contenedor principal
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
        
        # Fin mostrar todo
        self.show()


# Bucle del programa
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowMain()
    sys.exit(app.exec())
