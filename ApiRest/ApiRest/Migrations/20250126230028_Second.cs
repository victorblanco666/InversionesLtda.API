using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiRest.Migrations
{
    /// <inheritdoc />
    public partial class Second : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Tarjeta",
                columns: table => new
                {
                    CodTarjeta = table.Column<int>(type: "int", nullable: false),
                    NombreTransaccion = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Tarjeta", x => x.CodTarjeta);
                });

            migrationBuilder.CreateTable(
                name: "Boleta",
                columns: table => new
                {
                    CodBoleta = table.Column<int>(type: "int", nullable: false),
                    NumRun = table.Column<int>(type: "int", nullable: false),
                    CodTarjeta = table.Column<int>(type: "int", nullable: false),
                    FechaEmision = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Total = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Boleta", x => x.CodBoleta);
                    table.ForeignKey(
                        name: "FK_Boleta_Cliente_NumRun",
                        column: x => x.NumRun,
                        principalTable: "Cliente",
                        principalColumn: "NumRun",
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Boleta_Tarjeta_CodTarjeta",
                        column: x => x.CodTarjeta,
                        principalTable: "Tarjeta",
                        principalColumn: "CodTarjeta",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Boleta_CodTarjeta",
                table: "Boleta",
                column: "CodTarjeta");

            migrationBuilder.CreateIndex(
                name: "IX_Boleta_NumRun",
                table: "Boleta",
                column: "NumRun");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Boleta");

            migrationBuilder.DropTable(
                name: "Tarjeta");
        }
    }
}
