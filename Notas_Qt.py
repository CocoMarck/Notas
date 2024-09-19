from interface.Modulo_Util_Qt import(
    Dialog_TextEdit
)
from data.Modulo_Language import get_text as Lang
from data.Modulo_Notas import (data_Nota, read_Nota, save_Nota, file_icon, get_list as Nota_get_list)
import os


import sys
from pathlib import Path
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
    QHBoxLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Notas')
        self.setWindowIcon( QIcon( file_icon ) )
        self.resize(256, -1)

        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Secciones verticales - Botones
        button_new_note = QPushButton( Lang('new_note') )
        button_new_note.clicked.connect(self.evt_new_note)
        vbox_main.addWidget(button_new_note)

        button_edit_note = QPushButton( Lang('edit_note') )
        button_edit_note.clicked.connect(self.evt_edit_note)
        vbox_main.addWidget(button_edit_note)

        button_remove_note = QPushButton( Lang('remove_note') )
        button_remove_note.clicked.connect(self.evt_remove_note)
        vbox_main.addWidget(button_remove_note)

        button_change_main_dir = QPushButton( Lang('change_main_dir') )
        button_change_main_dir.clicked.connect(self.evt_change_main_dir)
        vbox_main.addWidget(button_change_main_dir)

        # Fin, Mostrar ventanta y los widgets agregados en ella.
        self.show()

    def evt_new_note(self):
        self.hide()
        Dialog_new_note(self).exec()
        self.show()

    def evt_edit_note(self):
        self.hide()
        Dialog_edit_remove_note(self, option='edit').exec()
        self.show()

    def evt_remove_note(self):
        self.hide()
        Dialog_edit_remove_note(self, option='remove').exec()
        self.show()

    def evt_change_main_dir(self):
        self.hide()
        Dialog_change_main_dir(self).exec()
        self.show()




class Dialog_new_note(QDialog):
    def __init__(
        self, parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle( Lang('new_note') )
        self.resize(308, 1)

        # Contenedor Pirncipal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Seccion Vertical - Entry para Establecer el nombre de la Notas
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)

        label_new_note = QLabel( f'{Lang("name")}:')
        hbox.addWidget(label_new_note)

        hbox.addStretch()

        self.entry_new_note = QLineEdit(
            self,
            placeholderText=Lang('text')
        )
        hbox.addWidget(self.entry_new_note)
        hbox.setStretchFactor(self.entry_new_note, 1)

        # Separar widgets
        vbox_main.addStretch()

        # Seccion Vertical fina - Boton aceptar
        button_save_note = QPushButton(Lang('save_note'))
        button_save_note.clicked.connect(self.evt_save_note)
        vbox_main.addWidget(button_save_note)

        # Fin, Mostrar ventanta y sus widgets agregados
        self.show()

    def evt_save_note(self):
        # Nota a guardar
        note = self.entry_new_note.text()
        if note =='':
            # Si no se escribio nada, la nota sera 'texto'
            note='texto'
        else:
            # Normal, la nota es correcta
            pass

        # Crear o no el archivo necesario
        save_Nota( data_Nota, save=note )
        note_save_or_not = data_Nota.note
        if type(note_save_or_not) is str:
            # Abrir archivo con un editor de texto
            self.hide()
            Dialog_TextEdit(
                self,
                text=note_save_or_not,
                edit=True
            ).exec()
            self.show()

        elif type(note_save_or_not) is list:
            # El texto creado ya existe, y abrirlo con un editor de texto

            # Mostrar mensaje de info de que ya existe.
            message_box = QMessageBox(self)
            message_box.setWindowTitle(Lang('save_note'))
            message_box.setText( Lang('this_file_exists') )
            message_box.exec()

            # Abrir el texto con un editor de texto
            self.hide()
            Dialog_TextEdit(
                self,
                text=note_save_or_not[1],
                edit=True
            ).exec()
            self.show()

        else:
            # Fallo en la creación del archivo
            # O El input tiene caracteres erroneos
            # Hay un Error
            pass

        self.close()
        
        


