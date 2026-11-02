import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).resolve().parent / "laboratorio.db"

PRODUCTOS = [
    (1, "Balón de fútbol", 28.50),
    (2, "Camiseta deportiva", 18.00),
    (3, "Guantes de arquero", 24.90),
    (4, "Canilleras", 12.50),
    (5, "Botella deportiva", 9.75),
]


def crear_base_datos():
    conexion = sqlite3.connect(RUTA_BD)

    try:
        with conexion:
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    usuario TEXT NOT NULL UNIQUE,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL
                )
            """)

            conexion.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL CHECK (precio >= 0)
                )
            """)

            # Credenciales ficticias para comparar ambas versiones.
            usuarios = [
                (1, "admin", "Admin123", "administrador"),
                (2, "ronny", "Ronny123", "estudiante"),
                (3, "invitado", "Invitado123", "visitante"),
            ]

            conexion.executemany(
                """
                INSERT OR IGNORE INTO usuarios
                (id, usuario, contrasena, rol)
                VALUES (?, ?, ?, ?)
                """,
                usuarios,
            )

            # Actualiza los productos existentes con ID del 1 al 5.
            conexion.executemany(
                """
                INSERT INTO productos (id, nombre, precio)
                VALUES (?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    nombre = excluded.nombre,
                    precio = excluded.precio
                """,
                PRODUCTOS,
            )

        total_usuarios = conexion.execute(
            "SELECT COUNT(*) FROM usuarios"
        ).fetchone()[0]

        total_productos = conexion.execute(
            "SELECT COUNT(*) FROM productos"
        ).fetchone()[0]

        print("TPE 4 - GRUPO 5")
        print("Base de datos preparada correctamente.")
        print(f"Archivo: {RUTA_BD}")
        print(f"Usuarios registrados: {total_usuarios}")
        print(f"Productos registrados: {total_productos}")
        print("Catálogo deportivo actualizado.")

    finally:
        conexion.close()


if __name__ == "__main__":
    crear_base_datos()