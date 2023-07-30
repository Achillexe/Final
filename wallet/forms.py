from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length
from wallet.models import *

dao = MovementDAO(app.config["PATH_SQLITE"])

def validate_from(form, field):
    if "Not a valid choice." in field.errors:
        field.errors.remove("Not a valid choice.")
    if field.data not in CURRENCIES:
        raise ValidationError("Moneda de origen inválida")
    
def validate_amount(form, field):
    if field.data <= 0:
        raise ValidationError("Cantidad debe ser mayor a 0")

def validate_to(form, field):
    if "Not a valid choice." in field.errors:
        field.errors.remove("Not a valid choice.")
    if field.data not in CURRENCIES:
        raise ValidationError("Moneda de destino inválida")
    if field.data == form.currency_from.data:
        raise ValidationError("La moneda de origen debe ser distinta a la de destino")
    
def choose_from(field):
    data = dao.get_permitted_currency_from()
    if not data:
        return [("EUR", "Euros")]
    else:
        choices = [("EUR", "Euros")]
        for currency in data:
            if currency == "ETH":
                choices.append((currency, "Ethereum"))
            elif currency == "BNB":
                choices.append((currency, "Binance Coin"))
            elif currency == "ADA":
                choices.append((currency, "Cardano"))
            elif currency == "DOT":
                choices.append((currency, "Polkadot"))
            elif currency == "BTC":
                choices.append((currency, "Bitcoin"))
            elif currency == "USDT":
                choices.append((currency, "Tether"))
            elif currency == "XRP":
                choices.append((currency, "Ripple"))
            elif currency == "SOL":
                choices.append((currency, "Solana"))
            elif currency == "MATIN":
                choices.append((currency, "Poligon"))

        return choices

class MovementForm(FlaskForm):
    currency_from = SelectField("From", validators=[DataRequired("Moneda obligatoria"), validate_from])
    
    amount_from = FloatField("Q From", validators=[DataRequired("Cantidad obligatoria"), validate_amount])
    
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
    amount_to = HiddenField("Q To")
    operation = HiddenField()

    calculate = SubmitField("Calculate")
    submit = SubmitField("Buy")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currency_from.choices = choose_from(self.currency_from)