from flask import Flask, jsonify, render_template, request ,redirect
import requests
import urllib3

app = Flask(__name__, template_folder='Frontend', static_folder='Frontend/Static/css')

# Deshabilitar advertencias de SSL para urllib3 (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/')
def vista():
    productos_url = 'https://localhost:5000/api/producto'
    region_url = 'https://localhost:5000/api/Region'
    provincia_url = 'https://localhost:5000/api/Provincia'
    comuna_url = 'https://localhost:5000/api/Comuna'
    sucursal_url = 'https://localhost:5000/api/Sucursal'
    stock_url = 'https://localhost:5000/api/Stock'  # NUEVA URL PARA STOCK

    try:
        # Obtener regiones
        response_regiones = requests.get(region_url, verify=False)
        regiones = response_regiones.json() if response_regiones.status_code == 200 else []

        # Obtener provincias
        response_provincias = requests.get(provincia_url, verify=False)
        provincias = response_provincias.json() if response_provincias.status_code == 200 else []

        # Obtener comunas
        response_comunas = requests.get(comuna_url, verify=False)
        comunas = response_comunas.json() if response_comunas.status_code == 200 else []

        # Obtener sucursales
        response_sucursales = requests.get(sucursal_url, verify=False)
        sucursales = response_sucursales.json() if response_sucursales.status_code == 200 else []

        # Obtener productos
        response_productos = requests.get(productos_url, verify=False)
        productos = response_productos.json() if response_productos.status_code == 200 else []

        # Obtener stock
        response_stock = requests.get(stock_url, verify=False)
        stock_data = response_stock.json() if response_stock.status_code == 200 else []

        # Crear un diccionario para asociar el stock con los productos
        stock_dict = {}
        for stock in stock_data:
            cod_producto = stock["codProducto"]
            if cod_producto not in stock_dict:
                stock_dict[cod_producto] = 0
            stock_dict[cod_producto] += stock["cantidad"]  # Sumamos todas las cantidades por producto

        # Añadir la cantidad de stock a cada producto
        for producto in productos:
            producto["stock_disponible"] = stock_dict.get(producto["codProducto"], 0)

        return render_template(
            'index.html',
            productos=productos,
            regiones=regiones,
            provincias=provincias,
            comunas=comunas,
            sucursales=sucursales
        )

    except requests.exceptions.RequestException as e:
        return "Error de conexión: " + str(e)


@app.route('/pago', methods=['GET', 'POST'])
def pago():
    # URLs de las APIs en .NET
    region_url = 'https://localhost:5000/api/Region'
    provincia_url = 'https://localhost:5000/api/Provincia'
    comuna_url = 'https://localhost:5000/api/Comuna'
    transbank_url = 'https://localhost:5000/api/Transbank/Crear_transaccion'
    cliente_url = 'https://localhost:5000/api/Cliente'

    # Obtener datos de regiones, provincias y comunas
    try:
        regiones = requests.get(region_url, verify=False).json()
        provincias = requests.get(provincia_url, verify=False).json()
        comunas = requests.get(comuna_url, verify=False).json()
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}"

    if request.method == 'POST':
        # Capturar datos del formulario
        montoPagar = float(request.form['montoPagar'])
        buy_order = "ORD12345678"
        session_id = "SESSION987654"
        return_url = "http://127.0.0.1:5001/"

        # Datos para Transbank
        datos_transbank = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": montoPagar,
            "return_url": return_url
        }

        # Realizar solicitud POST a Transbank
        try:
            response = requests.post(transbank_url, json=datos_transbank, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get("exito"):
                    urlCompleta = data["data"].get("urlCompleta")
                    
                    if urlCompleta:
                        # Si el pago es exitoso, registrar al cliente
                        datos_cliente = {
                            "numRun": int(request.form['numRun']),
                            "dvRun": request.form['dvRun'],
                            "p_Nombre": request.form['p_Nombre'],
                            "s_Nombre": request.form.get('s_Nombre', ''),
                            "a_Paterno": request.form['a_Paterno'],
                            "a_Materno": request.form['a_Materno'],
                            "correo": request.form['correo'],
                            "direccion": request.form['direccion'],
                            "codRegion": int(request.form['codRegion']),
                            "codProvincia": int(request.form['codProvincia']),
                            "codComuna": int(request.form['codComuna'])
                        }

                        try:
                            response_cliente = requests.post(cliente_url, json=datos_cliente, verify=False)
                            if response_cliente.status_code != 201:
                                return jsonify({"error": "Error al registrar el cliente"}), 500
                        except Exception as e:
                            return jsonify({"error": f"Error en el registro del cliente: {e}"}), 500

                        # Redirigir al usuario a la URL de pago
                        return redirect(urlCompleta)
                    else:
                        return jsonify({"error": "No se encontró la URL de pago"}), 500
                else:
                    return jsonify({"error": data.get("mensaje", "Error en la transacción")}), 500
            else:
                return jsonify({"error": f"Error en la solicitud a Transbank: {response.status_code}"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Si es GET, renderiza el formulario con regiones, provincias y comunas
    return render_template('pago.html', regiones=regiones, provincias=provincias, comunas=comunas)



if __name__ == '__main__':
    app.run(port=5001, debug=True)
