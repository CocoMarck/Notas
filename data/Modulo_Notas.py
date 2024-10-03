from logic.Modulo_System import(
    get_system
)
from logic.Modulo_Files import(
    Path,
    Files_List
)
from logic.Modulo_Text import(
    Text_Read,
    Ignore_Comment,
    Text_Separe
)
from interface.Modulo_ShowPrint import(
    Title
)
from entities import Nota

import os, sys
from pathlib import Path as pathlib

encoding = 'utf-8'

# Obtén la ruta al directorio actual del script
current_dir = os.path.dirname( os.path.abspath(sys.argv[0]) )

# Data
dir_data = os.path.join(current_dir, 'resources')
dir_icons = os.path.join( dir_data, 'icons')

# Construye la ruta a Languages desde el directorio que contiene el módulo
dir_note = os.path.join( 'resources', 'Notes' )
file_note = os.path.join(dir_data, 'notas.dat')




def get_data(mode_dict=True):
    '''
    Obtener datos de ultima nota o directorio de las notas, por medio de un diccionario.
    Obtener un texto str del archivo "notas.dat" 
    '''
    # Leer texto y ignorar comentarios tipo '#'
    note_archive = Text_Read(
        file_note,
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




preset = ['Note_', '.txt']








def get_list( Nota ):
    '''Obtener una lista de todas las notas disponibles'''
    list_note = Files_List(
        files = f'{preset[0]}*{preset[1]}',
        path = Path(Nota.path),
        remove_path = True
    )
    
    list_ready = []
    for text in list_note:
        list_ready.append(
            (text.replace(preset[0], '')).replace(preset[1], '')
        )
    
    return list_ready




def read_Nota( Nota ) -> bool:
    '''Establecer parametros'''
    Nota.path = get_data()['path']
    
    Nota.last_note = None
    Nota.note = None
    if not get_data()['last_note'].replace(' ', '') == '':
        Nota.last_note = get_data()['last_note']
        if pathlib( os.path.join( Nota.path, f'{preset[0]}{Nota.last_note}{preset[1]}') ).exists():
            Nota.note = os.path.join( Nota.path, f'{preset[0]}{Nota.last_note}{preset[1]}')

    
    return True




def save_Nota( Nota, save=None, remove=None ) -> bool:
    '''Guardar y esablecer parametros'''
    
    bool_value = False
    
    # Guardar nota
    if type(save) == str:
        # Nota a guardar
        note_to_save = os.path.join( Nota.path, f'{preset[0]}{save}{preset[1]}')

        # Establecer last_note o no
        if pathlib(Nota.path).exists():
            # Detectar que el texto exista y crear Archivo de texto
            if not pathlib( note_to_save ).exists():
                with open( note_to_save, 'w', encoding=encoding) as text_final:
                    text_final.write(
                        f'{Title(text=save, print_mode=False)}'
                    )
                Nota.last_note = save
                print('Nota guardada')
        
    
    # Remover nota
    if type(remove) == str:
        note_remove = os.path.join(Nota.path, f'{preset[0]}{remove}{preset[1]}')
        if os.path.isfile( note_remove ):
            bool_value = True
            # Existe el archivo, se eliminara
            os.remove( note_remove )
            print('Nota eliminada')
            
            if Nota.last_note == remove:
                Nota.last_note = None
    

    # Establecer last_note al archivo notas.dat
    if Nota.last_note == get_data()['last_note']:
        print('Nota ya establecida previamente')

    elif Nota.last_note == None:
        print('Quitar ultima nota accedida')
        note_archive = get_data(mode_dict=False)
        text_ready = ''
        for line in note_archive.split('\n'):
            if line.startswith('last_note='):
                line = f'last_note='
            else:
                pass
            text_ready += line + '\n'

        with open(file_note, 'w', encoding=encoding) as last_note:
            last_note.write(text_ready[:-1])

    else:
        print( 'Establecer ultima nota accedida al archivo' )
        note_archive = get_data(mode_dict=False)
        text_ready = ''
        for line in note_archive.split('\n'):
            if line.startswith('last_note='):
                line = f'last_note={Nota.last_note}'
            else:
                pass
            text_ready += line + '\n'

        with open(file_note, 'w', encoding=encoding) as last_note:
            last_note.write(text_ready[:-1])
    


    # Si exsite la carpeta, guardarla en el archivo
    if not Nota.path == get_data()['path']:
        if pathlib(Nota.path).exists():
            print('Guardando nueva ruta en el archivo')
            bool_value = True
        else:
            print('Ruta erronea, estableciendo una default')
            Nota.path = dir_note
        
        # Agregarndo path en notas.dat
        note_archive = get_data(mode_dict=False)
        text_ready = ''
        for line in note_archive.split('\n'):
            if line.startswith('path='):
                line = f'path={Nota.path}'
            text_ready += line + '\n'

        with open(file_note, 'w', encoding=encoding) as path_note:
            path_note.write(text_ready[:-1])
    

    # Eetablecer archivo actual si es que existe
    Nota.note = None
    if not Nota.last_note == None:
        if pathlib( os.path.join( Nota.path, f'{preset[0]}{Nota.last_note}{preset[1]}') ).exists():
            Nota.note = os.path.join( Nota.path, f'{preset[0]}{Nota.last_note}{preset[1]}')
    
    
    return bool_value



data_Nota = Nota
read_Nota( data_Nota )