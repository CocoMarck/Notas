import models
from .logging_controller import LoggingController

class DatabaseController( LoggingController ):
    def __init__(
        self, database: models.StandardDatabase, verbose=False, log_level: str="warning", save_log: bool=True,
        only_the_value: bool=True
    ):
        self.database = database
        self.name = self.database.name_database
        
        # Log
        super().__init__(
            name=f"database_{self.name}", verbose=verbose, log_level=log_level, save_log=save_log,
            only_the_value=only_the_value
        )
    
    
    def start_database(self) -> bool | str:
        start_database = self.database.start_database()
        
        if start_database != None:
            log_type = "info"
            message = f"[SQL] Create tables:\n{start_database}"
            value = True
        else:
            log_type = "error"
            message = f"Bad statement"
            value = False
        
        return self.return_value( value=value, message=message, log_type=log_type )
    

    def execute_statement(
        self, sql_statement: str, commit: bool = False, return_type: str="cursor"
    ) -> str | bool | object | tuple | list:
        # Funcion
        execute = self.database.execute_statement( sql_statement, commit, return_type )
        
        # Mensaje
        log_type = "info"
        message = f"[SQL] Statement:\n{sql_statement}"
        if execute != None:
            if commit:
                message += "\n[COMMIT] Changes made"
            else:
                message += "\n[COMMIT] Discart changes"
        else:
            log_type = "error"
            message += f"\nBad sqlite statement"

        # Return
        return self.return_value( value=execute, message=message, log_type=log_type )
    

    def create_database(self) -> str:
        # Funcion
        create = self.database.create_database()
        
        # Mensaje
        if create == "database-already" or create == "database-created":
            log_type = "info"
            message = "[SQL] Database created"
        else:
            log_type = "warning"
            message = "The database could not be created"

        # Return
        return self.return_value( value=create, message=message, log_type=log_type )
    

    def delete_database(self) -> str:
        # Función
        delete = self.database.delete_database()
        
        if delete:
            log_type = "info"
            message = "[SQL] Database deleted"
        else:
            log_type = "warning"
            message = "[WARNING] Database not deleted"
        
        # Return
        return self.return_value( value=delete, message=message, log_type=log_type )
    

    def tables(self) -> str | list:
        # Función
        tables = self.database.tables()
        
        return_tables = []
        message = ""
        if tables != None:
            log_type = "info"
            message = (
                f"[SQL] Returning all tables\n"
                f"Tables: {tables}"
            )
            return_tables = tables
        else:
            log_type = "warning"
            message = "No detect tables"
        
        # Return
        return self.return_value( value=return_tables, message=message, log_type=log_type )
    
    
    def exists_table(self, table: str) -> bool | str:
        # Función
        exists_table = self.database.exists_table( table=table )
        
        if exists_table:
            message = f'[SQL] The table "{table}" exists'
        else:
            message = f'[SQL] No exists the table "{table}"'
        
        # Return
        return self.return_value( value=exists_table, message=message, log_type="info" )
    
    
    def delete_table(self, table: str) -> bool | str:
        delete = False
        if self.database.exists_table( table=table ):
            # Función
            delete = self.database.delete_table( table=table )
        
            if delete:
                message = f'[SQL] The table "{table}" was deleted'
            else:
                message = f'[SQL] The table "{table}" could not be deleted'
        else:
            message = f'[SQL] The table "{table}" does not exist and will not be deleted'
        
        # Return
        return self.return_value( value=delete, message=message, log_type="info" )
    
    
    def clear_database(self) -> bool | str:
        # Funcion
        clear = self.database.clear_database()
        
        if clear:   message = "[SQL] All tables were cleared"
        else:       message = "[SQL] There are no tables in the database"
        
        # Return
        return self.return_value( value=clear, message=message, log_type="info" )