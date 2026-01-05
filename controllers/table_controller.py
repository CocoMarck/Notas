import models
from core.time_util import get_datetime
from core.text_util import text_or_none
from .logging_controller import LoggingController




class TableController( LoggingController ):
    def __init__( 
        self, table: models.StandardTable, verbose: bool=True, log_level: str="warning", save_log: bool=True,
        only_the_value: bool=True
    ):
        self.table = table
        self.name = table.table
        
        # Log
        super().__init__( 
            name=f"table_{self.name.lower()}", verbose=verbose, log_level=log_level, save_log=save_log,
            only_the_value=only_the_value
        )
    
    
    def structure_sql_message(self, message:str, sql_statement:str, commit:bool):
        '''
        Estructurar mensaje
        '''
        final_message = f"{message} | [SQL] {sql_statement} | commit={commit}"
        return final_message
    
        
    def get_all_columns(self):
        '''
        Mostrar todas las columnas de la tabla.
        '''
        all_column = self.table.get_all_columns( )
        return_value = []
        if all_column == [] or all_column == None:
            message = f"{self.name}: Not have columns"
        else:
            message = f"{self.name}: Have columns:\n{all_column}"
            return_value = all_column

        return self.return_value( value=return_value, message=message, log_type="info" )
    

    def get_all_values(self):
        '''
        Mostrar todas los valores de la tabla.
        '''
        all_value = self.table.get_all_values( )
        return_value = []
        if all_value == [] or all_value == None:
            message = f"{self.name}: Not have values"
        else:
            message = f"{self.name}: Have values:\n{all_value}"
            return_value = all_value
        
        return self.return_value( value=return_value, message=message, log_type="info" )
        

    def get_all_values_without_soft_delete(self) -> str | None:
        '''
        Mostrar todos los valores sin baja
        '''
        all_value = self.table.get_all_values_without_soft_delete()
        return_value = []
        if all_value == [] or all_value == None:
            message = f"{self.name}: Not have values"
        else:
            message = f"{self.name}: Have values without soft delete:\n{all_value}"
            return_value = all_value
        
        return self.return_value( value=return_value, message=message, log_type="info" )
        

    def clear_table(self) -> str | bool:
        clear_table = self.table.clear_table()
        if clear_table != None:
            log_type = "info"
            message = f'[SQL]\n{clear_table}\nThe table {self.name} was clear'
            return_value = True
        else:
            log_type = "error"
            message = f'{self.name}'
            return_value = False
        
        return self.return_value( value=return_value, message=message, log_type=log_type )
        
        
        
    def delete_table(self) -> str | bool:
        delete_table = self.table.delete_table()
        if delete_table != None:
            log_type = "info"
            message = f'[SQL]\n{delete_table}\nThe table {self.name} was deleted'
            return_value = True
        else:
            log_type = "error"
            message = f'{self.name}'
            return_value = False
            
        return self.return_value( value=return_value, message=message, log_type=log_type )
        


    def delete_row_by_column_value(self, column: str, value: str) -> str | bool:
        delete_value = self.table.delete_row_by_column_value( column, value )
        
        if isinstance( delete_value, str ):
            log_type = "info"
            message = f'[SQL]\n{delete_value}'
            return_value = True
        else:
            log_type = "error"
            message = f'{self.name}'
            return_value = False
        
        return self.return_value( value=return_value, message=message, log_type=log_type )
    
    
    
    
    def get_columns_for_the_view(self) -> list:
        '''Obtener columnas para la vista'''
        COLUMNS = self.table.COLUMNS_FOR_THE_VIEW
        list_ready = []
        for key in COLUMNS.keys():
            list_ready.append( COLUMNS[key] )
        if list_ready == []:
            log_type = "error"
            message = "No columns"
        else:
            log_type = "info"
            message = f"Columns:\n{list_ready}"

        return self.return_value( value=list_ready, message=message, log_type=log_type )
    
    
    def get_values_for_the_view(self) -> list:
        '''Obtener valores para la vista'''
        values = self.table.get_values_for_the_view()
        if isinstance(values, list):
            log_type = "info"
            message = f"Values:\n{values}"
        else:
            values = []
            log_type = "error"
            message = f"No values"
        
        return self.return_value( value=values, message=message, log_type=log_type )