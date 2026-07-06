// 1. CONTROL DE CARGA: Esperar a que el árbol del DOM esté construido en el navegador
document.addEventListener('DOMContentLoaded', () => {
    
    // 2. ACCESO AL DOM: Uso de getElementById para capturar los nodos de la interfaz
    const formProducto = document.getElementById('form-producto');
    const inputNombre = document.getElementById('prod-nombre');
    const selectCategoria = document.getElementById('prod-categoria');
    const txtDescripcion = document.getElementById('prod-descripcion');
    const listaProductos = document.getElementById('lista-productos');
    const totalRegistros = document.getElementById('total-registros');
    const mensajeAlerta = document.getElementById('mensaje-alerta');
    
    // Variable contadora para llevar el control del total de elementos creados
    let contadorPrendas = 0;

    // 3. EVENTOS DE FORMULARIO: Escuchar el evento 'submit' al enviar datos
    formProducto.addEventListener('submit', (event) => {
        const switchClasesValidacion = (elemento, esValido) => {
            if (esValido) {
                elemento.classList.remove('is-invalid');
                elemento.classList.add('is-valid');
            } else {
                elemento.classList.remove('is-valid');
                elemento.classList.add('is-invalid');
            }
        };

        const resetearClasesValidacion = () => {
            [inputNombre, selectCategoria, txtDescripcion].forEach(el => el.classList.remove('is-valid', 'is-invalid'));
        };

        const validarNombre = () => {
            const valor = inputNombre.value.trim();
            const esValido = valor !== '' && valor.length >= 4; // Mínimo 4 letras
            switchClasesValidacion(inputNombre, esValido);
            return esValido;
        };

        const validarCategoria = () => {
            const esValido = selectCategoria.value !== '';
            switchClasesValidacion(selectCategoria, esValido);
            return esValido;
        };

        const validarDescripcion = () => {
            const valor = txtDescripcion.value.trim();
            const esValido = valor !== '' && valor.length >= 10; // Mínimo 10 letras
            switchClasesValidacion(txtDescripcion, esValido);
            return esValido;
        };

        // ASIGNACIÓN DE EVENTOS EN TIEMPO REAL
        inputNombre.addEventListener('input', validarNombre);
        inputNombre.addEventListener('blur', validarNombre);
        selectCategoria.addEventListener('change', validarCategoria);
        selectCategoria.addEventListener('blur', validarCategoria);
        txtDescripcion.addEventListener('input', validarDescripcion);
        txtDescripcion.addEventListener('blur', validarDescripcion);

        // Uso obligatorio de preventDefault() para detener la recarga de la página
        event.preventDefault();

        // Forzar la ejecución de todas las validaciones individuales
        const esNombreValido = validarNombre();
        const esCategoriaValida = validarCategoria();
        const esDescripcionValida = validarDescripcion();

        // Comprobar si alguna falló
        if (!esNombreValido || !esCategoriaValida || !esDescripcionValida) {
            mostrarMensaje('¡Error! Verifique los campos marcados en rojo antes de continuar.', 'danger');
            return; // Corta la ejecución del código
        }

        // Obtención segura de valores para usarlos en tus tablas de abajo
        const nombre = inputNombre.value.trim();
        const categoria = selectCategoria.value;
        const descripcion = txtDescripcion.value.trim();
        // 5. CREACIÓN DE ELEMENTOS (MANIPULACIÓN DEL DOM): Generar nodos dinámicos
        const fila = document.createElement('tr'); // Nodo contenedor principal

        // Columna Nombre
        const colNombre = document.createElement('td');
        colNombre.className = 'fw-bold text-dark';
        colNombre.textContent = nombre;

        // Columna Categoría (Aplica badges dinámicos de Bootstrap)
        const colCategoria = document.createElement('td');
        colCategoria.innerHTML = `<span class="badge bg-secondary">${categoria}</span>`;

        // Columna Descripción
        const colDescripcion = document.createElement('td');
        colDescripcion.className = 'text-muted small';
        colDescripcion.textContent = descripcion;

        // Columna de Acción (Para el botón de remoción)
        const colAccion = document.createElement('td');
        colAccion.className = 'text-center';

        // Creación del Botón de Eliminar
        const botonEliminar = document.createElement('button');
        botonEliminar.className = 'btn btn-outline-danger btn-sm fw-bold';
        botonEliminar.textContent = 'Eliminar';

        // 6. EVENTOS DEL MOUSE: Manejo del evento 'click' para remover elementos de la lista
        botonEliminar.addEventListener('click', () => {
            // Remueve la fila correspondiente del árbol DOM
            fila.remove();
            
            // Decrementar el contador general y actualizar la UI
            contadorPrendas--;
            totalRegistros.textContent = contadorPrendas;
            
            mostrarMensaje('Prenda eliminada del catálogo.', 'warning');
        });

        // 7. ENSAMBLAJE DE NODOS CON APPENDCHILD: Estructurar la tabla jerárquicamente
        colAccion.appendChild(botonEliminar);
        
        fila.appendChild(colNombre);
        fila.appendChild(colCategoria);
        fila.appendChild(colDescripcion);
        fila.appendChild(colAccion);

        // Insertar la fila completa dentro del cuerpo de la tabla (tbody)
        listaProductos.appendChild(fila);

        // 8. CONTADOR DE REGISTROS: Incrementar el total de elementos activos
        contadorPrendas++;
        totalRegistros.textContent = contadorPrendas;

        // Mostrar notificación de éxito y limpiar las casillas del formulario
        mostrarMensaje('¡Prenda agregada al inventario correctamente!', 'success');
        formProducto.reset();
        resetearClasesValidacion();
    });

    // Función auxiliar para inyectar alertas dinámicas usando clases de Bootstrap
    function mostrarMensaje(texto, tipo) {
        mensajeAlerta.innerHTML = `
            <div class="alert alert-${tipo} alert-dismissible fade show p-2 small" role="alert">
                <strong>${tipo === 'danger' ? 'Aviso: ' : 'Info: '}</strong> ${texto}
                <button type="button" class="btn-close p-2" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;

        // Eliminación programada del nodo de alerta tras 4 segundos
        setTimeout(() => {
            const alertaActiva = document.querySelector('#mensaje-alerta .alert');
            if (alertaActiva) {
                alertaActiva.remove();
            }
        }, 4000);
    }
});