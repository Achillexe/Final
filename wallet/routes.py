from wallet import app
from flask import render_template, flash, request, redirect
from wallet.models import *
from wallet.forms import MovementForm

CURRENCIES = ["EUR", "BTC"]

dao = MovementDAO(app.config["PATH_SQLITE"])

@app.route("/")
def index():
    try:
        movements = dao.get_all()
        return render_template("index.html", mvm=movements, route=request.path)
    except ValueError as e:
        flash("Su base de datos no está operativa")
        flash(str(e))
        return render_template("index.html", mvm=movements, route=request.path)
    
@app.route("/purchase", methods=["GET", "POST"])
def purchase():
    form = MovementForm()

    if request.method == "GET":
        return render_template("purchase.html", form = form, route=request.path)
    
    else:
        
        if form.validate():
            try:
                
                if form.calculate.data:
                    form.amount_to.data = Exchange(form.amount_from.data, form.currency_from.data, form.currency_to.data).amount_to
                    form.operation.data = f"{form.currency_from.data};{form.amount_from.data};{form.currency_to.data};{form.amount_to.data}"
                    return render_template("purchase.html", form=form, route=request.path)
                
                elif form.operation.data != f"{form.currency_from.data};{form.amount_from.data};{form.currency_to.data};{form.amount_to.data}":
                    flash("La operación ha sido modificada")
                    return render_template("purchase.html", form=form, route=request.path)
                
                else:
                    validation = dao.validate(form.currency_from.data, form.currency_to.data)
                    balance = dao.balance(form.amount_from.data, form.currency_from.data)
                    
                    if form.submit.data and validation and balance:
                        dao.purchase(Movement(form.currency_from.data, form.amount_from.data, form.currency_to.data, form.amount_to.data))
                        return redirect("/")

            except ValueError as e:
                flash(str(e))
                return render_template("purchase.html", form=form, route=request.path)
        
        else:
            return render_template("purchase.html", form=form, route=request.path)

@app.route("/status")
def check():
    try:
        wallet = Wallet()
        if wallet:
            status = wallet.wallet
            value = wallet.value
            price = wallet.price
            earnings = wallet.earnings
            return render_template("status.html", status=status, value=value, price=price, earnings=earnings, route=request.path)

    except ValueError as e:
        flash(str(e))
        return render_template("status.html", route=request.path)