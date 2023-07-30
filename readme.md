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

2. Instalar dependencias del proyecto ejecutando:

'''
pip install -r requirements.txt
'''

# Ejecución
Ejecuta en el directorio de la aplicación:
'''
flask run
'''