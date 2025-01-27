namespace ApiRest.Models
{
    public class Boleta
    {
        public int CodBoleta { get; set; } // Clave primaria
        public DateTime Fecha { get; set; } // Fecha de la transacción
        public int CodTarjeta { get; set; } // FK hacia Tarjeta (opcional)
        public Tarjeta Tarjeta { get; set; } // Relación con Tarjeta
        public ICollection<DetalleBoleta> DetalleBoleta { get; set; } // Relación con DetalleBoleta
        public ICollection<Cliente> Cliente { get; set; } // Relación con DetalleBoleta
    }
}
