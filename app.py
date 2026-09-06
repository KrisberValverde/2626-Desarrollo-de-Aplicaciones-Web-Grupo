# Importar SQLite y las funciones necesarias de Flask
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash
from forms import ProductoForm, ClienteForm, ContactoForm, ProveedorForm, FacturaForm

# Se crea la instancia de la app Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'boutique_alison-2026-csrf-segura'


# Configuración de SQLite para la persistencia local
def get_db_connection():
    # Conexión con la base de datos SQLite
    conn = sqlite3.connect('data/boutique_alison.db')

    # Permite acceder a las columnas por nombre
    conn.row_factory = sqlite3.Row

    return conn


# Inicialización de la base de datos
def init_db():
    # Obtener conexión con SQLite
    conn = get_db_connection()

    # Crear la tabla productos si todavía no existe
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            stock INTEGER NOT NULL,
            imagen TEXT NOT NULL
        )
    ''')

    # Guardar los cambios realizados en la base de datos
    conn.commit()

    # Cerrar la conexión
    conn.close()


# Ejecutar la inicialización de la base de datos
init_db()


# Datos temporales para los demás módulos
# Estos módulos se mantendrán y posteriormente podrán integrarse con SQLite
proveedores = []
facturas = []
mensajes_contacto = []


# Ruta principal
@app.route('/')
def index():
    # Nombre de la tienda
    tienda_nombre = "boutique alison"

    # Lista de categorías que se enviará a la plantilla
    categorias = [
        "Vestidos",
        "Tops",
        "Pantalones",
        "Camisas",
        "Enterizos",
        "Faldas"
    ]

    # Enviar información a la plantilla index.html
    return render_template(
        'index.html',
        titulo="Inicio",
        tienda=tienda_nombre,
        categorias=categorias
    )


# Ruta del catálogo
# Los productos ahora se consultan desde la base de datos SQLite
@app.route('/catalogo')
def catalogo():

    # Abrir conexión con SQLite
    conn = get_db_connection()

    # Consultar todos los productos almacenados
    prendas = conn.execute(
        'SELECT * FROM productos'
    ).fetchall()

    # Cerrar la conexión
    conn.close()

    # Enviar los productos consultados a la plantilla
    return render_template(
        'catalogo.html',
        titulo="Catálogo",
        prendas=prendas
    )


# Ruta para registrar un nuevo producto
# Se utilizan los métodos GET y POST
@app.route('/catalogo/nuevo', methods=['GET', 'POST'])
def nuevo_producto():

    # Crear una instancia del formulario de productos
    form = ProductoForm()

    # Validar el formulario antes de guardar los datos
    if form.validate_on_submit():

        # Abrir conexión con SQLite
        conn = get_db_connection()

        # Insertar el producto validado en la base de datos
        # Se utilizan parámetros ? para evitar concatenar directamente los datos
        conn.execute('''
            INSERT INTO productos (
                nombre,
                precio,
                categoria,
                stock,
                imagen
            )
            VALUES (?, ?, ?, ?, ?)
        ''', (
            form.nombre.data,
            form.precio.data,
            form.categoria.data,
            form.stock.data,
            form.imagen.data
        ))

        # Confirmar y guardar el registro en SQLite
        conn.commit()

        # Cerrar la conexión con la base de datos
        conn.close()

        # Mostrar mensaje de confirmación
        flash(
            'Prenda registrada correctamente en la base de datos',
            'success'
        )

        # Regresar al catálogo
        return redirect(url_for('catalogo'))

    # Mostrar el formulario si todavía no ha sido enviado o no es válido
    return render_template(
        'producto_form.html',
        titulo="Nueva Prenda",
        form=form
    )


# Ruta para mostrar y procesar el formulario de contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():

    # Crear una instancia del formulario de contacto
    form = ContactoForm()

    # Validar el formulario
    if form.validate_on_submit():

        # Guardar temporalmente el mensaje de contacto
        mensajes_contacto.append({
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "mensaje": form.mensaje.data
        })

        # Mostrar mensaje de confirmación
        flash(
            'Mensaje enviado correctamente',
            'success'
        )

        # Mostrar la página de respuesta
        return render_template(
            'respuesta.html',
            titulo="Confirmación",
            nombre=form.nombre.data,
            correo=form.correo.data,
            mensaje=form.mensaje.data
        )

    # Mostrar el formulario de contacto
    return render_template(
        'contacto.html',
        titulo="Contacto",
        form=form
    )


# Ruta para mostrar los proveedores
@app.route('/proveedores')
def proveedores_list():

    # Enviar la lista de proveedores a la plantilla
    return render_template(
        'proveedores.html',
        titulo="Proveedores",
        proveedores=proveedores
    )


# Ruta para registrar un nuevo proveedor
@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():

    # Crear una instancia del formulario de proveedores
    form = ProveedorForm()

    # Validar el formulario
    if form.validate_on_submit():

        # Guardar temporalmente los datos del proveedor
        proveedores.append({
            "id": len(proveedores) + 1,
            "nombre_empresa": form.nombre_empresa.data,
            "ruc": form.ruc.data,
            "email": form.email.data,
            "telefono": form.telefono.data
        })

        # Mostrar mensaje de confirmación
        flash(
            'Proveedor registrado',
            'success'
        )

        # Regresar a la lista de proveedores
        return redirect(
            url_for('proveedores_list')
        )

    # Mostrar el formulario de proveedores
    return render_template(
        'proveedor_form.html',
        titulo="Nuevo Proveedor",
        form=form
    )


# Ruta para mostrar el módulo de facturación
@app.route('/facturacion')
def facturacion():

    # Abrir conexión con SQLite
    conn = get_db_connection()

    # Consultar los productos disponibles para la facturación
    prendas = conn.execute(
        'SELECT * FROM productos'
    ).fetchall()

    # Cerrar conexión
    conn.close()

    # Enviar los datos a la plantilla
    return render_template(
        'facturacion.html',
        titulo="Facturación",
        facturas=facturas,
        prendas=prendas
    )


# Ruta para crear una nueva factura
@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_factura():

    # Consultar los productos almacenados en SQLite
    conn = get_db_connection()

    prendas = conn.execute(
        'SELECT * FROM productos'
    ).fetchall()

    # Cerrar conexión
    conn.close()

    # Crear una instancia del formulario de facturación
    form = FacturaForm()

    # Cargar los productos disponibles en el campo de selección
    form.producto_id.choices = [
        (p['id'], p['nombre'])
        for p in prendas
    ]

    # Validar el formulario
    if form.validate_on_submit():

        # Guardar temporalmente la información de la factura
        facturas.append({
            "id": len(facturas) + 1,
            "cliente": form.cliente.data,
            "producto_id": form.producto_id.data,
            "cantidad": form.cantidad.data,
            "descuento": form.descuento.data
        })

        # Mostrar mensaje de confirmación
        flash(
            'Factura generada',
            'success'
        )

        # Regresar al módulo de facturación
        return redirect(
            url_for('facturacion')
        )

    # Mostrar el formulario de facturación
    return render_template(
        'factura_form.html',
        titulo="Nueva Factura",
        form=form
    )


# Ruta para procesar información
@app.route('/procesar', methods=['POST'])
def procesar():

    # Redirigir al formulario de contacto
    return redirect(url_for('contacto'))


# Ejecución del servidor
if __name__ == '__main__':
    app.run(debug=True)