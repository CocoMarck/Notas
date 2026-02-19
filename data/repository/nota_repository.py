from config.paths import resource_loader, NOTA_CONFIG_FILE, NOTA_DEFAULT_DIR
from core.text_util import (
    read_text, ignore_comment, separe_text, ignore_text_filter, PREFIX_ABC,
    only_one_char
)
from views.gui.show_print import title
import pathlib


ENCODING = "utf-8"
NAME = 'nota'
SPACE_CHAR = '-'
FILE_NAME_PREFIX = f"{NAME}-"
FILE_TYPE_PREFIX = ".txt"
INCLUDE_CHAR_PREFIX = PREFIX_ABC + f".{SPACE_CHAR}"


class NotaRepository:
    def __init__(self):
        self.get_config()

    def filter_text( self, text ):
        '''
        Filtro para los textos, nombres de archivo.
        '''
        filtered_text = ignore_text_filter(
            text.lower().replace(' ', SPACE_CHAR), INCLUDE_CHAR_PREFIX
        )
        if filtered_text:
            return only_one_char( char=SPACE_CHAR, text=filtered_text )
        else:
            # Se puede devoler none, pero creo que da menos bugs con string vacio
            return None

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

    def get_last_nota(self):
        # Obtener ultima nota
        if self.config_value['last_nota'].replace(' ', '') == '':
            return None
        return self.config_value['last_nota']

    def get_path(self):
        # Obtener path
        return pathlib.Path( self.config_value['path'] )

    def list_nota(self, path):
        '''
        Listar cantidad de notas disponibles. Usar un glob, para que nomas muestre los archivos de texto con el prefijo indicado.

        Solo las notas puestas en la ruta, no busqueda recursiva.
        '''
        notas = []
        for path in sorted( path.glob(f'{FILE_NAME_PREFIX}*') ):
            notas.append( self.get_name_only(path.name) )
        return notas

    def get_nota_path(self, name, path):
        file_name = self.get_name_prefix( name )
        return path.joinpath( self.filter_text(file_name) )

    def exists(self, name, path):
        return self.get_nota_path( name, path ).exists()

    def get_nota_text(self, name, path):
        '''
        Obtener texto de nota
        '''
        if self.exists( name, path ):
            return read_text(
                file_and_path=self.get_nota_path( name, path ), option='ModeText', encoding=ENCODING
            )
        else:
            return None

    def set_config(self, last_nota, path):
        '''
        Establecer configuracion
        '''
        change_last_nota = last_nota != self.config_value['last_nota']
        change_path = path != self.config_value['path']

        if change_last_nota or change_path:
            text_ready = ''
            for line in self.config_comment_text.split('\n'):
                if line.startswith('last_nota='):
                    if change_last_nota:
                        line = f'last_nota={ self.filter_text(last_nota) }'
                    elif change_path:
                        line = f'last_nota='
                elif line.startswith('path=') and change_path:
                    line = f'path={path}'
                text_ready += line + '\n'
            with open( NOTA_CONFIG_FILE, 'w', encoding=ENCODING) as text_file:
                text_file.write( text_ready[:-1] )
            self.get_config()
            return True
        else:
            return False


    def insert(self, name, path, text):
        text_title = name
        path = self.get_nota_path( name, path )
        with open( path, 'w', encoding=ENCODING) as empty_text:
            empty_text.write(
                f'{title(text=text_title, console=False)}{text}'
            )

    def update(self, name, path, text):
        name = self.filter_text( name )
        fullpath = self.get_nota_path( name, path )
        with open( fullpath, 'w', encoding=ENCODING) as empty_text:
            empty_text.write( text )

    def save(self, name, path, text):
        '''
        Actualizar o insertar, dependiendo de si existe o no.
        '''
        signal = "insert"
        if self.exists( name, path ):
            self.update( name, path, text )
            signal = "update"
        else:
            self.insert( name, path, text )
        return signal

    def remove( self, name, path ):
        if self.exists( name, path ):
            fullpath = self.get_nota_path( name, path )
            fullpath.unlink()
            return True
        else:
            return False
