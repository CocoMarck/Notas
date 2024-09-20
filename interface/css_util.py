# Listar los widgets
def get_list_text_widget( option='Qt' ) -> list:
    if option == 'Qt':
        list_text_widget = [
            'Label',
            'ComboBox',
            'LineEdit',
            'PushButton',
            'TextEdit'
        ]
        number = 0
    elif option == 'Gtk':
        list_text_widget = [
            'button',
            'label',
            'combobox',
            'entry',
            'textview',
        ]
        

    # Devolver la lista
    for index in range(0, len(list_text_widget) ):
        if option == 'Qt':
            list_text_widget[index] = f'Q{list_text_widget[index]}'
        elif option == 'Gtk':
            list_text_widget[index] = list_text_widget[index].lower()

    return list_text_widget



# Estilo de programa
def text_widget_style( widget=None, font=None, font_size=None, margin=None, padding=None, idented=0 ):
    '''Obtener estido para el widget'''
    text = ''

    # Establecer si se pondran corchetes o no {}
    # Inicio de corchete (solo si shell esta en true)
    shell = False
    if type(widget) == str:
        shell = True
        text += widget
        text += ' {\n'

    # Establecer el espacio de indentado
    space = ''
    if idented > 0:
        for x in range(0, idented):
            space += ' '


    # Agregar o no parametros
    if type(font) == str:
        text += f'{space}font-family: {font};\n'

    if type(font_size) == int:
        text += f'{space}font-size: {font_size}px;\n'

    if type(margin) == int:
        margin_xy = [int(margin/2), int(margin/4)]
        text += (
            f'{space}margin-left: {margin_xy[0]}px;\n'
            f'{space}margin-right: {margin_xy[0]}px;\n'
            f'{space}margin-top: {margin_xy[1]}px;\n'
            f'{space}margin-bottom: {margin_xy[1]}px;\n'
        )

    if type(padding) == int:
        text += f'{space}padding: {padding}px;\n' # Size adicional para el widget


    # Cierre de corchete
    if shell == True:
        text += '}\n'


    # Devolver texto
    return text
