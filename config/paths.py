from utils import ResourceLoader

resource_loader = ResourceLoader()

# Subcarpeta
ICON_DIR = resource_loader.resources_dir.joinpath( 'icons' )
NOTA_DEFAULT_DIR = resource_loader.resources_dir.joinpath( 'nota' )

# Archivos
ICON_FILE = ICON_DIR.joinpath( 'cm-nota.png' )
NOTA_CONFIG_FILE = resource_loader.get_config( 'nota.config' )
