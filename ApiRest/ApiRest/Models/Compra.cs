namespace ApiRest.Models
{
    public class Compra
    {
        public int CodCompra { get; set; } // Clave primaria
        public int CodBoleta { get; set; } // FK a Boleta
        public Boleta Boleta { get; set; } // Relación con Boleta
        public ICollection<DetalleCompra> DetalleCompra { get; set; } // Relación con DetalleCompra
    }
}
