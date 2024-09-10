import os

from logic.Modulo_System import (
    get_system,
    CleanScreen
)
from logic.Modulo_Text import (
    Text_Read
)
from interface.Modulo_ShowPrint import (
    Title,
    Continue,
    Separator
)
from data.Modulo_Language import (
    get_text as Lang,
    YesNo
)
import data.Modulo_Notas as Notas


#path = 'Notes/'
#path_main = os.getcwd()


def Menu_Main():
    loop = True
    while loop == True:
        # Parte visual
        CleanScreen()
        Title('Notas')
        text = (
            f'1. {Lang("new_note")}.\n'
            f'2. {Lang("edit_note")}.\n'
            f'3. {Lang("remove_note")}\n'
            f'4. {Lang("change_main_dir")}\n'
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
            Remove_Note()
        
        elif option == '4':
            Change_Path_Note()

        elif option == '0':
            loop = False

        else:
            pass


def New_Note():
    # Parte visual
    CleanScreen()
    Title(Lang('new_note'))
    text = input(f'{Lang("name")}: ')
    
    # Texto de input
    if text == '':
        # Si no escribio nada entonces, el texto sera texto
        text = 'texto'
    else:
        # Normal, el imput es correcto.
        pass
    
    # Crear el archivo necesario.
    text_ready = Notas.New( text=text)
    if type(text_ready) is str:
        # Abrir nano en base al texto creado
        if get_system() == 'linux':
            os.system(f'nano "{text_ready}"')
        elif get_system() == 'win':
            os.system(f'notepad "{text_ready}"')

    elif type(text_ready) is list:
        # El texto creado ya existe, y abrirlo con nano.
        input(
            Lang('this_file_exists') + '\n'
            f'{Lang("continue_enter")}...'
        )
        if get_system() == 'linux':
            os.system(f'nano "{text_ready[1]}"')
        elif get_system() == 'win':
            os.system(f'notepad "{text_ready[1]}"')

    else:
        # Fallo en la creación del archivo
        # O El input tiene caracteres erroneos
        # Hay un Error
        input(
            f'ERROR - {Lang("error_create_file")}\n'
            f'{Lang("continue_enter")}...'
        )


def Edit_Note():
    # Parte visual
    CleanScreen()
    Title(Lang('edit_note'))
    text = f'1. {Lang("last_note")}\n'

    number = 1
    dict_text = {}
    for note in Notas.get_list():
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
        edit = Notas.get_last_note()
        if type(edit) is str:
            if get_system() == 'linux':
                os.system(f'nano "{edit}"')
            elif get_system() == 'win':
                os.system(f'notepad "{edit}"')
        elif edit == None:
            input(
                f'{Lang("no_note")}.\n'
                f'{Lang("continue_enter")}...'
            )

    elif option in dict_text:
        # Eleguir una nota, entre las notas existentes.
        edit = Notas.Edit(text=dict_text[option])
        if get_system() == 'linux':
            os.system(f'nano "{edit}"')
        elif get_system() == 'win':
            os.system(f'notepad "{edit}"')

    else:
        # No hacer nada, no existe esa opcion
        pass


def Remove_Note():
    # Parte visual
    CleanScreen()
    Title(Lang('remove_note'))

    number = 0
    dict_text = {}
    for note in Notas.get_list():
        number += 1
        dict_text.update({ str(number) : note })

    text = ''
    for key in dict_text.keys():
        text += f'{key}. {dict_text[key]}\n'

    option = input (
        text + '\n'
        f'{Lang("set_option")}: '
    )
    
    # Opcion elegida
    if option in dict_text:
        # Eleguir una nota, entre las notas existentes.
        if Notas.Remove(text=dict_text[option]) == True:
            # Se pudo remover
            print(Lang('remove_good'))
        else:
            # No se pudo remover
            print(Lang('remove_not_good'))
            
        input(f'{Lang("continue_enter")}...')

    else:
        # No hacer nada, no existe esa opcion
        pass


def Change_Path_Note():
    CleanScreen()
    Title(Lang("dir_main"))
    print(
        f'{Lang("dir_current")}:\n' +
        Notas.get_path() + '\n'
    )
    option = Continue(
        Lang("change_main_dir")
    )
    
    if option == YesNo('yes'):
        new_path = Notas.Change_Path(
            path=input(f'{Lang("dir")}: ')
        )
        if new_path == True:
            print( Lang('dir_change_good') )
        elif new_path == False:
            print( Lang('dir_change_not_good') )

        input(f'{Lang("continue_enter")}...')

    elif option == YesNo('no'):
        pass


if __name__ == '__main__':
    Menu_Main()
