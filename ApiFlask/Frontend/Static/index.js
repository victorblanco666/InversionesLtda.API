document.addEventListener('DOMContentLoaded', function() {
    const botonesAgregar = document.querySelectorAll('.btn-agregar');
    let productosEnCarrito = JSON.parse(localStorage.getItem('productosEnCarrito')) || {};

    botonesAgregar.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            const productoId = this.dataset.productoId;
            const productoNombre = this.parentNode.querySelector('.card-title').textContent;
            const productoPrecioText = this.parentNode.querySelector('.card-precio').textContent;
            const productoPrecio = parseFloat(productoPrecioText.replace('Precio: $', '').trim());

            if (productosEnCarrito[productoId]) {
                productosEnCarrito[productoId].cantidad += 1;
            } else {
                productosEnCarrito[productoId] = { nombre: productoNombre, precio: productoPrecio, cantidad: 1 };
            }

            actualizarContadorCarrito();
            mostrarProductosEnCarrito();
            localStorage.setItem('productosEnCarrito', JSON.stringify(productosEnCarrito));
        });
    });

    function actualizarContadorCarrito() {
        const contadorCarrito = document.getElementById('contador-carrito');
        const cantidadTotal = Object.values(productosEnCarrito).reduce((acc, producto) => acc + producto.cantidad, 0);
        contadorCarrito.textContent = cantidadTotal;
    }

    function mostrarProductosEnCarrito() {
        const modalBody = document.querySelector('.modal-body');
        modalBody.innerHTML = '';

        let totalGeneral = 0;

        for (const productoId in productosEnCarrito) {
            const producto = productosEnCarrito[productoId];
            const totalProducto = producto.cantidad * producto.precio;
            totalGeneral += totalProducto;

            const productoElemento = document.createElement('p');
            productoElemento.textContent = `Producto: ${producto.nombre}, Cantidad: ${producto.cantidad}, Precio: $${producto.precio.toFixed(2)}`;
            modalBody.appendChild(productoElemento);
        }

        const totalElemento = document.createElement('p');
        totalElemento.className = 'fw-bold mt-3';
        totalElemento.textContent = `Total General: $${totalGeneral.toFixed(2)}`;
        modalBody.appendChild(totalElemento);
    }
    // Mostrar productos en carrito al cargar la página
    mostrarProductosEnCarrito();
    actualizarContadorCarrito();   

    const botonPagar = document.querySelector('.btn-pagar');
    if (botonPagar) {
        botonPagar.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = "{{ url_for('pago') }}";
        });
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