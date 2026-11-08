# Importamos la clase desde nuestro archivo modelo_sensor
from modelo_sensor import LecturaSensor

def ejecutar_pruebas_unitarias():
    # -------------------------------------------------------------
    # Caso 1: Lectura en rango óptimo (5.0 °C)
    # -------------------------------------------------------------
    lectura_optima = LecturaSensor("LOTE-01", 5.0, 85.0)
    
    # assert: Instrucción de Python que comprueba si una condición es verdadera;
    # si es falsa, detiene el programa y lanza un mensaje de error.
    assert lectura_optima.estado_conservacion == "OPTIMO", "Error: Debería resultar OPTIMO"

    # -------------------------------------------------------------
    # Caso 2: Temperatura por encima del límite (9.2 °C)
    # -------------------------------------------------------------
    lectura_calor = LecturaSensor("LOTE-02", 9.2, 80.0)
    assert lectura_calor.estado_conservacion == "ALERTA: RIESGO DE DESCOMPOSICION", "Error en alerta de calor"

    # -------------------------------------------------------------
    # Caso 3: Temperatura por debajo del límite (1.5 °C)
    # -------------------------------------------------------------
    lectura_frio = LecturaSensor("LOTE-03", 1.5, 90.0)
    assert lectura_frio.estado_conservacion == "ALERTA: RIESGO DE CONGELAMIENTO", "Error en alerta de frío"

    # -------------------------------------------------------------
    # Caso 4: Verificación de estructura del diccionario
    # -------------------------------------------------------------
    diccionario_resultado = lectura_optima.convertir_a_diccionario()
    
    # isinstance(): Función de Python que comprueba si una variable pertenece a un tipo de dato específico
    assert isinstance(diccionario_resultado, dict), "Error: El resultado debe ser un diccionario"
    assert "estado" in diccionario_resultado, "Error: Falta la clave 'estado' en el diccionario"

    # print(): Función de Python para mostrar mensajes en la consola
    print("==================================================")
    print(">>> TODAS LAS PRUEBAS UNITARIAS PASARON EXITOSAMENTE (4/4) <<<")
    print("==================================================")

if __name__ == "__main__":
    ejecutar_pruebas_unitarias()