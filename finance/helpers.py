import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
         return None

def check_credit_card_number(num_card):
	num_card_l = list(num_card)
	int_num_card = []
	int_num_card_1 = []
	int_num_card_2 = []
	for x in num_card_l:
		int_num_card.append(int(x))
	int_num_card.reverse()
	for x in int_num_card[1:len(int_num_card):2]:
		x = x * 2
		if x > 9:
			x = list(str(x))
			for y in x:
				int_num_card_1.append(int(y))
		else:
			int_num_card_1.append(x)
	for x in int_num_card[0:len(int_num_card):2]:
		int_num_card_2.append(x)
	add = sum(int_num_card_1) + sum(int_num_card_2)
	if add % 10 == 0:
		return True
	else:
		return False


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
