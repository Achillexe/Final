import sqlite3
from datetime import datetime
import os
import requests

CURRENCIES = ["EUR", "ETH", "BNB", "ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]

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
        return lista
    
    def wallet(self):
        
        query = """
        SELECT moneda_from, cantidad_from, moneda_to, cantidad_to FROM movements;
        """

        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(query)
        regs = cur.fetchall()
        
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

        for currency, amount in regs_from:
            if currency != "EUR" and currency in crypto_resta:
                crypto_resta[currency] += amount
            elif currency != "EUR":
                crypto_resta[currency] = amount
            elif currency == "EUR" and currency in euro_resta:
                euro_resta[currency] += amount
            elif currency == "EUR":
                euro_resta[currency] = amount                

        for key, value in crypto_resta.items():
            if key in crypto_resultado:
                crypto_resultado[key] -= value

        for key, value in euro_resta.items():
            if key in euro_resultado:
                euro_resultado[key] -= value

        listed_resultado = [(key, value) for key, value in crypto_resultado.items()]
        
        euros = []
        for currency, amount in crypto_resultado.items():
            euros.append(Exchange(amount, currency, "EUR").amount_to)
        
        self.wallet = []
        for item, euros in zip(listed_resultado, euros):
            self.wallet.append((item[0], item[1], euros))
        
        self.value = 0
        for i in self.wallet:
            self.value += i[2]

        self.price = euro_resultado[key]

        self.earnings = self.value + self.price

        return self.wallet

class Exchange:
    def __init__(self, amount, coin_from, coin_to):
        
        tasa = self.rate(coin_from, coin_to)
        self.amount_to = amount * tasa
        
    def rate(self, coin_from, coin_to):
        
        url = f"https://rest.coinapi.io/v1/exchangerate/{coin_from}/{coin_to}"
        headers = {'X-CoinAPI-Key' : '9111DE0E-4C75-4E13-A205-0318E57DCCFC'}
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if response.status_code == 200:
                return data["rate"]
            
            else:
                return data["error"]
            
        except requests.exceptions.RequestException as e:
            return False, str(e)
        
class Status:
    pass