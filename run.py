# Importa la variable app de la carpeta app
from app import app

app.run(app.config['HOST'], app.config['PORT'])