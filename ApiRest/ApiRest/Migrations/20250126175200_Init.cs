using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiRest.Migrations
{
    /// <inheritdoc />
    public partial class Init : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Region",
                columns: table => new
                {
                    CodRegion = table.Column<int>(type: "int", nullable: false),
                    NombreRegion = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Region", x => x.CodRegion);
                });

            migrationBuilder.CreateTable(
                name: "Provincia",
                columns: table => new
                {
                    CodRegion = table.Column<int>(type: "int", nullable: false),
                    CodProvincia = table.Column<int>(type: "int", nullable: false),
                    NombreProvincia = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Provincia", x => new { x.CodRegion, x.CodProvincia });
                    table.ForeignKey(
                        name: "FK_Provincia_Region_CodRegion",
                        column: x => x.CodRegion,
                        principalTable: "Region",
                        principalColumn: "CodRegion",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "Comuna",
                columns: table => new
                {
                    CodRegion = table.Column<int>(type: "int", nullable: false),
                    CodProvincia = table.Column<int>(type: "int", nullable: false),
                    CodComuna = table.Column<int>(type: "int", nullable: false),
                    NombreComuna = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Comuna", x => new { x.CodRegion, x.CodProvincia, x.CodComuna });
                    table.ForeignKey(
                        name: "FK_Comuna_Provincia_CodRegion_CodProvincia",
                        columns: x => new { x.CodRegion, x.CodProvincia },
                        principalTable: "Provincia",
                        principalColumns: new[] { "CodRegion", "CodProvincia" },
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "Cliente",
                columns: table => new
                {
                    NumRun = table.Column<int>(type: "int", nullable: false),
                    DvRun = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    P_Nombre = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    S_Nombre = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    A_Paterno = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    A_Materno = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Correo = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Direccion = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CodRegion = table.Column<int>(type: "int", nullable: false),
                    CodProvincia = table.Column<int>(type: "int", nullable: false),
                    CodComuna = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Cliente", x => x.NumRun);
                    table.ForeignKey(
                        name: "FK_Cliente_Comuna_CodRegion_CodProvincia_CodComuna",
                        columns: x => new { x.CodRegion, x.CodProvincia, x.CodComuna },
                        principalTable: "Comuna",
                        principalColumns: new[] { "CodRegion", "CodProvincia", "CodComuna" },
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Cliente_Provincia_CodRegion_CodProvincia",
                        columns: x => new { x.CodRegion, x.CodProvincia },
                        principalTable: "Provincia",
                        principalColumns: new[] { "CodRegion", "CodProvincia" },
                        onDelete: ReferentialAction.Restrict);
                    table.ForeignKey(
                        name: "FK_Cliente_Region_CodRegion",
                        column: x => x.CodRegion,
                        principalTable: "Region",
                        principalColumn: "CodRegion",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Cliente_CodRegion_CodProvincia_CodComuna",
                table: "Cliente",
                columns: new[] { "CodRegion", "CodProvincia", "CodComuna" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Cliente");

            migrationBuilder.DropTable(
                name: "Comuna");

            migrationBuilder.DropTable(
                name: "Provincia");

            migrationBuilder.DropTable(
                name: "Region");
        }
    }
}
