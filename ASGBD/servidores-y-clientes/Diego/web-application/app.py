# Importamos las librerías necesarias
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
import os

# Creamos la aplicación Flask
app = Flask(__name__)

# Generamos una clave secreta aleatoria para manejar sesiones de usuario
app.secret_key = os.urandom(24)

# Datos de conexión al servidor MongoDB
MONGODB_HOST = '192.168.122.187'   # Dirección IP del servidor MongoDB
MONGODB_PORT = '27017'             # Puerto de conexión
MONGODB_DATABASE = 'db'            # Nombre de la base de datos a usar


# Ruta principal de la aplicación (página de inicio)
@app.route('/')
def index():
    # Recuperamos los datos de usuario y contraseña guardados en la sesión
    usuario = session.get('usuario')
    password = session.get('password')
    
    # Si el usuario no está autenticado, mostramos el formulario de login
    if not usuario or not password:
        return render_template('index.html')
    
    # Construimos la URI de conexión a MongoDB con autenticación
    uri = f"mongodb://{usuario}:{password}@{MONGODB_HOST}:{MONGODB_PORT}/?authSource={MONGODB_DATABASE}"
    
    # Creamos un cliente de MongoDB con un tiempo máximo de espera de 2 segundos
    client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    
    # Seleccionamos la base de datos
    db = client[MONGODB_DATABASE]
    
    # Obtenemos la lista de colecciones disponibles en la base de datos
    colecciones = db.list_collection_names()

    # Renderizamos la plantilla 'index.html' pasando el usuario y las colecciones
    return render_template(
        'index.html',
        usuario=usuario,
        colecciones=colecciones
    )


# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el formulario fue enviado por método POST
    if request.method == 'POST':
        # Obtenemos los datos enviados desde el formulario
        usuario = request.form['username']
        password = request.form['password']

        # Creamos la URI de conexión con los datos del usuario
        uri = f"mongodb://{usuario}:{password}@{MONGODB_HOST}:{MONGODB_PORT}/?authSource={MONGODB_DATABASE}"
        
        try:
            # Intentamos conectar con MongoDB
            client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            db = client[MONGODB_DATABASE]
            # Si la conexión es exitosa, obtenemos las colecciones
            db.list_collection_names()
            
            # Guardamos las credenciales del usuario en la sesión
            session['usuario'] = usuario
            session['password'] = password

            # Redirigimos a la página principal
            return redirect(url_for('index'))
        
        except Exception as e:
            # Si ocurre un error, mostramos un mensaje en la misma página
            return render_template('index.html', error=f"Error de conexión: {e}")
    
    # Si la petición es GET (usuario accede sin enviar formulario)
    return render_template('index.html')


# Ruta para ver los documentos de una colección específica
@app.route('/colecciones/<nombre>')
def ver_coleccion(nombre):
    # Recuperamos el usuario y la contraseña de la sesión
    usuario = session.get('usuario')
    password = session.get('password')

    # Si el usuario no está autenticado, lo redirigimos al login
    if not usuario or not password:
        return redirect(url_for('login'))
    
    # Construimos la URI de conexión con las credenciales guardadas
    uri = f"mongodb://{usuario}:{password}@{MONGODB_HOST}:{MONGODB_PORT}/?authSource={MONGODB_DATABASE}"
    client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    db = client[MONGODB_DATABASE]

    # Listamos todas las colecciones
    colecciones = db.list_collection_names()

    # Obtenemos todos los documentos de la colección seleccionada
    documentos = list(db[nombre].find())

    # Renderizamos la plantilla mostrando usuario, colecciones y los documentos de la colección elegida
    return render_template(
        'index.html',
        usuario=usuario,
        colecciones=colecciones,
        documentos=documentos,
        nombre=nombre
    )


# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminamos todos los datos guardados en la sesión
    session.clear()
    # Redirigimos al inicio
    return redirect(url_for('index'))
