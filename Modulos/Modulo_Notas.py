from Modulos.Modulo_System import(
    get_system
)
from Modulos.Modulo_Files import(
    Path,
    Files_List
)
from Modulos.Modulo_Text import(
    Text_Read,
    Ignore_Comment,
    Text_Separe
)
from Modulos.Modulo_ShowPrint import(
    Title
)

import os
from pathlib import Path as pathlib


def get_data(mode_dict=True):
    '''Obtener datos de ultima nota o directorio de las notas, por medio de un diccionario.'''
    '''Otener un texto str del archivo "notas.dat" '''
    # Leer texto y ignorar comentarios tipo '#'
    note_archive = Text_Read(
        'data/notas.dat',
        'ModeText'
    )
    note_data = Ignore_Comment(
        text=note_archive,
        comment='#'
    )
    # Agragar valores en el texto a un diccionario
    note_data = Text_Separe(
        text=note_data,
        text_separe='='
    )
    
    # Retornar en modo solo los datos en modo diccionario
    # O retornar el texto completo.
    if mode_dict == True:
        # Retornar en modo diccionario
        return note_data
    else:
        # Retornar en modo texto
        return note_archive


def get_path():
    '''Obtener el path principal actual donde se guardan las notas'''
    # Path donde se guardan las notas
    note_data = get_data()
    note_path = Path(
        path=note_data['path']
    )
    return note_path
    #if note_path.startswith(''):
    #    return f'{Path(path=os.getcwd())}{get_note()}'
    #else:
    #    return note_path


def get_list(path=get_path()):
    '''Obtener una lista de todas las notas disponibles'''
    list_note = Files_List(
        files='Note_*.txt',
        path=get_path(),
        remove_path=True
    )
    
    list_ready = []
    for text in list_note:
        list_ready.append(
            (text.replace('Note_', '')).replace('.txt', '')
        )
    
    return list_ready


def get_last_note(path=get_path()):
    '''Devuelve el la ultima nota creada'''
    note_data = get_data()
    last_note_file = note_data['last_note']
    last_note = f"{path}Note_{last_note_file}.txt"

    if pathlib(last_note).exists():
        return last_note
    else:
        return None


def New(path=get_path(), text='texto'):
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
            note_archive = get_data(mode_dict=False)
            text_ready = ''
            for line in note_archive.split('\n'):
                if line.startswith('last_note='):
                    line = f'last_note={text}'
                else:
                    pass
                text_ready += line + '\n'

            with open('data/notas.dat', 'w') as last_note:
                last_note.write(text_ready[:-1])

            return file_ready
        except:
            # Si falla en la creación del archivo, retorna un none
            return False


def Edit(path=get_path(), text=''):
    '''Editar o ver una nota existente'''
    list_note = get_list(path=path)
    
    if text in list_note:
        # El archivo note_path existe en la list_note
        # Establece el la nota en last_note.dat
        note_archive = get_data(mode_dict=False)
        text_ready = ''
        for line in note_archive.split('\n'):
            if line.startswith('last_note='):
                line = f'last_note={text}'
            else:
                pass
            text_ready += line + '\n'

        with open('data/notas.dat', 'w') as last_note:
            last_note.write(text_ready[:-1])

        return f'{path}Note_{text}.txt'
    else:
        # El archivo note_path no existe en la list_note
        return None


def Remove(path=get_path(), text=''):
    '''Eliminar una nota'''
    '''Retorna un True o un False, si se puede o no borrar el archivo'''
    if os.path.isfile(f'{path}Note_{text}.txt'):
        # El arhcivo que se quiere eliminar es correcto
        os.remove(f'{path}Note_{text}.txt')
        return True

    else:
        # Ese no es un arhcivo o no existe.
        return False


def Change_Path(path=get_path()):
    '''Cambiar directorio de las notas a guardar'''
    '''Retorna un True o un False, si se puede o no cambiar el directorio'''
    if os.path.isdir(path):
        # El directorio si es correcto, ahora se guardara
        note_archive = get_data(mode_dict=False)
        text_ready = ''
        for line in note_archive.split('\n'):
            if line.startswith('path='):
                line = f'path={path}'
            else:
                pass
            text_ready += line + '\n'

        with open('data/notas.dat', 'w') as write_path:
            write_path.write(text_ready[:-1])
        return True

    else:
        # El directorio es incorrecto
        return False