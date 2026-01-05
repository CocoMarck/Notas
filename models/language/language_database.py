from models.standard_database import StandardDatabase
from models.model_names.language_names import LANGUAGES, LANGUAGE_TABLE_NAMES, LANGUAGE_CONFIG_TABLE_NAMES, NAME_SYSTEM_LANGUAGE

class LanguageDatabase( StandardDatabase ):
    def __init__(self):
        super().__init__( name_database="language", name_dir_data="data"  )
        
        # Campos languages
        language_table_fields = [
            [ LANGUAGE_TABLE_NAMES['id'], 'INTEGER', 'PRIMARY KEY AUTOINCREMENT' ],
            [ LANGUAGE_TABLE_NAMES['tag'], 'TEXT', 'UNIQUE' ],
        ]
        for key in LANGUAGES.keys():
            language_table_fields.append( [ LANGUAGES[key], 'TEXT' ] )
        
        # Diccionario de tablas a crear
        self.dictionary_of_tables = {
            LANGUAGE_TABLE_NAMES['table'] : language_table_fields,

            LANGUAGE_CONFIG_TABLE_NAMES['table']: [
                [ LANGUAGE_CONFIG_TABLE_NAMES['id'], 'INTEGER', 'PRIMARY KEY AUTOINCREMENT' ],
                [ LANGUAGE_CONFIG_TABLE_NAMES['language'], 'TEXT' ]
            ]
        }
        
        # Instrucciones adicionales
        self.instructions_after_creating_tables = [
            (
            f"INSERT OR IGNORE INTO {LANGUAGE_CONFIG_TABLE_NAMES['table']} "
            f"({LANGUAGE_CONFIG_TABLE_NAMES['id']}, {LANGUAGE_CONFIG_TABLE_NAMES['language']}) "
            f"VALUES(1, '{NAME_SYSTEM_LANGUAGE}');"
            )
        ]