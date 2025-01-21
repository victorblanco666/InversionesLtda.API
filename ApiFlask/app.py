from flask import Flask, jsonify, render_template, request ,redirect
import requests
import urllib3

app = Flask(__name__, template_folder='Frontend', static_folder='Frontend/Static/css')

# Deshabilitar advertencias de SSL para urllib3 (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/')
def vista():
    productos_url = 'https://localhost:5000/api/producto'

    try:
        response_productos = requests.get(productos_url, verify=False)
        if response_productos.status_code == 200:
            productos = response_productos.json()
        else:
            return "Error al obtener datos de la API de Productos en C#: " + str(response_productos.status_code)

        return render_template('index.html', productos=productos)

    except requests.exceptions.RequestException as e:
        return "Error de conexión: " + str(e)

"""@app.route('/pago', methods=['GET', 'POST'])
def pago():
    if request.method == 'POST':
        try:
            nombreCliente = request.form.get('nombreCliente')
            emailCliente = request.form.get('emailCliente')
            telefonoCliente = request.form.get('telefonoCliente')
            total = request.form.get('montoPagar')
            productoId = request.form.get('productoId')

            payload = {
                "total": total,
                "cliente": {
                    "nombreCliente": nombreCliente,
                    "email": emailCliente,
                    "telefono": telefonoCliente
                },
                "productoId": productoId
            }

            boleta_url = 'https://localhost:5000/api/boleta'
            response = requests.post(boleta_url, json=payload, verify=False)

            if response.status_code == 201:
                return "Pago realizado exitosamente."
            else:
                return f"Error al realizar el pago: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error de conexión: {str(e)}"

    # Si es un GET, renderiza el template pago.html sin datos de producto estáticos
    return render_template('pago.html')"""

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
