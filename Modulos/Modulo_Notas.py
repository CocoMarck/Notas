from Modulos.Modulo_Util import(
    System,
    Files_List,
    Text_Read
)
from Modulos.Modulo_Language import(
    get_lang as Lang
)
from Modulos.Modulo_ShowPrint import(
    Title
)

import os
from pathlib import Path as pathlib


note_path = Text_Read(
    'data/note_path.dat',
    'ModeText'
)


def get_path():
    if note_path.startswith(''):
        return f'{os.getcwd()}/{note_path}'
    else:
        return note_path


def get_list(path=note_path):
    '''Obtener una lista de todas las notas disponibles'''
    list_note = Files_List(
        files='Note_*.txt',
        path=note_path,
        remove_path=True
    )
    
    list_ready = []
    for text in list_note:
        list_ready.append(
            (text.replace('Note_', '')).replace('.txt', '')
        )
    
    return list_ready


def New(path=note_path, text='texto'):
    '''Crear una nueva nota'''
    # Archivo a crear
    file_ready = f'{path}Note_{text}.txt'
    
    # Verificar que no exista
    if pathlib(file_ready).exists():
        # Si existe no hace nada
        return [
            ('Este texto ya existe'),
            file_ready
        ]
    else:
        try:
            # Si no existe, crea el archivo y retorna la ruta del archivo creado
            with open(file_ready, 'w') as text_final:
                text_final.write(
                    f'{Title(text=text, print_mode=False)}'
                )
            return file_ready
        except:
            # Si falla en la creación del archivo, retorna un none
            return None


def Edit(path=note_path, text=''):
    '''Editar o ver una nota existente'''
    list_note = get_list(
        path=note_path
    )
    
    if text in list_note:
        return f'{path}Note_{text}.txt'
    else:
        return None


def Remove(path=note_path, text=''):
    '''Eliminar una nota'''
    '''Retorna un True o un False, si se puede o no borrar el archivo'''
    if os.path.isfile(f'{path}Note_{text}.txt'):
        # El arhcivo que se quiere eliminar es correcto
        os.remove(f'{path}Note_{text}.txt')
        return True

    else:
        # Ese no es un arhcivo o no existe.
        return False


def Change_Path(path=note_path):
    '''Cambiar directorio de las notas a guardar'''
    '''Retorna un True o un False, si se puede o no cambiar el directorio'''
    if os.path.isdir(path):
        # El directorio si es correcto, ahora se guardara
        with open('data/note_path.dat', 'w') as write_path:
            write_path.write(path)
        return True

    else:
        # El directorio es incorrecto
        return False