# Nota functions
from views.dialogs.qt import SetItemDialog
from models.nota_model import NotaModel
from controllers.nota_controller import NotaController
from core.nota_repository import NotaRepository

nota_model = NotaModel()
nota_repository = NotaRepository()
nota_controller = NotaController( nota_model, nota_repository )

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
        
        # TextEdit
        self.set_textedit()

        # Actions
        self.actionLastNota.triggered.connect( self.on_last_nota )
        self.actionNew.triggered.connect(self.on_new)
        self.actionOpen.triggered.connect(self.on_open)
        self.actionSave.triggered.connect(self.on_save)
        self.actionRemove.triggered.connect(self.on_remove)

    def set_textedit(self):
        self.textedit.setText( nota_model.text )

    def on_open(self, signal):
        set_item_dialog = SetItemDialog( self, items=nota_controller.list_nota(), checkable=False )
        set_item_dialog.exec()
        item = set_item_dialog.get_item()
        if isinstance(item, str):
            nota_model.last_nota = item
            nota_controller.set_config()
            nota_controller.load()
            self.set_textedit()

    def on_save(self):
        nota_model.text = self.textedit.toPlainText()
        nota_controller.save()

    def on_new(self, signal):
        nota, ok = QInputDialog.getText(self, get_text('new-nota'), get_text('name'))
        if nota and ok:
            nota_model.last_nota = nota
            nota_model.text = ""
            nota_controller.save()
            nota_controller.read()
            self.set_textedit()

    def on_last_nota(self):
        nota_controller.load()
        self.set_textedit()

    def on_remove(self):
        set_item_dialog = SetItemDialog( self, items=nota_controller.list_nota(), checkable=False )
        set_item_dialog.exec()
        item = set_item_dialog.get_item()
        if isinstance(item, str):
            nota_controller.remove( item )
            self.set_textedit()




# Bucle del programa
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec())
