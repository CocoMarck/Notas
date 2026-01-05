from logic.Modulo_System import *
import os, sys

# Obtén la ruta al directorio actual del script
current_dir = os.path.dirname( os.path.abspath(sys.argv[0]) )

# Data
dir_data = os.path.join(current_dir, 'resources')

# Subcarpeta
dir_icon = os.path.join( dir_data, 'icons' )

# Archivos
file_icon = os.path.join( dir_icon, 'Icono-Notas.png' )

# Archivos | Fuente de texto
if get_system() == 'win':
    #font = 'Cascadia Code'
    file_font = 'Consolas'
    #font = 'times'
else:
    file_font = 'Liberation Mono'
