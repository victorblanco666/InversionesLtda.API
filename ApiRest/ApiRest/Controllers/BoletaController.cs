using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ApiRest.Context;
using ApiRest.Models;

namespace ApiRest.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BoletaController : ControllerBase
    {
        private readonly AppDbContext _context;

        public BoletaController(AppDbContext context)
        {
            _context = context;
        }

        // GET: api/Boletas
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Boleta>>> GetBoleta()
        {
            return await _context.Boleta.ToListAsync();
        }

        // GET: api/Boletas/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Boleta>> GetBoleta(int id)
        {
            var boleta = await _context.Boleta.FindAsync(id);

            if (boleta == null)
            {
                return NotFound();
            }

            return boleta;
        }

        // PUT: api/Boletas/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutBoleta(int id, Boleta boleta)
        {
            if (id != boleta.Id)
            {
                return BadRequest();
            }

            _context.Entry(boleta).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!BoletaExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Boletas
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Boleta>> PostBoleta(Boleta boleta)
        {
            _context.Boleta.Add(boleta);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetBoleta", new { id = boleta.Id }, boleta);
        }

        // DELETE: api/Boletas/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBoleta(int id)
        {
            var boleta = await _context.Boleta.FindAsync(id);
            if (boleta == null)
            {
                return NotFound();
            }

            _context.Boleta.Remove(boleta);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool BoletaExists(int id)
        {
            return _context.Boleta.Any(e => e.Id == id);
        }
    }
}
