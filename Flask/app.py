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

        # Guardamos el carrito en sesión para usarlo al confirmar la transacción
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

        # Guardar datos del cliente en sesión y marcar la sesión como modificada
        session['cliente'] = datos_cliente
        # Marcamos la sesión como modificada para que Flask actualice la cookie
        session.modified = True

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
    # URL de Cliente para reconstruir el cliente si falta en sesión
    cliente_url = f'{base_url}/Cliente'

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

        # Si no encontramos datos de cliente en la sesión, intentamos reconstruirlos
        if not cliente_session:
            usuario_session = session.get('usuario')
            if usuario_session:
                try:
                    resp_clientes = requests.get(cliente_url, verify=False)
                    if resp_clientes.status_code == 200:
                        clientes = resp_clientes.json()
                        cliente_session = next((c for c in clientes if c.get('usuarioId') == usuario_session.get('id')), None)
                        if cliente_session:
                            # Guardamos el cliente reconstruido en sesión
                            session['cliente'] = cliente_session
                            session.modified = True
                except Exception:
                    pass
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
    """
    Página de registro: permite crear simultáneamente una cuenta de usuario y un
    cliente asociado. En el GET se cargan las listas de regiones, provincias y
    comunas para el formulario; en el POST se valida y registra el usuario y
    luego se crea el cliente con el usuarioId resultante.
    """
    base_url = 'https://localhost:5000/api'
    register_url = f'{base_url}/Auth/Register'
    cliente_url = f'{base_url}/Cliente'
    region_url = f'{base_url}/Region'
    provincia_url = f'{base_url}/Provincia'
    comuna_url = f'{base_url}/Comuna'

    error = None
    success = None

    # Para GET: obtener regiones, provincias y comunas para las listas
    try:
        regiones = requests.get(region_url, verify=False).json()
        provincias = requests.get(provincia_url, verify=False).json()
        comunas = requests.get(comuna_url, verify=False).json()
    except Exception as e:
        regiones = []
        provincias = []
        comunas = []
        error = f"Error al cargar datos de territorio: {e}"

    if request.method == 'POST':
        # Datos de la cuenta
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # Datos del cliente
        numRun = request.form.get('numRun')
        dvRun = request.form.get('dvRun')
        p_Nombre = request.form.get('p_Nombre')
        s_Nombre = request.form.get('s_Nombre')
        a_Paterno = request.form.get('a_Paterno')
        a_Materno = request.form.get('a_Materno')
        # Usaremos el mismo correo de la cuenta como correo de contacto
        correo = email
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        codRegion = request.form.get('codRegion')
        codProvincia = request.form.get('codProvincia')
        codComuna = request.form.get('codComuna')

        # Validar contraseñas
        if password != password2:
            error = "Las contraseñas no coinciden."
        else:
            # Registrar usuario
            payload_user = {
                "username": username,
                "email": email,
                "password": password
            }
            try:
                resp_user = requests.post(register_url, json=payload_user, verify=False)
                if resp_user.status_code == 200:
                    data_user = resp_user.json()
                    if data_user.get("exito"):
                        # Usuario creado; obtener usuarioId
                        user_data = data_user.get("data", {})
                        # Según la API, el campo puede llamarse id/Id/usuarioId; usamos el que exista
                        usuario_id = (user_data.get("usuarioId") or
                                      user_data.get("id") or
                                      user_data.get("Id"))
                        # Construir cliente
                        cliente_dto = {
                            "numRun": int(numRun),
                            "dvRun": dvRun,
                            "p_Nombre": p_Nombre,
                            "s_Nombre": s_Nombre,
                            "a_Paterno": a_Paterno,
                            "a_Materno": a_Materno,
                            "correo": correo,
                            "direccion": direccion,
                            "telefono": telefono,
                            "codRegion": int(codRegion) if codRegion else None,
                            "codProvincia": int(codProvincia) if codProvincia else None,
                            "codComuna": int(codComuna) if codComuna else None,
                            "usuarioId": usuario_id
                        }
                        # Registrar cliente
                        try:
                            resp_cliente = requests.post(cliente_url, json=cliente_dto, verify=False)
                            if resp_cliente.status_code in (200, 201):
                                # Cliente creado con éxito
                                success = "Usuario y cliente registrados correctamente. Ahora puedes iniciar sesión."
                            elif resp_cliente.status_code == 409:
                                # Ya existe un cliente con este RUN; hacemos un PUT para asociar el usuarioId
                                try:
                                    resp_put = requests.put(f"{cliente_url}/{int(numRun)}", json=cliente_dto, verify=False)
                                    if resp_put.status_code == 204:
                                        success = "Usuario creado y cliente existente actualizado correctamente. Ahora puedes iniciar sesión."
                                    else:
                                        try:
                                            data_cli = resp_put.json()
                                            error = data_cli.get('mensaje', f"Error al actualizar cliente ({resp_put.status_code}).")
                                        except Exception:
                                            error = f"Error al actualizar cliente ({resp_put.status_code})."
                                except Exception as e:
                                    error = f"Error al actualizar cliente existente: {e}"
                            else:
                                try:
                                    data_cli = resp_cliente.json()
                                    error = data_cli.get('mensaje', f"Error al registrar cliente ({resp_cliente.status_code}).")
                                except Exception:
                                    error = f"Error al registrar cliente ({resp_cliente.status_code})."
                        except Exception as e:
                            error = f"Error al registrar cliente: {e}"
                    else:
                        error = data_user.get("mensaje", "No se pudo registrar el usuario.")
                else:
                    try:
                        data_user = resp_user.json()
                    except Exception:
                        data_user = {}
                    error = data_user.get("mensaje", f"Error al registrar usuario ({resp_user.status_code}).")
            except Exception as e:
                error = f"Error de conexión al registrar: {e}"

    # Renderizar formulario de registro con los datos cargados
    return render_template('signup.html', regiones=regiones, provincias=provincias,
                           comunas=comunas, error=error, success=success)


