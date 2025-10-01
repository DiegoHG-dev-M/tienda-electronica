import os
from flask import Flask, request, jsonify, render_template,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Crear instancia
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    precio = db.Column(db.Float)
    stock = db.Column(db.Integer)
    categoria_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)


    def to_dict(self):
        return{
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'categoria_id': self.categoria_id,
        }
    
#endpoint del index
@app.route('/', methods=['GET'])
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

#Endpoint  para crear producto
@app.route('/productos/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        categoria_id = int(request.form['categoria_id'])

        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id
        )

        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('index'))  # Redirige a la lista de productos

    return render_template('crear_producto.html')

#EDitar
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = request.form['precio']
        producto.stock = request.form['stock']
        producto.categoria_id = request.form['categoria_id']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', producto=producto)

#Ruta /tienda
@app.route('/tienda')
def getTienda():
    return 'Bienvenidos a tienda'

if __name__ == '__Main__':
    app.run(debug=True)