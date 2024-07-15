from flask import Flask, render_template, jsonify, redirect, url_for
import requests
import urllib3

app = Flask(__name__, static_folder="Frontend/Static", template_folder='Frontend')

# Deshabilitar advertencias de SSL para urllib3 (solo para desarrollo)
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Endpoint para obtener clientes y productos desde la API en C#
@app.route('/')
def vista():
    # URL de la API en C# para los clientes y productos
    clientes_url = 'https://localhost:5000/api/cliente'
    productos_url = 'https://localhost:5000/api/producto'   

    try:
        # Realizar solicitud GET a la API en C# para clientes
        response_clientes = requests.get(clientes_url, verify=False)  # Deshabilitar verificación SSL (solo para desarrollo)

        # Verificar si la solicitud de clientes fue exitosa
        if response_clientes.status_code == 200:
            clientes = response_clientes.json()  # Convertir respuesta a JSON
        else:
            return "Error al obtener datos de la API de Clientes en C#: " + str(response_clientes.status_code)

        # Realizar solicitud GET a la API en C# para productos
        response_productos = requests.get(productos_url, verify=False)  # Deshabilitar verificación SSL (solo para desarrollo)

        # Verificar si la solicitud de productos fue exitosa
        if response_productos.status_code == 200:
            productos = response_productos.json()  # Convertir respuesta a JSON
        else:
            return "Error al obtener datos de la API de Productos en C#: " + str(response_productos.status_code)

        # Renderizar template index.html con clientes y productos
        return render_template('index.html', clientes=clientes, productos=productos)

    except requests.exceptions.RequestException as e:
        return "Error de conexión: " + str(e)

@app.route('/pagar')
def pagar():
    # Renderizar la página de pago
    return render_template('pagar.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
