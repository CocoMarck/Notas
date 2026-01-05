import os, sys, sqlite3
from utils.resource_loader import ResourceLoader
from core.sqlite_util import detect_list_datatype, from_list_to_string, struct_table_statement



class StandardDatabase():
    '''
    Un objeto modelo estandar para manejar una base de datos sqlite3
    
    Crea borra y se conecta a la db. Puede ejecutar sql statement directamente al db.
    Se puede usar para ejcutar sql statement de forma general.
    Se recomienda manejar las tablas con un StandardTable.

    Tiene metodos generales como:
        get_table_all_column, get_table_all_value.
    
    No tiene funciones especificas de manejo de columnas como: get_id. Eso lo maneja el modelo tabla.
    
    Para funcion `start_database`
    Atributo `self.dictionary_of_tables = {}`
    Es un diciconario asi: `{ "table" : [ "column difinition" ] }`
    
    Atributo `self.additional_instructions_for_tables = []`
    Una lista así: `[ "instruction" ]`
    '''
    def __init__(self, name_database=str, name_dir_data: str="data"  ):
        # Ruta
        self.__resource_loader = ResourceLoader()
        self.name_dir_data = name_dir_data
        self.name_database = name_database
        
        # Ruta | Declarar dir_data y path_database
        self.set_directory_data()
        self.set_database_path()
        
        # Tablas a generar
        self.dictionary_of_tables = {}
        self.additional_instructions_for_tables = []
        self.instructions_after_creating_tables = []
        
    
    def instruction_to_create_tables(self) -> list[str]:
        '''
        Lista de instrucciones para crear tabla
        '''
        list_instruction = []
        for key in self.dictionary_of_tables.keys():
            list_instruction.append( 
                struct_table_statement(
                    type_statement = "create-table", table = key,
                    sql_statement = self.dictionary_of_tables[key]
                )
            )
        return list_instruction


    def start_database(self) -> str | None:
        # Crear base de datos
        create = self.create_database()
        
        # Texto final
        instruction_text = ""
        
        # Instrucciones adicionales
        if (
            isinstance(self.additional_instructions_for_tables, list) and
            self.additional_instructions_for_tables != []
        ):
            additional_instruction = False

            for sql_statement in self.additional_instructions_for_tables:
                additional_instruction = self.execute_statement(
                    sql_statement=sql_statement, commit=True, return_type="bool"
                )        
                instruction_text += sql_statement + "\n"
        else:
            additional_instruction = True

        # Crear tablas
        instruction = False
        for sql_statement in self.instruction_to_create_tables():
            instruction = self.execute_statement(
                sql_statement=sql_statement, commit=True, return_type="bool"
            )
            instruction_text += sql_statement + "\n"
            
        # Instrucciones despues de crear tabla
        if (
            isinstance(self.instructions_after_creating_tables, list) and
            self.instructions_after_creating_tables != []
        ):
            additional_instruction_two = False

            for sql_statement in self.instructions_after_creating_tables:
                additional_instruction_two = self.execute_statement(
                    sql_statement=sql_statement, commit=True, return_type="bool"
                )        
                instruction_text += sql_statement + "\n"
        else:
            additional_instruction_two = True
        
        # Deveolver o no instruccion
        if create and additional_instruction and instruction and additional_instruction_two:
            return instruction_text[:-1]
        else:
            return None


    def set_directory_data(self) -> None:
        '''
        Función necesaria para declarar el atrubuto: dir_data
        '''
        self.__resource_loader.data_dir = self.__resource_loader.get_base_path( self.name_dir_data )
        self.dir_data = self.__resource_loader.data_dir
    
    
    def set_database_path(self) -> None:
        '''
        Función necesaria para declarar el atrubuto: path_database
        '''
        self.path_database = self.__resource_loader.get_data( f'{self.name_database}.db' )
    
    
    def connect(self) -> sqlite3.Connection:
        '''
        Conectar con db y devolver la coneccion
        '''
        return sqlite3.connect( self.path_database )
    
    
    def execute_statement(
        self, sql_statement: str, commit: bool = True, return_type: str = "cursor"
    ) -> None | tuple | list | object:
        '''
        Ejecutar alguna instrucción. 
        
        Returns:
            list | tuple | None | cursor: 
            Devuelve algo si la instrucción se realizo correctamente (Por defecto un objeto cursor).
            Devuelve None si no pudo.
        '''
        # Ejecutar instrucción
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("BEGIN TRANSACTION") # Iniciar transacción Para que jale el rollback
                cursor.execute(sql_statement)

                if commit:
                    conn.commit()
                else:
                    conn.rollback()

                if return_type == "cursor":
                    return cursor
                elif return_type == "fetchall":
                    return cursor.fetchall()
                elif return_type == "fetchone":
                    return cursor.fetchone()
                elif return_type == "statement":
                    return sql_statement
                else:
                    return True

        #except sqlite3.OperationalError as e:
        except Exception as e:
            return None
    

    def create_database(self) -> str | None:
        '''
        Crear base de datos vacia.
        
        Returns:
            bool: Si se crea la tabla True, de lo contrario False.
        '''
        message = None
        if os.path.isfile(self.path_database):
            message = "database-already"
        else:
            try:
                message = "database-created"
                conn = self.connect()
                conn.close()
            except:
                pass
        return message
                
                
    def delete_database(self) -> bool:
        '''
        Remueve base de datos
        '''
        if os.path.isfile( self.path_database ):
            os.remove( self.path_database )
        
        return not os.path.isfile( self.path_database )
    

    def tables(self) -> list | None:
        '''
        Detecta todas las tablas disponibles
        
        Returns:
            list | None: Lista de tablas que tiene la base de datos. O none si no se pudo.
        '''
        fetchall_tables = self.execute_statement( 
            sql_statement=struct_table_statement( "tables" ), 
            commit=False, return_type="fetchall" 
        )
        tables = []
        if fetchall_tables != None:
            for name in fetchall_tables:
                tables.append( name[0] )
            return tables
        else: return None
        
    

    def exists_table(self, table: str) -> bool:
        '''
        Detecta si existe una tabla
        
        Returns:
            bool: True si existe, False si no existe.
        '''
        all_tables = self.tables()
        exists = False
        if all_tables != None:
            for table_name in all_tables:
                if table == table_name:
                    exists = True
                    break
        return exists
    

    def delete_table(self, table: str) -> bool:
        '''
        Borra una tabla existente.

        Returns:
            bool: True si borra tabla o no existe tabla, False si existe pero no puede borrar tabla.
        '''
        sql_statement = struct_table_statement( "delete-table", table )
        return ( self.execute_statement(sql_statement, commit=True, return_type="bool") != None )
    

    def clear_database(self) -> bool:
        '''
        Borra todas las tablas
        
        Returns:
            bool: True borra todas las tablas. Lo contrario es un false.
        '''
        all_tables = self.tables()
        if all_tables != None:
            # Aca pasa el False
            all_deleted = True
            for table_name in all_tables:
                if self.delete_table( table=table_name ) == False: 
                    all_deleted = False
            return all_deleted
        else:
            return True
    

    def get_table_all_columns(self, table: str) -> list | None:
        #sql_statement = f"SELECT * FROM {table};"
        sql_statement = struct_table_statement( "select-column", table, "*" )
        cursor = self.execute_statement( sql_statement, commit=False, return_type="cursor" )

        if cursor != None:
            # Establecer lista, y deveolver lista
            return_list = []
            for x in cursor.description:
                return_list.append( x[0] )
        
            return return_list
        else:
            return None
    
    
    def get_table_all_values(self, table: str) -> list | None:
        sql_statement = struct_table_statement( "select-column", table, "*" )
        #sql_statement = struct_table_statement( 
        #    "select-column", table, self.get_table_all_columns( table=table )
        #)
        return self.execute_statement( sql_statement=sql_statement, commit=False, return_type="fetchall" )