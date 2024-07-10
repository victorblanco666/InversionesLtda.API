using ApiRest.Models;
using Microsoft.AspNetCore.Mvc;

namespace ApiRest.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ClienteController : ControllerBase
    {


        private static List<Cliente> Clientes = new List<Cliente>
        {
            new Cliente { Id = 1, Nombre = "Juan Perez", Email = "juan.perez@example.com", Telefono = "123456789" },
            new Cliente { Id = 2, Nombre = "Maria Garcia", Email = "maria.garcia@example.com", Telefono = "987654321" }
        };



        [HttpGet]
        public ActionResult<IEnumerable<Cliente>> GetClientes()
        {
            return Clientes;
        }


        [HttpGet("{id}")]
        public ActionResult<Cliente> GetCliente(int id)
        {
            var cliente = Clientes.FirstOrDefault(c => c.Id == id);
            if (cliente == null)
            {
                return NotFound();
            }
            return cliente;
        }

        [HttpPost]
        public ActionResult<Cliente> CreateCliente(Cliente cliente)
        {
            cliente.Id = Clientes.Max(c => c.Id) + 1;
            Clientes.Add(cliente);
            return CreatedAtAction(nameof(GetCliente), new { id = cliente.Id }, cliente);
        }


        [HttpPut("{id}")]
        public IActionResult UpdateCliente(int id, Cliente cliente)
        {
            var existingCliente = Clientes.FirstOrDefault(c => c.Id == id);
            if (existingCliente == null)
            {
                return NotFound();
            }

            existingCliente.Nombre = cliente.Nombre;
            existingCliente.Email = cliente.Email;
            existingCliente.Telefono = cliente.Telefono;

            return NoContent();
        }


        [HttpDelete("{id}")]
        public IActionResult DeleteCliente(int id)
        {
            var cliente = Clientes.FirstOrDefault(c => c.Id == id);
            if (cliente == null)
            {
                return NotFound();
            }

            Clientes.Remove(cliente);
            return NoContent();
        }



    }
}
