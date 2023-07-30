from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, HiddenField, ValidationError
from wtforms.validators import DataRequired
from wallet.models import *

def validate_from(form, field):
    if field.data not in CURRENCIES:
        raise ValidationError("Moneda de origen inválida")
    
def validate_amount(form, field):
    if field.data <= 0:
        raise ValidationError("Cantidad debe ser mayor a 0")

def validate_to(form, field):
    if field.data not in CURRENCIES:
        raise ValidationError("Moneda de destino inválida")
    if field.data == form.currency_from.data:
        raise ValidationError("La moneda de origen debe ser distinta a la de destino")

class MovementForm(FlaskForm):
    currency_from = SelectField("From", validators=[DataRequired("Moneda obligatoria"), validate_from], choices=[("EUR", "Euros"), 
                                                                                                                    ("ETH", "Ethereum"), 
                                                                                                                    ("BNB", "Binance Coin"), 
                                                                                                                    ("ADA", "Cardano"), 
                                                                                                                    ("DOT", "Polkadot"), 
                                                                                                                    ("BTC", "Bitcoin"), 
                                                                                                                    ("USDT", "Tether"), 
                                                                                                                    ("XRP", "Ripple"), 
                                                                                                                    ("SOL", "Solana"), 
                                                                                                                    ("MATIC", "Polygon")])
    
    amount_from = FloatField("Q", validators=[DataRequired("Cantidad obligatoria"), validate_amount])
    
    currency_to = SelectField("To", validators=[DataRequired("Moneda obligatoria"), validate_to], choices=[("EUR", "Euros"), 
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
    operation = HiddenField()

    calculate = SubmitField("Calculate")
    submit = SubmitField("Buy")