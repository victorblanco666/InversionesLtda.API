namespace ApiRest.Models
{
    public class Boleta
    {
        public int CodBoleta { get; set; }
        public int CodTarjeta { get; set; } // Clave foránea
        public int Total { get; set; }
        public DateTime FechaEmision { get; set; }

        // Propiedad de navegación hacia Tarjeta
        public Tarjeta Tarjeta { get; set; }

        // Propiedad de navegación hacia DetalleCompra
        public ICollection<DetalleCompra> DetalleCompra { get; set; }
    }
}
