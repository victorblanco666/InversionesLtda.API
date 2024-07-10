using ApiRest.Models;
using Microsoft.AspNetCore.Mvc;

namespace ApiRest.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductoController : ControllerBase
    {

        private static List<Producto> Productos = new List<Producto>
        {
            new Producto { Id = 1, Nombre = "Producto 1", Descripcion = "Descripción del Producto 1", Precio = 99, Stock = 10 },
            new Producto { Id = 2, Nombre = "Producto 2", Descripcion = "Descripción del Producto 2", Precio = 49, Stock = 20 }
        };


        // GET: api/producto
        [HttpGet]
        public ActionResult<IEnumerable<Producto>> GetProductos()
        {
            return Productos;
        }

        [HttpGet("{id}")]
        public ActionResult<Producto> GetProducto(int id)
        {
            var producto = Productos.FirstOrDefault(p => p.Id == id);
            if (producto == null)
            {
                return NotFound();
            }
            return producto;
        }



        // POST: api/producto
        [HttpPost]
        public ActionResult<Producto> CreateProducto(Producto producto)
        {
            producto.Id = Productos.Max(p => p.Id) + 1;
            Productos.Add(producto);
            return CreatedAtAction(nameof(GetProducto), new { id = producto.Id }, producto);
        }

        // PUT: api/producto/5
        [HttpPut("{id}")]
        public IActionResult UpdateProducto(int id, Producto producto)
        {
            var existingProducto = Productos.FirstOrDefault(p => p.Id == id);
            if (existingProducto == null)
            {
                return NotFound();
            }

            existingProducto.Nombre = producto.Nombre;
            existingProducto.Descripcion = producto.Descripcion;
            existingProducto.Precio = producto.Precio;
            existingProducto.Stock = producto.Stock;

            return NoContent();
        }



        // DELETE: api/producto/5
        [HttpDelete("{id}")]
        public IActionResult DeleteProducto(int id)
        {
            var producto = Productos.FirstOrDefault(p => p.Id == id);
            if (producto == null)
            {
                return NotFound();
            }

            Productos.Remove(producto);
            return NoContent();
        }

    }
}
