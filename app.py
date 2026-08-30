# Importar Flask, render_template y request
from flask import Flask, render_template, redirect, url_for, flash
from forms import ProductoForm, ClienteForm, ContactoForm, ProveedorForm, FacturaForm

# Se crea la instancia de la app Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'boutique_alison-2026-csrf-segura'

# Datos temporales
prendas = [
        {"id": 1, "nombre": "Vestido Elegante de Noche", "precio": 45.00, "categoria": "Ropa", "stock": 5, "imagen": "vestido.jpeg"},
        {"id": 2, "nombre": "Blusa Casual Primavera", "precio": 22.50, "categoria": "Ropa", "stock": 12, "imagen": "blusa.png"},
        {"id": 3, "nombre": "Jeans Tiro Alto Classic", "precio": 35.00, "categoria": "Ropa", "stock": 0, "imagen": "jeans.png"},
        {"id": 4, "nombre": "Chaqueta de Cuero Sintético", "precio": 60.00, "categoria": "Abrigos", "stock": 3, "imagen": "chaqueta.png"}
    ]
proveedores = []
facturas = []
mensajes_contacto = []

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
    return render_template('catalogo.html', titulo="Catálogo", prendas=prendas)

@app.route('/catalogo/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        prendas.append({  # ERROR CORREGIDO: era predas
            "id": len(prendas)+1,
            "nombre": form.nombre.data,
            "precio": form.precio.data,
            "categoria": form.categoria.data,
            "stock": form.stock.data,
            "imagen": form.imagen.data
        })
        flash('Prenda registrada correctamente', 'success')
        return redirect(url_for('catalogo'))
    return render_template('producto_form.html', titulo="Nueva Prenda", form=form)

# Ruta para mostrar el formulario 
@app.route('/contacto', methods=['GET', 'POST']) # ERROR CORREGIDO: era [GET, 'POST'] sin comillas
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        mensajes_contacto.append({ # ERROR CORREGIDO: era [ ] debe ser { }
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "mensaje": form.mensaje.data
        })
        flash('Mensaje enviado correctamente', 'success')
        return render_template('respuesta.html', titulo="Confirmación", nombre=form.nombre.data, correo=form.correo.data, mensaje=form.mensaje.data)
    return render_template('contacto.html', titulo="Contacto", form=form)

@app.route('/proveedores') # ERROR CORREGIDO: era /proveedor singular, ahora plural
def proveedores_list():
    return render_template('proveedores.html', titulo="Proveedores", proveedores=proveedores)

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor(): # ERROR CORREGIDO: era nuevo_proveedo
    form = ProveedorForm()
    if form.validate_on_submit():
        proveedores.append({ # ERROR CORREGIDO: era [ ] debe ser { }
            "id": len(proveedores)+1,
            "nombre_empresa": form.nombre_empresa.data,
            "ruc": form.ruc.data,
            "email": form.email.data,
            "telefono": form.telefono.data
        })
        flash('Proveedor registrado', 'success')
        return redirect(url_for('proveedores_list'))
    return render_template('proveedor_form.html', titulo="Nuevo Proveedor", form=form)

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', titulo="Facturación", facturas=facturas, prendas=prendas)

@app.route('/facturacion/nuevo', methods=['GET', 'POST']) # ERROR CORREGIDO: faltaba methods
def nueva_factura():
    form = FacturaForm()
    form.producto_id.choices = [(p['id'], p['nombre']) for p in prendas]
    if form.validate_on_submit():
        facturas.append({
            "id": len(facturas)+1,
            "cliente": form.cliente.data,
            "producto_id": form.producto_id.data,
            "cantidad": form.cantidad.data,
            "descuento": form.descuento.data
        })
        flash('Factura generada', 'success')
        return redirect(url_for('facturacion'))
    return render_template('factura_form.html', titulo="Nueva Factura", form=form) # ERROR CORREGIDO: era facturacion.html

@app.route('/procesar', methods=['POST'])
def procesar():
    return redirect(url_for('contacto'))

# Ejecución del servidor
if __name__ == '__main__': 
    app.run(debug=True)
