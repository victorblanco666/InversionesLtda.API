namespace ApiRest.Models
{
    public class Boleta
    {
        public int CodBoleta { get; set; } // Clave primaria
        public int NumRun { get; set; } // FK al cliente
        public Cliente Cliente { get; set; } // Relación con Cliente
        public int CodTarjeta { get; set; } // FK a Tarjeta
        public Tarjeta Tarjeta { get; set; } // Relación con Tarjeta
        public DateTime FechaEmision { get; set; } // Fecha de la boleta
        public int Total { get; set; } // Total de la compra
    }
}
