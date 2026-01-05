from controllers import LanguageTableController


controller = LanguageTableController()

def get_text( tag:str, language:str=None ):
    return controller.get_text( tag=tag, language=language )