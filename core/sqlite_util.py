from .list_util import detect_list_datatype, from_list_to_string

    
    
def struct_table_statement( 
    type_statement: str, table: str=str, 
    sql_statement: str | list[str] | list[list[str]] = str
) -> str:
    '''
    Estructurar una Declaración para sqlite3 dependiendo de los parametros.
    
    Args:
        type_statement: str: Tipo de instrucción, opciones:
            create-table, para crear una tabla.
            select-column, para seleccionar una columna
            insert-or-update, para insertar dato o actualizar dato en tabla.
            delete-value, para borrar un valor en una tabla (columna/valor).
        table: str.
            Nombre de la tabla.
        sql_statement: str | list[str] | list[list[str]]
            datos para estructurar en la declaración.
    
    Returns:
        string: Declaración para sqlite3
    '''
    # Inicailizar
    type_statement = type_statement.lower().replace( " ", "")
    full_sql_statement = ""
    
    go = False
    if type_statement == "tables" or type_statement == "delete-table":
        # Forzar statement
        go = True
    else:
        # Determinar tipo de dato            
        data_type = detect_list_datatype(sql_statement, str)
        
        # Establecer o no statement
        go = (data_type != None) and isinstance(table, str)
    
    # Opciones
    space = "    "
    if go:
        if type_statement=='create-table':
            parameter = from_list_to_string( sql_statement, space=space )
                
            # Instrucción completa | Ejecución de instrucción
            full_sql_statement = (
                f"CREATE TABLE IF NOT EXISTS {table}(\n"
                f"{parameter}\n"
                f");"
            )
        elif type_statement=='select-column':
            if data_type == list[str]:
                column = from_list_to_string( sql_statement )
            else:
                column = sql_statement

            full_sql_statement = (
                f'SELECT {column} FROM {table};'
            )

        elif type_statement=='insert-or-update' and data_type == list[str]:
            column = sql_statement[0]
            value = sql_statement[1]
            conflict = sql_statement[2]
            
            full_sql_statement = (
                f"INSERT OR IGNORE INTO {table} ({column})\n"
                f"VALUES({value})\n"
                f"ON CONFLICT({conflict}) DO UPDATE SET {column}={value};"
            )
        elif type_statement=="delete-value" and data_type == list[str]:
            column = sql_statement[0]
            value = sql_statement[1]
            full_sql_statement = (
                f'DELETE FROM {table}\n'
                f'WHERE {column} = {value};'
            )
        
        # Los que solo necesitan "type_statement"
        elif type_statement=="delete-table":
            full_sql_statement = f"DROP TABLE IF EXISTS {table};"
        
        elif type_statement=="tables":
            full_sql_statement = "SELECT name FROM sqlite_master WHERE type='table';"
        

    return full_sql_statement