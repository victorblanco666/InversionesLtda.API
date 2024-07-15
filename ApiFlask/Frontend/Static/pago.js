document.addEventListener('DOMContentLoaded', function() {
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
            productoElemento.textContent = `Producto: ${producto.nombre}, Cantidad: ${producto.cantidad}, Precio: $${producto.precio.toFixed(2)}`;
            detalleCompraElemento.appendChild(productoElemento);
        }

        // Mostrar el total general
        const totalElemento = document.createElement('p');
        totalElemento.className = 'fw-bold mt-3';
        totalElemento.textContent = `Total General: $${totalGeneral.toFixed(2)}`;
        detalleCompraElemento.appendChild(totalElemento);
    }

    // Llamar a la función para mostrar el detalle de la compra al cargar la página
    mostrarDetalleCompra();

    const btnConfirmarPago = document.getElementById('btnConfirmarPago');

    btnConfirmarPago.addEventListener('click', function() {
        const nombreCliente = document.getElementById('nombreCliente').value;
        const emailCliente = document.getElementById('emailCliente').value;
        const telefonoCliente = document.getElementById('telefonoCliente').value;
        const montoPagar = document.getElementById('montoPagar').value;

        // Aquí podrías validar los campos antes de continuar

        // Ejemplo de cómo podrías usar estos datos (puedes adaptarlo según tu lógica)
        const datosCliente = {
            nombre: nombreCliente,
            email: emailCliente,
            telefono: telefonoCliente,
            monto: parseFloat(montoPagar)
        };

        // Ejemplo de cómo podrías enviar estos datos a través de una petición AJAX, por ejemplo
        enviarDatosCompra(datosCliente);
    });
    // Función para enviar los datos del cliente y continuar con el proceso de compra
    function enviarDatosCompra(datosCliente) {
        // Aquí podrías implementar tu lógica para enviar los datos al servidor
        // Por ejemplo, podrías usar fetch() o axios para enviar una solicitud POST
        // y procesar la respuesta del servidor según sea necesario.
        console.log('Datos del cliente:', datosCliente);
        alert('Compra confirmada. Datos del cliente enviados.');
    }
});


