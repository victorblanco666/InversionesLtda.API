from flask import Flask, jsonify, render_template, request 
import requests
import urllib3

app = Flask(__name__, template_folder='Frontend', static_folder='Frontend/Static/css')

# Deshabilitar advertencias de SSL para urllib3 (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/')
def vista():
    productos_url = 'https://ferremasinterfc.azurewebsites.net/api/Producto'
                        
    try:
        response_productos = requests.get(productos_url, verify=False)
        if response_productos.status_code == 200:
            productos = response_productos.json()
        else:
            return "Error al obtener datos de la API de Productos en C#: " + str(response_productos.status_code)

        return render_template('index.html', productos=productos)

    except requests.exceptions.RequestException as e:
        return "Error de conexión: " + str(e)

@app.route('/pago', methods=['GET', 'POST'])
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

            boleta_url = 'https://ferremasinterfc.azurewebsites.net/api/Boleta'
            response = requests.post(boleta_url, json=payload, verify=False)

            if response.status_code == 201: 
                return "Pago realizado exitosamente."
            else:
                return f"Error al realizar el pago: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error de conexión: {str(e)}"

    # Si es un GET, renderiza el template pago.html sin datos de producto estáticos
    return render_template('pago.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
