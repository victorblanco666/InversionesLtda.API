from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import requests
import urllib3
import string
import random
import json
from datetime import datetime
from functools import wraps

# Flask config
app = Flask(__name__, template_folder='Frontend', static_folder='Frontend/Static/css')

# Clave para usar sesiones (SOLO DESARROLLO, cámbiala en producción)
app.secret_key = "dev-unishop-secret-key"

# Deshabilitar advertencias de SSL para urllib3 (solo para desarrollo)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        usuario = session.get('usuario')
        roles = usuario.get('roles', []) if usuario else []
        if 'Admin' not in roles:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def vista():
    base_url = 'https://localhost:5000/api'
    productos_url = f'{base_url}/Producto'
    region_url = f'{base_url}/Region'
    provincia_url = f'{base_url}/Provincia'
    comuna_url = f'{base_url}/Comuna'
    sucursal_url = f'{base_url}/Sucursal'
    stock_url = f'{base_url}/Stock'

    try:
        # Obtener regiones, provincias, comunas y sucursales
        regiones = requests.get(region_url, verify=False).json()
        provincias = requests.get(provincia_url, verify=False).json()
        comunas = requests.get(comuna_url, verify=False).json()
        sucursales = requests.get(sucursal_url, verify=False).json()
        productos = requests.get(productos_url, verify=False).json()

        # Obtener stock y agrupar por producto
        stock_data = requests.get(stock_url, verify=False).json()
        stock_dict = {}
        for stock in stock_data:
            cod_producto = stock["codProducto"]
            stock_dict[cod_producto] = stock_dict.get(cod_producto, 0) + stock["cantidad"]

        # Asignar stock a cada producto
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
    base_url = 'https://localhost:5000/api'
    transbank_url = f'{base_url}/Transbank/Crear_transaccion'
    cliente_url = f'{base_url}/Cliente'
    region_url = f'{base_url}/Region'
    provincia_url = f'{base_url}/Provincia'
    comuna_url = f'{base_url}/Comuna'

    def generar_codigo(prefijo, longitud=8):
        return f"{prefijo}{''.join(random.choices(string.digits, k=longitud))}"

    # Cargar datos de región/provincia/comuna para el formulario
    try:
        regiones = requests.get(region_url, verify=False).json()
        provincias = requests.get(provincia_url, verify=False).json()
        comunas = requests.get(comuna_url, verify=False).json()
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}"

    if request.method == 'POST':
        # Carrito recibido desde el formulario
        carrito_json = request.form.get('carrito_json', '[]')
        try:
            carrito = json.loads(carrito_json)
        except json.JSONDecodeError:
            carrito = []

        if not carrito:
            return jsonify({"error": "El carrito está vacío o no se pudo leer."}), 400

        session['carrito'] = carrito

        # Monto total a pagar (calculado en el frontend)
        monto_pagar = float(request.form['montoPagar'])

        buy_order = generar_codigo("ORD", 8)
        session_id = generar_codigo("SESSION", 10)
        return_url = "http://127.0.0.1:5001/confirmar_pago"

        # Datos del cliente desde el formulario
        datos_cliente = {
            "numRun": int(request.form['numRun']),
            "dvRun": request.form['dvRun'],
            "p_Nombre": request.form['p_Nombre'],
            "s_Nombre": request.form.get('s_Nombre', ''),
            "a_Paterno": request.form['a_Paterno'],
            "a_Materno": request.form['a_Materno'],
            "correo": request.form['correo'],
            "direccion": request.form['direccion'],
            "telefono": request.form['telefono'],  
            "codRegion": int(request.form['codRegion']),
            "codProvincia": int(request.form['codProvincia']),
            "codComuna": int(request.form['codComuna'])
        }

        # Si el usuario está autenticado, asociamos el cliente con su UsuarioId
        usuario_session = session.get('usuario')
        if usuario_session:
            datos_cliente["usuarioId"] = usuario_session.get("id")

        # Guardar datos del cliente en sesión
        session['cliente'] = datos_cliente

        try:
            # Registrar o actualizar cliente
            resp_cliente = requests.post(cliente_url, json=datos_cliente, verify=False)
            if resp_cliente.status_code not in (200, 201, 409):
                return jsonify({"error": "Error al registrar el cliente"}), 500
        except Exception as e:
            return jsonify({"error": f"Error en el registro del cliente: {e}"}), 500

        # Iniciar transacción con Transbank
        datos_transbank = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": monto_pagar,
            "return_url": return_url
        }

        try:
            resp_tbk = requests.post(transbank_url, json=datos_transbank, verify=False)
            if resp_tbk.status_code == 200:
                data = resp_tbk.json()
                if data.get("exito"):
                    url_completa = data["data"].get("urlCompleta")
                    if url_completa:
                        return redirect(url_completa)
                    else:
                        return jsonify({"error": "No se encontró la URL de pago"}), 500
                else:
                    return jsonify({"error": data.get("mensaje", "Error en la transacción")}), 500
            else:
                return jsonify({"error": f"Error en la solicitud a Transbank: {resp_tbk.status_code}"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template('pago.html', regiones=regiones, provincias=provincias, comunas=comunas)

@app.route('/confirmar_pago', methods=['GET'])
def recibir_token():
    """Recibe el token de Transbank después del pago y redirige a la confirmación."""
    token = request.args.get('token_ws')
    if not token:
        return jsonify({"error": "No se recibió token de transacción"}), 400
    return redirect(f"/confirmar_transaccion/{token}")

@app.route('/confirmar_transaccion/<token>', methods=['GET'])
def confirmar_transaccion(token):
    base_url = 'https://localhost:5000/api'
    confirmacion_url = f'{base_url}/Transbank/Confirmar_transaccion/{token}'
    tarjeta_url = f'{base_url}/Tarjeta'
    boleta_url = f'{base_url}/Boleta'

    try:
        # 1. Confirmar la transacción con TransbankController
        resp = requests.get(confirmacion_url, verify=False)
        if resp.status_code != 200:
            return jsonify({"error": f"Error al confirmar la transacción: {resp.status_code}"}), 500

        data = resp.json()
        if not data.get("exito"):
            return jsonify({"error": data.get("mensaje", "Error al confirmar la transacción")}), 500

        detalles_transaccion = data.get("data", {})
        cod_transaccion = str(detalles_transaccion.get("buyOrder"))
        card_number = detalles_transaccion.get("cardDetail", {}).get("cardNumber")

        if not cod_transaccion or not card_number:
            return jsonify({"error": "No se pudo obtener la información de la transacción"}), 500

        cod_tarjeta = int(card_number)

        # 2. Verificar si la transacción ya está registrada en Tarjeta
        resp_verificar = requests.get(f"{tarjeta_url}/{cod_transaccion}", verify=False)
        if resp_verificar.status_code != 200:
            # 3. Registrar la transacción si no existe
            datos_tarjeta = {
                "codTransaccion": cod_transaccion,
                "numTarjeta": cod_tarjeta,
                "nombreTransaccion": "Compra Online",
                "token": token
            }
            resp_tarjeta = requests.post(tarjeta_url, json=datos_tarjeta, verify=False)
            if resp_tarjeta.status_code not in (200, 201):
                print(f"⚠️ Error al registrar la transacción: {resp_tarjeta.status_code}")
                print(f"🔍 Respuesta del servidor: {resp_tarjeta.text}")

        # 4. Crear la Boleta en la API
        cliente_session = session.get('cliente')
        carrito = session.get('carrito', [])

        if not cliente_session:
            return jsonify({"error": "No se encontraron datos de cliente en sesión. No se puede emitir la boleta."}), 400
        if not carrito:
            return jsonify({"error": "No se encontró el carrito en sesión. No se puede emitir la boleta."}), 400

        num_run = cliente_session.get("numRun")
        dv_run = cliente_session.get("dvRun")
        correo = cliente_session.get("correo")
        if not num_run or not dv_run:
            return jsonify({"error": "Datos de RUN del cliente incompletos."}), 400

        cod_sucursal = carrito[0].get('codSucursal', 1)

        detalles = []
        for item in carrito:
            detalles.append({
                "codProducto": item["codProducto"],
                "cantidad": item["cantidad"]
            })

        # Definir si la compra es invitada según si existe usuario en sesión
        es_invitada = True
        if session.get('usuario'):
            es_invitada = False

        datos_boleta = {
            "numRun": num_run,
            "dvRun": dv_run,
            "correoContacto": correo,
            "esInvitada": es_invitada,
            "codSucursal": cod_sucursal,
            "codTransaccion": cod_transaccion,
            "detalles": detalles
        }

        resp_boleta = requests.post(boleta_url, json=datos_boleta, verify=False)
        if resp_boleta.status_code not in (200, 201):
            print(f"⚠️ Error al crear la boleta: {resp_boleta.status_code}")
            print(f"🔍 Respuesta del servidor: {resp_boleta.text}")
        else:
            print("✅ Boleta creada correctamente en la API.")

        # 5. Mostrar la confirmación
        return render_template('transaccion_confirmada.html', detalles=detalles_transaccion)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    base_url = 'https://localhost:5000/api'
    login_url = f'{base_url}/Auth/Login'
    error = None

    if request.method == 'POST':
        username_or_email = request.form.get('usernameOrEmail')
        password = request.form.get('password')

        payload = {
            "usernameOrEmail": username_or_email,
            "password": password
        }

        try:
            resp = requests.post(login_url, json=payload, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("exito"):
                    user_data = data.get("data", {})
                    session['usuario'] = {
                        "id": user_data.get("usuarioId"),
                        "username": user_data.get("username"),
                        "email": user_data.get("email"),
                        "roles": user_data.get("roles", [])
                    }

                    if "Admin" in session['usuario']["roles"]:
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('vista'))
                else:
                    error = data.get("mensaje", "Credenciales incorrectas.")
            else:
                error = f"Error en el servidor de autenticación ({resp.status_code})."
        except Exception as e:
            error = f"Error de conexión al autenticar: {e}"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('vista'))

@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    base_url = 'https://localhost:5000/api'
    reset_url = f'{base_url}/Auth/ResetPassword'
    error = None
    success = None

    if request.method == 'POST':
        username_or_email = request.form.get('usernameOrEmail')
        new_password = request.form.get('newPassword')
        new_password2 = request.form.get('newPassword2')

        if new_password != new_password2:
            error = "Las contraseñas no coinciden."
        else:
            payload = {
                "usernameOrEmail": username_or_email,
                "newPassword": new_password
            }
            try:
                resp = requests.post(reset_url, json=payload, verify=False)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("exito"):
                        success = "Contraseña actualizada correctamente. Ahora puedes iniciar sesión."
                    else:
                        error = data.get("mensaje", "No se pudo actualizar la contraseña.")
                else:
                    try:
                        data = resp.json()
                    except Exception:
                        data = {}
                    error = data.get("mensaje", f"Error al actualizar contraseña ({resp.status_code}).")
            except Exception as e:
                error = f"Error de conexión al actualizar contraseña: {e}"

    return render_template('password_reset.html', error=error, success=success)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    base_url = 'https://localhost:5000/api'
    register_url = f'{base_url}/Auth/Register'
    error = None
    success = None

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            error = "Las contraseñas no coinciden."
        else:
            payload = {
                "username": username,
                "email": email,
                "password": password
            }
            try:
                resp = requests.post(register_url, json=payload, verify=False)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("exito"):
                        success = "Usuario registrado correctamente. Ahora puedes iniciar sesión."
                    else:
                        error = data.get("mensaje", "No se pudo registrar el usuario.")
                else:
                    try:
                        data = resp.json()
                    except Exception:
                        data = {}
                    error = data.get("mensaje", f"Error al registrar usuario ({resp.status_code}).")
            except Exception as e:
                error = f"Error de conexión al registrar: {e}"

    return render_template('signup.html', error=error, success=success)

@app.route('/admin')
@admin_required
def admin_dashboard():

    
    """
    Vista de administrador: muestra métricas básicas del negocio
    + arreglo ventas_mensuales (enero a diciembre).
    """
    base_url = 'https://localhost:5000/api'
    boleta_url = f'{base_url}/Boleta'
    cliente_url = f'{base_url}/Cliente'
    producto_url = f'{base_url}/Producto'

    total_ventas = 0
    total_boletas = 0
    total_clientes = 0
    total_productos = 0

    ventas_mensuales = [0] * 12

    try:
        boletas = requests.get(boleta_url, verify=False).json()
        clientes = requests.get(cliente_url, verify=False).json()
        productos = requests.get(producto_url, verify=False).json()

        total_boletas = len(boletas)
        total_clientes = len(clientes)
        total_productos = len(productos)

        for b in boletas:
            monto = int(b.get("total", 0) or 0)
            total_ventas += monto

            fecha_str = (
                b.get("fechaBoleta")
                or b.get("fechaEmision")
                or b.get("fecha")
            )

            if fecha_str:
                try:
                    fecha_clean = str(fecha_str).replace('Z', '')
                    if '.' in fecha_clean:
                        fecha_part, frac = fecha_clean.split('.', 1)
                        frac = frac[:6]
                        fecha_clean = f"{fecha_part}.{frac}"
                    fecha = datetime.fromisoformat(fecha_clean)
                    mes_idx = fecha.month - 1
                    if 0 <= mes_idx < 12:
                        ventas_mensuales[mes_idx] += monto
                except Exception as e:
                    print(f"Error parseando fecha de boleta ({fecha_str}): {e}")

        return render_template(
            'admin_dashboard.html',
            total_boletas=total_boletas,
            total_clientes=total_clientes,
            total_productos=total_productos,
            total_ventas=total_ventas,
            ventas_mensuales=ventas_mensuales
        )

    except requests.exceptions.RequestException as e:
        return f"Error de conexión al cargar panel admin: {e}"

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    """
    Muestra el perfil del usuario logeado. Permite ver y actualizar datos personales
    y listar las compras del cliente (boletas).
    """
    base_url = 'https://localhost:5000/api'
    cliente_url = f'{base_url}/Cliente'
    boleta_url = f'{base_url}/Boleta'

    # Usuario autenticado
    usuario_session = session.get('usuario')
    if not usuario_session:
        return redirect(url_for('login'))

    # Buscar el cliente asociado al usuario mediante su UsuarioId
    try:
        resp_clientes = requests.get(cliente_url, verify=False)
        clientes = resp_clientes.json() if resp_clientes.status_code == 200 else []
        cliente = next((c for c in clientes if c.get('usuarioId') == usuario_session.get('id')), None)
    except Exception as e:
        return f"Error al cargar datos del cliente: {e}", 500

    if not cliente:
        return "No se encontró un cliente asociado a este usuario.", 404

    error = None
    success = None

    if request.method == 'POST':
        # Leer datos enviados desde el formulario
        updated_cliente = {
            "numRun": cliente['numRun'],
            "dvRun": request.form.get('dvRun', cliente.get('dvRun')),
            "p_Nombre": request.form.get('p_Nombre', cliente.get('p_Nombre')),
            "s_Nombre": request.form.get('s_Nombre', cliente.get('s_Nombre')),
            "a_Paterno": request.form.get('a_Paterno', cliente.get('a_Paterno')),
            "a_Materno": request.form.get('a_Materno', cliente.get('a_Materno')),
            "correo": request.form.get('correo', cliente.get('correo')),
            "direccion": request.form.get('direccion', cliente.get('direccion')),
            "codRegion": cliente.get('codRegion'),
            "codProvincia": cliente.get('codProvincia'),
            "codComuna": cliente.get('codComuna'),
            "usuarioId": usuario_session.get('id')
        }
        try:
            # Actualizar cliente mediante PUT
            resp_put = requests.put(f"{cliente_url}/{cliente['numRun']}", json=updated_cliente, verify=False)
            if resp_put.status_code == 204:
                success = "Datos actualizados correctamente."
                cliente = updated_cliente  # Actualizamos los datos locales
            else:
                # Intentamos extraer mensaje de error
                try:
                    data_err = resp_put.json()
                    error = data_err.get('mensaje', f"Error al actualizar datos ({resp_put.status_code}).")
                except Exception:
                    error = f"Error al actualizar datos ({resp_put.status_code})."
        except Exception as e:
            error = f"Error al actualizar datos: {e}"

    # Obtener todas las boletas y filtrar por el cliente actual
    try:
        resp_boletas = requests.get(boleta_url, verify=False)
        boletas_all = resp_boletas.json() if resp_boletas.status_code == 200 else []
        mis_boletas = [b for b in boletas_all if b.get('runCliente') == cliente['numRun']]
    except Exception as e:
        mis_boletas = []
        error = f"Error al cargar boletas: {e}"

    # Renderizar plantilla de perfil
    return render_template(
        'perfil.html',
        cliente=cliente,
        boletas=mis_boletas,
        error=error,
        success=success
    )



if __name__ == '__main__':
    app.run(port=5001, debug=True)
