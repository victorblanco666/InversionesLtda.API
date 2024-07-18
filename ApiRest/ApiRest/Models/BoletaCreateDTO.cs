namespace ApiRest.Models
{
    public class BoletaCreateDTO
    {
        public int Id { get; set; }
        public int Total { get; set; }
        public int ClienteId { get; set; }
        public ClienteDTO Cliente { get; set; }
        public int ProductoId { get; set; }
    }

    public class ClienteDTO
    {
        public int Id { get; set; }
        public string NombreCliente { get; set; }
        public string Email { get; set; }
        public string Telefono { get; set; }
    }
}
