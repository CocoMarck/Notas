from models import LanguageTable, LanguageConfigTable
from models.model_names.language_names import DEFAULT_LANGUAGE
from controllers.table_controller import TableController

from core.text_util import ignore_text_filter, text_or_none




# Filtros
FILTER_ABC = 'abcdefghijklmnñopqrstuvwxyz'
FILTER_NUMBERS = '1234567890'
FILTER_FOR_TAG = FILTER_ABC + FILTER_NUMBERS + '-'




class LanguageTableController( TableController ):
    '''
    Controller para modelo LangaugeTable
    El tag siempre recibira un filtro.
    '''
    def __init__( self, log_level="warning" ):
        super().__init__( 
            table=LanguageTable(), verbose=True, log_level=log_level, save_log=True, only_the_value=True
        )
        self.language_config_table = LanguageConfigTable()
        
        self.COLUMN_WHERE_LANGUAGES_BEGIN = self.table.COLUMN_WHERE_LANGUAGES_BEGIN
    
    
    # Filtros de texto
    def tag_filter( self, text:str ):
        text = ignore_text_filter( text.lower(), FILTER_FOR_TAG )
        return text_or_none(text)
    
    def text_filter(self, text:str=None):
        return text_or_none(text)
    
    
    def language_filter( self, text:str=None ):
        '''
        Si no existe el lenguaje se pone el default, se establece el lenguaje default.
        '''
        return self.language_config_table.language_filter(language=text)
    
    
    def get_languages(self):
        languages = self.table.get_languages()
        if languages == {}:
            log_type = "error"
            message = "No detect anything language"
        else:
            log_type = "info"
            message = "Good languages"
            
        return self.return_value( value=languages, message=message, log_type=log_type )
        
    
    # Funciones chidas
    def get_text(self, tag: str, language: str=None ) -> str:
        # tag
        filtered_tag = self.tag_filter( tag )
        filtered_language = self.language_filter(language)

        value, sql_statement, commit = self.table.select_tag( tag=filtered_tag, language=filtered_language )
        string_value = filtered_tag
        if isinstance(value, tuple):
            # Si no existe el tag en el lenguaje que no sea en
            if value[0] == None and language != self.language_config_table.default_language:
                log_type = "warning"
                message = f"The tag value no exists in `{filtered_language}`"
                value, sql_statement, commit = self.table.select_tag(
                    tag=tag, language=self.language_config_table.default_language
                )
            # Existe el tag
            else:
                log_type = "info"
                message = f"Nice, the tag `{filtered_tag}` exists"
            
            string_value = value[0]
        else:
            # Si no existe el tag, devolver el texto tag que no exite.
            log_type = "warning"
            message = f"The tag `{filtered_tag}` does not exist"
        message = self.structure_sql_message( message, sql_statement, commit )
        
        # Asegurarse que el valor final sea un string
        string_value = str(string_value) if string_value is not None else filtered_tag
        
        return self.return_value( value=string_value, message=message, log_type=log_type )
        
        
        
    def insert_tag(self, tag: str, language: str=None, text: str=str) -> bool:
        filtered_tag = self.tag_filter( tag )
        filtered_language = self.language_filter(language)
        text = self.text_filter(text)
        
        value = False; message = f"Bad parameters; tag, language, or text"; log_type="error"
        if isinstance(filtered_tag, str) and isinstance(filtered_language, str):
            value, sql_statement, commit = self.table.insert_tag( 
                tag=filtered_tag, language=filtered_language, text=text
            )
            if value:
                log_type = "info"
                message = "Good insert"
            else:
                log_type = "error"
                message = "Bad insert"
            message = self.structure_sql_message( message, sql_statement, commit )
        
        return self.return_value( value=value, message=message, log_type=log_type)
    
    
    def update_tag(self, tag:str, language: str="en", text: str="") -> bool:
        filtered_tag = self.tag_filter(tag)
        filtered_language = self.language_filter(language)
        text = self.text_filter(text)
        
        value = False; message = f"Bad parameters; tag, language, or text"; log_type="error"
        if isinstance(filtered_tag, str) and isinstance(filtered_language, str):
            value, sql_statement, commit = self.table.update_tag( 
                tag=filtered_tag, language=filtered_language, text=text
            )
            if value:
                log_type = "info"
                message = "Good update"
            else:
                log_type = "error"
                message = "Bad update"
            message = self.structure_sql_message( message, sql_statement, commit )
        
        return self.return_value( value=value, message=message, log_type=log_type )
    
    
    def update_row(self, languageId: int=1, tag:str="", language: str=None, text: str="") -> bool:
        tag = self.tag_filter(tag)
        language = self.language_filter(language)
        
        value = False; message = f"Bad parameters; tag, language, or text"; log_type="error"
        if isinstance(tag, str) and isinstance(language, str):
            value, sql_statement, commit = self.table.update_row(
                languageId=languageId, tag=tag, language=language, text=text
            )
            if value:
                log_type = "info"
                message = "Good update"
            else:
                log_type = "error"
                message = "Bad update"
            message = self.structure_sql_message( message, sql_statement, commit )
        
        return self.return_value( value=value, message=message, log_type=log_type )
    
    
    def save_tag(self, languageId:int=None, tag:str=None, language: str=None, text: str="") -> bool:
        '''
        No es necesario establecer el ID, pero sire si se quiere cambiar el texto del tag.
        '''
        # Guardar por medio del id
        if isinstance(languageId, int):
            return self.update_row( languageId=languageId, tag=tag, language=language, text=text )

        # Guardar por meddio del tag
        else:
            # Determinar que exista el tag
            value, sql_statement, commit = self.table.select_tag(
                tag=self.tag_filter(tag), language=self.language_filter(language)
            )
            exists_text = ( isinstance(value, tuple) )
            
            # Devolver
            if exists_text:
                return self.update_tag( tag=tag, language=language, text=text )
            else:
                return self.insert_tag( tag=tag, language=language, text=text )