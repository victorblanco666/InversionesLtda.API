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
});
