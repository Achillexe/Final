from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SelectField, SubmitField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length
from datetime import date
from wallet.models import *

class MovementForm(FlaskForm):
    currency_from = SelectField("Moneda", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR", "Euros"), 
                                                                                                    ("ETH", "Ethereum"), 
                                                                                                    ("BNB", "Binance Coin"), 
                                                                                                    ("ADA", "Cardano"), 
                                                                                                    ("DOT", "Polkadot"), 
                                                                                                    ("BTC", "Bitcoin"), 
                                                                                                    ("USDT", "Tether"), 
                                                                                                    ("XRP", "Ripple"), 
                                                                                                    ("SOL", "Solana"), 
                                                                                                    ("MATIC", "Polygon")])
    amount_from = FloatField("Cantidad de Origen", validators=[DataRequired("Cantidad obligatoria")])
    currency_to = SelectField("Moneda", validators=[DataRequired("Moneda obligatoria")], choices=[("EUR", "Euros"), 
                                                                                                    ("ETH", "Ethereum"), 
                                                                                                    ("BNB", "Binance Coin"), 
                                                                                                    ("ADA", "Cardano"), 
                                                                                                    ("DOT", "Polkadot"), 
                                                                                                    ("BTC", "Bitcoin"), 
                                                                                                    ("USDT", "Tether"), 
                                                                                                    ("XRP", "Ripple"), 
                                                                                                    ("SOL", "Solana"), 
                                                                                                    ("MATIC", "Polygon")])
    amount_to = HiddenField()

    calculate = SubmitField("Calculate")
    submit = SubmitField("Buy")