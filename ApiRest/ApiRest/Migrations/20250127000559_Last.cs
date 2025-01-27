using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiRest.Migrations
{
    /// <inheritdoc />
    public partial class Last : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Compra",
                columns: table => new
                {
                    CodCompra = table.Column<int>(type: "int", nullable: false),
                    CodBoleta = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Compra", x => x.CodCompra);
                    table.ForeignKey(
                        name: "FK_Compra_Boleta_CodBoleta",
                        column: x => x.CodBoleta,
                        principalTable: "Boleta",
                        principalColumn: "CodBoleta",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "DetalleCompra",
                columns: table => new
                {
                    CodDetalleCompra = table.Column<int>(type: "int", nullable: false),
                    CodCompra = table.Column<int>(type: "int", nullable: false),
                    CodProducto = table.Column<int>(type: "int", nullable: false),
                    Cantidad = table.Column<int>(type: "int", nullable: false),
                    Subtotal = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DetalleCompra", x => x.CodDetalleCompra);
                    table.ForeignKey(
                        name: "FK_DetalleCompra_Compra_CodCompra",
                        column: x => x.CodCompra,
                        principalTable: "Compra",
                        principalColumn: "CodCompra",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_DetalleCompra_Producto_CodProducto",
                        column: x => x.CodProducto,
                        principalTable: "Producto",
                        principalColumn: "CodProducto",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Compra_CodBoleta",
                table: "Compra",
                column: "CodBoleta",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_DetalleCompra_CodCompra",
                table: "DetalleCompra",
                column: "CodCompra");

            migrationBuilder.CreateIndex(
                name: "IX_DetalleCompra_CodProducto",
                table: "DetalleCompra",
                column: "CodProducto");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "DetalleCompra");

            migrationBuilder.DropTable(
                name: "Compra");
        }
    }
}
