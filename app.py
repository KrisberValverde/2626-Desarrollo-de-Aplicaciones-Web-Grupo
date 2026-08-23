# Importar Flask, render_template y request
from flask import Flask, render_template, request

# Se crea la instancia de la app Flask
app = Flask(__name__)

# Ruta principal (Se envían variables simples y listas)
@app.route('/')
def index():
    tienda_nombre = "boutique alison"
    # Cambiamos los elementos de la lista enviada al template
    categorias = ["Vestidos", "Tops", "Pantalones", "Camisas", "Enterizos", "Faldas"]
    return render_template('index.html', titulo="Inicio", tienda=tienda_nombre, categorias=categorias)

# Ruta del catálogo (Se envía la lista de diccionarios con stock e imagen)
@app.route('/catalogo')
def catalogo():
    prendas = [
        {"id": 1, "nombre": "Vestido Elegante de Noche", "precio": 45.00, "categoria": "Ropa", "stock": 5, "imagen": "vestido.jpeg"},
        {"id": 2, "nombre": "Blusa Casual Primavera", "precio": 22.50, "categoria": "Ropa", "stock": 12, "imagen": "blusa.png"},
        {"id": 3, "nombre": "Jeans Tiro Alto Classic", "precio": 35.00, "categoria": "Ropa", "stock": 0, "imagen": "jeans.png"},
        {"id": 4, "nombre": "Chaqueta de Cuero Sintético", "precio": 60.00, "categoria": "Abrigos", "stock": 3, "imagen": "chaqueta.png"}
    ]
    return render_template('catalogo.html', titulo="Catálogo", prendas=prendas)

# Ruta para mostrar el formulario 
@app.route('/contacto')
def contacto():
    return render_template('contacto.html', titulo="Contacto")

# Ruta para recibir los datos por POST 
@app.route('/procesar', methods=['POST'])
def procesar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    mensaje = request.form['mensaje']
    return render_template('respuesta.html', titulo="Confirmación", nombre=nombre, correo=correo, mensaje=mensaje)

# Ejecución del servidor
if __name__ == '__main__': 
    app.run(debug=True)