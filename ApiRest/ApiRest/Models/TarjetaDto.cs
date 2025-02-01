namespace ApiRest.Models
{
    public class TarjetaDto
    {
        public int CodTarjeta { get; set; }
        public string NombreTransaccion { get; set; }
    }

    public class CreateTarjetaDto
    {
        public int CodTarjeta { get; set; }
        public string NombreTransaccion { get; set; }
    }

}
