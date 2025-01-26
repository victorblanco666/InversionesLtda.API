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
        public DbSet<Cliente> Cliente { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Configuración de Region
            modelBuilder.Entity<Region>()
                .Property(r => r.CodRegion)
                .ValueGeneratedNever(); // Clave manual
            modelBuilder.Entity<Region>()
                .HasKey(r => r.CodRegion);

            // Configuración de Provincia
            modelBuilder.Entity<Provincia>()
                .Property(p => p.CodProvincia)
                .ValueGeneratedNever(); // Clave manual
            modelBuilder.Entity<Provincia>()
                .HasKey(p => new { p.CodRegion, p.CodProvincia });

            modelBuilder.Entity<Provincia>()
                .HasOne(p => p.Region)
                .WithMany(r => r.Provincia)
                .HasForeignKey(p => p.CodRegion)
                .OnDelete(DeleteBehavior.Restrict);

            // Configuración de Comuna
            modelBuilder.Entity<Comuna>()
                .Property(c => c.CodComuna)
                .ValueGeneratedNever(); // Clave manual
            modelBuilder.Entity<Comuna>()
                .HasKey(c => new { c.CodRegion, c.CodProvincia, c.CodComuna });

            modelBuilder.Entity<Comuna>()
                .HasOne(c => c.Provincia)
                .WithMany(p => p.Comuna)
                .HasForeignKey(c => new { c.CodRegion, c.CodProvincia })
                .OnDelete(DeleteBehavior.Restrict);

            // Configuración de Cliente
            modelBuilder.Entity<Cliente>()
                .Property(cl => cl.NumRun)
                .ValueGeneratedNever(); // Clave primaria manual
            modelBuilder.Entity<Cliente>()
                .HasKey(cl => cl.NumRun);

            modelBuilder.Entity<Cliente>()
                .HasOne(cl => cl.Region)
                .WithMany(r => r.Cliente) // Agregar ICollection<Cliente> a la clase Region
                .HasForeignKey(cl => cl.CodRegion)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Cliente>()
                .HasOne(cl => cl.Provincia)
                .WithMany(p => p.Cliente) // Agregar ICollection<Cliente> a la clase Provincia
                .HasForeignKey(cl => new { cl.CodRegion, cl.CodProvincia })
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Cliente>()
                .HasOne(cl => cl.Comuna)
                .WithMany(c => c.Cliente) // Agregar ICollection<Cliente> a la clase Comuna
                .HasForeignKey(cl => new { cl.CodRegion, cl.CodProvincia, cl.CodComuna })
                .OnDelete(DeleteBehavior.Restrict);

            // Configuración de Sucursal
            modelBuilder.Entity<Sucursal>()
                .Property(s => s.CodSucursal)
                .ValueGeneratedNever(); // Clave primaria manual
            modelBuilder.Entity<Sucursal>()
                .HasKey(s => s.CodSucursal);

            modelBuilder.Entity<Sucursal>()
                .HasOne(s => s.Comuna)
                .WithMany(c => c.Sucursal) // Agregar ICollection<Sucursal> en Comuna
                .HasForeignKey(s => new { s.CodRegion, s.CodProvincia, s.CodComuna })
                .OnDelete(DeleteBehavior.Restrict);

            // Configuración de Producto
            modelBuilder.Entity<Producto>()
                .Property(p => p.CodProducto)
                .ValueGeneratedNever(); // Clave primaria manual
            modelBuilder.Entity<Producto>()
                .HasKey(p => p.CodProducto);

            // Configuración de Stock
            modelBuilder.Entity<Stock>()
                .Property(st => st.CodStock)
                .ValueGeneratedNever(); // Clave primaria manual
            modelBuilder.Entity<Stock>()
                .HasKey(st => st.CodStock);

            modelBuilder.Entity<Stock>()
                .HasOne(st => st.Producto)
                .WithMany(p => p.Stock)
                .HasForeignKey(st => st.CodProducto)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Stock>()
                .HasOne(st => st.Sucursal)
                .WithMany(s => s.Stock)
                .HasForeignKey(st => st.CodSucursal)
                .OnDelete(DeleteBehavior.Restrict);

            base.OnModelCreating(modelBuilder);
        }
    }
}
