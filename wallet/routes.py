from wallet import app
from flask import render_template, flash, request, redirect
from wallet.models import *
from wallet.forms import MovementForm

dao = MovementDAO(app.config["PATH_SQLITE"])

@app.route("/")
def index():
    movements = dao.get_all()
    return render_template("index.html", mvm=movements, title = "Todos")
    
@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    form = MovementForm()

    if request.method == "GET":
        return render_template("purchase.html", the_form = form, title = "Compra de Crypto")
    else:
        try:
            if form.calculate.data:
                form.amount_to.data = Exchange(form.amount_from.data, form.currency_from.data, form.currency_to.data).amount_to
                return render_template("purchase.html", the_form = form, title= "Compra de Crypto")
            else:
                if form.submit.data:
                    dao.purchase(Movement(form.currency_from.data, form.amount_from.data, form.currency_to.data, form.amount_to.data))
                    return redirect("/")

        except ValueError as e:
            flash(str(e))
            return render_template("purchase.html", the_form=form, title="Compra de Crypto")

@app.route("/status")
def check():
    status = dao.wallet()
    value = dao.value
    price = dao.price
    earnings = dao.earnings
    return render_template("status.html", status=status, value=value, price=price, earnings=earnings, title="Estado de la Inversión")