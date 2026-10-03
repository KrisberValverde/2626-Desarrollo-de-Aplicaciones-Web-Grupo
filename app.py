from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

from forms import ProductoForm, ClienteForm, ContactoForm, ProveedorForm, FacturaForm
from forms.forms import FormularioLogin, FormularioRegistro
from models import Usuario
from conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'boutique_alison-2026-csrf-segura'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debe iniciar sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)

mensajes_contacto = []


# --- RUTAS DE AUTENTICACIÓN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.rol == 'administrador':
            return redirect(url_for('catalogo'))
        return redirect(url_for('productos_servicios'))
    
    form = FormularioLogin()
    if form.validate_on_submit():
        usuario_ingresado = form.usuario.data.strip()
        password_ingresada = form.password.data.strip()
        
        # ATANJO DE SEGURIDAD PARA ADMIN (Manejado por Python)
        if usuario_ingresado.lower() == 'admin' and password_ingresada == 'admin123':
            admin_user = Usuario(1, 'admin', '', 'administrador')
            login_user(admin_user)
            flash('¡Bienvenido Administrador!', 'success')
            return redirect(url_for('catalogo'))

        # Lógica normal de base de datos para otros usuarios (clientes)
        user = Usuario.obtener_por_nombre(usuario_ingresado)
        if user and check_password_hash(user.password, password_ingresada):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('productos_servicios'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            
    return render_template('login.html', titulo="Iniciar Sesión", form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = FormularioRegistro()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data.strip(), method='pbkdf2:sha256')
        usuario_limpio = form.usuario.data.strip()
        
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (%s, %s, %s)", 
                (usuario_limpio, hashed_password, 'cliente')
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registro exitoso. Ahora puede iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error en registro: {e}")
            flash('El nombre de usuario ya se encuentra registrado o ocurrió un error.', 'danger')
    else:
        if request.method == 'POST':
            print(">>> ERRORES DE VALIDACIÓN EN REGISTRO:", form.errors)
            
    return render_template('registro.html', titulo="Registro de Usuario", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ha cerrado sesión correctamente.', 'info')
    return redirect(url_for('login'))


# --- RUTAS PÚBLICAS ---

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

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/productos-servicios')
def productos_servicios():
    categoria_f = request.args.get('categoria')
    
    # Lista unificada de 6 categorías oficiales
    categorias = ["Vestidos", "Tops", "Pantalones", "Camisas", "Enterizos", "Faldas"]
    
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    if categoria_f:
        cursor.execute('SELECT * FROM productos WHERE categoria = %s ORDER BY id_producto DESC', (categoria_f,))
    else:
        cursor.execute('SELECT * FROM productos ORDER BY id_producto DESC')
        
    prendas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template(
        'productos_servicios.html',
        titulo="Productos o Servicios",
        prendas=prendas,
        categorias=categorias,
        categoria_activa=categoria_f
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

@app.route('/procesar', methods=['POST'])
def procesar():
    return redirect(url_for('contacto'))


# --- RUTAS PROTEGIDAS (Requieren Login) ---

@app.route('/catalogo')
@login_required
def catalogo():
    if current_user.rol != 'administrador':
        flash('Acceso denegado. Se requieren permisos de administrador.', 'danger')
        return redirect(url_for('index'))

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM productos')
    prendas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template(
        'catalogo.html',
        titulo="Panel de Administración",
        prendas=prendas
    )

@app.route('/catalogo/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        stock_s = form.stock_s.data or 0
        stock_m = form.stock_m.data or 0
        stock_l = form.stock_l.data or 0
        stock_total = stock_s + stock_m + stock_l
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO productos (nombre, categoria, precio, stock, stock_s, stock_m, stock_l, imagen) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
            (form.nombre.data, form.categoria.data, form.precio.data, stock_total, stock_s, stock_m, stock_l, form.imagen.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('catalogo'))
        
    return render_template('producto_form.html', form=form, titulo="Añadir Producto")

@app.route('/catalogo/editar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def editar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    producto = cursor.fetchone()
    
    if not producto:
        cursor.close()
        conn.close()
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('catalogo'))

    form = ProductoForm(data=producto)
    
    if form.validate_on_submit():
        stock_s = form.stock_s.data or 0
        stock_m = form.stock_m.data or 0
        stock_l = form.stock_l.data or 0
        stock_total = stock_s + stock_m + stock_l
        
        cursor.execute(
            '''UPDATE productos 
               SET nombre=%s, categoria=%s, precio=%s, stock=%s, stock_s=%s, stock_m=%s, stock_l=%s, imagen=%s 
               WHERE id_producto=%s''',
            (form.nombre.data, form.categoria.data, form.precio.data, stock_total, stock_s, stock_m, stock_l, form.imagen.data, id_producto)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('catalogo'))

    cursor.close()
    conn.close()
    return render_template('producto_form.html', form=form, titulo="Editar Producto")

@app.route('/catalogo/eliminar/<int:id_producto>', methods=['POST', 'GET'])
@login_required
def eliminar_producto(id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id_producto = %s', (id_producto,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Prenda eliminada correctamente del catálogo', 'success')
    return redirect(url_for('catalogo'))

# Carrito de compras
@app.route('/agregar_al_carrito/<int:id_producto>', methods=['POST'])
def agregar_al_carrito(id_producto):
    talla = request.form.get('talla')
    
    if not talla:
        flash('Debes seleccionar una talla antes de agregar al carrito.', 'warning')
        return redirect(request.referrer or url_for('productos_servicios'))
        
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM productos WHERE id_producto = %s', (id_producto,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not producto:
        flash('El producto seleccionado no existe.', 'danger')
        return redirect(url_for('productos_servicios'))
        
    if 'carrito' not in session:
        session['carrito'] = []
        
    carrito = session['carrito']
    
    # Verificar si el mismo producto y talla ya está en el carrito
    existente = False
    for item in carrito:
        if item['id_producto'] == id_producto and item['talla'] == talla:
            item['cantidad'] += 1
            existente = True
            break
            
    if not existente:
        carrito.append({
            'id_producto': producto['id_producto'],
            'nombre': producto['nombre'],
            'precio': float(producto['precio']),
            'imagen': producto['imagen'],
            'talla': talla,
            'cantidad': 1,
            'stock_s': producto['stock_s'],
            'stock_m': producto['stock_m'],
            'stock_l': producto['stock_l']
        })
        
    session.modified = True
    flash(f'¡{producto["nombre"]} (Talla {talla}) añadido al carrito!', 'success')
    return redirect(request.referrer or url_for('productos_servicios'))

@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    subtotal = sum(item['precio'] * item['cantidad'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, subtotal=subtotal)

@app.route('/eliminar_del_carrito/<int:indice>')
def eliminar_del_carrito(indice):
    carrito = session.get('carrito', [])
    if 0 <= indice < len(carrito):
        eliminado = carrito.pop(indice)
        session.modified = True
        flash(f'Se eliminó {eliminado["nombre"]} del carrito.', 'info')
    return redirect(url_for('ver_carrito'))

@app.route('/vaciar_carrito')
def vaciar_carrito():
    session.pop('carrito', None)
    flash('El carrito ha sido vaciado.', 'info')
    return redirect(url_for('ver_carrito'))

@app.route('/proveedores')
@login_required
def proveedores_list():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
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
@login_required
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

@app.route('/facturacion')
@login_required
def facturacion():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Consulta sin especificar el nombre exacto de la clave foránea en f
        cursor.execute('''
            SELECT f.*, p.nombre AS producto_nombre, p.precio AS producto_precio 
            FROM facturas f, productos p 
            WHERE f.id_producto = p.id_producto
        ''')
        facturas = cursor.fetchall()
    except Exception:
        conn.rollback()
        # Alternativa si en facturas la columna id se llama de otra forma
        cursor.execute('SELECT * FROM facturas')
        facturas = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template(
        'facturacion.html',
        titulo="Facturación",
        facturas=facturas
    )

@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
@login_required
def nueva_factura():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        # Se reemplaza dictionary=True por RealDictCursor
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)