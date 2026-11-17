import os
os.environ["DATABASE_URL"] = "sqlite:///./test_market_prices.db"

from app.database import init_db
from app.ussd import process_ussd

def setup_module():
    init_db()

def test_language_menu():
    assert process_ussd("test-session-1", "").startswith("CON")

def test_english_welcome():
    response = process_ussd("test-session-2", "1")
    assert response.startswith("CON")
    assert "Welcome, Farmer" in response

def test_tomato_prices():
    response = process_ussd("test-session-3", "1*1*1")
    assert response.startswith("END")
    assert "Tomatoes" in response
    assert "Cape Town" in response

def test_swahili_welcome():
    response = process_ussd("test-session-4", "6")
    assert "Karibu" in response

def test_exit():
    response = process_ussd("test-session-5", "1*0")
    assert response.startswith("END")
    assert "Goodbye" in response
