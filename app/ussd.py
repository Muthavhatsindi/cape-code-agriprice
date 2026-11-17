from datetime import datetime
from app.database import SessionLocal, USSDSession
from app.language_service import translate, SUPPORTED_LANGUAGES
from app.market_service import COMMODITIES, prices_for, best_price_for

def _session_language(session_id: str):
    with SessionLocal() as db:
        return db.get(USSDSession, session_id)

def _set_language(session_id: str, language: str):
    with SessionLocal() as db:
        row = db.get(USSDSession, session_id)
        if row is None:
            row = USSDSession(session_id=session_id, language=language)
            db.add(row)
        else:
            row.language = language
        db.commit()

def _format_price(row, language, key="price_line"):
    return translate(
        language, key, market=row.market_name, price=f"{row.price:.2f}",
        currency=row.currency, unit=row.unit
    )

def process_ussd(session_id: str, text: str) -> str:
    """Process cumulative Africa's Talking USSD text and return CON/END response."""
    parts = [p for p in (text or "").split("*") if p != ""]

    # First interaction: show language menu.
    if not parts:
        return "CON " + translate("en", "choose_language")

    # First input chooses language.
    language = SUPPORTED_LANGUAGES.get(parts[0])
    if language is None:
        return "END " + translate("en", "invalid")
    _set_language(session_id, language)

    # Language selected; show home menu.
    if len(parts) == 1:
        return "CON " + translate(language, "welcome")

    action = parts[1]

    if action == "0":
        return "END " + translate(language, "goodbye")

    if action == "4":
        if len(parts) == 2:
            return "CON " + translate(language, "change_language")
        new_language = SUPPORTED_LANGUAGES.get(parts[2])
        if new_language:
            _set_language(session_id, new_language)
            return "CON " + translate(new_language, "welcome")
        return "CON " + translate(language, "invalid")

    if action not in {"1", "2", "3"}:
        return "CON " + translate(language, "invalid") + "\n" + translate(language, "welcome")

    # Ask for commodity.
    if len(parts) == 2:
        key = "choose_compare" if action == "2" else "choose_commodity"
        return "CON " + translate(language, key)

    commodity = COMMODITIES.get(parts[2])
    if commodity is None:
        return "CON " + translate(language, "invalid") + "\n" + translate(language, "choose_commodity")

    rows = prices_for(commodity)
    if not rows:
        return "END " + translate(language, "no_prices")

    if action == "3":
        best = best_price_for(commodity)
        body = translate(language, "best_title", commodity=commodity)
        body += "\n" + _format_price(best, language, "best_line")
    else:
        title_key = "compare_title" if action == "2" else "prices_title"
        body = translate(language, title_key, commodity=commodity)
        for row in rows[:3]:
            body += "\n" + _format_price(row, language)
    body += "\n" + translate(language, "demo_notice")
    body += "\n" + translate(language, "help")
    return "END " + body
