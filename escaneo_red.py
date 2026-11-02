import socket

HOST = "127.0.0.1"

PUERTOS = [80, 443, 5000, 8000, 8080]


def escanear():
    print("TPE 4 - GRUPO 5")
    print("ESCANEO BÁSICO DE PUERTOS TCP")
    print(f"Equipo: {HOST}")
    print()

    abiertos = 0

    for puerto in PUERTOS:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        ) as conexion:

            conexion.settimeout(1)

            try:
                resultado = conexion.connect_ex(
                    (HOST, puerto)
                )

                if resultado == 0:
                    estado = "ABIERTO"
                    abiertos += 1

                else:
                    estado = "SIN CONEXIÓN"

                print(f"Puerto {puerto}: {estado}")

            except OSError as error:
                print(
                    f"Puerto {puerto}: "
                    f"error de conexión ({error})"
                )

    print()
    print(f"Puertos abiertos encontrados: {abiertos}")
    print("Escaneo finalizado.")
    print("Solo se examinan cinco puertos de esta computadora.")


if __name__ == "__main__":
    escanear()