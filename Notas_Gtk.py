from Interface.Modulo_Util_Gtk import(
    Dialog_TextView
)
from Modulos.Modulo_Language import get_text as Lang
from Modulos import Modulo_Notas as Notas


import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__( title='Notas' )
        self.set_resizable(True)
        self.set_default_size(256, -1)
        
        # Contenedor Principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        
        # Seccion Vertical - Botones
        button_new_note = Gtk.Button(label=Lang('new_note'))
        button_new_note.connect('clicked', self.evt_new_note)
        vbox_main.pack_start(button_new_note, False, True, 0)
        
        button_edit_note = Gtk.Button(label=Lang('edit_note'))
        button_edit_note.connect('clicked', self.evt_edit_note)
        vbox_main.pack_start(button_edit_note, False, True, 0)
        
        button_remove_note = Gtk.Button( label=Lang('remove_note') )
        button_remove_note.connect('clicked', self.evt_remove_note)
        vbox_main.pack_start(button_remove_note, False, True, 0)
        
        button_change_main_dir = Gtk.Button( label=Lang('change_main_dir') )
        button_change_main_dir.connect('clicked', self.evt_change_main_dir)
        vbox_main.pack_start(button_change_main_dir, False, True, 0)
        
        # Mostrar todo y agregar contenedor principal
        self.add(vbox_main)
        self.show_all()
    
    def evt_new_note(self, widget):
        dialog = Dialog_new_note(self)
        dialog.run()
        dialog.destroy()
    
    def evt_edit_note(self, widget):
        print('edit')
    
    def evt_remove_note(self, widget):
        print('remove')
    
    def evt_change_main_dir(self, widget):
        print('change main dir')


class Dialog_new_note(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title=Lang('new_note'),
            transient_for=parent, flags=0
        )
        self.set_resizable(True)
        self.set_default_size(308, -1)
        
        # Contenedor Principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        vbox_main.set_property('expand', True)
        
        # Seccion Vertical - Entry para Establecer el nombre de nota
        hbox = Gtk.Box(spacing=4)
        vbox_main.pack_start(hbox, False, True, 0)
        
        label_new_note = Gtk.Label(label=f"{Lang('name')}:")
        hbox.pack_start(label_new_note, False, False, 0)
        
        self.entry_new_note = Gtk.Entry()
        self.entry_new_note.set_placeholder_text( Lang('text') )
        hbox.pack_end(self.entry_new_note, False, False, 0)
        
        # Seccion Vertical - Boton final, para guardar nota
        button_save_note = Gtk.Button( label=Lang('save_note') )
        button_save_note.connect('clicked', self.evt_save_note)
        vbox_main.pack_end(button_save_note, False, True, 0)
        
        # Fin, Mostrar contenido ventana y contenedor principal
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_save_note(self, widget):
        # Nota a guardar
        note = self.entry_new_note.get_text()
        if note == '':
            # Si no escribio nada entonces la nota sera 'texto'
            note = 'texto'
        else:
            # Normal, la nota es correcta
            pass
        
        # Crear o no el archivo necesario
        note_save_or_not = Notas.New(
            text=note
        )
        if type(note_save_or_not) is str:
            # Abrir archivo con un editor de texto.
            dialog = Dialog_TextView(
                self,
                text=note_save_or_not,
                edit=True
            )
            dialog.run()
            dialog.destroy()

        elif type(note_save_or_not) is list:
            # El texto creado ya existe, y abrirlo con un editor de texto
            # Mostrar info de que ya existe ese archivo
            dialog_info = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=Lang('this_file_exists')
            )
            dialog_info.run()
            dialog_info.destroy()

            # Abrir el texto con Text View
            dialog = Dialog_TextView(
                self,
                text=note_save_or_not[1],
                edit=True
            )
            dialog.run()
            dialog.destroy()
        
        else:
            # Fallo en la creación del archivo
            # O El input tiene caracteres erroneos
            # Hay un Error
            dialog_error = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text=f'ERROR - {Lang("error_create_file")}\n'
            )
            dialog_error.run()
            dialog_error.destroy()
        
        self.destroy()


win = Window_Main()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()