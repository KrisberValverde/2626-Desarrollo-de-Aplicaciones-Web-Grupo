import sqlite3
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import ProductoForm, ClienteForm, ContactoForm, ProveedorForm, FacturaForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boutique_alison-2026-csrf-segura'


def get_db_connection():
    conn = sqlite3.connect('data/boutique_alison.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
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
    conn.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_empresa TEXT NOT NULL,
            ruc TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()

facturas = []
mensajes_contacto = []


@app.route('/')
def index():
    tienda_nombre = "boutique alison"
    categorias = [
        "Vestidos",
        "Tops",
        "Pantalones",
        "Camisas",
        "Enterizos",
        "Faldas"
    ]
    return render_template(
        'index.html',
        titulo="Inicio",
        tienda=tienda_nombre,
        categorias=categorias
    )


@app.route('/catalogo')
def catalogo():
    conn = get_db_connection()
    prendas = conn.execute(
        'SELECT * FROM productos'
    ).fetchall()
    conn.close()
    return render_template(
        'catalogo.html',
        titulo="Catálogo",
        prendas=prendas
    )


@app.route('/catalogo/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_db_connection()
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
        conn.commit()
        conn.close()
        flash(
            'Prenda registrada correctamente en la base de datos',
            'success'
        )
        return redirect(url_for('catalogo'))
    return render_template(
        'producto_form.html',
        titulo="Nueva Prenda",
        form=form
    )


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        mensajes_contacto.append({
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "mensaje": form.mensaje.data
        })
        flash(
            'Mensaje enviado correctamente',
            'success'
        )
        return render_template(
            'respuesta.html',
            titulo="Confirmación",
            nombre=form.nombre.data,
            correo=form.correo.data,
            mensaje=form.mensaje.data
        )
    return render_template(
        'contacto.html',
        titulo="Contacto",
        form=form
    )


@app.route('/proveedores')
def proveedores_list():
    conn = get_db_connection()
    proveedores = conn.execute(
        'SELECT * FROM proveedores'
    ).fetchall()
    conn.close()
    return render_template(
        'proveedores.html',
        titulo="Proveedores",
        proveedores=proveedores
    )


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO proveedores (
                nombre_empresa,
                ruc,
                email,
                telefono
            )
            VALUES (?, ?, ?, ?)
        ''', (
            form.nombre_empresa.data,
            form.ruc.data,
            form.email.data,
            form.telefono.data
        ))
        conn.commit()
        conn.close()
        flash(
            'Proveedor registrado correctamente en la base de datos',
            'success'
        )
        return redirect(
            url_for('proveedores_list')
        )
    elif request.method == 'POST':
        print("Errores de validación en ProveedorForm:", form.errors)

    return render_template(
        'proveedor_form.html',
        titulo="Nuevo Proveedor",
        form=form
    )


@app.route('/facturacion')
def facturacion():
    conn = get_db_connection()
    prendas = conn.execute(
        'SELECT * FROM productos'
    ).fetchall()
    conn.close()
    return render_template(
        'facturacion.html',
        titulo="Facturación",
        facturas=facturas,
        prendas=prendas
    )


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_factura():
    conn = get_db_connection()
    prendas = conn.execute(
        'SELECT * FROM productos'
    ).fetchall()
    conn.close()
    form = FacturaForm()
    form.producto_id.choices = [
        (p['id'], p['nombre'])
        for p in prendas
    ]
    if form.validate_on_submit():
        facturas.append({
            "id": len(facturas) + 1,
            "cliente": form.cliente.data,
            "producto_id": form.producto_id.data,
            "cantidad": form.cantidad.data,
            "descuento": form.descuento.data
        })
        flash(
            'Factura generada',
            'success'
        )
        return redirect(
            url_for('facturacion')
        )
    return render_template(
        'factura_form.html',
        titulo="Nueva Factura",
        form=form
    )


@app.route('/procesar', methods=['POST'])
def procesar():
    return redirect(url_for('contacto'))


if __name__ == '__main__':
    app.run(debug=True)