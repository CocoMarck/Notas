class NotaController:
    def __init__(self, nota_model, nota_repository):
        self.nota_model = nota_model
        self.nota_model.text = ""
        self.nota_repository = nota_repository
        self.load()

    def get_config(self):
        '''
        Establecer configuración.
        '''
        self.nota_repository.get_config()
        self.nota_model.last_nota = self.nota_repository.get_last_nota()
        self.nota_model.path = self.nota_repository.get_path()

    def list_nota(self):
        '''
        Listar cantidad de notas disponibles
        '''
        return self.nota_repository.list_nota( self.nota_model.path )


    def read(self):
        '''
        Leer texto de ultima nota.
        '''
        if self.nota_model.last_nota == None:
            return False

        text = self.nota_repository.get_nota_text(
            self.nota_model.last_nota, self.nota_model.path
        )
        if text:
            self.nota_model.text = text
            return True
        else:
            return False


    def load(self):
        '''
        Obtener configuracion, y texto de ultima nota (solo si existe el texto).
        '''
        self.get_config()
        self.read()


    def set_config(self):
        '''
        Establecer configuracion
        '''
        return self.nota_repository.set_config(self.nota_model.last_nota, self.nota_model.path)



    def save(self):
        if self.nota_model.last_nota == None:
            return False

        signal = self.nota_repository.save(
            self.nota_model.last_nota, self.nota_model.path, self.nota_model.text
        )
        self.set_config()
        self.read()
        return signal


    def remove(self, name):
        success = self.nota_repository.remove( name, self.nota_model.path )
        if success:
            self.nota_model.text = ""
            if (
                self.nota_repository.get_name_only( self.nota_model.last_nota ) ==
                self.nota_repository.get_name_only( name )
            ):
                self.nota_model.last_nota = ""
                self.set_config()
            self.load()
        return success
