document.addEventListener('DOMContentLoaded', function() {
    const botonesAgregar = document.querySelectorAll('.btn-agregar');
    const productosEnCarrito = JSON.parse(localStorage.getItem('productosEnCarrito')) || {};

    botonesAgregar.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            const productoId = this.dataset.productoId;
            const productoNombre = this.parentNode.querySelector('.card-title').textContent;
            const productoPrecio = this.parentNode.querySelector('.card-precio').textContent;

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
        for (const productoId in productosEnCarrito) {
            const producto = productosEnCarrito[productoId];
            const productoElemento = document.createElement('p');
            productoElemento.textContent = `Producto: ${producto.nombre}, ${producto.precio}, Cantidad: ${producto.cantidad}`;
            modalBody.appendChild(productoElemento);
        }
    }

    // Mostrar los productos en la página de pago
    const resumenCarrito = document.getElementById('resumen-carrito');
    if (resumenCarrito) {
        for (const productoId in productosEnCarrito) {
            const producto = productosEnCarrito[productoId];
            const productoElemento = document.createElement('p');
            productoElemento.textContent = `Producto: ${producto.nombre}, ${producto.precio}, Cantidad: ${producto.cantidad}`;
            resumenCarrito.appendChild(productoElemento);
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
