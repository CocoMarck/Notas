from data.Modulo_Language import get_text
from data.Modulo_Notas import (data_Nota, read_Nota, save_Nota, get_list as Nota_get_list)
from data.interface_data import file_icon, file_font

from logic.Modulo_Text import pass_text_filter

from interface.Modulo_Util_Gtk import Dialog_TextView, Dialog_Input
from interface.interface_number import *
from interface.css_util import *


import gi, gtk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk




class Window_Main( Gtk.Window ):
    def __init__(self):
        super().__init__(title='Notas')
        
        self.set_resizable(True)
        self.set_default_size( nums_win_main[0], nums_win_main[1] )
        self.set_icon_from_file( file_icon )
        
        # Contenedor vertical principal
        vbox_main = Gtk.Box( orientation=Gtk.Orientation.VERTICAL, spacing=nums_space_xy[1] )
        
        # Sección Vertical - Botones
        list_options = ['new_note', 'edit_note', 'remove_note']
        self.dict_button = {}
        for option in list_options:
            button = Gtk.Button( label=get_text(option) )
            button.connect( 'clicked', self.note )
            vbox_main.pack_start(button, True, False, 0)
            self.dict_button.update( { button : option })
            
        button = Gtk.Button( label=get_text('change_main_dir') )
        button.connect( 'clicked', self.change_main_dir )
        vbox_main.pack_start(button, True, False, 0)
        
        # Mostrar todo y agergar contenedor principal
        self.add(vbox_main)
        self.show_all()
    

    def note(self, button):
        self.hide()
        
        # Opcion actual
        option = self.dict_button[button]
        
        # Input para Nueva nota
        if option == 'new_note':
            dialog = Dialog_Input( 
                self, title=get_text(option), label=get_text(option),
                size=nums_win_input, space_xy=nums_space_xy
            )
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                # Guardar si pasa el filtro
                text = dialog.get_input()
                if pass_text_filter(text.lower(), filter=' abcdefghijklmnñopqrstuvwxyz_-'):
                    save_Nota( data_Nota, save=text )
                else:
                    print('No paso el filtro')

            dialog.destroy()
            
            option = 'edit_note'

        # Abrir menu de notas
        if option == 'edit_note' or option == 'remove_note':
            dialog = Dialog_edit_remove_note( self, option )
            dialog.run()
            dialog.destroy()

        self.show_all()
    
    def change_main_dir(self, button):
        # Cambiar directorio
        self.hide()

        dialog = Dialog_Input( 
            self, title=button.get_label(), label=get_text('dir'), entry=data_Nota.path,
            size=nums_win_input, space_xy=nums_space_xy, size_file_chooser=nums_win_file_chooser,
            mode='set_dir'
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if isinstance(dialog.get_input(), str):
                data_Nota.path = dialog.get_input()
                save_Nota( data_Nota )

        dialog.destroy()
        
        self.show_all()




class Dialog_edit_remove_note(Gtk.Dialog):
    def __init__(self, parent, option=None):
        super().__init__(
            title=get_text(option), transient_for=parent, flags=0
        )

        self.set_resizable(True)
        self.set_default_size( nums_win_edit_remove[0], nums_win_edit_remove[1] )
        self.option = option
        self.parent = parent
        
        # Contenedor principal
        vbox_main = Gtk.Box( orientation=Gtk.Orientation.VERTICAL, spacing=nums_space_xy[1] )
        vbox_main.set_property( 'expand', True )
        
        
        # Sección vertical - Ultima nota
        if option == 'edit_note':
            button = Gtk.Button( label=get_text('last_note') )
            button.connect( 'clicked', self.edit_last_note )
            vbox_main.pack_start( button, False, True, 0 )
        
        # Secciones verticales - Botones - Lista de notas
        scroll = Gtk.ScrolledWindow()
        scroll.set_hexpand(False)
        scroll.set_vexpand(True)
        vbox_main.pack_start( scroll, True, True, 0 )
        
        self.vbox_scroll = Gtk.Box( orientation=Gtk.Orientation.VERTICAL, spacing=nums_space_xy[1] )
        scroll.add(self.vbox_scroll)
        
        self.list_button = []
        self.update_notes()
        
        
        # Entry para buscar botones
        hbox = Gtk.HBox( spacing=nums_space_xy[0] )
        vbox_main.pack_start( hbox, False, False, 0 )

        label = Gtk.Label( label=get_text('search') )
        hbox.pack_start( label, False, True, 0 )

        entry = Gtk.Entry( )
        entry.connect( 'changed', self.search_note )
        hbox.pack_start( entry, True, True, 0 )
        
        
        # Fin, mostrar todo y el contenedor principal
        self.get_content_area().add(vbox_main)
        self.show_all()
    

    def update_notes(self):
        # Limpiar lo contenido en el vbox y el diccionario
        for child in self.vbox_scroll.get_children():
            self.vbox_scroll.remove(child)
        self.list_button.clear()
        
        # Agergar botones
        for note in Nota_get_list( data_Nota ):
            button = Gtk.Button( label=note )
            button.connect( 'clicked', self.edit_remove_note )
            self.vbox_scroll.pack_start( button, False, False, 0 )
            self.list_button.append( button )
        self.vbox_scroll.show_all() # Asegurarse que se muestren los widgets contenidos
    
    
    def edit_last_note(self, button):
        # Leer/Editar la ultima nota
        read_Nota( data_Nota )
        if isinstance(data_Nota.note, str):
            dialog = Dialog_TextView(
                self.parent,
                text=data_Nota.note,
                edit=True,
                size=nums_win_text_edit
            )
            dialog.run()
            dialog.destroy()
    

    def edit_remove_note(self, button):
        # Editar o remover nota
        if self.option == 'edit_note':
            # Leer/Editar nota seleccionada
            data_Nota.last_note=button.get_label()
            save_Nota( data_Nota )
            dialog = Dialog_TextView(
                self.parent,
                text=data_Nota.note,
                edit=True,
                size=nums_win_text_edit
            )
            dialog.run()
            dialog.destroy()

        elif self.option == 'remove_note':
            # Eliminar nota
            dialog_question = Gtk.MessageDialog(
                transient_for=self, flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text=get_text('remove_note')
            )
            response = dialog_question.run()
            if response == Gtk.ResponseType.YES:
                # Intentar eliminar la nota
                save_Nota( data_Nota, remove=button.get_label() )
            elif response == Gtk.ResponseType.NO:
                # Se eligio no eliminar la nota
                pass
            dialog_question.destroy()
            self.destroy()

        self.update_notes()
    
    
    def search_note(self, entry):
        # Obtener el texto del entry
        search_text = entry.get_text().lower()
        
        # Buscar el boton
        for button in self.list_button:
            # Coincidencia parcial
            if search_text in button.get_label().lower():
                # Darle foco al botón
                button.grab_focus()
                break
        entry.grab_focus()




# Estilo de programa
css_style = ''
for widget in get_list_text_widget('Gtk'):
    if widget == 'textview':
        css_style += text_widget_style( 
            widget=widget, font=file_font, font_size=num_font, 
            margin=None, padding=None, idented=4
        )
    else:
        css_style += text_widget_style( 
            widget=widget, font=file_font, font_size=num_font, 
            margin=None, padding=num_space_padding, idented=4
        )
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
style_context = Gtk.StyleContext()
style_context.add_provider_for_screen(
    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
provider.load_from_data( str.encode(css_style) )
print( css_style )




# Bucle del programa
win = Window_Main()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()