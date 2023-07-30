from wallet import app
import sqlite3
from datetime import datetime
import os
import requests

CURRENCIES = ["EUR", "ETH", "BNB", "ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]
PURCHASE = ["EUR", "BTC"]
TRADE = ["ETH", "BNB", "ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]

class Movement:
    def __init__(self, currency_from, amount_from, currency_to, amount_to, id = None, date=None, time=None):
        
        self.current_date = ""
        self.current_time = ""

        if date:
            self.current_date = date
        else:     
            self.current_date = datetime.now().date().strftime("%Y-%m-%d")
        
        if time:
            self.current_time = time
        else:     
            self.current_time = datetime.now().time().strftime("%H:%M:%S")

        self.currency_from = currency_from
        self.amount_from = amount_from
        self.currency_to = currency_to
        self.amount_to = amount_to

        self.id = id

    @property
    def currency_from(self):
        return self._currency_from

    @currency_from.setter
    def currency_from(self, value):
        self._currency_from = value
        if self._currency_from not in CURRENCIES:
            raise ValueError(f"Currency must be {CURRENCIES}")
        
    @property
    def amount_from(self):
        return self._amount_from

    @amount_from.setter
    def amount_from(self, value):
        self._amount_from = float(value)
        if self._amount_from <= 0:
            raise ValueError("Amount must be higher than 0")
        
    @property
    def currency_to(self):
        return self._currency_to

    @currency_to.setter
    def currency_to(self, value):
        self._currency_to = value
        if self._currency_to not in CURRENCIES:
            raise ValueError(f"Currency must be {CURRENCIES}")
        
    @property
    def amount_to(self):
        return self._amount_to

    @amount_to.setter
    def amount_to(self, value):
        self._amount_to = float(value)
        if self._amount_to <= 0:
            raise ValueError("Amount must be higher than 0")
        
    def __eq__(self, other):
        return self.current_date == other.current_date and self.current_time == other.current_time and self.currency_from == other.currency_from and self.amount_from == other.amount_from and self.currency_to == other.currency_to and self.amount_to == other.amount_to

    def __repr__ (self):
        return f"Movimiento: {self.current_date} - {self.current_time} - {self.currency_from} - {self.amount_from} - {self.currency_to} - {self.amount_to}"

class MovementDAO:
    def __init__(self, db_path):
        self.path = db_path

        if not os.path.exists(self.path):

            query = """
            CREATE TABLE "movements" (
                "id"	INTEGER,
                "date"	TEXT NOT NULL,
                "time"	TEXT NOT NULL,
                "moneda_from"	TEXT NOT NULL,
                "cantidad_from"	REAL NOT NULL,
                "moneda_to"	TEXT NOT NULL,
                "cantidad_to"	REAL NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
            
            conn = sqlite3.connect(self.path)
            cur = conn.cursor()
            cur.execute(query)
            conn.close()

    def validate (self, currency_from, currency_to):
        if currency_from in PURCHASE and currency_to in PURCHASE:
            return True
        elif currency_from in TRADE and currency_to in TRADE:
            return True
        else:
            raise ValueError("Las operaciones permitidas son: EUR a BTC | BTC a EUR | Entre cryptos")

    def balance (self, amount_from, currency_from):
        query = """
        SELECT moneda_from, cantidad_from, moneda_to, cantidad_to FROM movements 
        WHERE moneda_from = :currency OR moneda_to = :currency
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query, {"currency": currency_from})
        regs = cur.fetchall()
        
        if regs and currency_from != "EUR":
            regs_to = []
            regs_from = []

            for reg in regs:
                if reg[2] == currency_from:
                    regs_to.append(reg[2:])
                else:
                    regs_from.append(reg[:2])

            crypto_resultado = {}
            crypto_resta = {}
            
            for currency, amount in regs_to:
                if currency in crypto_resultado:
                    crypto_resultado[currency] += amount
                else:
                    crypto_resultado[currency] = amount

            if regs_from:
                for currency, amount in regs_from:
                    if currency in crypto_resta:
                        crypto_resta[currency] += amount
                    else:
                        crypto_resta[currency] = amount

                for key, value in crypto_resta.items():
                    if key in crypto_resultado:
                        crypto_resultado[key] -= value

            key, value = crypto_resultado.popitem()
            
            if value >= amount_from:
                return True
            else:
                raise ValueError("No tienes suficientes fondos para esta operación")
        
        elif currency_from == "EUR":
            return True
        
        else:
            raise ValueError("Todavía no has comprado ninguna cripto con la que puedas operar. Has tu primera compra con euros")
    
    def purchase(self, movement):

        query = """
        INSERT INTO movements
            (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        
        cur.execute(query, (movement.current_date, movement.current_time,
                            movement.currency_from, movement.amount_from, movement.currency_to, movement.amount_to))
        conn.commit()
        conn.close()

    def get_permitted_currency_from(self):
        query = """
        SELECT DISTINCT moneda_to FROM movements;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        currencies = [currency[0] for currency in res]
        conn.close()

        return currencies

    def get_all(self):
        query = """
        SELECT moneda_from, cantidad_from, moneda_to, cantidad_to, id, date, time
        FROM movements ORDER by date;
        """
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()

        lista = []
        for reg in res:
            lista.append(Movement(*reg))

        conn.close()

        if lista:
            return lista
        else:
            return False
 
class Wallet:
    def __init__(self):

        calculations = self.calculations(app.config["PATH_SQLITE"])

        if isinstance(calculations, tuple):
            self.wallet, self.price = calculations
            
            self.value = 0
            for i in self.wallet:
                self.value += i[2]

            self.earnings = self.value + self.price

        else:
            self.wallet = []
            self.price = 0
            self.value = 0
            self.earnings = 0
            raise ValueError("No hay movimientos en la base de datos")

    def calculations(self, db):
        
        query = """
        SELECT moneda_from, cantidad_from, moneda_to, cantidad_to FROM movements;
        """

        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(query)
        regs = cur.fetchall()
        
        if regs:
            regs_to = []
            regs_from = []

            for reg in regs:
                regs_to.append(reg[2:])
                regs_from.append(reg[:2])
            
            crypto_resultado = {}
            crypto_resta = {}
            euro_resultado = {}
            euro_resta = {}

            for currency, amount in regs_to:
                if currency != "EUR" and currency in crypto_resultado:
                    crypto_resultado[currency] += amount
                elif currency != "EUR":
                    crypto_resultado[currency] = amount
                elif currency == "EUR" and currency in euro_resultado:
                    euro_resultado[currency] += amount
                elif currency == "EUR":
                    euro_resultado[currency] = amount
                else:
                    euro_resultado["EUR"] = 0

            for currency, amount in regs_from:
                if currency != "EUR" and currency in crypto_resta:
                    crypto_resta[currency] += amount
                elif currency != "EUR":
                    crypto_resta[currency] = amount
                elif currency == "EUR" and currency in euro_resta:
                    euro_resta[currency] += amount
                elif currency == "EUR":
                    euro_resta[currency] = amount                

            for currency, amount in crypto_resta.items():
                if currency in crypto_resultado:
                    crypto_resultado[currency] -= amount

            for currency, amount in euro_resta.items():
                if currency in euro_resultado:
                    euro_resultado[currency] -= amount
                else:
                    euro_resultado[currency] = 0 - amount

            listed = [(key, value) for key, value in crypto_resultado.items()]
        
            euros = []
            for currency, amount in crypto_resultado.items():
                euros.append(Exchange(amount, currency, "EUR").amount_to)
            
            wallet = []
            for item, euros in zip(listed, euros):
                wallet.append((item[0], item[1], euros))

            price = euro_resultado["EUR"]

            return wallet, price
            
        else:
            return False

class Exchange:
    def __init__(self, amount, coin_from, coin_to):
        
        status, tasa = self.rate(coin_from, coin_to)

        if status:
            self.amount_to = amount * tasa
        else:
            raise ValueError("No se ha podido consultar el valor de la crypto por problemas de conexión. Volver a intentar en unos segundos.")
        
    def rate(self, coin_from, coin_to):
        
        url = f"https://rest.coinapi.io/v1/exchangerate/{coin_from}/{coin_to}"
        headers = {'X-CoinAPI-Key': app.config["COINAPI_KEY"]}
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if response.status_code == 200:
                return True, data["rate"]
            
            else:
                return False, data["error"]
            
        except requests.exceptions.RequestException as e:
            return False, str(e)