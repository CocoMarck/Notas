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
        
        # TextEdit
        self.set_textedit()

        self.actionOpen.triggered.connect(self.on_open)

    def set_textedit(self):
        self.textedit.setText( nota_model.text )

    def on_open(self, signal):
        set_item_dialog = SetItemDialog( self, items=nota_controller.list_nota(), checkable=False )
        set_item_dialog.exec()
        item = set_item_dialog.get_item()
        if isinstance(item, str):
            print(item)
            nota_model.last_nota = item
            nota_controller.set_config()
            nota_controller.load()
            self.set_textedit()

    def on_save(self):
        nota_model.text = self.textedit.toPlainText()
        nota_controller.save()



class SetItemDialog( QDialog ):
    def __init__(
        self, parent=None, size=[256, 256], text_dict={
            "title": "Set something",
            "ok": "Ok",
            "cancel": "Cancel",
            'search': 'Search'
        },
        items=[], checkable=False, search=True
    ):
        super().__init__(parent)

        self.setWindowTitle( text_dict['title'] )
        self.resize( 256, 256 )

        # Contenedor principal
        self.main_layout = QVBoxLayout()
        self.setLayout( self.main_layout )

        # Scroll de botones
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )
        self.scroll_area.setWidgetResizable(True) # Para centrer el scroll
        self.main_layout.addWidget( self.scroll_area )

        # Scroll/Widget, contenedor de botones
        self.selected_items = []
        self.checkable = checkable
        self.widget_buttons = QWidget()
        self.widget_buttons_vbox = QVBoxLayout()
        self.widget_buttons.setLayout( self.widget_buttons_vbox )

        self.items = items
        self.button_dict = {}
        for i in self.items:
            button = QPushButton( str(i) )
            button.setCheckable(checkable)
            if self.checkable == False:
                button.clicked.connect( partial(self.on_button_item, button=button) )
            self.button_dict.update( {button: i} )
            self.widget_buttons_vbox.addWidget( button )

        self.scroll_area.setWidget( self.widget_buttons )

        # Buscar
        self.search = search
        if self.search:
            self.line_edit_search = QLineEdit(self, placeholderText=text_dict['search'] )
            self.line_edit_search.textChanged.connect(self.on_search)
            self.main_layout.addWidget(self.line_edit_search)

        # Aceptar o cancelar
        self.text_dict = text_dict
        hbox = QHBoxLayout()
        button_options = ['cancel']
        if self.checkable:
            button_options = ['ok', 'cancel']
        for option in button_options:
            hbox.addStretch()
            button = QPushButton( self.text_dict[option] )
            if option == 'ok':
                button.clicked.connect( self.get_item )
            elif option == 'cancel':
                button.clicked.connect( self.close )
            hbox.addWidget( button )
            hbox.addStretch()
        self.main_layout.addLayout(hbox)


    def on_button_item(self, button):
        self.selected_items = []
        if self.checkable:
            for button in self.button_dict.keys():
                if button.isChecked():
                    self.selected_items.append( self.button_dict[button] )
        else:
            self.selected_items = self.button_dict[button]
            self.close()


    def on_search(self, text):
        lower_text = text.lower()
        if not lower_text:
            return
        for button in self.button_dict.keys():
            if button.text().lower().startswith(lower_text):
                button.setFocus()
                self.scroll_area.ensureWidgetVisible(button)
                self.line_edit_search.setFocus()
                break


    def get_item(self):
        if self.selected_items == []:
            return None
        else:
            return self.selected_items




# Bucle del programa
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec())
