# Estilo cabelCase
LANGUAGE_NAME = "language"
LANGUAGES = {
    "en": "en",
    "es": "es",
    "pt": "pt",
    "ru": "ru"
}
DEFAULT_LANGUAGE = LANGUAGES['en']
NAME_DEFAULT_LANGUAGE = "default"
NAME_SYSTEM_LANGUAGE = "system"



# Campos generalistas
SOFT_DELETE_COLUMN = { "soft_delete": "soft_delete" }
TABLE_CONTROL_FIELDS = {
    "creation_date": "creation_date",
    "modification_date": "modification_date"
}
TABLE_CONTROL_FIELDS.update( SOFT_DELETE_COLUMN )




# Tablas
LANGUAGE_TABLE_NAMES = {
    "table": LANGUAGE_NAME,
    "id": f"{LANGUAGE_NAME}Id",
    "tag": "tag",
}
LANGUAGE_TABLE_NAMES.update( LANGUAGES )
LANGUAGE_TABLE_NAMES.update( TABLE_CONTROL_FIELDS )

CONFIG_NAME = "config"
LANGUAGE_CONFIG_TABLE_NAMES = {
    "table": CONFIG_NAME,
    "id": f"{CONFIG_NAME}Id",
    "language": LANGUAGE_TABLE_NAMES["table"]
}