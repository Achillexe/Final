from wallet import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html", title="Movimiento")

@app.route("/purchase")
def new_purchase():
    return render_template("purchase.html", title="Compra de Criptos")

@app.route("/status")
def check_status():
    return render_template("status.html", title="Estado de la Inversión")