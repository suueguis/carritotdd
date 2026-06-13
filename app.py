# app.py
import os
import psycopg2
from flask import Flask, request, jsonify
from carrito import Carrito

app = Flask(__name__)


def obtener_conexion():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "carrito_db"),
        user=os.environ.get("DB_USER", "carrito_user"),
        password=os.environ.get("DB_PASSWORD", "carrito_pass"),
    )


def inicializar_base_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            cantidad INTEGER NOT NULL,
            precio NUMERIC(10, 2) NOT NULL
        )
    """)
    conexion.commit()
    cursor.close()
    conexion.close()


def cargar_carrito_desde_bd():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, cantidad, precio FROM productos ORDER BY id")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()

    carrito = Carrito()
    for fila in filas:
        carrito.agregar_producto(fila[0], fila[1], float(fila[2]))
    return carrito


@app.route("/")
def inicio():
    return jsonify({"mensaje": "API del carrito de compras en funcionamiento"})


@app.route("/productos", methods=["GET"])
def listar_productos():
    carrito = cargar_carrito_desde_bd()
    return jsonify(carrito.productos)


@app.route("/productos", methods=["POST"])
def agregar_producto():
    datos = request.get_json()
    nombre = datos["nombre"]
    cantidad = datos["cantidad"]
    precio = datos["precio"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
        (nombre, cantidad, precio),
    )
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "Producto agregado", "nombre": nombre}), 201


@app.route("/productos/<nombre>", methods=["DELETE"])
def eliminar_producto(nombre):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE nombre = %s", (nombre,))
    eliminados = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()

    if eliminados == 0:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
    return jsonify({"mensaje": "Producto eliminado", "nombre": nombre})


@app.route("/total", methods=["GET"])
def calcular_total():
    carrito = cargar_carrito_desde_bd()
    return jsonify({"total": carrito.calcular_total()})


# Endpoint agregado en la Parte 5: total del carrito aplicando un descuento
@app.route("/total/descuento/<int:porcentaje>", methods=["GET"])
def total_con_descuento(porcentaje):
    carrito = cargar_carrito_desde_bd()
    try:
        total = carrito.aplicar_descuento(porcentaje)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"porcentaje": porcentaje, "total_con_descuento": total})


if __name__ == "__main__":
    inicializar_base_datos()
    app.run(host="0.0.0.0", port=5000)
