# Manual de instalación y uso

**Trabajo Práctico Experimental 4 — Grupo 5**  
**Universidad Estatal de Milagro**  
**Carrera:** Tecnologías de la Información  
**Asignatura:** Seguridad Informática

## 1. Descripción del laboratorio

Este proyecto permite comparar una aplicación vulnerable a inyección SQL
con una versión corregida mediante consultas parametrizadas.

Ambas versiones incluyen un formulario de acceso y un buscador
de productos deportivos. Comparten la misma interfaz y base de datos,
lo que permite repetir las pruebas y comparar sus resultados.

El laboratorio también incluye programas para automatizar las pruebas,
comprobar cinco puertos locales y generar un respaldo de la base de datos.

Todas las comprobaciones se realizan en la computadora local
y utilizan datos ficticios.

### 1.1. Versión vulnerable

El archivo `app_vulnerable.py` incorpora directamente lo que escribe
el usuario dentro del texto de las consultas SQL.

Esto permite que determinadas entradas modifiquen la instrucción
que recibe la base de datos. Durante las pruebas, esta debilidad permitió
conseguir acceso sin una contraseña válida y consultar usuarios
desde el buscador de productos.

La página identifica esta versión con la etiqueta:

**Versión vulnerable · Consultas por concatenación**

### 1.2. Versión corregida

El archivo `app_segura.py` utiliza consultas parametrizadas.
La instrucción SQL contiene marcadores `?` y los valores del formulario
se envían por separado al ejecutar la consulta.

Así, las entradas se utilizan como datos y no pueden cambiar
la estructura de esas consultas.

En las pruebas realizadas, esta versión rechazó el intento de acceso
indebido y evitó la extracción de usuarios. El acceso con credenciales
válidas y la búsqueda normal continuaron funcionando.

La página identifica esta versión con la etiqueta:

**Versión corregida · Consultas parametrizadas**

### 1.3. Diferencias principales

| Aspecto | Versión vulnerable | Versión corregida |
|---|---|---|
| Archivo | `app_vulnerable.py` | `app_segura.py` |
| Consultas SQL | Incorpora las entradas directamente al texto SQL. | Envía los valores por separado mediante parámetros. |
| Credenciales válidas | Permite el acceso. | Permite el acceso. |
| Contraseña incorrecta | Rechaza el acceso normal. | Rechaza el acceso. |
| Intento de bypass evaluado | Permite acceder sin una contraseña válida. | Rechaza el acceso. |
| Búsqueda normal | Devuelve el producto correspondiente. | Devuelve el producto correspondiente. |
| Intento de extracción evaluado | Devuelve tres usuarios desde el buscador. | No devuelve registros. |

Las dos aplicaciones consultan la base mediante conexiones de solo lectura.
Esto evita escrituras desde esas conexiones, pero no impide que una consulta
vulnerable lea información que no debería mostrar.

## 2. Requisitos

Para ejecutar el proyecto se necesita:

- Windows con Python instalado. En las pruebas se utilizó Python 3.12.10.
- Visual Studio Code o un editor equivalente.
- Una terminal de PowerShell.
- Un navegador web.
- Conexión a Internet para instalar las dependencias.

Abre la carpeta completa del proyecto en Visual Studio Code
y selecciona **Terminal → Nueva terminal**.

Todos los comandos de este manual deben ejecutarse desde la carpeta
principal, donde se encuentran `crear_bd.py`, `app_vulnerable.py`
y `app_segura.py`.

## 3. Archivos del proyecto

| Archivo | Función |
|---|---|
| `crear_bd.py` | Prepara las tablas, los usuarios ficticios y los productos deportivos. |
| `app_vulnerable.py` | Ejecuta la aplicación con consultas vulnerables. |
| `app_segura.py` | Ejecuta la aplicación corregida con consultas parametrizadas. |
| `templates/laboratorio.html` | Contiene la interfaz compartida por ambas versiones. |
| `ataque_sql_i.py` | Ejecuta cinco pruebas HTTP controladas. |
| `escaneo_red.py` | Comprueba cinco puertos TCP de la computadora local. |
| `seguridad_bd.py` | Comprueba la integridad y genera un respaldo de la base. |
| `requirements.txt` | Indica la dependencia que debe instalarse. |
| `.gitignore` | Excluye del repositorio los archivos generados localmente. |
| `README.md` | Presenta el proyecto y sus instrucciones generales. |
| `MANUAL_USO.md` | Explica la instalación, el uso y las comprobaciones. |

