'''
Dialogos con funciones especificas, hechos para Gtk.
'''
from os.path import isfile, isdir
from logic.Modulo_System import Command_Run
from logic.Modulo_Text import Text_Read
from interface.Modulo_ShowPrint import Separator
from data.Modulo_Language import Language, get_text as Language_get_text

import threading

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


lang = Language()



space_xy = [8,4]
class Dialog_TextView(Gtk.Dialog):
    def __init__(
        self, parent,
        text = f'{lang["text"]}...',
        edit=False,
        size=[512, 256],
        line_wrap=True,
        space_xy=space_xy
    ):
        super().__init__(
            title=lang['text'], transient_for=parent, flags=0
        )
        self.set_default_size( size[0], size[1] )
        
        # Verificar si el Text View sera es editable
        if edit == True:
            self.text_file = text
        else:
            pass
        self.edit = edit
        
        # Verificar si texto, es un archivo
        if isfile(text):
            # Si lo es, el titulo sera el arhcivo.
            self.set_title(text)
            # Si lo es, entonces se leera
            text = Text_Read(
                file_and_path=text, 
                option='ModeText'
            )
            self.text_isfile = True
        else:
            # So no es texto, no pasa nada
            self.text_isfile = False

        # Contenedor principal
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=space_xy[1])

        # Seccion Vertical - Text View
        text_scroll = Gtk.ScrolledWindow()
        text_scroll.set_hexpand(True)
        text_scroll.set_vexpand(True)
        
        self.text_view = Gtk.TextView()
        #text_view.set_size_request(512, 256)
        self.text_view.set_wrap_mode(line_wrap) # Ajustar lineas
        self.text_view.set_editable(edit)
        text_buffer = self.text_view.get_buffer()
        text_buffer.set_text(text)
        text_scroll.add(self.text_view)
        
        box_v.pack_start(text_scroll, True, True, 0)
        
        # Seccion Vertical Final - Boton para salir o guardar.
        if (
            self.text_isfile == True and
            self.edit == True
        ):
            text_button = lang['save_arch']
        else:
            text_button = lang['exit']
        button_exit_or_save = Gtk.Button( label=text_button )
        button_exit_or_save.connect('clicked', self.evt_exit_or_save)
        box_v.pack_end(button_exit_or_save, False, True, 0)
        
        # Fin, Mostar contenedor principal y todo lo demas.
        self.get_content_area().add(box_v)
        self.show_all()
        
    def evt_exit_or_save(self, button):
        if (
            self.text_isfile == True and
            self.edit == True
        ):
            buffer_text_view = self.text_view.get_buffer()
            text_text_view = buffer_text_view.get_text(
                buffer_text_view.get_start_iter(),
                buffer_text_view.get_end_iter(),
                False
            )
            with open(self.text_file, 'w') as archive:
                archive.write( text_text_view )
        else:
            pass
        self.destroy()


class Dialog_Command_Run(Gtk.Dialog):
    def __init__(
        self,
        parent, cfg='',
        txt=lang['exec'],
        cfg_file='',
        size=[512, 256],
        line_wrap=True,
        space_xy=space_xy
    ):
        super().__init__(
            title=f"{lang['cmd']} - {lang['exec']}",
            transient_for=parent, flags=0
        )
        self.set_default_size( size[0], size[1] )
        self.cfg = cfg
        self.cfg_file = cfg_file
        
        title_HeaderBar = Gtk.HeaderBar()
        title_HeaderBar.set_show_close_button(True)
        title_HeaderBar.props.title = lang['cmd']
        self.set_titlebar(title_HeaderBar)
        
        box_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=space_xy[1])
        #box_v.set_homogeneous(False)
        #box_v.set_property("expand", True)
        #box_v.set_property("halign", Gtk.Align.CENTER)
        
        #label = Gtk.Label()
        #label.set_markup(f'<b>Comando</b>')
        #label.set_line_wrap(True)
        #box_v.pack_start(label, False, False, 16)
        
        # Zona donde se ve el comando
        cmd_scroll = Gtk.ScrolledWindow()
        cmd_scroll.set_hexpand(True)
        cmd_scroll.set_vexpand(True)
        cmd_label = Gtk.Label()
        cmd_label.set_line_wrap(line_wrap)
        cmd_label.set_selectable(True)
        #cmd_label.set_justify(Gtk.Justification.LEFT)
        cmd_label.set_text(f'{self.cfg}')
        cmd_scroll.add(cmd_label)
        box_v.pack_start(cmd_scroll, True, True, 0)
        
        button = Gtk.Button(label=txt)
        button.connect('clicked', self.evt_command_run)
        box_v.pack_end(button, False, False, 16)
        
        self.get_content_area().add(box_v)
        self.show_all()
        
    def evt_command_run(self, widget):
        # Destruir dialogo
        self.destroy()
        
        # Subproceso al precionar el boton ejecutar
        self.thread = threading.Thread(
            target=self.thread_command_run
        )
        self.thread.start()
    
    def thread_command_run(self):
        # Subproceso, ejecutando programa
        if self.cfg_file == '':
            pass
        else:
            with open(self.cfg_file, 'a') as file_cfg:
                    file_cfg.write(
                        self.cfg + f'\n{Separator(print_mode=False)}\n'
                    )
                
        Command_Run(
            cmd=self.cfg,
            open_new_terminal=True,
            text_input=lang['continue_enter']
        )


