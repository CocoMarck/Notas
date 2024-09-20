from data.Modulo_Language import get_text as Lang
from data.Modulo_Notas import (data_Nota, read_Nota, save_Nota, get_list as Nota_get_list)
from data.interface_data import file_icon, file_font

from interface.Modulo_Util_Gtk import(
    Dialog_TextView
)
from interface.interface_number import *
from interface.css_util import *


import gi, gtk

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



# Estilo de Interfaz.
# Convertir estilo en bytes
css_style = ''
for widget in get_list_text_widget('Gtk'):
    css_style += text_widget_style( 
        widget=widget, font=file_font, font_size=num_font, 
        margin=None, padding=num_space_padding, idented=4
    )
print( css_style )
css_style = str.encode(css_style)

# Aplicar estilo
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
style_context = Gtk.StyleContext()
style_context.add_provider_for_screen(
    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
provider.load_from_data( css_style )
print( css_style )
print( type(css_style) )




class Window_Main(Gtk.Window):
    def __init__(self):
        super().__init__( title='Notas' )
        self.set_resizable(True)
        self.set_default_size( nums_win_main[0], nums_win_main[1] )
        self.set_icon_from_file( file_icon )
        
        # Contenedor Principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        
        # Seccion Vertical - Botones
        button_new_note = Gtk.Button(label=Lang('new_note'))
        button_new_note.connect('clicked', self.evt_new_note)
        vbox_main.pack_start(button_new_note, True, True, 0)
        
        button_edit_note = Gtk.Button(label=Lang('edit_note'))
        button_edit_note.connect('clicked', self.evt_edit_note)
        vbox_main.pack_start(button_edit_note, True, True, 0)
        
        button_remove_note = Gtk.Button( label=Lang('remove_note') )
        button_remove_note.connect('clicked', self.evt_remove_note)
        vbox_main.pack_start(button_remove_note, True, True, 0)
        
        button_change_main_dir = Gtk.Button( label=Lang('change_main_dir') )
        button_change_main_dir.connect('clicked', self.evt_change_main_dir)
        vbox_main.pack_start(button_change_main_dir, True, True, 0)
        
        # Mostrar todo y agregar contenedor principal
        self.add(vbox_main)
        self.show_all()
    
    def evt_new_note(self, widget):
        self.hide()
        dialog = Dialog_new_note(self)
        dialog.run()
        dialog.destroy()
        self.show_all()
    
    def evt_edit_note(self, widget):
        self.hide()
        dialog = Dialog_edit_note(self)
        dialog.run()
        dialog.destroy()
        self.show_all()
    
    def evt_remove_note(self, widget):
        self.hide()
        dialog = Dialog_remove_note(self)
        dialog.run()
        dialog.destroy()
        self.show_all()
    
    def evt_change_main_dir(self, widget):
        self.hide()
        dialog = Dialog_change_main_dir(self)
        dialog.run()
        dialog.destroy()
        self.show_all()


class Dialog_new_note(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(
            title=Lang('new_note'),
            transient_for=parent, flags=0
        )
        self.set_resizable(True)
        self.set_default_size( nums_win_new[0], nums_win_new[1] )
        
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
        save_Nota( data_Nota, save=note )
        note_save_or_not = data_Nota.note
        if type(note_save_or_not) is str:
            # Abrir archivo con un editor de texto.
            dialog = Dialog_TextView(
                self,
                text=note_save_or_not,
                edit=True,
                size=nums_win_text_edit
            )
            self.hide()
            dialog.run()
            dialog.destroy()
            self.show_all()

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
                edit=True,
                size=nums_win_text_edit
            )
            self.hide()
            dialog.run()
            dialog.destroy()
            self.show_all()
        
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


class Dialog_edit_note(Gtk.Dialog):
    def __init__(
        self, parent
    ):
        super().__init__(
            title=Lang('edit_note'),
            transient_for=parent, flags=0
        )
        self.set_resizable(True)
        self.set_default_size( nums_win_edit_remove[0], nums_win_edit_remove[1] )
        
        # Contenedor Principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        vbox_main.set_property('expand', True)
        
        # Scciones Verticales - Botones para elegir una nota
        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_hexpand(False)
        scroll_window.set_vexpand(True)
        vbox_main.pack_start(scroll_window, True, True, 0)
        
        vbox_scroll = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )
        scroll_window.add(vbox_scroll)
        
        button = Gtk.Button( label=Lang('last_note') )
        button.connect('clicked', self.evt_edit_last_note)
        vbox_scroll.pack_start(button, False, True, 0)
        
        for note in Nota_get_list( data_Nota ):
            button = Gtk.Button( label=note )
            button.connect('clicked', self.evt_edit_a_note)
            vbox_scroll.pack_start(button, False, True, 0)
        
        # Fin, mostrar todo y el contenedor principal
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_edit_last_note(self, button):
        # Ultimo texto creado
        read_Nota( data_Nota )
        edit = data_Nota.note
        if type(edit) is str:
            # El texto existe y se editara con un TextView
            dialog = Dialog_TextView(
                self,
                text=edit,
                edit=True,
                size=nums_win_text_edit
            )
            dialog.run()
            dialog.destroy()
        elif edit == None:
            # El texto no existe y no se hara nada, mas que un mensaje indicador.
            dialog_error = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text=Lang('no_note')
            )
            dialog_error.run()
            dialog_error.destroy()
    
    def evt_edit_a_note(self, button):
        # Editar la nota elegida, basado en el texto/label del button precionado.
        data_Nota.last_note=button.get_label()
        save_Nota( data_Nota )
        dialog = Dialog_TextView(
            self,
            text=data_Nota.note,
            edit=True,
            size=nums_win_text_edit
        )
        dialog.run()
        dialog.destroy()


