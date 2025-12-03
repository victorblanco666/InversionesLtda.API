using ApiRest.Context;
using ApiRest.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Mvc;

namespace ApiRest.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SucursalController : ControllerBase
    {
        private readonly AppDbContext _context;

        public SucursalController(AppDbContext context)
        {
            _context = context;
        }

        // GET: api/Sucursal
        [HttpGet]
        public async Task<ActionResult<IEnumerable<SucursalDto>>> GetSucursales()
        {
            var sucursales = await _context.Sucursal
                .Select(s => new SucursalDto
                {
                    CodSucursal = s.CodSucursal,
                    Direccion = s.Direccion,
                    Telefono = s.Telefono,
                    CodRegion = s.CodRegion,
                    CodProvincia = s.CodProvincia,
                    CodComuna = s.CodComuna
                })
                .ToListAsync();

            return Ok(sucursales);
        }

        // POST: api/Sucursal
        [HttpPost]
        public async Task<ActionResult<SucursalDto>> CreateSucursal(SucursalDto sucursalDto)
        {
            // Validar que la Comuna asociada exista
            var comuna = await _context.Comuna.FindAsync(sucursalDto.CodRegion, sucursalDto.CodProvincia, sucursalDto.CodComuna);
            if (comuna == null)
            {
                return BadRequest("La comuna asociada no existe.");
            }

            var sucursal = new Sucursal
            {
                CodSucursal = sucursalDto.CodSucursal,
                Direccion = sucursalDto.Direccion,
                Telefono = sucursalDto.Telefono,
                CodRegion = sucursalDto.CodRegion,
                CodProvincia = sucursalDto.CodProvincia,
                CodComuna = sucursalDto.CodComuna
            };

            _context.Sucursal.Add(sucursal);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetSucursales), new { id = sucursal.CodSucursal }, sucursalDto);
        }

        // PUT: api/Sucursal/{id}
        [HttpPut("{id:int}")]
        public async Task<IActionResult> UpdateSucursal(int id, [FromBody] SucursalDto sucursalDto)
        {
            var sucursal = await _context.Sucursal.FindAsync(id);
            if (sucursal == null)
                return NotFound("Sucursal no encontrada.");

            // Validar existencia de la nueva comuna
            var comuna = await _context.Comuna.FindAsync(
                sucursalDto.CodRegion, sucursalDto.CodProvincia, sucursalDto.CodComuna);
            if (comuna == null)
                return BadRequest("La comuna asociada no existe.");

            sucursal.Direccion = sucursalDto.Direccion;
            sucursal.Telefono = sucursalDto.Telefono;
            sucursal.CodRegion = sucursalDto.CodRegion;
            sucursal.CodProvincia = sucursalDto.CodProvincia;
            sucursal.CodComuna = sucursalDto.CodComuna;

            _context.Sucursal.Update(sucursal);
            await _context.SaveChangesAsync();
            return NoContent();
        }

        // DELETE: api/Sucursal/{id}
        [HttpDelete("{id:int}")]
        public async Task<IActionResult> DeleteSucursal(int id)
        {
            var sucursal = await _context.Sucursal.FindAsync(id);
            if (sucursal == null)
                return NotFound("Sucursal no encontrada.");

            _context.Sucursal.Remove(sucursal);
            await _context.SaveChangesAsync();
            return NoContent();
        }

    }
}
