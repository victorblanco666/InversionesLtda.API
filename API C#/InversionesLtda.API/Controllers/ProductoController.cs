using InversionesLtda.API.Models;
using Microsoft.AspNetCore.Mvc;

namespace InversionesLtda.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductoController: ControllerBase
    {

        private static IList<Producto> lista = new List<Producto>();


        // GET: api/<ClienteController>
        [HttpGet]
        public IEnumerable<Producto> Get()
        {
            return lista;
        }


        [HttpGet("{id}")]
        public Producto Get(int id)
        {
            return lista.FirstOrDefault(x => x.id == id);
        }

        // POST api/<ClienteController>
        [HttpPost]
        public void Post([FromBody] Producto value)
        {
            lista.Add(value);
        }


        // PUT api/<ClienteController>/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody] Producto value)
        {
            Producto selection = lista.FirstOrDefault(x => x.id == id);
            lista[lista.IndexOf(selection)] = value;
        }

        // DELETE api/<ClienteController>/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
            lista.Remove(lista.FirstOrDefault(x => x.id == id));
        }



    }


}
