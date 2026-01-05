from .standard_database import StandardDatabase, struct_table_statement


class StandardTable():
    '''
    Para manejar una tabla de una base de datos.
    No crea tablas, no crea la base de datos. No tiene funcion para ejecutar sql statements
    Usa un StandartDatabase, para manejar una tabla. Solo una tabla.
    
    Constante, alias, permite obtener los alias de la tabla y tambien las tablas relacionadas con esta tabla
    '''
    def __init__(
        self, database: StandardDatabase, table=str
    ):
        self.database = database
        self.table = table
        self.column_soft_delete = "softDelete"
        
        # Alias
        self.ALIAS = {
            "table": "a"
        }
        # Columnas relacionadas con la vista. Columnas para la vista.
        self.COLUMNS_FOR_THE_VIEW = {}
        
    
    def execute_and_return_values(
        self, sql_statement:str, commit=False, return_type="statement") -> (object, str, bool
    ):
        '''
        Ejecutar un sql_statement
        El resultado del ejecución, y devolver valores, como commit, y el statement.
        '''
        value = self.database.execute_statement( 
            sql_statement=sql_statement, commit=commit, return_type=return_type 
        )
        return value, sql_statement, commit
    

    def get_alias(self, alias="table", point: bool=False) -> str:
        '''
        Obtener alias
        '''
        if alias in self.ALIAS.keys():
            if point == True:
                return f"{self.ALIAS[alias]}."
            else:
                return self.ALIAS[alias]
        else:
            return ""

    def get_all_columns(self) -> list:
        '''
        Mostrar todas las columnas de la tabla.
        '''
        return self.database.get_table_all_columns( table=self.table )
    
    def get_all_values(self) -> list:
        '''
        Mostrar todas los valores de la tabla.
        '''
        return self.database.get_table_all_values( table=self.table )
        
    def get_all_values_without_soft_delete(self) -> str | None:
        '''
        Obtener datos sin baja
        '''
        sql_statement = (
            f"SELECT * FROM {self.table} WHERE {self.column_soft_delete}=0;"
        )
        return self.database.execute_statement( sql_statement, commit=False, return_type="fetchall" )
        
    def get_type_parameter(self):
        '''
        sqlite3 Obtener tipo de dato de las columnas de la tabla
        '''
        pass
    
    def clear_table(self) -> str | None:
        '''
        sqlite3 Eliminar todos las filas de la tabla.
        
        DELETE FROM table;

        Para eliminar secuencia autoincrement de tabla (si es que tiene)
        DELETE FROM sqlite_sequence WHERE name='tabla';
        '''
        
        # Instrucciones SQLite
        sqlite_sequence = self.database.execute_statement( 
            f"DELETE FROM sqlite_sequence WHERE name='{self.table}';", commit=True, return_type="statement"
        )
        clear_table = self.database.execute_statement( 
            f'DELETE FROM "{self.table}";', commit=True, return_type="statement"
        )
        
        # Determinar qeue devolver
        sql_statement = ""
        return_string = False

        if isinstance(clear_table, str):
            sql_statement += f"{clear_table} "
        if isinstance(sqlite_sequence, str):
            sql_statement += sqlite_sequence
        if isinstance(clear_table, str) or isinstance(sqlite_sequence, str):
            return_string = True
        
        # Devovler valor, ya sea None o str
        if return_string == True:
            return sql_statement
        else:
            return None
    

    def delete_table(self) -> str | None:
        full_sql_statement = self.clear_table()
        if full_sql_statement == None:
            full_sql_statement = ""
        
        sql_statement = self.database.delete_table( self.table )
        if sql_statement == True:
            full_sql_statement += f"\nDROP {self.table};"
        
        if full_sql_statement == "":
            full_sql_statement = None
        
        return full_sql_statement
    
    
    def delete_row_by_column_value(self, column: str, value: str) -> str | None:
        '''
        Eliminar una fila por el valor de una columna. Normalmente el Id.
        '''
        sql_statement = struct_table_statement( 
            type_statement="delete-value", table=self.table, sql_statement=[ column, value ]
        )
        
        # Ejecutar instrucción
        delete_value = self.database.execute_statement( 
            sql_statement, commit=True, return_type="statement"
        )
        return delete_value
    
    
    
    
    def get_values_for_the_view(self) -> list | None:
        '''
        Obtener valores de la vista.
        '''
        columns_text = ""
        for key in self.COLUMNS_FOR_THE_VIEW.keys():
            columns_text += f"{self.COLUMNS_FOR_THE_VIEW[key]}, "
        
        # Retornar valores de columnas vista.
        if columns_text != "":
            columns_text = columns_text[:-2]
        
            sql_statement = (
                f"SELECT {columns_text} FROM {self.table}"
            )
            return self.database.execute_statement( sql_statement, commit=False, return_type="fetchall" )

        # Retornar valores de todosa las columnas
        else:
            return self.get_all_values()