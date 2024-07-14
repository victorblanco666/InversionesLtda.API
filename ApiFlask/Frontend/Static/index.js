// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    const botonesAgregar = document.querySelectorAll('.btn-agregar');

    botonesAgregar.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            const productoId = this.dataset.productoId;
            
            // Lógica para agregar al carrito (puedes implementarla aquí)
            console.log(`Añadir producto con ID ${productoId} al carrito`);
            
            // Actualizar contador de carrito (por ejemplo, incrementar)
            actualizarContadorCarrito();
        });
    });

    function actualizarContadorCarrito() {
        // Obtener el elemento de contador del carrito
        const contadorCarrito = document.getElementById('contador-carrito');
        
        // Incrementar el contador (ejemplo simple)
        let cantidadActual = parseInt(contadorCarrito.textContent);
        contadorCarrito.textContent = cantidadActual + 1;
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