class Dialog_Wait(Gtk.Dialog):
    def __init__(self, parent, text=lang['help_wait']):
        super().__init__(
            title=lang['help_wait'],
            transient_for=parent, flags=0,
            size=[256, 128],
            space_xy=space_xy
        )
        self.set_default_size( size[0], size[1] )
        
        # Contenedor Principal - VBox
        vbox_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=space_xy[1])
        vbox_main.set_property("expand", True)
        
        # Seccion Vertical - Label
        label = Gtk.Label(label=text)
        vbox_main.pack_start(label, True, True, 0)
        
        # Seccion Vertical - Progress Bar bailarin
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.pulse()
        vbox_main.pack_end(self.progress_bar, True, False, 0)
        
        self.timeout_id = GLib.timeout_add(
            100,
            self.on_timeout,
            None
        )
        
        # Fin, agregar contenedor principal VBox
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def on_timeout(self, user_data):
        self.progress_bar.pulse()
        return True




class Dialog_Input(Gtk.Dialog):
    def __init__(
        self, parent, title='titulo', label='label', entry='', mode=None,
        size=[256, 96], space_xy=space_xy, size_file_chooser=[800, 400]
    ):
        super().__init__(title=title, transient_for=parent, flags=0)
        '''
        Un dialogo que te pide un entry. Si respondes OK o CANCEL, puedes obtener el texto con 
        self.get_input()
        Esta función devuelve un str si es satisfacotorio el entry, y devuelve un None si no lo es.
        
        Modos:
        Si esta en mode='set_dir' o 'set_arch
        Se agregara un boton para cambiar el entry por un directorio o archivo respectivamente, seleccionado con otro dialogo.
        
        En sel.get_input devuelve un str del dir/file, si existe el archivo. De lo contrario devuelve un None.
        '''

        self.set_default_size( size[0], size[1] )
        self.mode = mode
        self.size_file_chooser = size_file_chooser
        self.parent = parent
        
        # Contenedor principal
        vbox_main = Gtk.VBox( spacing=space_xy[1] )
        vbox_main.set_property( 'expand', True )
        
        # Sección vertical | Entry Label | Etiqueta con el mensaje
        hbox = Gtk.HBox( spacing=space_xy[0] )
        vbox_main.pack_start( hbox, True, False, 0 )
        
        label = Gtk.Label( label=label )
        hbox.pack_start( label, False, False, 0 )
        
        self.entry = Gtk.Entry( text=entry )
        hbox.pack_start( self.entry, True, True, 0 )
        
        if self.mode == 'set_dir' or self.mode == 'set_arch':
            button = Gtk.Button( label=Language_get_text(self.mode) )
            button.connect( 'clicked', self.set_dir_file )
            hbox.pack_start( button, False, False, 0 )
        
        # Sección vertical | Botones de aceptar y cancelar.
        self.add_buttons( 
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        # Fin, agregar contenedor principal VBox
        self.get_content_area().add(vbox_main)
        self.show_all()
    
    def get_input(self):
        # Devolver el texto del entry o no
        return_text = False
        if self.mode == 'set_dir':
            if isdir(self.entry.get_text()):
                return_text = True

        elif self.mode == 'set_arch':
            if isfile(self.entry.get_text()):
                return_text = True

        else:
            return_text = True
        
        if return_text == True:
            return self.entry.get_text()
        else:
            return None
    
    
    def set_dir_file(self, button):
        # Seleccionar archivo o carpeta
        if self.mode == 'set_dir':
            action = Gtk.FileChooserAction.SELECT_FOLDER
        elif self.mode == 'set_arch':
            action = Gtk.FileChooserAction.OPEN
        
        if self.mode == 'set_dir' or self.mode == 'set_arch':
            dialog = Gtk.FileChooserDialog(
                title=button.get_label(),
                parent=self.parent,
                action=action,
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK,
                Gtk.ResponseType.OK
            )
            dialog.set_default_size(self.size_file_chooser[0], self.size_file_chooser[1])
            dialog.set_current_folder( self.entry.get_text() )
            
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.entry.set_text( dialog.get_filename() )
                
            dialog.destroy()