namespace ApiRest.Models
{
    public class DetalleCompra
    {
        public int CodDetalleCompra { get; set; } // Clave primaria
        public int CodCompra { get; set; } // FK a Compra
        public Compra Compra { get; set; } // Relación con Compra
        public int CodProducto { get; set; } // FK a Producto
        public Producto Producto { get; set; } // Relación con Producto
        public int Cantidad { get; set; } // Cantidad del producto comprado
        public int Subtotal { get; set; } // Subtotal para este producto (Cantidad * PrecioProducto)
    }
}