El archivo `laboratorio.db` y la carpeta `respaldos` se generan
al ejecutar los programas correspondientes.

## 4. Instalación

Si el entorno virtual, Flask y la base de datos ya están preparados,
continúa con el apartado 5.

### 4.1. Crear el entorno virtual

Ejecuta:

```powershell
py -m venv .venv
```

Se creará la carpeta `.venv`, que permite mantener las dependencias
del proyecto en un entorno propio.

Los comandos siguientes utilizan directamente el Python de esa carpeta,
por lo que no es necesario activar el entorno virtual.

### 4.2. Instalar las dependencias

Comprueba que `requirements.txt` contenga:

```text
Flask==3.1.3
```

Después ejecuta:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Espera a que termine la instalación de Flask y sus dependencias.

SQLite forma parte de Python y no necesita instalarse por separado.

### 4.3. Preparar la base de datos

Ejecuta:

```powershell
.\.venv\Scripts\python.exe crear_bd.py
```

En una instalación nueva se generará `laboratorio.db`
con tres usuarios y cinco productos deportivos.

La terminal mostrará la ubicación de la base y la cantidad de registros.

Si la base ya existe, el programa conserva los usuarios existentes
y actualiza los cinco productos definidos sin duplicar sus identificadores.
No es necesario borrar la base para cambiar entre versiones.

## 5. Ejecutar la aplicación

Se debe ejecutar una sola versión a la vez, porque ambas utilizan
el puerto `5000`.

### 5.1. Iniciar la versión vulnerable

```powershell
.\.venv\Scripts\python.exe app_vulnerable.py
```

### 5.2. Iniciar la versión corregida

```powershell
.\.venv\Scripts\python.exe app_segura.py
```

Después de ejecutar uno de estos comandos, espera a que aparezca:

```text
Running on http://127.0.0.1:5000
```

Abre en el navegador:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

La dirección `127.0.0.1` corresponde a la computadora donde
se está ejecutando el proyecto.

Mantén el servidor activo mientras utilizas los formularios.
Es normal que la terminal muestre las solicitudes recibidas.

### 5.3. Cambiar de versión

1. Selecciona la terminal donde está ejecutándose Flask.
2. Presiona **Ctrl + C** para detener el servidor.
3. Ejecuta el comando de la otra versión.
4. Abre nuevamente la dirección local en el navegador.
5. Comprueba la etiqueta que identifica la versión activa.

Cerrar el navegador no detiene el servidor.
La detención se realiza desde su terminal.

## 6. Utilizar el formulario de acceso

### 6.1. Acceso con credenciales válidas

En **Acceso de usuarios**, escribe:

| Campo | Valor |
|---|---|
| Usuario | `admin` |
| Contraseña | `Admin123` |

Pulsa **Ingresar**.

Debe aparecer:

```text
Acceso concedido. Bienvenido, admin.
```

También se mostrará una tabla con el identificador,
el nombre del usuario y su rol.

Respeta las mayúsculas de la contraseña.

### 6.2. Acceso con una contraseña incorrecta

Utiliza el usuario `admin` y una contraseña incorrecta,
por ejemplo `Incorrecta123`.

Pulsa **Ingresar**. El resultado esperado es:

```text
Acceso denegado. Credenciales incorrectas.
```

Estas dos comprobaciones deben funcionar de la misma manera
en ambas versiones.

El formulario verifica las credenciales y presenta el resultado.
No mantiene una sesión de usuario después de la prueba.

## 7. Buscar productos

En **Catálogo deportivo**, escribe:

```text
Camiseta
```

Pulsa **Buscar producto**.

Debe aparecer:

```text
Registros encontrados: 1
```

La tabla mostrará:

| ID | Producto | Precio (USD) |
|---|---|---|
| 2 | Camiseta deportiva | 18.00 |

La búsqueda admite el nombre completo o una parte del nombre
y puede utilizarse sin completar primero el formulario de acceso.

Los productos preparados para el laboratorio son:

- Balón de fútbol.
- Camiseta deportiva.
- Guantes de arquero.
- Canilleras.
- Botella deportiva.

Si no existen coincidencias, aparecerá:

```text
Registros encontrados: 0
```

Para volver a la pantalla inicial, utiliza el enlace
**Limpiar formularios**, ubicado al final de la página.

## 8. Comparar las consultas SQL

