from flask import Flask, jsonify, render_template, request 
import requests
import urllib3

app = Flask(__name__, template_folder='Frontend' , static_folder='Frontend/Static/css')

# Deshabilitar advertencias de SSL para urllib3 (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Endpoint para obtener clientes y productos desde la API en C#
@app.route('/')
def vista():
    # URLs de la API en C# para clientes, productos y boletas
    
    productos_url = 'https://localhost:5000/api/producto'
   

    try:
        # Realizar solicitud GET a la API en C# para clientes
        
        response_productos = requests.get(productos_url, verify=False)
        

        # Verificar si la solicitud de clientes fue exitosa
       

        # Verificar si la solicitud de productos fue exitosa
        if response_productos.status_code == 200:
            productos = response_productos.json()
        else:
            return "Error al obtener datos de la API de Productos en C#: " + str(response_productos.status_code)

        # Verificar si la solicitud de boletas fue exitosa
       

        # Renderizar template index.html con clientes, productos y boletas
        return render_template('index.html', productos=productos,)

    except requests.exceptions.RequestException as e:
        return "Error de conexión: " + str(e)
    
# Ejemplo de datos del producto que quieres mostrar en detalleCompra
producto = {
    'id': 1,
    'nombre': 'Sierra Circular',
    'cantidad': 1,
    'precio': 70000
}

@app.route('/pago', methods=['GET', 'POST'])
def pago():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombreCliente = request.form.get('nombreCliente')
            emailCliente = request.form.get('emailCliente')
            telefonoCliente = request.form.get('telefonoCliente')
            total = request.form.get('montoPagar')  # Cambiado de 'total' a 'montoPagar'
            productoId = request.form.get('productoId')

            # Crear el payload para enviar a la API de Boleta
            payload = {
                "total": total,
                "cliente": {
                    "nombreCliente": nombreCliente,
                    "email": emailCliente,
                    "telefono": telefonoCliente
                },
                "productoId": productoId
            }

            # Realizar solicitud POST a la API de Boleta
            boleta_url = 'https://localhost:5000/api/boleta'
            response = requests.post(boleta_url, json=payload, verify=False)

            # Verificar si la solicitud fue exitosa
            if response.status_code == 201:
                return "Pago realizado exitosamente."
            else:
                return f"Error al realizar el pago: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error de conexión: {str(e)}"

    # Si es un GET, renderiza el template pago.html pasando los detalles del producto
    return render_template('pago.html', producto=producto)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
