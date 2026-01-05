import datetime, calendar

# Constantes
MULTIPLER_MILLISECOND = 1
MULTIPLER_SECOND = 1000
MULTIPLER_MINUTE = 60
MULTIPLER_HOUR = 60
MULTIPLER_DAY = 24

MILLISECOND = 1 * MULTIPLER_MILLISECOND
MILLISECOND_PER_SECOND = MILLISECOND * MULTIPLER_SECOND
MILLISECOND_PER_MINUTE = MILLISECOND_PER_SECOND * MULTIPLER_MINUTE
MILLISECOND_PER_HOUR = MILLISECOND_PER_MINUTE * MULTIPLER_HOUR
MILLISECOND_PER_DAY = MILLISECOND_PER_HOUR * MULTIPLER_DAY


# Diccionario
TIME_VALUES = {
    "millisecond": MILLISECOND,
    "second": MILLISECOND_PER_SECOND,
    "minute": MILLISECOND_PER_MINUTE,
    "hour": MILLISECOND_PER_HOUR,
    "day": MILLISECOND_PER_DAY
}

TIME_MULTIPLER = {
    "millisecond": MULTIPLER_MILLISECOND,
    "second": MULTIPLER_SECOND,
    "minute": MULTIPLER_MINUTE,
    "hour": MULTIPLER_HOUR,
    "day": MULTIPLER_DAY
}


DATETIME_FORMAT = "yyyy-MM-ddTHH:mm:ss"



def get_time( 
        value: int, value_type: str = "minute", convert_to: str = "hour"
    ):
    '''
    # Función milisegundos, segundos, minutos, horas, dias
    Obtener el valor en milisegundos, segundos, minutos, horas, o dias.
    
    Permite convertir el valor `x` de tipo `y` a tipo `z`. Donde los tipo `y` y `z`, pueden ser:
    - millisecond
    - second
    - minute
    - hour
    - day
    
    Parametros:
        Son tres parametros: `value: int | float`, `value_type: str`, y `convert_to: str`
    
    Ejemplo e uso
    ```python
    get_time( 60, "minute", "hour" )
    
    # Su resultado sera: 1.0
    ```
    
    Retunrs:
        *Por lo general devolvera un float, debido a la operación de conversión*
        int | float
    '''
    
    if ( value_type in TIME_VALUES.keys() ) and ( convert_to in TIME_VALUES.keys() ):
        millisecond_value = value*TIME_VALUES[value_type]
        
        if TIME_VALUES[value_type] != TIME_VALUES[convert_to]:
            ready_value = millisecond_value / TIME_VALUES[convert_to]
        elif TIME_VALUES[value_type] == TIME_VALUES[convert_to]:
            ready_value = value
        
        return ready_value

    else:
        return value



def set_datetime_formatted( obj: datetime.datetime ):
    return str( obj.replace(microsecond=0).isoformat() )
    

def set_time_formatted( obj: datetime.time ):
    return str( obj.replace(microsecond=0).isoformat() )


def set_date_formatted( obj: datetime.date ):
    return str( obj.isoformatted() )
        
        
def get_datetime( mode: str="dateTime") -> str:
    '''
    Devolver fecha completa actual
    '''
    dateTime = set_datetime_formatted( datetime.datetime.now() )
    if mode == "date" or mode == "time":
        time_or_date = dateTime.split("T")
        
        if mode == "date":
            return time_or_date[0]
        elif mode == "time":
            return time_or_date[1]
    else:
        return dateTime


def get_first_day_of_the_month( obj: datetime.datetime = datetime.datetime.now() ) -> str:
    '''
    Devolver dia inicial del mes incicado, como fecha completa. Por defecto el mes actual
    '''
    obj_ready = obj.replace( day = 1, hour = 0, minute = 0, second = 0 )
    return set_datetime_formatted( obj_ready )


def get_end_day_of_the_month( obj: datetime.datetime = datetime.datetime.now() ) -> str:
    '''
    Devolver dia final del mes indicado, como fecha completa. Por defect el mes actual
    '''
    final_day = calendar.monthrange( obj.year, obj.month )
    obj_ready = obj.replace( 
        day = int(final_day[1]), hour = 0, minute = 0, second = 0
    )
    
    return set_datetime_formatted(obj_ready)



def separate_datetime_formatted( datetime_formatted: str, return_only: None  ) -> list | str:
    '''
    Separar tiempo y fecha
    '''
    separate = datetime_formatted.split("T")
    if return_only == "date":
        return separate[0]
    elif return_only == "time":
        return separate[1]    
    else:
        return separate


def get_date_from_formatted_datetime( datetime_formatted: str ):
    '''
    Obtener solo la fecha de un datetime
    '''
    return separate_datetime_formatted(
        datetime_formatted=datetime_formatted, return_only="date" 
    )


def get_time_from_formatted_datetime( datetime_formatted: str ):
    '''
    Obtener solo el tiempo de un date time
    '''
    return separate_datetime_formatted( 
        datetime_formatted=datetime_formatted, return_only="time" 
    )