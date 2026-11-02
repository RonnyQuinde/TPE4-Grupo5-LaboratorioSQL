# Laboratorio de inyección SQL y protección de datos

**Trabajo Práctico Experimental 4 — Grupo 5**  
Universidad Estatal de Milagro  
Carrera de Tecnologías de la Información  
Asignatura de Seguridad Informática

## Presentación

Este proyecto permite comprobar cómo cambia el comportamiento de una
aplicación cuando se corrige la forma de construir sus consultas SQL.

Para realizar la comparación, se prepararon dos versiones del mismo
formulario de acceso y catálogo deportivo. Ambas utilizan los mismos
datos ficticios, pero procesan las entradas del usuario de manera diferente.

La práctica incluye pruebas manuales y automáticas, comprobación de puertos
locales y verificación de integridad con respaldo de la base de datos.

## Propósito

El objetivo es identificar los efectos de una consulta vulnerable
y comprobar que las consultas parametrizadas impiden los intentos
de inyección evaluados, manteniendo las funciones normales de la aplicación.

## Las dos versiones

| Versión | Archivo | Característica |
|---|---|---|
| Vulnerable | `app_vulnerable.py` | Incorpora directamente las entradas del usuario al texto SQL. |
| Corregida | `app_segura.py` | Utiliza parámetros para separar las instrucciones SQL de los valores recibidos. |

Las dos versiones comparten la interfaz y la base de datos.
Esto permite comparar sus resultados bajo las mismas condiciones.

## Funciones del proyecto

- Comprobación de credenciales ficticias.
- Búsqueda de productos deportivos.
- Visualización de la consulta SQL utilizada.
- Ejecución de cinco pruebas HTTP controladas.
- Comprobación de cinco puertos TCP locales.
- Revisión de integridad y creación de respaldos de SQLite.

La interfaz utiliza fondo oscuro, botones rojos e identificación del Grupo 5.

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Desarrollo y ejecución de los programas. |
| Flask | Funcionamiento de la aplicación web. |
| SQLite | Almacenamiento de usuarios y productos. |
| HTML y CSS | Presentación de los formularios y resultados. |

El proyecto se probó en Windows con Python 3.12.10 y Flask 3.1.3.

## Organización de los archivos

| Archivo | Contenido |
|---|---|
| `crear_bd.py` | Preparación de la base y los datos ficticios. |
| `app_vulnerable.py` | Aplicación con la vulnerabilidad intencional. |
| `app_segura.py` | Aplicación con consultas parametrizadas. |
| `templates/laboratorio.html` | Interfaz compartida por ambas versiones. |
| `ataque_sql_i.py` | Pruebas HTTP para comparar las aplicaciones. |
| `escaneo_red.py` | Comprobación de puertos locales. |
| `seguridad_bd.py` | Verificación de integridad y respaldo. |
| `requirements.txt` | Dependencia necesaria para ejecutar el proyecto. |
| `MANUAL_USO.md` | Instrucciones detalladas de instalación y uso. |

## Inicio rápido

Desde PowerShell, ubicado en la carpeta principal del proyecto,
ejecuta los siguientes comandos en orden:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe crear_bd.py
.\.venv\Scripts\python.exe app_segura.py
```

Después abre:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

Para utilizar la versión vulnerable, detén el servidor con **Ctrl + C**
y ejecuta:

```powershell
.\.venv\Scripts\python.exe app_vulnerable.py
```

Ejecuta una sola versión a la vez, ya que ambas utilizan el puerto 5000.

Las instrucciones para utilizar los formularios, repetir las pruebas
y resolver problemas están en el [manual de uso](MANUAL_USO.md).

## Resultados de la comparación

| Prueba | Versión vulnerable | Versión corregida |
|---|---|---|
| Credenciales válidas | Acceso concedido. | Acceso concedido. |
| Credenciales incorrectas | Acceso denegado. | Acceso denegado. |
| Intento de bypass | Acceso concedido sin una contraseña válida. | Acceso denegado. |
| Búsqueda normal | Un producto encontrado. | Un producto encontrado. |
| Intento de extracción | Tres usuarios obtenidos desde el buscador. | Cero registros. |

Las pruebas mostraron que la corrección impidió los dos intentos
de inyección evaluados y conservó el acceso válido y la búsqueda normal.

En las comprobaciones complementarias, el puerto 5000 aceptó conexiones
mientras Flask estaba activo y dejó de hacerlo al detener el servidor.
También se verificó la integridad de la base y de la copia de respaldo.

## Datos generados localmente

La base `laboratorio.db` se prepara mediante `crear_bd.py`.
Las copias se guardan en la carpeta `respaldos`.

Estos archivos, el entorno virtual y los temporales de Python
están excluidos del repositorio mediante `.gitignore`.
Al descargar el proyecto en otra computadora, se deben seguir
los pasos de instalación para generar el entorno y la base.

## Alcance

El proyecto es un laboratorio académico local con datos ficticios.
La versión vulnerable contiene fallos intencionales para su estudio.

La versión corregida demuestra el uso de consultas parametrizadas
frente a las entradas evaluadas. El proyecto conserva contraseñas
de prueba en texto plano y no incluye una autenticación completa
para producción.