class Dialog_remove_note(Gtk.Dialog):
    def __init__(
        self, parent
    ):
        super().__init__(
            title=Lang('remove_note'),
            transient_for=parent, flags=0
        )
        self.set_resizable(True)
        self.set_default_size( nums_win_edit_remove[0], nums_win_edit_remove[1] )
        
        # Contenedor Principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        vbox_main.set_property('expand', True)
        
        # Secciones Verticales - Botones para elegir una nota
        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_hexpand(False)
        scroll_window.set_vexpand(True)
        vbox_main.pack_start(scroll_window, True, True, 0)
        
        vbox_scroll = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )
        scroll_window.add(vbox_scroll)
        
        for note in Nota_get_list( data_Nota ):
            button = Gtk.Button(label=note)
            button.connect('clicked', self.evt_remove_a_note)
            vbox_scroll.pack_start(button, False, True, 0)
        
        # Fin, mostrar todo y el contenedor principal
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_remove_a_note(self, button):
        # Verificar remover o no la nota
        dialog_question = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=Lang('remove_note')
        )
        response = dialog_question.run()
        
        if response == Gtk.ResponseType.YES:
            # Eliminar una nota
            if save_Nota( data_Nota, remove=button.get_label() ) == True:
                # Se pudo remover
                dialog_info = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=Lang('remove_good')
                )
                dialog_info.run()
                dialog_info.destroy()
            else:
                # No se pudo remover
                dialog_error = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text=Lang('remove_not_good')
                )
                dialog_error.run()
                dialog_error.destroy()

        elif response == Gtk.ResponseType.NO:
            # Se eligio no eliminar la nota
            pass

        dialog_question.destroy()
        self.destroy()


class Dialog_change_main_dir(Gtk.Dialog):
    def __init__(
        self, parent
    ):
        super().__init__(
            title=Lang('dir_main'),
            transient_for=parent, flags=0
        )
        self.set_resizable(True)
        self.set_default_size( nums_win_change_dir[0], nums_win_change_dir[1] )
        
        # Contenedor Principal
        vbox_main = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8
        )
        vbox_main.set_property('expand', True)
        
        # Seccion Vertical - entry
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        vbox_main.pack_start(hbox, True, False, 0)
        
        self.entry_main_dir = Gtk.Entry()
        self.entry_main_dir.set_placeholder_text( Lang('dir') )
        self.entry_main_dir.set_hexpand(True)
        self.entry_main_dir.set_text( data_Nota.path )
        hbox.pack_start(self.entry_main_dir, False, True, 0)
        
        button_set_dir = Gtk.Button( label=Lang('set_dir') )
        button_set_dir.connect('clicked', self.evt_set_dir)
        hbox.pack_end(button_set_dir, False, True, 0)
        
        # Seccion Vertical final, boton para cambiar ruta
        button_change_main_dir = Gtk.Button( label=Lang('change_main_dir') )
        button_change_main_dir.connect('clicked', self.evt_change_main_dir)
        vbox_main.pack_end(button_change_main_dir, False, True, 0)
        
        # Fin, mostrar todo y el contenedor principal
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def evt_set_dir(self, widget):
        # Establecer ruta en el self.entry_main_dir
        # por medio de un FileChooserDialog
        dialog_set_dir = Gtk.FileChooserDialog(
            parent=self,
            title=Lang('set_dir'),
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog_set_dir.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            'Select',
            Gtk.ResponseType.OK
        )
        dialog_set_dir.set_current_folder( self.entry_main_dir.get_text() )
        
        response = dialog_set_dir.run()
        if response == Gtk.ResponseType.OK:
            # Cambiar ruta
            self.entry_main_dir.set_text( dialog_set_dir.get_filename() )
        elif response == Gtk.ResponseType.CANCEL:
            # No cambiar ruta
            pass
            
        dialog_set_dir.destroy()
    
    def evt_change_main_dir(self, widget):
        # Cambiar ruta principal donde se guardan las notas
        data_Nota.path = self.entry_main_dir.get_text()
        new_path = save_Nota( data_Nota )
        if new_path == True:
            # Se pudo cambiar la ruta principal de las notas
            dialog_info = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=Lang('dir_change_good')
            )
            dialog_info.run()
            dialog_info.destroy()
            win.destroy()
        elif new_path == False:
            # No se pudo cambiar la ruta principal de las notas
            dialog_error = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text=Lang('dir_change_not_good')
            )
            dialog_error.run()
            dialog_error.destroy()
        self.destroy()


win = Window_Main()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()