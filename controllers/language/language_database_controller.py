from models import LanguageDatabase
from controllers.database_controller import DatabaseController

class LanguageDatabaseController( DatabaseController ):
    def __init__(self, log_level="warning"):
        super().__init__( 
            database=LanguageDatabase(), verbose=True, save_log=True, log_level=log_level, only_the_value=True
        )