Después de enviar un formulario, abre la opción
**Ver consulta SQL del laboratorio**.

Esta sección permite observar la diferencia entre las dos versiones.

### 8.1. Consulta de acceso vulnerable

Al ingresar las credenciales ficticias `admin` y `Admin123`,
la versión vulnerable muestra una consulta equivalente a:

```sql
SELECT id, usuario, rol
FROM usuarios
WHERE usuario = 'admin' AND contrasena = 'Admin123'
```

Los valores del formulario aparecen dentro de la instrucción.
El problema está en incorporarlos directamente al texto SQL,
permitiendo que determinadas entradas alteren su significado.

### 8.2. Consulta de acceso corregida

La versión corregida muestra:

```sql
SELECT id, usuario, rol
FROM usuarios
WHERE usuario = ? AND contrasena = ?
```

Los signos `?` son marcadores de posición.
El programa envía el usuario y la contraseña por separado
al ejecutar la consulta.

La base recibe esos valores y los utiliza para comprobar
las credenciales, aunque no aparezcan dentro del SQL mostrado.

### 8.3. Consulta de productos

Al buscar `Camiseta`, la versión vulnerable muestra:

```sql
SELECT id, nombre, precio
FROM productos
WHERE nombre LIKE '%Camiseta%'
```

La versión corregida muestra:

```sql
SELECT id, nombre, precio
FROM productos
WHERE nombre LIKE ?
```

En la versión corregida, `%Camiseta%` se envía como parámetro.
Los símbolos `%` permiten encontrar nombres que contengan
el texto buscado.

Ambas versiones deben devolver el mismo producto en esta búsqueda normal.
La corrección modifica la forma de procesar las entradas
y conserva la funcionalidad del buscador.

## 9. Ejecutar las pruebas automáticas

El archivo `ataque_sql_i.py` realiza cinco pruebas controladas
contra `http://127.0.0.1:5000`.

Para ejecutarlo se utilizan dos terminales:

| Terminal | Función |
|---|---|
| Primera terminal | Mantener una versión de la aplicación ejecutándose. |
| Segunda terminal | Ejecutar el programa de pruebas. |

### 9.1. Comprobar la primera versión

1. Inicia una de las aplicaciones en la primera terminal.
2. Espera a que aparezca la dirección del servidor.
3. Abre una segunda terminal con el botón **+** del panel Terminal.
4. Desde la carpeta del proyecto, ejecuta:

```powershell
.\.venv\Scripts\python.exe ataque_sql_i.py
```

El programa mostrará la versión detectada y, para cada prueba,
la petición HTTP, el código de respuesta y el resultado.

### 9.2. Comprobar la otra versión

1. Regresa a la terminal del servidor.
2. Detén la aplicación con **Ctrl + C**.
3. Inicia la otra versión.
4. Espera a que el servidor esté disponible.
5. En la segunda terminal, ejecuta nuevamente el mismo comando.

### 9.3. Resultados comprobados

| Prueba | Versión vulnerable | Versión corregida |
|---|---|---|
| Credenciales válidas | HTTP 200: acceso concedido | HTTP 200: acceso concedido |
| Credenciales incorrectas | HTTP 401: acceso denegado | HTTP 401: acceso denegado |
| Intento de bypass | HTTP 200: acceso concedido | HTTP 401: acceso denegado |
| Búsqueda normal | HTTP 200: 1 producto | HTTP 200: 1 producto |
| Intento de extracción | HTTP 200: 3 usuarios | HTTP 200: 0 registros |

### 9.4. Interpretación de los resultados

Las pruebas con credenciales válidas, contraseñas incorrectas
y búsquedas normales comprueban el funcionamiento habitual.
Esas operaciones producen resultados equivalentes en ambas versiones.

Las diferencias aparecen en los dos intentos de inyección evaluados:

- **Intento de bypass:** la versión vulnerable permite acceder
  sin una contraseña válida. La corregida rechaza la entrada
  y mantiene la comprobación del usuario y la contraseña.

- **Intento de extracción:** la versión vulnerable devuelve tres usuarios
  desde una consulta destinada a buscar productos. La corregida utiliza
  la entrada como texto de búsqueda y devuelve cero registros.

El resultado de cero registros no significa que la aplicación
haya mostrado un aviso de ataque detectado. Significa que la entrada
no consiguió modificar la consulta y no coincidió con ningún producto.

El código HTTP debe interpretarse junto con el resultado.
En el intento de extracción, ambas versiones responden HTTP `200`,
pero la vulnerable devuelve usuarios y la corregida no devuelve registros.

