
#  a2Auto-Vpos

Podrás automatizar las operaciones bancarias generadas con vpos de megasoft solo con el correo enviado con la informacion del cierre de lote o detalle de operaciones.


## Requisitos

ODBC_64_bitsdbisam.exe

Sistema operativo: Windows 10 o superior 64bits

Conexión a la base de datos de a2 de forma local, no remota.

Python 3.11.1 o superior



## Instalación

Asegurate de instalar el controlador odbc de dbisam, puedes descargar su version gratuita desde este enlace [odbc_driver](https://www.elevatesoft.com/), debes registrarte para poder descargar el demo.

El nombre del origen de datos debe ser `a2GKC`, al momento de instalar el controlador debes dejar en blanco la ruta hacia la base de datos, ya que mas adelante la configuraremos mediante una variable de entorno para poder acceder a ella mas facilmente.

Puedes verificar tu instalacion ejecutando en powershell:

```bash
  Get-OdbcDriver -Name "DBISAM 4 ODBC Driver" | Format-List
```
Salida:

```bash
  Name      : DBISAM 4 ODBC Driver
  Platform  : 64-bit
  Attribute : {APILevel, DriverODBCVer, FileUsage, Driver...}
```

#### Descarga el binario

los ultimos binarios de la version estan disponibles aqui



    
## Iniciar App

Una vez finalizada la descarga crea una carpeta:

```bash
mkdir auto-Vpos
```

En la carpeta inicia la app haciendo doble clic en el .exe

dentro de la carpeta `auto-Vpos` debes tener una jerarquia de carpetas como la siguiente:

```markdown
 Estructura de carpetas

auto-Vpos
├── downloads
│   ├── archivo.zip
│   └── archivo2.zip
├── logs
│   ├── logs_data.log
├── detalle
├── lote
├── auto-Vpos.exe


