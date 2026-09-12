from flask import Flask, render_template, redirect, url_for, flash, request
from forms import ProductoForm, ClienteForm, ContactoForm, ProveedorForm, FacturaForm
from conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boutique_alison-2026-csrf-segura'

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


# 1. Vista Pública para Clientes (SELECT)
@app.route('/productos-servicios')
def productos_servicios():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    prendas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'productos_servicios.html',
        titulo="Catálogo Exclusivo",
        prendas=prendas
    )


# 2. Panel de Administración (SELECT)
@app.route('/catalogo')
def catalogo():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    prendas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'catalogo.html',
        titulo="Panel de Administración",
        prendas=prendas
    )


# AGREGAR (INSERT)
@app.route('/catalogo/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO productos (
                nombre,
                precio,
                categoria,
                stock,
                imagen
            )
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            form.nombre.data,
            form.precio.data,
            form.categoria.data,
            form.stock.data,
            form.imagen.data
        ))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Prenda registrada correctamente en la base de datos MySQL', 'success')
        return redirect(url_for('catalogo'))
    elif request.method == 'POST':
        print("Errores de validación en ProductoForm:", form.errors)

    return render_template(
        'producto_form.html',
        titulo="Nueva Prenda",
        form=form
    )


# MODIFICAR (UPDATE) - Uso de id_producto
@app.route('/catalogo/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        form = ProductoForm()
        if form.validate_on_submit():
            cursor.execute('''
                UPDATE productos 
                SET nombre = %s, precio = %s, categoria = %s, stock = %s, imagen = %s
                WHERE id_producto = %s
            ''', (
                form.nombre.data,
                form.precio.data,
                form.categoria.data,
                form.stock.data,
                form.imagen.data,
                id_producto
            ))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Prenda modificada correctamente en la base de datos', 'success')
            return redirect(url_for('catalogo'))
    
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    form = ProductoForm(data=producto)
    return render_template(
        'producto_form.html',
        titulo="Editar Prenda",
        form=form
    )


# ELIMINAR (DELETE) - Uso de id_producto
@app.route('/catalogo/eliminar/<int:id_producto>', methods=['POST', 'GET'])
def eliminar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Prenda eliminada correctamente del catálogo', 'success')
    return redirect(url_for('catalogo'))


@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        mensajes_contacto.append({
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "mensaje": form.mensaje.data
        })
        flash('Mensaje enviado correctamente', 'success')
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
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM proveedores')
    proveedores = cursor.fetchall()
    cursor.close()
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
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO proveedores (
                nombre,
                telefono,
                correo
            )
            VALUES (%s, %s, %s)
        ''', (
            form.nombre_empresa.data,
            form.telefono.data,
            form.email.data
        ))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proveedor registrado correctamente en la base de datos', 'success')
        return redirect(url_for('proveedores_list'))
    elif request.method == 'POST':
        print("Errores de validación en ProveedorForm:", form.errors)

    return render_template(
        'proveedor_form.html',
        titulo="Nuevo Proveedor",
        form=form
    )


# 1. Listar Facturas desde la Base de Datos
@app.route('/facturacion')
def facturacion():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT f.*, p.nombre AS producto_nombre, p.precio AS producto_precio 
        FROM facturas f
        JOIN productos p ON f.id_producto = p.id_producto
    ''')
    facturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'facturacion.html',
        titulo="Facturación",
        facturas=facturas
    )


# 2. Registrar Nueva Factura (INSERT)
@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nueva_factura():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos')
    prendas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    form = FacturaForm()
    form.producto_id.choices = [
        (p['id_producto'], f"{p['nombre']} - ${p['precio']}")
        for p in prendas
    ]
    
    if form.validate_on_submit():
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT precio FROM productos WHERE id_producto = %s', (form.producto_id.data,))
        producto = cursor.fetchone()
        
        precio_unitario = float(producto['precio']) if producto else 0.0
        cantidad = int(form.cantidad.data)
        total = precio_unitario * cantidad
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facturas (cliente, id_producto, cantidad, total)
            VALUES (%s, %s, %s, %s)
        ''', (
            form.cliente.data,
            form.producto_id.data,
            cantidad,
            total
        ))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Factura generada y registrada correctamente en la base de datos', 'success')
        return redirect(url_for('facturacion'))
        
    return render_template(
        'factura_form.html',
        titulo="Nueva Factura",
        form=form
    )


@app.route('/procesar', methods=['POST'])
def procesar():
    return redirect(url_for('contacto'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)