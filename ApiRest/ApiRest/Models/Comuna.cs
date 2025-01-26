namespace ApiRest.Models
{
    public class Comuna
    {
        public int CodRegion { get; set; } // Clave compuesta (parte de la relación con Region y Provincia)
        public int CodProvincia { get; set; } // Clave compuesta (parte de la relación con Provincia)
        public int CodComuna { get; set; } // Clave primaria

        public string NombreComuna { get; set; } 

        // Relación con Provincia
        public Provincia Provincia { get; set; }

        public ICollection<Cliente> Cliente { get; set; }

    }
}
