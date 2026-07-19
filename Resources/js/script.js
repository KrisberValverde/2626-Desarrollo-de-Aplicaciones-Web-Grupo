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
        event.preventDefault(); // Detener la recarga de la página

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
            const esValido = valor !== '' && valor.length >= 4;
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
            const esValido = valor !== '' && valor.length >= 10;
            switchClasesValidacion(txtDescripcion, esValido);
            return esValido;
        };

        // Forzar la ejecución de todas las validaciones
        if (!validarNombre() || !validarCategoria() || !validarDescripcion()) {
            mostrarMensaje('¡Error! Verifique los campos marcados en rojo antes de continuar.', 'danger');
            return;
        }

        // --- NUEVA LÓGICA: MODAL DE CONFIRMACIÓN ---
        const modal = new bootstrap.Modal(document.getElementById('modalConfirmacion'));
        modal.show();

        // 4. EVENTO DEL MODAL: Solo se ejecuta al confirmar
        document.getElementById('btn-confirmar-add').onclick = () => {
            modal.hide();
            const spinner = document.getElementById('spinner-carga');
            spinner.style.display = 'block';

            // Simulación de carga
            setTimeout(() => {
                spinner.style.display = 'none';

                // 5. CREACIÓN DE ELEMENTOS (MANIPULACIÓN DEL DOM): Generar nodos dinámicos
                const nombre = inputNombre.value.trim();
                const categoria = selectCategoria.value;
                const descripcion = txtDescripcion.value.trim();

                const fila = document.createElement('tr'); 
                fila.innerHTML = `
                    <td class="fw-bold text-dark">${nombre}</td>
                    <td><span class="badge bg-secondary">${categoria}</span></td>
                    <td class="text-muted small">${descripcion}</td>
                    <td class="text-center"><button class="btn btn-outline-danger btn-sm fw-bold">Eliminar</button></td>
                `;

                // 6. EVENTOS DEL MOUSE: Manejo del evento 'click' para remover elementos
                fila.querySelector('button').addEventListener('click', () => {
                    fila.remove();
                    contadorPrendas--;
                    totalRegistros.textContent = contadorPrendas;
                    mostrarMensaje('Prenda eliminada del catálogo.', 'warning');
                });

                // 7. ENSAMBLAJE DE NODOS CON APPENDCHILD
                listaProductos.appendChild(fila);

                // 8. CONTADOR DE REGISTROS: Incrementar el total
                contadorPrendas++;
                totalRegistros.textContent = contadorPrendas;

                mostrarMensaje('¡Prenda agregada al inventario correctamente!', 'success');
                formProducto.reset();
                resetearClasesValidacion();
            }, 1500);
        };
    });

    // Función auxiliar para inyectar alertas dinámicas
    function mostrarMensaje(texto, tipo) {
        mensajeAlerta.innerHTML = `
            <div class="alert alert-${tipo} alert-dismissible fade show p-2 small" role="alert">
                <strong>${tipo === 'danger' ? 'Aviso: ' : 'Info: '}</strong> ${texto}
                <button type="button" class="btn-close p-2" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        setTimeout(() => {
            const alertaActiva = document.querySelector('#mensaje-alerta .alert');
            if (alertaActiva) alertaActiva.remove();
        }, 4000);
    }
});