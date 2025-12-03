// admin_dashboard.js

document.addEventListener('DOMContentLoaded', function () {
    // ==========================================================
    // LEER DATOS DESDE EL <script type="application/json">
    // ==========================================================
    const dataScript = document.getElementById('dashboard-data');
    if (!dataScript) {
        console.error('No se encontró el script con id "dashboard-data"');
        return;
    }

    let data;
    try {
        data = JSON.parse(dataScript.textContent);
    } catch (e) {
        console.error('Error parseando JSON de dashboard-data:', e);
        return;
    }

    const ventasMensuales      = data.ventas_mensuales || [];
    const clientesRegistrados  = data.clientes_registrados || 0;
    const clientesNoRegistrados = data.clientes_no_registrados || 0;
    const labelsProductos      = data.labels_productos || [];
    const cantidadesProductos  = data.cantidades_productos || [];

    // ==========================================================
    // GESTIÓN DE CONTENEDORES
    // ==========================================================
    function ocultarTodos() {
        const ids = ["containerVentas", "containerClientes", "containerProductos"];
        ids.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.style.display = "none";
            }
        });
    }

    function toggleContainer(id) {
        const box = document.getElementById(id);
        if (!box) return;

        const visible = box.style.display === "block";
        ocultarTodos();
        box.style.display = visible ? "none" : "block";
    }

    // ==========================================================
    // GRÁFICO 1: VENTAS
    // ==========================================================
    let chartVentas = null;

    function initChartVentas() {
        const canvas = document.getElementById('ventasMensualesChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        chartVentas = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
                datasets: [{
                    label: 'Total ventas por mes',
                    data: ventasMensuales,
                    borderWidth: 1
                }]
            },
            options: { responsive: true }
        });
    }

    // ==========================================================
    // GRÁFICO 2: CLIENTES
    // ==========================================================
    let chartClientes = null;

    function initChartClientes() {
        const canvas = document.getElementById('chartClientes');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        chartClientes = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Registrados', 'No registrados'],
                datasets: [{
                    data: [clientesRegistrados, clientesNoRegistrados]
                }]
            }
        });
    }

    // ==========================================================
    // GRÁFICO 3: PRODUCTOS
    // ==========================================================
    let chartProductos = null;

    function initChartProductos() {
        const canvas = document.getElementById('chartProductos');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        chartProductos = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labelsProductos,
                datasets: [{
                    data: cantidadesProductos
                }]
            }
        });
    }

    // ==========================================================
    // EVENTOS CLICK EN CARDS
    // ==========================================================
    const cardTotalVentas = document.getElementById("cardTotalVentas");
    const cardClientes    = document.getElementById("cardClientes");
    const cardProductos   = document.getElementById("cardProductos");

    if (cardTotalVentas) {
        cardTotalVentas.onclick = function () {
            if (!chartVentas) initChartVentas();
            toggleContainer("containerVentas");
        };
    }

    if (cardClientes) {
        cardClientes.onclick = function () {
            if (!chartClientes) initChartClientes();
            toggleContainer("containerClientes");
        };
    }

    if (cardProductos) {
        cardProductos.onclick = function () {
            if (!chartProductos) initChartProductos();
            toggleContainer("containerProductos");
        };
    }
});
