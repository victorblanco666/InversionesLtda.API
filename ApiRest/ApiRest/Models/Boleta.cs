

namespace ApiRest.Models
{
    public class Boleta 
    {
        public int Id { get; set; }
        public int Total { get; set; }

        public int ClienteId { get; set; } // Propiedad para la clave foránea de Cliente
        public Cliente Cliente { get; set; }

        public int ProductoId { get; set; } // Propiedad para la clave foránea de Producto
        public Producto Producto { get; set; }

    }
}

