from data.Modulo_Language import get_text
from data.Modulo_Notas import (data_Nota, read_Nota, save_Nota, get_list as Nota_get_list)
from data.interface_data import file_icon, file_font

from interface.Modulo_Util_Qt import Dialog_TextEdit, Dialog_InputDirFile
from interface.interface_number import *
from interface.css_util import *

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




class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle('Notas')
        self.setWindowIcon( QIcon( file_icon ) )
        self.resize( nums_win_main[0], nums_win_main[1] )
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones verticales - Botones - Notas; Editar nuevo y remover
        list_option = ['new_note', 'edit_note', 'remove_note']
        for option in list_option:
            button = QPushButton( get_text(option) )
            button.clicked.connect( partial(self.note_new_edit_remove, option=option) )
            vbox_main.addWidget( button )
        
        # Seccion vertical boton cambiar directorio de nota
        button = QPushButton( get_text('change_main_dir') )
        button.clicked.connect( self.change_main_dir )
        vbox_main.addWidget( button)
        
        # Fin mostrar todo
        self.show()
    
    def note_new_edit_remove(self, option=str):
        self.hide()
        
        # Agregar nota, y despues ver notas disponibles
        if option == 'new_note':
            note, ok = QInputDialog.getText(
                self,
                get_text(option), # Titulo
                f"{get_text('name')}:"
            )
            if ok and note:
                # Agregar nota
                save_Nota( data_Nota, save=note )
                Dialog_TextEdit( self, text=data_Nota.note, edit=True, size=nums_win_text_edit ).exec()

        else:
            # Editar o remover nota
            Dialog_edit_remove_note( self, option=option ).exec()

        self.show()
    
    def change_main_dir(self):
        self.hide()

        # Dialogo para establecer nuevo directorio
        dialog = Dialog_InputDirFile(
            self, 
            title=get_text('change_main_dir'), label=get_text('dir'), entry=data_Nota.path,
            mode='set_dir', size=nums_win_input
        )
        dialog.exec()

        # Establecer directorio
        new_dir = dialog.get_input()
        if isinstance( new_dir, str ):
            data_Nota.path = new_dir
            save_Nota( data_Nota )
        
        self.show()




class Dialog_edit_remove_note(QDialog):
    def __init__( self, parent=None, option='edit_note' ):
        super().__init__(parent)
        
        self.setWindowTitle( get_text(option) )
        self.resize( nums_win_edit_remove[0], nums_win_edit_remove[1] )
        self.option = option
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Sección vertical - Ultima nota | solo si esta en la opcion editar nota
        if option == 'edit_note':
            button = QPushButton( get_text('last_note') )
            button.clicked.connect( self.edit_last_note )
            vbox_main.addWidget(button)
        
        
        # Secciones vertical - scroll - Opciones/Notas
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll.setWidgetResizable(True)
        vbox_main.addWidget(self.scroll)
        
        # Scroll - Contenedor de widgets
        scroll_widget = QWidget()
        self.scroll_vbox = QVBoxLayout()
        scroll_widget.setLayout(self.scroll_vbox)
        
        # Scroll - Notas
        self.list_button = []
        self.update_scroll()
        
        # Scroll - Agregar el contenedor
        self.scroll.setWidget( scroll_widget )
        

        # Sección vertical - Entry - Busqueda de notas
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        label = QLabel( get_text('search') )
        hbox.addWidget(label)

        self.entry = QLineEdit()
        self.entry.textChanged.connect(self.search_note)
        hbox.addWidget(self.entry)
        
        # Fin - Mostrar todo
        self.show()
    

    def edit_last_note(self):
        # Leer/Editar la ultima nota
        read_Nota( data_Nota )
        if isinstance( data_Nota.note, str):
            Dialog_TextEdit( self, text=data_Nota.note, edit=True, size=nums_win_text_edit ).exec()
    

    def update_scroll(self):
        # Scroll | Quitar todos los widgets del layaut | Quitar items de la lista
        for i in reversed( range(self.scroll_vbox.count()) ):
            self.scroll_vbox.itemAt(i).widget().setParent(None)
        self.list_button.clear()
        
        # Scroll | Agregar botones al layout | Notas a seleccionar
        for note in Nota_get_list( data_Nota ):
            button = QPushButton( note )
            button.clicked.connect(
                partial(self.edit_remove_note, note=note )
            )
            self.scroll_vbox.addWidget(button)
            self.list_button.append(button)
    

    def edit_remove_note(self, note=None):
        # Editar o remover nota
        if self.option == 'edit_note':
            # Leer/Editar nota seleccionada
            data_Nota.last_note=note
            save_Nota( data_Nota )
            Dialog_TextEdit( self, text=data_Nota.note, edit=True, size=nums_win_text_edit ).exec()
        elif self.option == 'remove_note':
            # Remover Nota seleccionada
            message_box_question = QMessageBox.question(
                self,
                get_text('remove_note'),
                get_text('remove_note'),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if message_box_question == QMessageBox.StandardButton.Yes:
                # Eliminar una nota
                if save_Nota( data_Nota, remove=note ) == True:
                    # Se pudo remover
                    QMessageBox.information(
                        self,
                        get_text('remove_note'),
                        get_text('remove_good'),
                        QMessageBox.StandardButton.Ok
                    )
                    #self.close()
                else:
                    # No se pudo remover
                    QMessageBox.critical(
                        self,
                        get_text('remove_note'),
                        get_text('remove_not_good')
                    )

        # Actualizar botones/notas disponibles
        self.update_scroll()
    

    def search_note(self):
        # Texto de entry
        text = self.entry.text().lower()
        
        if isinstance(text, str):
            # Recorrer los botones y dar focus el mas cercano por inicial
            for button in self.list_button:
                if button.text().lower().startswith(text):
                    button.setFocus()
                    self.scroll.ensureWidgetVisible(button)
                    self.entry.setFocus()




# Estilo de programa
qss_style = ''
for widget in get_list_text_widget('Qt'):
    if widget == 'QTextEdit':
        qss_style += text_widget_style( 
            widget=widget, font=file_font, font_size=num_font, 
            margin_based_font=True, padding=None, idented=4
        )
    else:
        qss_style += text_widget_style( 
            widget=widget, font=file_font, font_size=num_font, 
            margin_xy=nums_margin_xy, padding=num_space_padding, idented=4
        )
print(qss_style)


# Bucle del programa
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss_style)
    window = Window_Main()
    sys.exit(app.exec())