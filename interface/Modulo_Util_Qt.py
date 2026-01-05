'''
Dialogos con funciones especificas, hechos para funcionar en Qt.
'''
from os.path import isfile, isdir
from logic.Modulo_System import(Command_Run)
from logic.Modulo_Text import(Text_Read)
from interface.Modulo_ShowPrint import(Separator)
from data.Modulo_Language import Language, get_text

from PyQt6.QtWidgets import(
    QWidget,
    QDialog,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog
)


lang = Language()


class Dialog_TextEdit(QDialog):
    def __init__(
        self, parent=None,
        text=f'{lang["text"]}...',
        edit=False,
        size=[512, 256]
    ):
        super().__init__(parent)
        
        self.setWindowTitle( lang['text'] )
        self.resize( size[0], size[1] )
        
        # Verificar si el Text Edit es editable
        if edit == True:
            self.text_file = text
            ReadOnly = False
        else:
            ReadOnly = True
        self.edit = edit
        
        # Verificar si texto, es un archivo
        if isfile(text):
            # Si lo es, el titulo sera el archivo
            self.setWindowTitle(text)
            
            # Si lo es, entonces se leera
            text = Text_Read(
                file_and_path=text,
                option='ModeText'
            )
            self.text_isfile = True
        else:
            # Si no es un texto, no pasa nada.
            self.text_isfile = False
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vertical 1 - Text Edit
        self.text_edit = QTextEdit(str(text).replace('\n', '<br>'))
        self.text_edit.setReadOnly(ReadOnly)
        vbox_main.addWidget(self.text_edit)
        
        # Seccion Vetical 2 - Boton para salir
        if (
            self.text_isfile == True and
            self.edit == True
        ):
            text_button = lang['save_arch']
        else:
            text_button = lang['exit']
        button_exit_or_save = QPushButton( text_button )
        button_exit_or_save.clicked.connect(self.evt_exit_or_save)
        vbox_main.addWidget(button_exit_or_save)

    def evt_exit_or_save(self):
        if (
            self.text_isfile == True and
            self.edit == True
        ):
            with open(self.text_file, 'w') as archive:
                archive.write( 
                    self.text_edit.toPlainText()
                )
        else:
            pass
        self.close()
        

class Dialog_Command_Run(QDialog):
    def __init__(self, parent=None, cmd='', cfg_file='', size=[512,256]):
        super().__init__(parent)
        
        self.setWindowTitle(f"{lang['cmd']} - {lang['exec']}")
        self.setMinimumWidth( size[0] )
        self.setMinimumHeight( size[1] )
        
        self.cmd = cmd
        self.cfg_file = cfg_file
        
        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccion Vrtical - Label
        label = QLabel(f'{lang["cmd"]}:')
        vbox_main.addWidget(label)
        
        # Seccion Vertical - Text Edit
        text_edit = QTextEdit( str(cmd).replace('\n', '<br>') )
        text_edit.setReadOnly(True)
        vbox_main.addWidget(text_edit)
        
        # Seccion Vertical - Boton Ejecutar comando
        button_cmdRun = QPushButton( lang['exec'] )
        button_cmdRun.clicked.connect(self.evt_command_run)
        vbox_main.addWidget(button_cmdRun)
        
    def evt_command_run(self):
        self.close()
        
        if self.cfg_file == '':
            pass
        else:
            with open(self.cfg_file, 'a') as cfg_file:
                cfg_file.write(self.cmd + f'\n{Separator(print_mode=False)}\n')
                
        Command_Run(
            self.cmd,
            text_input=lang['continue_enter'],
            open_new_terminal=True
        )


class Dialog_Wait(QDialog):
    def __init__(self, parent=None, text=lang['help_wait'], size=[256, 128]):
        super().__init__(parent)
        
        self.setWindowTitle( lang['wait'] )
        self.resize( size[0], size[1] )
        
        # Contenedor Pincipal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Label en el medio del dialogo
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)

        hbox.addStretch()

        label = QLabel(text)
        hbox.addWidget(label)

        hbox.addStretch()




class Dialog_InputDirFile(QDialog):
    def __init__(
        self, parent, title='title', label='label', entry='', mode='set_dir',
        size=[256, 96]
    ):
        '''
        Dialogo para seleccionar un directorio o un archivo.
        Boton que te abre un dialogo para buscar lo necesario. Una vez seleccionado se remplaza el input/entry
        
        mode=str. 'set_dir' 'set_arch'
        set_dir para seleccionar carpeta
        set_arch para seleccionar archivo
        
        Para obtener lo seleccionado, usar funcion get_input()
        Deveulve un str si hay algo, y None si no hay nada.
        
        Ejemplo de uso:
        dialog = Dialog_InputDirFile(mode='dir')
        dialog.exec()
        text = dialog.get_input()
        '''
        super().__init__(parent)
        
        self.setWindowTitle( title )
        self.resize( size[0], size[1] )
        self.parent=parent
        self.mode=mode
        
        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)
        
        # Seccón vertical | Label | Entry | Boton para seleccionar directiorio o archivo
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)
        
        label_entry = QLabel( label )
        hbox.addWidget(label_entry)
        
        self.entry = QLineEdit( 
            text=entry,
            placeholderText = get_text('text')
        )
        hbox.addWidget(self.entry)
        
        if self.mode == 'set_dir' or self.mode == 'set_arch':
            button = QPushButton( get_text(self.mode) )
            button.clicked.connect( self.set_dir_arch )
            hbox.addWidget( button )
            
        
        # Seperador
        vbox_main.addStretch()
            

        # Seccion vertical | Botones de aceptar y cancelar
        hbox = QHBoxLayout()
        vbox_main.addLayout(hbox)

        button = QPushButton( get_text('no_set') )
        button.clicked.connect( self.remove_entry )
        hbox.addWidget( button )
        
        hbox.addStretch()
        
        button = QPushButton( get_text('set') )
        button.clicked.connect( self.close )
        hbox.addWidget( button )
        
        
        # Fin Mostrar ventana
        self.show()
    
    def get_input(self):
        # Devolver el texto si es que hay
        if isinstance( self.entry.text(), str ):
            return_text = False
            if self.mode == 'set_dir' and isdir(self.entry.text()):
                return_text = True
            elif self.mode == 'set_arch' and isfile(self.entry.text()):
                return_text = True
            
            if return_text == True:
                return self.entry.text()
        else:
            return None
    
    def set_dir_arch(self):
        from pathlib import Path

        # Seleccionar archivo o carpeta
        if self.mode == 'set_dir':
            dir_name = QFileDialog.getExistingDirectory(
                self.parent, 
                get_text(self.mode),
                self.entry.text()
            )
            if dir_name:
                self.entry.setText( str(Path(dir_name)) )

        elif self.mode == 'set_arch':
            file_name, ok = QFileDialog.getOpenFileName(
                self.parent,
                get_text(self.mode),
                self.entry.text(),
                'All (*)'
            )
            if file_name and ok:
                self.entry.setText( str(Path(file_name)) )
    
    def remove_entry(self):
        self.entry.clear()
        self.close()