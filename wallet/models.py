import sqlite3
from datetime import datetime

CURRENCIES = ["EUR", "ETH", "BNB", "ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]

class Movement:
    def __init__(self, currency_from, amount_from, currency_to, amount_to, id = None):
        self.current_date = datetime.now().date().strftime("%Y-%m-%d")
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
        return self.date == other.date and self.time == other.time and self.currency_from == other.currency_from and self.amount_from == other.amount_from and self.currency_to == other.currency_to and self.amount_to == other.amount_to

    def __repr__ (self):
        return f"Movimiento: {self.date} - {self.time} - {self.currency_from} - {self.amount_from} - {self.currency_to} - {self.amount_to}"


class MovementDAO:
    def __init__(self, db_path):
        self.path = db_path

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
