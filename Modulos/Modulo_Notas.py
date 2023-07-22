from Modulos.Modulo_Util import(
    System,
    Files_List
)
from Modulos.Modulo_Language import(
    get_lang as Lang
)

import os
from pathlib import Path as pathlib


def get_list(path=''):
    '''Obtener una lista de todas las notas disponibles'''
    list_note = Files_List(
        files='Note_*.txt',
        path=path,
        remove_path=True
    )
    
    list_ready = []
    for text in list_note:
        list_ready.append(
            (text.replace('Note_', '')).replace('.txt', '')
        )
    
    if list_ready == []:
        return None
    else:
        return list_ready


def New(path='./', text='texto'):
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
                    f'title={text}'
                )
            return file_ready
        except:
            # Si falla en la creación del archivo, retorna un none
            return None


def Edit(path='', text=''):
    '''Editar o ver una nota existente'''
    list_note = get_list(
        path=path
    )
    
    if text in list_note:
        return f'{path}Note_{text}.txt'
    else:
        return None


def Remove():
    '''Eliminar una nota'''
    pass