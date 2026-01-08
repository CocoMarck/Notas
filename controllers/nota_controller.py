from config.paths import resource_loader, NOTA_CONFIG_FILE, NOTA_DEFAULT_DIR
from core.text_util import (
    read_text, ignore_comment, separe_text, ignore_text_filter, PREFIX_ABC,
    only_one_char
)
import pathlib

from views.gui.show_print import title


ENCODING = "utf-8"
NAME = 'nota'
SPACE_CHAR = '-'
FILE_NAME_PREFIX = f"{NAME}-"
FILE_TYPE_PREFIX = ".txt"
INCLUDE_CHAR_PREFIX = PREFIX_ABC + f".{SPACE_CHAR}"


class NotaController:
    def __init__(self, nota_model):
        self.nota = nota_model
        self.nota.text = ""
        self.load()

    def filter_text( self, text ):
        filtered_text = ignore_text_filter(
            text.lower().replace(' ', SPACE_CHAR), INCLUDE_CHAR_PREFIX
        )
        if filtered_text:
            return only_one_char( char=SPACE_CHAR, text=filtered_text )
        return filtered_text

    def get_name_only( self, name ):
        return self.filter_text(
         text=name.replace( FILE_NAME_PREFIX, "" ).replace(FILE_TYPE_PREFIX, "").replace( NAME, "" )
        )

    def get_name_prefix( self, name ):
        return f"{FILE_NAME_PREFIX}{self.get_name_only(name=name)}{FILE_TYPE_PREFIX}"

    def get_config(self):
        '''
        Establecer configuración.
        '''
        self.config_comment_text = read_text(
            file_and_path=NOTA_CONFIG_FILE, option='ModeText', encoding=ENCODING
        )
        self.config_uncomment_text = ignore_comment( self.config_comment_text, comment="#" )
        self.config_value = separe_text( self.config_uncomment_text, "=" )
        self.nota.last_nota = pathlib.Path( self.config_value['last_nota'] ).name
        self.nota.path = pathlib.Path( self.config_value['path'] )

    def list_nota(self):
        '''
        Listar cantidad de notas disponibles. Usar un glob, para que nomas muestre los archivos de texto con el prefijo indicado.

        Solo las notas puestas en la ruta, no busqueda recursiva.
        '''
        notas = []
        #for path in resource_loader.get_recursive_tree( self.nota.path )['file']:
            #if path.name.startswith(FILE_NAME_PREFIX):
        for path in sorted( self.nota.path.glob(f'{FILE_NAME_PREFIX}*') ):
            notas.append( self.get_name_only(path.name) )
        return notas

    def get_nota_path(self):
        file_name = self.get_name_prefix( self.nota.last_nota )
        return self.nota.path.joinpath( self.filter_text(file_name) )

    def exists(self):
        return self.get_nota_path().exists()


    def read(self):
        '''
        Leer ultima nota, guardada o seleccionada.
        '''
        path = self.get_nota_path()
        if path.exists():
            self.nota.text = read_text(
                file_and_path=path, option='ModeText', encoding=ENCODING
            )
            return True
        else:
            return False


    def load(self):
        self.get_config()
        self.read()


    def set_config(self):
        '''
        Establecer configuracion
        '''
        change_last_nota = self.nota.last_nota != self.config_value['path']
        change_path = self.nota.path != self.config_value['path']

        if change_last_nota or change_path:
            text_ready = ''
            for line in self.config_comment_text.split('\n'):
                if line.startswith('last_nota=') and change_last_nota:
                    line = f'last_nota={ self.filter_text(self.nota.last_nota) }'
                elif line.startswith('path=') and change_path:
                    line = f'path={self.nota.path}'
                text_ready += line + '\n'
            with open( NOTA_CONFIG_FILE, 'w', encoding=ENCODING) as text_file:
                text_file.write( text_ready[:-1] )
            self.get_config()
            return True
        else:
            return False

    def insert(self):
        text_title = self.nota.last_nota
        path = self.get_nota_path()
        with open( path, 'w', encoding=ENCODING) as empty_text:
            empty_text.write(
                f'{title(text=text_title, console=False)}{self.nota.text}'
            )


    def update(self):
        self.nota.last_nota = self.filter_text( self.nota.last_nota )
        path = self.get_nota_path()
        with open( path, 'w', encoding=ENCODING) as empty_text:
            empty_text.write( self.nota.text )



    def save(self):
        if self.exists():
            self.update()
        else:
            self.insert()
        self.set_config()
        self.read()


    def remove(self):
        if self.exists():
            nota = self.get_nota_path()
            nota.unlink()
            return True
        else:
            return False
