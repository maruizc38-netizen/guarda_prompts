from flask import Flask, render_template, request, redirect
import mysql.connector

# Creamos la aplicación Flask
# Indicamos que index.html está en esta carpeta y el css en la carpeta 'css'
app = Flask(__name__, template_folder='.', static_folder='css', static_url_path='/css')

# Función simple para conectarse a la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      
        database="guarda_prompts"
    )

# Ruta principal: muestra la página con la lista de prompts
@app.route('/')
def inicio():
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True) # dictionary=True para poder usar p.nombre, p.texto, etc.
        cursor.execute("SELECT * FROM prompts ORDER BY id DESC")
        mis_prompts = cursor.fetchall()
        cursor.close()
        conexion.close()
    except Exception as error:
        print("Aviso: No se pudo conectar a MySQL o la tabla no existe aún:", error)
        mis_prompts = []

    return render_template('index.html', prompts=mis_prompts)

# Ruta para guardar un nuevo prompt
@app.route('/guardar', methods=['POST'])
def guardar():
    # Obtenemos los datos que el usuario escribió en el formulario
    nombre = request.form['nombre']
    texto = request.form['prompt']

    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        sql = "INSERT INTO prompts (nombre, texto) VALUES (%s, %s)"
        valores = (nombre, texto)
        cursor.execute(sql, valores)
        conexion.commit() # Guardamos los cambios en la base de datos
        cursor.close()
        conexion.close()
    except Exception as error:
        print("Error al guardar el prompt:", error)

    # Redirigimos a la página principal para ver el nuevo prompt
    return redirect('/')

# Ruta para eliminar un prompt por su ID
@app.route('/eliminar/<int:id>')
def eliminar(id):
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        sql = "DELETE FROM prompts WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.commit() # Guardamos los cambios en la base de datos
        cursor.close()
        conexion.close()
    except Exception as error:
        print("Error al eliminar el prompt:", error)

    return redirect('/')

# Arrancamos la aplicación
if __name__ == '__main__':
    print("Servidor iniciado en http://127.0.0.1:5000")
    app.run(debug=True)
