from core.standard_logging import StandardLogging


class LoggingController():
    def __init__(
        self, name: str="text", verbose: bool=True, log_level: str="debug", save_log: bool=True,
        only_the_value: bool=True
    ):
        # Log
        self.name = name
        self.verbose = verbose
        self.log_level = log_level
        self.save_log = save_log
        self.__standard_log = StandardLogging(
            name=self.name, verbose=self.verbose, level=self.log_level, save=self.save_log
        )
        self.__only_the_value = only_the_value
    
    def return_value( 
        self, value: bool | str | list, message: str, log_type="debug"
    ) -> (object, str, str):
        '''
        Devolver valor o texto dependiendo de atributos: verbose y return_message
        
        value, log_type, message
        '''
        # Establecer config de log. Si es que cambian `save_log, log_level, verbose`
        if (
            (self.verbose != self.__standard_log.verbose) or (self.save_log != self.__standard_log.save) or
            (self.log_level != self.__standard_log.level)
        ):
            self.__standard_log.verbose = self.verbose
            self.__standard_log.save = self.save_log
            self.__standard_log.level = self.log_level
            self.__standard_log.set_level()
            self.__standard_log.set_logger()
        
        # Mensaje log
        final_log, final_message = self.__standard_log.log( message=f"{message}\n", log_type=log_type )
        
        # Devolver mensaje y valor, o solo el valor
        if self.__only_the_value:
            return value
        else:
            return value, final_log, final_message