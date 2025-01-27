from flask import Flask, jsonify, render_template, request ,redirect , url_for
import requests
import urllib3

app = Flask(__name__, template_folder='Frontend', static_folder='Frontend/Static/css')

# Deshabilitar advertencias de SSL para urllib3 (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/')
def vista():
    productos_url = 'https://localhost:5000/api/producto'
    sucursales_url = 'https://localhost:5000/api/sucursal'
    stock_url = 'https://localhost:5000/api/stock'  # URL para el stock

    try:
        # Obtener productos
        response_productos = requests.get(productos_url, verify=False)
        if response_productos.status_code == 200:
            productos = response_productos.json()
        else:
            return "Error al obtener datos de la API de Productos: " + str(response_productos.status_code)
        
        # Obtener sucursales
        response_sucursales = requests.get(sucursales_url, verify=False)
        if response_sucursales.status_code == 200:
            sucursales = response_sucursales.json()  # Obtenemos la lista de sucursales
        else:
            return "Error al obtener datos de la API de Sucursales: " + str(response_sucursales.status_code)

        # Obtener stock
        response_stock = requests.get(stock_url, verify=False)
        if response_stock.status_code == 200:
            stock = response_stock.json()  # Obtenemos la lista de stock
        else:
            return "Error al obtener datos de la API de Stock: " + str(response_stock.status_code)

        # Pasar productos, sucursales y stock a la plantilla
        return render_template('index.html', productos=productos, sucursales=sucursales, stock=stock)

    except requests.exceptions.RequestException as e:
        return "Error de conexión: " + str(e)
    



@app.route('/pago', methods=['GET', 'POST'])
def pago():
    if request.method == 'POST':
        # Obtener el monto a pagar desde el formulario (viene desde el modal)
        montoPagar = float(request.form['montoPagar'])

        # Valores fijos para buy_order y session_id
        buy_order = "ORD12345678"  # Valor fijo para el número de orden
        session_id = "SESSION987654"  # Valor fijo para el ID de la sesión

        # URL de retorno fija (puedes cambiarla si lo necesitas)
        return_url = "http://127.0.0.1:5001/"  

        # Crear el objeto JSON que se enviará a la API de Transbank
        datos_transbank = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": montoPagar,
            "return_url": return_url
        }

        # Realizar la solicitud POST a la API de Transbank
        try:
            response = requests.post('https://localhost:5000/api/Transbank/Crear_transaccion', json=datos_transbank, verify=False)

            # Verificar la respuesta de la API de Transbank
            if response.status_code == 200:
                data = response.json()
                print("Respuesta de Transbank:", data)

                # Verificar si la respuesta indica éxito
                if data.get("exito"):
                    # Obtener la URL completa desde la respuesta
                    urlCompleta = data["data"].get("urlCompleta")
                    if urlCompleta:
                        # Redirigir al usuario a la URL completa
                        return redirect(urlCompleta)
                    else:
                        return jsonify({"error": "No se encontró la URL completa en la respuesta"}), 500
                else:
                    return jsonify({"error": data.get("mensaje", "Error desconocido al generar la transacción")}), 500
            else:
                return jsonify({"error": f"Error en la solicitud a Transbank: {response.status_code}"}), 500
        except Exception as e:
            print(f"Excepción al hacer la solicitud: {e}")
            return jsonify({"error": str(e)}), 500

    # Si el método es GET, simplemente renderizamos la página
    return render_template('pago.html')



if __name__ == '__main__':
    app.run(port=5001, debug=True)
