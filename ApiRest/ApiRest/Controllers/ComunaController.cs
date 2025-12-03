using ApiRest.Context;
using ApiRest.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ApiRest.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ComunaController : ControllerBase
    {
        private readonly AppDbContext _context;

        public ComunaController(AppDbContext context)
        {
            _context = context;
        }

        // GET: api/Comuna
        [HttpGet]
        public async Task<ActionResult<IEnumerable<ComunaDto>>> GetComunas()
        {
            var comunas = await _context.Comuna
                .Select(c => new ComunaDto
                {
                    CodRegion = c.CodRegion,
                    CodProvincia = c.CodProvincia,
                    CodComuna = c.CodComuna,
                    NombreComuna = c.NombreComuna
                })
                .ToListAsync();

            return Ok(comunas);
        }

        // POST: api/Comuna
        [HttpPost]
        public async Task<ActionResult<ComunaDto>> CreateComuna(ComunaDto comunaDto)
        {
            if (await _context.Comuna.AnyAsync(c =>
                c.CodRegion == comunaDto.CodRegion &&
                c.CodProvincia == comunaDto.CodProvincia &&
                c.CodComuna == comunaDto.CodComuna))
            {
                return BadRequest("La comuna con este ID ya existe.");
            }

            var comuna = new Comuna
            {
                CodRegion = comunaDto.CodRegion,
                CodProvincia = comunaDto.CodProvincia,
                CodComuna = comunaDto.CodComuna,
                NombreComuna = comunaDto.NombreComuna
            };

            _context.Comuna.Add(comuna);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetComunas), new { id = comuna.CodComuna }, comunaDto);
        }
        // PUT: api/Comuna/{codRegion}/{codProvincia}/{codComuna}
        [HttpPut("{codRegion:int}/{codProvincia:int}/{codComuna:int}")]
        public async Task<IActionResult> UpdateComuna(int codRegion, int codProvincia, int codComuna, [FromBody] ComunaDto comunaDto)
        {
            var comuna = await _context.Comuna.FindAsync(codRegion, codProvincia, codComuna);
            if (comuna == null)
                return NotFound("Comuna no encontrada.");

            comuna.NombreComuna = comunaDto.NombreComuna;
            _context.Comuna.Update(comuna);
            await _context.SaveChangesAsync();
            return NoContent();
        }

        // DELETE: api/Comuna/{codRegion}/{codProvincia}/{codComuna}
        [HttpDelete("{codRegion:int}/{codProvincia:int}/{codComuna:int}")]
        public async Task<IActionResult> DeleteComuna(int codRegion, int codProvincia, int codComuna)
        {
            var comuna = await _context.Comuna.FindAsync(codRegion, codProvincia, codComuna);
            if (comuna == null)
                return NotFound("Comuna no encontrada.");

            _context.Comuna.Remove(comuna);
            await _context.SaveChangesAsync();
            return NoContent();
        }

    }
}
