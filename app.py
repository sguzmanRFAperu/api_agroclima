# Importamos las herramientas de Flask
from flask import Flask, request, jsonify
from modelo_sensor import LecturaSensor

# Inicializamos el servidor web de Flask
servidor_web = Flask(__name__)

# Lista en memoria para almacenar las instancias creadas
historial_lecturas = []


# RUTA 1: Consultar lecturas históricas (Método GET)

@servidor_web.route('/telemetria', methods=['GET'])
def consultar_telemetria():
    # Comprensión de lista: recorre cada objeto y lo convierte a diccionario
    lista_en_formato_diccionario = [
        lectura.convertir_a_diccionario() for lectura in historial_lecturas
    ]
    
    # jsonify(): Función de Flask que convierte diccionarios o listas de Python
    # en una respuesta con formato estructurado JSON y cabeceras web HTTP.
    # El número 200 representa el código de estado HTTP: OK (éxito).
    return jsonify(lista_en_formato_diccionario), 200

# RUTA 2: Recibir telemetría desde sensores o clientes (Método POST)

@servidor_web.route('/telemetria', methods=['POST'])
def registrar_telemetria():
    # request.get_json(): Función de Flask que extrae el cuerpo JSON enviado
    # por el cliente y lo transforma en un diccionario manipulable de Python.
    datos_recibidos = request.get_json()

    # Validación defensiva: verificar que el paquete contenga las claves mínimas
    if not datos_recibidos or 'temperatura' not in datos_recibidos or 'humedad' not in datos_recibidos:
        # El número 400 representa el código de estado HTTP: Bad Request (Petición incorrecta)
        return jsonify({
            "error": "Peticion rechazada: Datos incompletos",
            "indicacion": "Los campos 'temperatura' y 'humedad' son estrictamente obligatorios."
        }), 400

    try:
        # get(): Método de diccionarios en Python que obtiene el valor de una clave;
        # si la clave no existe, asigna el valor por defecto que le indiquemos sin provocar error.
        nombre_lote = datos_recibidos.get("lote", "LOTE-GENERAL-01")

        # Instanciamos el objeto utilizando la clase LecturaSensor (POO)
        nueva_lectura = LecturaSensor(
            identificador_lote=nombre_lote,
            valor_temperatura=datos_recibidos["temperatura"],
            valor_humedad=datos_recibidos["humedad"]
        )

        # append(): Método de listas en Python para agregar un nuevo elemento al final de la colección
        historial_lecturas.append(nueva_lectura)

        # El número 201 representa el código de estado HTTP: Created (Recurso creado con éxito)
        return jsonify({
            "mensaje": "Lectura registrada con exito en el sistema",
            "datos_guardados": nueva_lectura.convertir_a_diccionario()
        }), 201

    except (ValueError, TypeError):
        # Captura errores cuando el usuario envía texto en lugar de números
        return jsonify({
            "error": "Formato de datos no valido",
            "indicacion": "Los valores de 'temperatura' y 'humedad' deben ser numeros."
        }), 400


# ENCEDIDO DEL SERVIDOR LOCAL

if __name__ == '__main__':
    # run(): Función de Flask que arranca el servidor web en la máquina local.
    # port=5000: Define el puerto de red por donde escuchará peticiones.
    # debug=True: Permite recargar el servidor automáticamente si editamos el código.
    servidor_web.run(debug=True, port=5000)