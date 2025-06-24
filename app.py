from flask import Flask
from routes.login_routes import login_blueprint
from routes.usuario_routes import usuario_blueprint
# importa los demás si ya los tienes

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Registra todos los blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(usuario_blueprint)
# app.register_blueprint(estudiante_blueprint), etc.
from routes.asignatura_routes import asignatura_blueprint

app.register_blueprint(asignatura_blueprint)
from routes.estudiante_routes import estudiante_blueprint
app.register_blueprint(estudiante_blueprint)


from routes.calificacion_routes import calificacion_blueprint
app.register_blueprint(calificacion_blueprint)
from routes.asistencia_routes import asistencia_blueprint
app.register_blueprint(asistencia_blueprint)

#set a specific port 


if __name__ == '__main__':
    app.run(debug=True, port = 5001)  # Puedes cambiar el puerto si es necesario

