from Interface.Modulo_Util_Qt import(
    Dialog_TextEdit
)
from Modulos.Modulo_Language import get_text as Lang
from Modulos import Modulo_Notas as Notas
import os


import sys
from pathlib import Path
from PyQt6.QtWidgets import(
    QApplication,
    QWidget,
    QDialog,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtGui import QIcon


class Window_Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Notas')
        #self.setWindowIcon(QIcon('icono'))
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
        Dialog_new_note(self).exec()

    def evt_edit_note(self):
        Dialog_edit_note(self).exec()

    def evt_remove_note(self):
        pass

    def evt_change_main_dir(self):
        pass


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
        # Nota a guarder
        note = self.entry_new_note.text()
        if note =='':
            # Si no se escribio nada, la nota sera 'texto'
            note='texto'
        else:
            # Normal, la nota es correcta
            pass

        # Crear o no el archivo necesario
        note_save_or_not = Notas.New(
            text=note
        )
        if type(note_save_or_not) is str:
            # Abrir archivo con un editor de texto
            os.system(f'notepad "{note_save_or_not}"')

        elif type(note_save_or_not) is list:
            # El texto creado ya existe, y abrirlo con un editor de texto

            # Mostrar mensaje de info de que ya existe.
            message_box = QMessageBox(self)
            message_box.setWindowTitle(Lang('save_note'))
            message_box.setText( Lang('this_file_exists') )
            message_box.exec()

            # Abrir el texto con un editor de texto
            os.system(f'notepad {note_save_or_not[1]}')

        else:
            # Fallo en la creación del archivo
            # O El input tiene caracteres erroneos
            # Hay un Error
            pass

        self.close()


class Dialog_edit_note(QDialog):
    def __init__(
        self, parent=None
    ):
        super().__init__(parent)

        self.setWindowTitle( Lang('edit_note') )
        self.resize(512, 308)

        # Contenedor Pirncipal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Fin, Mostrar ventanta y sus widgets agregados
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window_Main()
    sys.exit(app.exec())
