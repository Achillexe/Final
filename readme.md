# Simulación de wallet 
Registro de inversiones y compra/venta de criptomonedas para simular una cartera de inversión. Para ello se ha creado una aplicación en flask que consulta el valor real en euros de las siguientes criptomonedas:

Monedas y criptomonedas posibles:
EUR, BTC,
ETH, USDT,
BNB, XRP,
ADA, SOL,
DOT, MATIC

La consultas de valores relativos entre estas criptomonedas se hacen utilizando la api siguiente:
https://www.coinapi.io/


# Instalación
1. Incluir el fichero .env en el directorio root del proyecto. El fichero será proveído por el CTO de Syvila. 
    a. En caso de estar probando la aplicación, podrán utilizarse las variables de entorno dentro del fichero .env_template. Crear un fichero .env y copiar en el las variables.

2. informar FLASK_DEBUG a TRUE o FALSE. 
    a. Solo configurar a FALSE si la aplicación está operativa en un entorno de desarrollo/pruebas. En producción configurar siempre a TRUE.

3. Instalar dependencias del proyecto ejecutando:
`pip install -r requirements.txt`

4. Crear base de datos ejecutando el script `create_db.py` dentro de la carpeta "data".


# Ejecución
Ejecutar en el directorio de la aplicación:
`flask run`


# NOTA
La consigna del ejercicio tenía dos criterios contradictorios en las instrucciones. Transcribiendo textualmente:

1. VENTA: De cualquier cripto a euros: Se considerará recuperación de la inversión. Si
al vender conseguimos más euros de los que invertimos será considerado beneficio,
si obtenemos menos euros de los que invertimos será considerado pérdida.

2. /purchase: mostrará un formulario en el que realizar una compra, venta o
intercambio de monedas. Se podrá comprar BTC en euros y vender BTC a euros, el
resto de cripto monedas se intercambiarán por BTC y entre ellas

Se eligió el camino 2.