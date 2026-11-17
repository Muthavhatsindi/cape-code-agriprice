from app.database import get_prices, get_best_price

COMMODITIES = {
    "1": "Tomatoes",
    "2": "Maize",
    "3": "Potatoes",
}

def prices_for(commodity: str):
    return get_prices(commodity)

def best_price_for(commodity: str):
    return get_best_price(commodity)
