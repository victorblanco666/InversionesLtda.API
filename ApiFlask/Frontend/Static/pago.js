document.addEventListener('DOMContentLoaded', function () {
    // Función para formatear números en miles de pesos chilenos (CLP)
    function formatearCLP(numero) {
        return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', minimumFractionDigits: 0 }).format(numero);
    }

    // Función para obtener y mostrar el detalle de la compra
    function mostrarDetalleCompra() {
        // Obtener el elemento donde se mostrará el detalle de la compra
        const detalleCompraElemento = document.getElementById('detalleCompra');

        // Obtener los productos en el carrito desde localStorage
        const productosEnCarrito = JSON.parse(localStorage.getItem('productosEnCarrito')) || {};

        // Verificar si hay productos en el carrito
        if (Object.keys(productosEnCarrito).length === 0) {
            detalleCompraElemento.innerHTML = '<p>No hay productos en el carrito.</p>';
            return;
        }

        // Crear elementos HTML para mostrar el detalle de cada producto
        let totalGeneral = 0;
        for (const productoId in productosEnCarrito) {
            const producto = productosEnCarrito[productoId];
            const totalProducto = producto.cantidad * producto.precio;
            totalGeneral += totalProducto;

            const productoElemento = document.createElement('p');
            productoElemento.textContent = `Producto: ${producto.nombre}, Cantidad: ${producto.cantidad}, Precio: ${formatearCLP(producto.precio)}`;
            detalleCompraElemento.appendChild(productoElemento);
        }

        // Mostrar el total general
        const totalElemento = document.createElement('p');
        totalElemento.className = 'fw-bold mt-3';
        totalElemento.textContent = `Total General: ${formatearCLP(totalGeneral)}`;
        detalleCompraElemento.appendChild(totalElemento);
    }

    // Llamar a la función para mostrar el detalle de la compra al cargar la página
    mostrarDetalleCompra();

    const btnConfirmarPago = document.getElementById('btnConfirmarPago');

    btnConfirmarPago.addEventListener('click', function () {
        const nombreCliente = document.getElementById('nombreCliente').value;
        const emailCliente = document.getElementById('emailCliente').value;
        const telefonoCliente = document.getElementById('telefonoCliente').value;
        const montoPagar = document.getElementById('montoPagar').value;

        if (!nombreCliente || !emailCliente || !telefonoCliente || !montoPagar) {
            alert('Por favor complete todos los campos.');
            return;
        }

        const datosCliente = {
            nombre: nombreCliente,
            email: emailCliente,
            telefono: telefonoCliente,
            monto: parseFloat(montoPagar)
        };

        enviarDatosCompra(datosCliente);
    });

    // Función para enviar los datos del cliente y continuar con el proceso de compra
    function enviarDatosCompra(datosCliente) {
        // Obtener los productos en el carrito desde localStorage
        const productosEnCarrito = JSON.parse(localStorage.getItem('productosEnCarrito')) || {};
    
        // Verificar si hay productos en el carrito
        if (Object.keys(productosEnCarrito).length === 0) {
            alert('No hay productos en el carrito.');
            window.location.reload();
            return;
        }
        
    
        fetch('/api/enviar_cliente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosCliente)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error al enviar los datos del cliente.');
            } else {
                alert('Compra confirmada. Datos del cliente enviados.');
                window.print();
    
                document.getElementById('nombreCliente').value = '';
                document.getElementById('emailCliente').value = '';
                document.getElementById('telefonoCliente').value = '';
                document.getElementById('montoPagar').value = '';
                localStorage.removeItem('productosEnCarrito');
    
                // Recargar la página para reflejar los cambios en index.html
                window.location.reload();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al enviar los datos del cliente.');
        });
    }
    



});