class Dialog_edit_remove_note(QDialog):
    def __init__(self, parent=None, option = 'edit'):
        super().__init__(parent)
        
        self.setWindowTitle( Lang('edit_note') )
        self.resize(256, 256)
        
        self.mode = option
        
        # Contenedor Pirncipal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Secciones Verticales - Botones
        # Scroll
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setWidgetResizable(True) # Para centrar el scroll
        vbox_main.addWidget(scroll_area)
        
        # Scroll - Contenedor de Widgets
        widget_buttons = QWidget()
        
        # Scroll - Layout
        self.widget_vbox = QVBoxLayout()
        widget_buttons.setLayout(self.widget_vbox)
        
        # Scroll - Layout - Botones en orden vertical
        self.list_buttons = []
        self.update_scroll()

        
        # Scroll - Agregar el Contenedor
        scroll_area.setWidget(widget_buttons)

        # Fin, Mostrar ventanta y sus widgets agregados
        self.show()
    
    
    def update_scroll( self ):
        # Scroll | Quitar todos los widgets del layout 
        for i in reversed(range(self.widget_vbox.count())): 
            self.widget_vbox.itemAt(i).widget().setParent(None)
    
        # Scroll | Si esta en modo editar agregar boton de ultima nota accedida
        if self.mode == 'edit':
            button_last_note = QPushButton( Lang('last_note') )
            button_last_note.clicked.connect(self.evt_last_note)
            self.widget_vbox.addWidget(button_last_note)

        # Scroll | Agregar todos los botones al layout
        self.list_buttons = []
        list_note = Nota_get_list( data_Nota )
        for index in range( 0, len(list_note) ):
            self.list_buttons.append( QPushButton( list_note[index] ) )
            self.list_buttons[index].clicked.connect(
                partial(self.evt_set_note, button=self.list_buttons[index])
            )
            self.widget_vbox.addWidget(self.list_buttons[index])
            
            
    def evt_last_note(self):
        # Editar ultimo texto creado
        read_Nota( data_Nota )
        if type(data_Nota.note) is str:
            # El texto existe y se editara con un TextView
            Dialog_TextEdit(
                self,
                text=data_Nota.note,
                edit=True
            ).exec()
        elif data_Nota.note == None:
            # Mostrar mensaje de info de que no existe.
            QMessageBox.critical(
                self,
                'ERROR', # Titulo   
                Lang('no_note') # Texto de ventana
            )
            
            
    def evt_set_note(self, button=QPushButton):
        # Remover o establecer ultima nota
        # Abrir texto o remover texto seleccionado 
        if self.mode == 'edit':
            # Editar | Abrir texto | Establecer ultima nota
            data_Nota.last_note = button.text()
            save_Nota( data_Nota )
            Dialog_TextEdit(
                self,
                text=data_Nota.note,
                edit=True
            ).exec()
        else:
            # Remover | Nota seleccionada
            # Preguntar el remover
            message_box_question = QMessageBox.question(
                self,
                Lang('remove_note'), # Titulo
                Lang('remove_note'), # Texto
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )
            
            if message_box_question == QMessageBox.StandardButton.Yes:
                # Eliminar una nota
                if save_Nota( data_Nota, remove=button.text() ) == True:
                    # Se pudo remover
                    QMessageBox.information(
                        self,
                        Lang('remove_note'),
                        Lang('remove_good'),
                        QMessageBox.StandardButton.Ok
                    )
                else:
                    # No se pudo remover
                    QMessageBox.critical(
                        self,
                        Lang('remove_note'),
                        Lang('remove_not_good')
                    )
                
                # Actualizar botones/notas disponibles
                self.update_scroll()




class Dialog_change_main_dir(QDialog):
    def __init__(
        self, parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle( Lang('dir_main') )
        self.resize(512, 128)

        # Contenedor Pirncipal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Sección Vertical - Directorio principal
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        self.entry_main_dir = QLineEdit(
            self,
            maxLength=90,
            placeholderText=Lang('dir'),
            clearButtonEnabled=True
        )
        self.entry_main_dir.setText( data_Nota.path )
        hbox.addWidget(self.entry_main_dir)
        
        button_set_dir = QPushButton(
            Lang('set_dir')
        )
        button_set_dir.clicked.connect(self.evt_set_dir)
        hbox.addWidget(button_set_dir)
        
        # Seccion Vertical - Separador
        vbox_main.addStretch()
        
        # Seccion Vertical final, boton para cambiar ruta
        button_change_main_dir = QPushButton( Lang('change_main_dir') )
        button_change_main_dir.clicked.connect(self.evt_change_main_dir)
        vbox_main.addWidget(button_change_main_dir)

        # Fin, Mostrar ventanta y sus widgets agregados
        self.show()
    
    def evt_set_dir(self):
        # Establecer ruta en el self.entry_main_dir
        # por medio de un FileChooserDialog
        dialog_set_dir = QFileDialog.getExistingDirectory(
            self,
            Lang('set_dir'),
            self.entry_main_dir.text()
        )
        if dialog_set_dir:
            # Cambiar ruta
            self.entry_main_dir.setText(
                str(Path( dialog_set_dir ))
            )
        else:
            # No cambiar ruta
            pass
    
    def evt_change_main_dir(self):
        # Cambiar ruta principal donde se guardan las notas
        data_Nota.path = self.entry_main_dir.text()
        new_path = save_Nota( data_Nota )
        if new_path == True:
            # Se pudo cambiar la ruta principal de las notas
            # Mostrar mensaje informativo, y cerrar todo el programa
            QMessageBox.information(
                self,
                Lang('change_main_dir'),
                Lang('dir_change_good'),
                QMessageBox.StandardButton.Ok
            )
            window.close()
        elif new_path == False:
            # No se pudo cambiar la ruta principal de las notas.
            # Mostrar mensaje de error y cerrar unicamente el dialogo
            QMessageBox.critical(
                self,
                Lang('change_main_dir'),
                Lang('dir_change_not_good'),
            )
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Main()
    sys.exit(app.exec())
