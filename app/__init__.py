from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Carga la configuración con la ruta definida
# en la variable APP_CONFIG_FILE. Esta variable
# se ha definido en el start.sh
app.config.from_envvar('APP_CONFIG_FILE')

from app import routes

# El import al final evita referencias circulares
# Routes utiliza el módula app definido aquí