import re
from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "http://127.0.0.1:5000"


class TextoHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.partes = []

    def handle_data(self, data):
        self.partes.append(data)


def enviar(ruta, datos=None, metodo="GET"):
    codificado = urlencode(datos or {})
    url = BASE_URL + ruta
    cuerpo = None

    if metodo == "POST":
        cuerpo = codificado.encode("utf-8")

    elif codificado:
        url += "?" + codificado

    solicitud = Request(
        url,
        data=cuerpo,
        method=metodo,
    )

    try:
        with urlopen(solicitud, timeout=5) as respuesta:
            return (
                respuesta.status,
                respuesta.read().decode("utf-8"),
            )

    except HTTPError as error:
        return (
            error.code,
            error.read().decode("utf-8"),
        )


def interpretar(html):
    lector = TextoHTML()
    lector.feed(html)

    texto = " ".join(lector.partes)

    if "Acceso concedido." in texto:
        return "Acceso concedido"

    if "Acceso denegado." in texto:
        return "Acceso denegado"

    if "Error al procesar la consulta SQL." in texto:
        return "Error al procesar la consulta"

    resultado = re.search(
        r"Registros encontrados:\s*(\d+)",
        texto,
    )

    if resultado:
        return f"Registros encontrados: {resultado.group(1)}"

    return "Respuesta no reconocida: revisar la página"


def ejecutar_pruebas():
    _, portada = enviar("/")

    if "Versión corregida" in portada:
        version = "corregida"

    elif "Versión vulnerable" in portada:
        version = "vulnerable"

    else:
        version = "no identificada"

    print("TPE 4 - GRUPO 5")
    print("PRUEBAS CONTROLADAS DE SQL INJECTION")
    print(f"Servidor: {BASE_URL}")
    print(f"Versión: {version}")
    print()

    pruebas = [
        (
            "1. Credenciales válidas",
            "/login",
            {
                "usuario": "admin",
                "contrasena": "Admin123",
            },
            "POST",
        ),
        (
            "2. Credenciales incorrectas",
            "/login",
            {
                "usuario": "admin",
                "contrasena": "Incorrecta123",
            },
            "POST",
        ),
        (
            "3. Intento de bypass",
            "/login",
            {
                "usuario": "admin' --",
                "contrasena": "Incorrecta123",
            },
            "POST",
        ),
        (
            "4. Búsqueda normal",
            "/buscar",
            {"nombre": "Camiseta"},
            "GET",
        ),
        (
            "5. Intento de extracción",
            "/buscar",
            {
                "nombre":
                    "zzzz' UNION SELECT id, usuario, rol "
                    "FROM usuarios -- "
            },
            "GET",
        ),
    ]

    for nombre, ruta, datos, metodo in pruebas:
        estado, html = enviar(ruta, datos, metodo)

        print(nombre)
        print(f"  Petición: {metodo} {ruta}")
        print(f"  Estado HTTP: {estado}")
        print(f"  Resultado: {interpretar(html)}")
        print()


if __name__ == "__main__":
    try:
        ejecutar_pruebas()

    except (URLError, TimeoutError, OSError) as error:
        print(f"No se pudo completar la conexión: {error}")
        print("Comprueba que el servidor esté funcionando.")