Esta comparación muestra que la corrección impide las inyecciones
evaluadas y mantiene funcionando las operaciones normales.

Conserva una captura de cada ejecución donde se vean
la versión detectada y las cinco pruebas.

## 10. Comprobar los puertos locales

El archivo `escaneo_red.py` comprueba los puertos
`80`, `443`, `5000`, `8000` y `8080` de la computadora local.

### 10.1. Con el servidor activo

Mantén una aplicación ejecutándose y, desde otra terminal, ejecuta:

```powershell
.\.venv\Scripts\python.exe escaneo_red.py
```

El puerto `5000` debe aparecer como:

```text
Puerto 5000: ABIERTO
```

Esto indica que Flask está aceptando conexiones en ese puerto.

### 10.2. Con el servidor detenido

Detén Flask con **Ctrl + C** y repite el comando.

En las pruebas realizadas, el puerto `5000` pasó a:

```text
Puerto 5000: SIN CONEXIÓN
```

El total fue de cero puertos abiertos entre los cinco examinados.

Si otro programa utiliza alguno de esos puertos, el resultado puede variar.
El escaneo solo comprueba si se puede establecer una conexión TCP
y no determina por sí mismo si existe una vulnerabilidad.

Guarda una captura con el servidor activo y otra con el servidor detenido.

## 11. Verificar y respaldar la base de datos

Con el servidor detenido, ejecuta:

```powershell
.\.venv\Scripts\python.exe seguridad_bd.py
```

El programa realiza estas acciones:

1. Abre `laboratorio.db` en modo de solo lectura.
2. Comprueba la integridad de la base original.
3. Genera una copia en la carpeta `respaldos`.
4. Comprueba también la integridad de la copia.

Si termina correctamente, mostrará:

```text
Comprobación de integridad: OK
Conexión a la base original: solo lectura
Copia de respaldo creada y verificada.
```

La terminal también indica la ubicación del archivo generado.

Despliega la carpeta `respaldos` en el Explorador de Visual Studio Code
y comprueba que el nombre coincida con el mostrado en la terminal.

Cada ejecución crea un respaldo nuevo con fecha y hora.
La aplicación sigue utilizando `laboratorio.db`; los respaldos
son copias separadas.

Conserva la base original y al menos un respaldo reciente.

La comprobación de integridad revisa la estructura de SQLite.
No sustituye una prueba completa de restauración ni demuestra
que la aplicación esté protegida frente a todos los ataques.

## 12. Solución de problemas frecuentes

| Problema | Acción recomendada |
|---|---|
| La página no abre | Comprueba que Flask siga ejecutándose y utiliza `http://127.0.0.1:5000`. |
| Falta Flask | Repite la instalación de dependencias del apartado 4.2. |
| Falta la base de datos o alguna tabla | Ejecuta `crear_bd.py` antes de iniciar la aplicación. |
| Aparece `TemplateNotFound` | Comprueba que exista `templates/laboratorio.html` dentro del proyecto. |
| El puerto 5000 está ocupado | Detén la aplicación anterior antes de iniciar otra. |
| Las pruebas no pueden conectarse | Inicia una aplicación y ejecuta las pruebas desde una segunda terminal. |
| Aparecen varios respaldos | Es normal: cada ejecución genera una copia con un nombre diferente. |

No elimines una base de datos con información que quieras conservar
para intentar resolver un error.

## 13. Finalizar y continuar otro día

Al terminar:

1. Detén el servidor con **Ctrl + C**.
2. Guarda los archivos modificados.
3. Cierra el navegador y Visual Studio Code cuando hayas terminado.

Para continuar otro día, abre la carpeta del proyecto,
inicia la versión que necesites y accede a la dirección local.

No hace falta reinstalar las dependencias ni crear nuevamente
la base de datos si esos elementos se conservan.

## 14. Ejecutar el proyecto en otra computadora

Copia o descarga los archivos del proyecto junto con la carpeta `templates`.
Después realiza la instalación siguiendo el apartado 4.

El archivo `.gitignore` excluye del repositorio los elementos
que se generan localmente:

- `.venv/`
- Las bases de datos `.db`.
- La carpeta `respaldos/`.
- Los archivos temporales de Python.

Por eso es normal que no aparezcan al descargar el código desde GitHub.
El entorno y la base se crean al seguir las instrucciones de instalación.

