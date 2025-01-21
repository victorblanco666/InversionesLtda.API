using ApiRest.Models;
using Microsoft.EntityFrameworkCore;

namespace ApiRest.Context
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options): base(options)
        {
            
        }
        public DbSet<Boleta> Boleta {  get; set; }        
        public DbSet<Cliente> Cliente { get; set; } 
        public DbSet<Producto> Producto { get; set; }
        
        
    }
}
