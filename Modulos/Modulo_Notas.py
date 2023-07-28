from Modulos.Modulo_System import(
    get_system
)
from Modulos.Modulo_Files import(
    Path,
    Files_List
)
from Modulos.Modulo_Text import(
    Text_Read
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
note_path = Path(path=note_path)


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


def get_last_note():
    '''Devuelve el la ultima nota creada'''
    last_note_file = Text_Read(
        'data/last_note.dat',
        'ModeText'
    )
    last_note = f"{note_path}Note_{last_note_file}.txt"
    if pathlib(last_note).exists():
        return last_note
    else:
        return None


def New(path=note_path, text='texto'):
    '''Crear una nueva nota'''
    '''Si logra crear el archivo, devolvera un str del nombre del archivo'''
    '''Si ya existe el archivo, devolvera una lista, con un true y el nombre del archivo'''
    '''Si falla en la cración der achivo devolcera un boleano tipo False'''
    # Archivo a crear
    file_ready = f'{path}Note_{text}.txt'
    
    # Verificar que no exista
    if pathlib(file_ready).exists():
        # Si existe, retorna una lista
        return [
            True, file_ready
        ]
    else:
        try:
            # Si no existe, crea el archivo y retorna la ruta del archivo creado
            with open(file_ready, 'w') as text_final:
                text_final.write(
                    f'{Title(text=text, print_mode=False)}'
                )

            # Establece el archivo creado en last_note.dat
            with open('data/last_note.dat', 'w') as last_note:
                last_note.write(text)

            return file_ready
        except:
            # Si falla en la creación del archivo, retorna un none
            return False


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