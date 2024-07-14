document.addEventListener('DOMContentLoaded', function() {
    const botonesAgregar = document.querySelectorAll('.btn-agregar');
    const productosEnCarrito = {};

    botonesAgregar.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            const productoId = this.dataset.productoId;
            const productoNombre = this.parentNode.querySelector('.card-title').textContent; // Obtener el nombre del producto
            const productoPrecio = this.parentNode.querySelector('.card-precio').textContent; // Obtener el precio del producto

            // Agregar el producto al carrito o incrementar la cantidad si ya existe
            if (productosEnCarrito[productoId]) {
                productosEnCarrito[productoId].cantidad += 1;
            } else {
                productosEnCarrito[productoId] = { nombre: productoNombre, precio: productoPrecio, cantidad: 1 };
            }

            // Actualizar el contador del carrito
            actualizarContadorCarrito();

            // Mostrar los productos agregados en el modal
            mostrarProductosEnCarrito();
        });
    });

    function actualizarContadorCarrito() {
        // Obtener el elemento de contador del carrito
        const contadorCarrito = document.getElementById('contador-carrito');
        
        // Calcular la cantidad total de productos en el carrito
        const cantidadTotal = Object.values(productosEnCarrito).reduce((acc, producto) => acc + producto.cantidad, 0);
        
        // Actualizar el contador
        contadorCarrito.textContent = cantidadTotal;
    }

    function mostrarProductosEnCarrito() {
        // Obtener el elemento donde mostrar los productos en el modal
        const modalBody = document.querySelector('.modal-body');
        
        // Limpiar el contenido actual del modal
        modalBody.innerHTML = '';

        // Agregar cada producto al contenido del modal
        for (const productoId in productosEnCarrito) {
            const producto = productosEnCarrito[productoId];
            const productoElemento = document.createElement('p');
            productoElemento.textContent = `Producto: ${producto.nombre}, ${producto.precio}, Cantidad: ${producto.cantidad}`;
            modalBody.appendChild(productoElemento);
        }
    }
});



function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        window.scrollTo({
            top: section.offsetTop,
            behavior: 'smooth'
        });
    }
}

