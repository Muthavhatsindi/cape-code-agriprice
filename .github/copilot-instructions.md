# African Farmer Market USSD

Build a multilingual USSD service that helps African farmers check and compare agricultural market prices using basic mobile phones.

## Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite for hackathon MVP
- Pytest
- Browser-based USSD simulator
- Africa's Talking form-encoded USSD callback

## Languages
English (en), isiZulu (zu), isiXhosa (xh), Sesotho (st), Afrikaans (af), Kiswahili (sw).
Translations live in app/languages/*.json. Use native-speaker reviewed translations for production.

## Engineering rules
- Keep USSD flow, translation, market service and persistence separate.
- Use type hints and parameterised ORM queries.
- Never claim seeded demo prices are live or verified.
- Keep market, commodity, currency, unit, timestamp and verification status together.
- Return CON to continue and END to terminate.
- USSD text is cumulative across a session.
- Add pytest tests for changes.
- Avoid logging full phone numbers or personal information.
- Validate user inputs and provide English fallback for missing translations.
