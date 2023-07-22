import os
from pathlib import Path as pathlib

from Modulos.Modulo_Util import (
    System,
    CleanScreen,
    Text_Read
)
from Modulos.Modulo_ShowPrint import (
    Title,
    Continue,
    Separator
)
from Modulos.Modulo_Language import (
    get_text as Lang
)
import Modulos.Modulo_Notas as Notas


path = 'Notes/'
path_main = os.getcwd()


def Menu_Main():
    loop = True
    while loop == True:
        # Parte visual
        CleanScreen()
        Title('Notas')
        text = (
            f'1. Crear una nueva nota.\n'
            f'2. Editar o ver una nota.\n'
            f'3. Eliminar una nota\n'
            f'0. {Lang("exit")}'
        )
        option = input(
            text + '\n'
            f"{Lang('set_option')}: "
        )
        
        # Opcion elegida
        if option == '1':
            New_Note()

        elif option == '2':
            Edit_Note()

        elif option == '3':
            pass

        elif option == '0':
            loop = False

        else:
            pass


def New_Note():
    # Parte visual
    CleanScreen()
    Title(f'Nueva Nota')
    text = input(f'{Lang("name")}: ')
    
    # Texto de input
    if text == '':
        # Si no escribio nada entonces, el texto sera texto
        text = 'texto'
    else:
        # Normal, el imput es correcto.
        pass
    
    # Crear el archivo necesario.
    text_ready = Notas.New(path=path, text=text)
    if type(text_ready) is str:
        # Abrir nano en base al texto creado
        os.system(f'nano {text_ready}')

    elif type(text_ready) is list:
        # El texto creado ya existe, y abrirlo con nano.
        input(
            text_ready[0] + '\n'
            f'{Lang("continue_enter")}...'
        )
        os.system(f'nano {text_ready[1]}')

    else:
        # Fallo en la creación del archivo
        # O El input tiene caracteres erroneos
        # Hay un Error
        input(
            f'Error - Fallo en la creación del archivo\n'
            f'{Lang("continue_enter")}...'
        )


def Edit_Note():
    # Parte visual
    CleanScreen()
    Title('Ver notas')
    text = f'1. Ultima nota\n'

    number = 1
    dict_text = {}
    for note in Notas.get_list(path=path):
        number += 1
        dict_text.update({ str(number) : note })
    
    for key in dict_text.keys():
        text += f'{key}. {dict_text[key]}\n'

    option = input (
        text + '\n'
        f'{Lang("set_option")}: '
    )
    
    # Opcion elegida
    if option == '1':
        # Ultimo texto creado
        pass

    elif option in dict_text:
        # Eleguir una nota, entre las notas existentes.
        print(path)
        print(dict_text[option])
        edit = Notas.Edit(path=path, text=dict_text[option])
        os.system(f'nano {edit}')

    else:
        # No hacer nada, no existe esa opcion
        pass


if __name__ == '__main__':
    Menu_Main()