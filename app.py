from flask import Flask, request, jsonify, render_template,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Crear instancia
app = Flask(__name__)


#Ruta /tienda
@app.route('/tienda')
def getTienda():
    return 'Bienvenidos a tienda'

if __name__ == '__Main__':
    app.run(debug=True)