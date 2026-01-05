from models import LanguageConfigTable
from controllers.table_controller import TableController




class LanguageConfigTableController( TableController ):
    def __init__(self, log_level="warning" ):
        super().__init__( table=LanguageConfigTable(), log_level=log_level )
    
    
    
    def get_list_of_languages(self):
        languages = self.table.get_list_of_languages()
        if languages == []:
            log_type = "error"
            message = "No languages were detected"
        else:
            log_type = "info"
            message = "There are languages"

        return self.return_value( value=languages, message=message, log_type=log_type)
        
        
    
    def select_language(self):
        # Obtener valor, y si no hay, ponerle uno default
        value, sql_statement, commit = self.table.select_language()
        if isinstance(value, tuple):
            language = value[0]
            log_type = "info"
            message = f"Language: {language}"
        else:
            language = None
            log_type = "error"
            message = f"El lenguaje no existe"
        message = self.structure_sql_message( message, sql_statement, commit )

        # Devolver
        return self.return_value( value=language, message=message, log_type=log_type)
    
    
    def get_language(self):
        language, sql_statement, commit, warning = self.table.get_language()
        if warning:
            log_type = "warning"
            message = f"El lenguaje no existe, devolviendo: {language}"
        else:
            log_type = "info"
            message = f"Language: {language}"
        message = self.structure_sql_message( message, sql_statement, commit )
        
        return self.return_value( value=language, message=message, log_type=log_type )
        
    
    
    def update_language(self, language=str):
        if isinstance(language, str):        
            value, sql_statement, commit = self.table.update_language( language=language )
            if value:
                log_type = "info"
                message = f"Now, de language is: {language}"
            else:
                log_type = "error"
                message = f"Very strange case, update cannot be performed"
            message = self.structure_sql_message( message, sql_statement, commit )
        else:
            log_type = "error"
            message = "The language parameteris are not a string"
            value = False
        
        return self.return_value( value=value, message=message, log_type=log_type )