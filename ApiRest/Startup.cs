namespace ApiRest
{
    public class Startup
    {


        // Constructor que recibe IConfiguration para acceder a la configuración de la aplicación
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // Este método se llama por el tiempo de ejecución. Usa este método para agregar servicios al contenedor.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllers();

            // Configuración de CORS para permitir solicitudes desde la API Flask
            services.AddCors(options =>
            {
                options.AddPolicy("AllowFlask",
                    builder => builder.WithOrigins("http://localhost:5001") // Reemplaza con la URL de tu API Flask
                                      .AllowAnyMethod()
                                      .AllowAnyHeader());
            });
        }

        // Este método se llama por el tiempo de ejecución. Usa este método para configurar el pipeline de solicitudes HTTP.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                // En producción, puedes configurar manejo de errores más robusto aquí
                app.UseExceptionHandler("/Error");
                app.UseHsts();
            }

            app.UseHttpsRedirection();

            // Habilitar CORS para permitir solicitudes desde la API Flask
            app.UseCors("AllowFlask");

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
