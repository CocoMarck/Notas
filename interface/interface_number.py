'''
Este modulo es para información numerica relacionada con la interfaz.
Por ejemplo:
Valores xy de dimenciónes de ventana.
Valores xy de para fuente de texto.
Valores xy de para iconos.
'''
from logic.display_number import *


# Establecer dimenciones de windegts y ventana
# Limite de resolucion: Anchura y altura de 480px como minimo.
num_font = get_display_number(divisor=120)
num_space_padding = int(num_font/3)

nums_win_main = [
    get_display_number(multipler=0.15, based='width'),
    get_display_number(multipler=0.2, based='height')
]
nums_win_edit_remove = [
    get_display_number(multipler=0.15, based='width'),
    get_display_number(multipler=0.25, based='height')
]
nums_win_new = [
    get_display_number(multipler=0.2, based='width'),
    get_display_number(multipler=0.12, based='height')
]
nums_win_change_dir = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.12, based='height')
]
nums_win_text_edit = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.25, based='height')
]