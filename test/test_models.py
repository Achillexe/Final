from wallet.models import Movement, MovementDAO
import os
import sqlite3
import pytest
from datetime import datetime


# class Movement Tests:
def test_create_movement():
    m = Movement("EUR", 50, "BTC", 3.234234234)
    assert m.currency_from == "EUR"
    assert m.amount_from == 50.0
    assert m.currency_to == "BTC"
    assert m.amount_to == 3.234234234
def test_fails_if_amount_zero():
    with pytest.raises(ValueError):
        m = Movement("EUR", 0, "BTC", 3.234234234)
    with pytest.raises(ValueError):
        m = Movement("EUR", 50, "BTC", 0)
def test_fails_if_amount_changes_to_zero():
    m = Movement("EUR", 50, "BTC", 3.234234234)
    with pytest.raises(ValueError):
        m.amount_from = 0
        m.amount_to = 0
def test_converts_to_float():
    m = Movement("EUR", "50", "BTC", 3.234234234)
    m = Movement("EUR", 50, "BTC", "3.234234234")
    assert m.amount_from == 50.0
    assert m.amount_to == 3.234234234
def test_fails_if_currency_not_in_currencies():
    with pytest.raises(ValueError):
        m = Movement("ARG", "50", "BTC", 3.234234234)
        m = Movement("EUR", "50", "XML", 3.234234234)
def test_fails_if_currency_changes_not_in_currencies():
    m = Movement("EUR", 50, "BTC", 3.234234234)
    with pytest.raises(ValueError):
        m.currency_from = "ARG"
        m.currency_to = "XML"
def test_date_is_today():
    m = Movement("EUR", 50, "BTC", 3.234234234)
    #Test it manually:
    assert m.current_date == "2023-07-09"
    #Test it with datetime module:
    today = datetime.now().date().strftime("%Y-%m-%d")
    assert m.current_date == today
def test_time_is_now():
    m = Movement("EUR", 50, "BTC", 3.234234234)
    time = datetime.now().time().strftime("%H:%M:%S")
    assert m.current_time == time
def test_datetime_attribute_changes():
    m = Movement("EUR", 50, "BTC", 3.234234234)
    m.current_date = "2022-04-03"
    m.current_time = "12:23:54"
    assert m.current_date == "2022-04-03"
    assert m.current_time == "12:23:54"

# class MovementDAO Tests:
def test_create_dao():
    path = "data/test_db.db"
    if os.path.exists(path):
        os.remove(path)

    dao = MovementDAO(path)

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT * from movements")
    
    assert cursor.fetchall() == []