@app.route('/admin')
@admin_required
def admin_dashboard():
    """
    Vista de administrador: muestra métricas básicas del negocio:
    - total_ventas
    - total_boletas
    - total_clientes
    - total_productos
    - ventas_mensuales (enero a diciembre)
    - clientes_registrados vs clientes_no_registrados
    - productos más vendidos (labels_productos, cantidades_productos)
    """
    base_url = 'https://localhost:5000/api'
    boleta_url = f'{base_url}/Boleta'
    cliente_url = f'{base_url}/Cliente'
    producto_url = f'{base_url}/Producto'

    total_ventas = 0
    total_boletas = 0
    total_clientes = 0
    total_productos = 0

    # Ventas por mes (enero a diciembre)
    ventas_mensuales = [0] * 12

    # Clientes registrados vs no registrados
    clientes_registrados = 0
    clientes_no_registrados = 0

    # Productos más vendidos (por cantidad)
    ventas_por_producto = {}  # { codProducto: cantidad_total }

    try:
        boletas = requests.get(boleta_url, verify=False).json()
        clientes = requests.get(cliente_url, verify=False).json()
        productos = requests.get(producto_url, verify=False).json()

        # Totales simples
        total_boletas = len(boletas)
        total_clientes = len(clientes)
        total_productos = len(productos)

        # ================================
        # 1) CLIENTES REGISTRADOS / NO
        # ================================
        for c in clientes:
            usuario_id = c.get("usuarioId")
            if usuario_id is None:
                clientes_no_registrados += 1
            else:
                clientes_registrados += 1

        # ================================
        # 2) VENTAS TOTALES Y POR MES
        #    + ACUMULAR CANTIDAD POR PRODUCTO
        # ================================
        for b in boletas:
            monto = int(b.get("total", 0) or 0)
            total_ventas += monto

            # Fecha de la boleta
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

            # Detalles de la boleta: acumular cantidades por producto
            # Ajusta la clave "detalles" si en tu API viene con otro nombre
            detalles = b.get("detalles", [])
            if detalles:
                for d in detalles:
                    cod_producto = d.get("codProducto")
                    cantidad = int(d.get("cantidad", 0) or 0)
                    if cod_producto is not None:
                        ventas_por_producto[cod_producto] = ventas_por_producto.get(cod_producto, 0) + cantidad

        # ================================
        # 3) ARMAR LISTAS PARA GRÁFICO DE PRODUCTOS
        # ================================
        # Mapa para encontrar nombre del producto por código
        map_productos = {}
        for p in productos:
            cod = p.get("codProducto")
            # Ajusta el nombre según tu API: "nombreProducto", "nombre", etc.
            nombre = p.get("nombreProducto") or p.get("nombre") or f"Producto {cod}"
            if cod is not None:
                map_productos[cod] = nombre

        # Ordenar productos por cantidad vendida (descendiente)
        productos_ordenados = sorted(
            ventas_por_producto.items(),
            key=lambda x: x[1],
            reverse=True
        )

        labels_productos = []
        cantidades_productos = []

        # Si quieres solo el TOP 5, usa [:5]; si quieres todos, quita el slice
        for cod_producto, cantidad_total in productos_ordenados[:5]:
            nombre = map_productos.get(cod_producto, f"Producto {cod_producto}")
            labels_productos.append(nombre)
            cantidades_productos.append(cantidad_total)
        
        boletas_listado = boletas  # o boletas[-20:] si quieres limitar a las últimas
        # Renderizar plantilla
        return render_template(
            'admin_dashboard.html',
            total_boletas=total_boletas,
            total_clientes=total_clientes,
            total_productos=total_productos,
            total_ventas=total_ventas,
            ventas_mensuales=ventas_mensuales,
            clientes_registrados=clientes_registrados,
            clientes_no_registrados=clientes_no_registrados,
            labels_productos=labels_productos,
            cantidades_productos=cantidades_productos,
            boletas=boletas_listado
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
            "telefono": request.form.get('telefono', cliente.get('telefono')),
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

    return render_template(
        'perfil.html',
        cliente=cliente,
        boletas=mis_boletas,
        error=error,
        success=success
    )


if __name__ == '__main__':
    app.run(port=5001, debug=True)