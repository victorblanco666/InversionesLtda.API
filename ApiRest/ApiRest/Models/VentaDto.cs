namespace ApiRest.Models
{
    public class VentaDto
    {
        public int CodBoleta { get; set; }
        public int CodTarjeta { get; set; }
        public string RunCliente { get; set; } // Nuevo campo
        public List<DetalleVentaDto> DetalleProductos { get; set; }
    }
}
