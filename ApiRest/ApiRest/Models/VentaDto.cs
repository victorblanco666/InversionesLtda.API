namespace ApiRest.Models
{
    public class VentaDto
    {
        public int CodBoleta { get; set; }
        public int CodTarjeta { get; set; }
        public List<DetalleVentaDto> DetalleProductos { get; set; }
    }
}
