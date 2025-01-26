using ApiRest.Models;
using Microsoft.EntityFrameworkCore;

namespace ApiRest.Context
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Region> Region { get; set; }
        public DbSet<Provincia> Provincia { get; set; }
        public DbSet<Comuna> Comuna { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Region>()
                .Property(r => r.CodRegion)
                .ValueGeneratedNever(); // Desactivar autoincremento en Region

            modelBuilder.Entity<Provincia>()
                .Property(p => p.CodProvincia)
                .ValueGeneratedNever(); // Desactivar autoincremento en Provincia

            modelBuilder.Entity<Comuna>()
                .Property(c => c.CodComuna)
                .ValueGeneratedNever(); // Desactivar autoincremento en Comuna
            // Configuración de Region
            modelBuilder.Entity<Region>()
                .HasKey(r => r.CodRegion); // Clave primaria manual

            // Configuración de Provincia
            modelBuilder.Entity<Provincia>()
                .HasKey(p => new { p.CodRegion, p.CodProvincia }); // Clave primaria compuesta

            modelBuilder.Entity<Provincia>()
                .HasOne(p => p.Region)
                .WithMany(r => r.Provincia)
                .HasForeignKey(p => p.CodRegion)
                .OnDelete(DeleteBehavior.Restrict); // Sin eliminación en cascada

            // Configuración de Comuna
            modelBuilder.Entity<Comuna>()
                .HasKey(c => new { c.CodRegion, c.CodProvincia, c.CodComuna }); // Clave primaria compuesta

            modelBuilder.Entity<Comuna>()
                .HasOne(c => c.Provincia)
                .WithMany(p => p.Comuna)
                .HasForeignKey(c => new { c.CodRegion, c.CodProvincia })
                .OnDelete(DeleteBehavior.Restrict); // Sin eliminación en cascada
        }
    }
}