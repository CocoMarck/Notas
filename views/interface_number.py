from core.display_number import get_display_number

WINDOW_MAIN_SIZE = [
    get_display_number( multipler=0.5, based="width" ),
    get_display_number( multipler=0.5, based="height" )
]

SET_ITEM_DIALOG_SIZE = [
    get_display_number( multipler=0.4, based="width" ),
    get_display_number( multipler=0.25, based="height" )
]

SET_PATH_DIALOG_SIZE = [
    get_display_number( multipler=0.4, based="width" ),
    get_display_number( multipler=0.1, based="height" )
]
