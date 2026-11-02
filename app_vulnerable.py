import sqlite3
from pathlib import Path
from flask import Flask, request, render_template

app = Flask(__name__)

RUTA_BD = Path(__file__).resolve().parent / "laboratorio.db"


def mostrar(
    mensaje="",
    consulta="",
    columnas=None,
    filas=None,
    termino="",
    estado=200,
    tipo="info",
    busqueda=False,
):
    return render_template(
        "laboratorio.html",
        corregida=False,
        mensaje=mensaje,
        consulta=consulta,
        columnas=columnas or [],
        filas=filas or [],
        termino=termino,
        tipo=tipo,
        busqueda=busqueda,
    ), estado


def consultar(consulta):
    conexion = sqlite3.connect(
        RUTA_BD.as_uri() + "?mode=ro",
        uri=True,
    )

    try:
        return conexion.execute(consulta).fetchall()
    finally:
        conexion.close()


@app.route("/")
def inicio():
    return mostrar()


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "")
    contrasena = request.form.get("contrasena", "")

    # Vulnerabilidad intencional del laboratorio:
    # las entradas se incorporan directamente al SQL.
    consulta = (
        "SELECT id, usuario, rol FROM usuarios "
        f"WHERE usuario = '{usuario}' "
        f"AND contrasena = '{contrasena}'"
    )

    try:
        filas = consultar(consulta)

    except sqlite3.Error:
        app.logger.exception("Error SQL en inicio de sesión")

        return mostrar(
            mensaje="Error al procesar la consulta SQL.",
            consulta=consulta,
            estado=400,
            tipo="error",
        )

    if filas:
        return mostrar(
            mensaje=f"Acceso concedido. Bienvenido, {filas[0][1]}.",
            consulta=consulta,
            columnas=["ID", "Usuario", "Rol"],
            filas=filas,
            tipo="exito",
        )

    return mostrar(
        mensaje="Acceso denegado. Credenciales incorrectas.",
        consulta=consulta,
        estado=401,
        tipo="error",
    )


@app.route("/buscar")
def buscar():
    nombre = request.args.get("nombre", "")

    # Vulnerabilidad intencional por concatenación.
    consulta = (
        "SELECT id, nombre, precio FROM productos "
        f"WHERE nombre LIKE '%{nombre}%'"
    )

    try:
        filas = consultar(consulta)

    except sqlite3.Error:
        app.logger.exception("Error SQL en búsqueda")

        return mostrar(
            mensaje="Error al procesar la consulta SQL.",
            consulta=consulta,
            termino=nombre,
            estado=400,
            tipo="error",
        )

    return mostrar(
        mensaje=f"Registros encontrados: {len(filas)}",
        consulta=consulta,
        columnas=["ID", "Producto", "Precio (USD)"],
        filas=filas,
        termino=nombre,
        busqueda=True,
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )