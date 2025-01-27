namespace ApiRest.Models
{
    public class DetalleCompra
    {
        public int CodDetalleCompra { get; set; }
        public int CodProducto { get; set; } // Clave foránea
        public int CodBoleta { get; set; } // Clave foránea
        public int Cantidad { get; set; }
        public int Subtotal { get; set; }

        // Propiedad de navegación hacia Producto
        public Producto Producto { get; set; }

        // Propiedad de navegación hacia Boleta
        public Boleta Boleta { get; set; }
    }
}
