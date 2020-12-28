import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, check_credit_card_number

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM users WHERE id == :user_id", user_id=session["user_id"])
    for dictionary in cash:
        user_cash = dictionary["cash"]
        
    portfolio = db.execute("SELECT symbol, stock, purchaseprice, quantity, totalprice FROM shares WHERE buyerid == :user_id", user_id=session["user_id"])
    profit = []
    current_investments = []
    
    for dictionary in portfolio:
        current_price = lookup(dictionary["symbol"])
        dictionary["current_price"] = current_price["price"]
        
        profit.append(dictionary["current_price"] * dictionary["quantity"])
        current_investments.append(dictionary["totalprice"])
    
    current_profit = sum(profit) - sum(current_investments)
    
    return render_template("index.html", user_cash=usd(user_cash), portfolio=portfolio, profit=usd(current_profit), current_profit=current_profit, current_investments = usd(sum(current_investments)), total_user_cash=usd(sum(profit) + user_cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'POST':
        if not request.form.get("symbol"):
            return apology("must symbol provide", 403)
        if not request.form.get("shares"):
            return apology("must shares provide", 403)
        if request.form.get("shares").isdigit():
            quote = lookup(request.form.get("symbol"))
            if quote != None:
                cash = db.execute("SELECT cash FROM users WHERE id == :user_id", user_id=session["user_id"])
                for dictionary in cash:
                    user_cash = dictionary["cash"]
                symbols = db.execute("SELECT symbol, quantity, totalprice FROM shares WHERE symbol == :symbol AND buyerid == :user_id GROUP BY symbol", symbol=request.form.get("symbol").upper(), user_id=session["user_id"])
                if symbols != []:
                    if quote["price"] * float(request.form.get("shares")) > user_cash:
                        return apology("underfunded", 403)
                    else:
                        for dictionary in symbols:
                            quantity = dictionary["quantity"]
                            totalprice = dictionary["totalprice"]
        
                        current_cash = user_cash - (quote["price"] * float(request.form.get("shares")))
                        db.execute("UPDATE 'users' SET 'cash' = :current_cash WHERE id == :user_id", current_cash=current_cash, user_id=session["user_id"])
                        db.execute("UPDATE 'shares' SET 'quantity' = :quantity, 'totalprice' = :totalprice, datetime = :datetime WHERE symbol == :symbol AND buyerid == :user_id", quantity=quantity+int(request.form.get("shares")), totalprice=totalprice+(quote["price"]*int(request.form.get("shares"))), datetime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), symbol=request.form.get("symbol").upper(), user_id=session["user_id"])
                        db.execute("INSERT INTO 'transactions' ('userid', 'stock', 'symbol', 'quantity', 'price', 'totalprice', 'value', 'datetime') VALUES(:user_id, :stock, :symbol, :quantity, :price, :totalprice, :value, :datetime)", user_id=session["user_id"], stock=quote["name"], symbol=quote["symbol"], quantity=int(request.form.get("shares")), price=quote["price"], totalprice=quote["price"]*float(request.form.get("shares")), value="bought", datetime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
                        return redirect("/")
                else:
                    if quote["price"] * float(request.form.get("shares")) > user_cash:
                        return apology("underfunded", 403)
                    else:
                        current_cash = user_cash - (quote["price"] * float(request.form.get("shares")))
                        db.execute("UPDATE 'users' SET 'cash' = :current_cash WHERE id == :user_id", current_cash=current_cash, user_id=session["user_id"])
                        db.execute("INSERT INTO 'shares' ('buyerid', 'symbol', 'stock', 'purchaseprice', 'quantity', 'totalprice', 'datetime') VALUES(:buyerid, :symbol, :stock, :purchaseprice, :quantity, :totalprice, :datetime)", buyerid=session["user_id"], symbol=quote["symbol"], stock=quote["name"], purchaseprice=quote["price"], quantity=int(request.form.get("shares")), totalprice=quote["price"]*float(request.form.get("shares")), datetime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
                        db.execute("INSERT INTO 'transactions' ('userid', 'stock', 'symbol', 'quantity', 'price', 'totalprice', 'value', 'datetime') VALUES(:user_id, :stock, :symbol, :quantity, :price, :totalprice, :value, :datetime)", user_id=session["user_id"], stock=quote["name"], symbol=quote["symbol"], quantity=int(request.form.get("shares")), price=quote["price"], totalprice=quote["price"]*float(request.form.get("shares")), value="bought", datetime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
                        return redirect("/")
            else:
                return apology("not found symbol", 403)
        else:
            return apology("must shares positive num", 403)
    else:
        return render_template("buy.html")

"""
@app.route("/check", methods=["GET"])
def check():
    #Return true if username available, else false, in JSON format
    return jsonify("TODO")
"""

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM 'transactions' WHERE userid == :user_id", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == 'POST':
        if not request.form.get("symbol"):
            return apology("must symbol provide", 403)
        else:
            quote = lookup(request.form.get("symbol"))
            if quote != None:
                return render_template("quoted.html", quote=quote)
            else:
                return apology("not found symbol", 403)
    else:
        return render_template("quote.html")
        

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        if not request.form.get("password"):
            return apology("must provide password", 403)
        if not request.form.get("confirmation") or request.form.get("password") != request.form.get("confirmation"):
            return apology("must confirm password", 403)
        else:
            rows = db.execute("SELECT :username FROM users", username=request.form.get("username"))
            if rows != []:
                return apology("username already exists", 403)
            else:
                hash_password = generate_password_hash(request.form.get("password"))
                db.execute("INSERT INTO 'users' ('username', 'hash') VALUES(:name, :hash_password)", name=request.form.get("username"), hash_password=hash_password)
                return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("shares"):
            return apology("must provide shares", 403)
        if request.form.get("shares").isdigit():
            if int(request.form.get("shares")) >= 1:
                sell_stock = db.execute("SELECT stock, symbol, quantity, totalprice FROM shares WHERE stock == :stock AND buyerid == :user_id", stock=request.form.get("symbol"), user_id=session["user_id"])
                for dictionary in sell_stock:
                    quantity = dictionary["quantity"]
                    totalprice = dictionary["totalprice"]
                    quote = lookup(dictionary["symbol"])
                cash = db.execute("SELECT cash FROM users WHERE id == :user_id", user_id=session["user_id"])
                for dictionary in cash:
                    user_cash = dictionary["cash"]
                if int(request.form.get("shares")) > quantity:
                    return apology("you do not have that many shares", 403)
                if int(request.form.get("shares")) == quantity:
                    db.execute("DELETE FROM shares WHERE stock == :stock", stock=request.form.get("symbol"))
                    current_cash = user_cash + (quote["price"] * float(request.form.get("shares")))
                    db.execute("UPDATE 'users' SET 'cash' = :current_cash WHERE id == :user_id", current_cash=current_cash, user_id=session["user_id"])
                    db.execute("INSERT INTO 'transactions' ('userid', 'stock', 'symbol', 'quantity', 'price', 'totalprice', 'value', 'datetime') VALUES(:user_id, :stock, :symbol, :quantity, :price, :totalprice, :value, :datetime)", user_id=session["user_id"], stock=quote["name"], symbol=quote["symbol"], quantity=int(request.form.get("shares")), price=quote["price"], totalprice=quote["price"]*float(request.form.get("shares")), value="sold", datetime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
                    return redirect("/")
                else:
                    current_cash = user_cash + (quote["price"] * float(request.form.get("shares")))
                    db.execute("UPDATE 'shares' SET 'quantity' = :quantity, totalprice = :totalprice WHERE buyerid == :user_id AND stock == :sell_stock", quantity=quantity-int(request.form.get("shares")), totalprice=totalprice-(quote["price"]*int(request.form.get("shares"))), user_id=session["user_id"], sell_stock=request.form.get("symbol"))
                    db.execute("UPDATE 'users' SET 'cash' = :current_cash WHERE id == :user_id", current_cash=current_cash, user_id=session["user_id"])
                    db.execute("INSERT INTO 'transactions' ('userid', 'stock', 'symbol', 'quantity', 'price', 'totalprice', 'value', 'datetime') VALUES(:user_id, :stock, :symbol, :quantity, :price, :totalprice, :value, :datetime)", user_id=session["user_id"], stock=quote["name"], symbol=quote["symbol"], quantity=int(request.form.get("shares")), price=quote["price"], totalprice=quote["price"]*float(request.form.get("shares")), value="sold", datetime=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
                    return redirect("/")
            else:
                return apology("must provide positive number and not null", 403)
        else:
            return apology("must shares positive number", 403)
    else:
        stocks = db.execute("SELECT stock FROM shares WHERE buyerid == :user_id GROUP BY stock", user_id=session["user_id"])
        print(stocks)
        return render_template("sell.html", stocks=stocks)
   
        
@app.route("/cash_in", methods=["GET", "POST"])
@login_required
def cash_in():
    """Cash in"""
    if request.method == "POST":
        if not request.form.get("amount"):
            return apology("must provide amount", 403)
        if not request.form.get("credit_card_number"):
            return apology("must provide credit card number", 403)
        else:
            if request.form.get("amount").isdigit() and float(request.form.get("amount")) >= 1:
                master_card = ['51', '52', '53', '54', '55']
                cash = db.execute("SELECT cash FROM users WHERE id == :user_id", user_id=session["user_id"])
                for dictionary in cash:
                    user_cash = dictionary["cash"]
                    
                if request.form.get("credit_card_number")[:2] == '34' or request.form.get("credit_card_number")[:2] == '37':
                    if len(request.form.get("credit_card_number")) == 15:
                        if check_credit_card_number(request.form.get("credit_card_number")) == True:
                            db.execute("UPDATE users SET cash = :cash_in WHERE id == :user_id", cash_in=user_cash+float(request.form.get("amount")), user_id=session["user_id"])
                            return redirect("/")
                        else:
                            return apology("invalid AMEX card number", 403)
                    else:
                        return apology("invalid AMEX card number", 403)
                if request.form.get("credit_card_number")[:2] in master_card:
                    if len(request.form.get("credit_card_number")) == 16:
                        if check_credit_card_number(request.form.get("credit_card_number")) == True:
                            db.execute("UPDATE users SET cash = :cash_in WHERE id == :user_id", cash_in=user_cash+float(request.form.get("amount")), user_id=session["user_id"])
                            return redirect("/")
                        else:
                            return apology("invalid MasterCard card number", 403)
                    else:
                        return apology("invalid MasterCard card number", 403)
                if request.form.get("credit_card_number")[:1] == '4':
                    if len(request.form.get("credit_card_number")) == 13 or len(request.form.get("credit_card_number")) == 16:
                        if check_credit_card_number(request.form.get("credit_card_number")) == True:
                            db.execute("UPDATE users SET cash = :cash_in WHERE id == :user_id", cash_in=user_cash+float(request.form.get("amount")), user_id=session["user_id"])
                            return redirect("/")
                        else:
                            return apology("invalid Visa card number", 403)
                    else:
                        return apology("invalid Visa card number", 403)
                else:
                    return apology("invalid card number", 403)
            else:
                return apology("must provide positive number", 403)
    else:
        return render_template("cash_in.html")
        

@app.route("/cash_out", methods=["GET", "POST"])
@login_required
def cash_out():
    """Cash out"""
    if request.method == "POST":
        if not request.form.get("amount"):
            return  apology("must provide amount", 403)
        if not request.form.get("credit_card_number"):
            return apology("must provide credit card number", 403)
        else:
            if request.form.get("amount").isdigit() and float(request.form.get("amount")) >= 1:
                cash = db.execute("SELECT cash FROM users WHERE id == :user_id", user_id=session["user_id"])
                for dictionary in cash:
                    user_cash = dictionary["cash"]
                if float(request.form.get("amount")) <= user_cash:
                    master_card = ['51', '52', '53', '54', '55']
                    if request.form.get("credit_card_number")[:2] == '34' or request.form.get("credit_card_number")[:2] == '37':
                        if len(request.form.get("credit_card_number")) == 15:
                            if check_credit_card_number(request.form.get("credit_card_number")) == True:
                                db.execute("UPDATE users SET cash = :cash_in WHERE id == :user_id", cash_in=user_cash-float(request.form.get("amount")), user_id=session["user_id"])
                                return redirect("/")
                            else:
                                return apology("invalid AMEX card number", 403)
                        else:
                            return apology("invalid AMEX card number", 403)
                    if request.form.get("credit_card_number")[:2] in master_card:
                        if len(request.form.get("credit_card_number")) == 16:
                            if check_credit_card_number(request.form.get("credit_card_number")) == True:
                                db.execute("UPDATE users SET cash = :cash_in WHERE id == :user_id", cash_in=user_cash-float(request.form.get("amount")), user_id=session["user_id"])
                                return redirect("/")
                            else:
                                return apology("invalid MasterCard card number", 403)
                        else:
                            return apology("invalid MasterCard card number", 403)
                    if request.form.get("credit_card_number")[:1] == '4':
                        if len(request.form.get("credit_card_number")) == 13 or len(request.form.get("credit_card_number")) == 16:
                            if check_credit_card_number(request.form.get("credit_card_number")) == True:
                                db.execute("UPDATE users SET cash = :cash_in WHERE id == :user_id", cash_in=user_cash-float(request.form.get("amount")), user_id=session["user_id"])
                                return redirect("/")
                            else:
                                return apology("invalid Visa card number", 403)
                        else:
                            return apology("invalid Visa card number", 403)
                    else:
                        return apology("invalid card number", 403)
                else:
                    return apology("underfunded", 403)
            else:
                return apology("must provide positive number", 403)
    else:
        return render_template("cash_out.html")
        
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""
    if request.method == "POST":
        password = db.execute("SELECT hash FROM users WHERE id == :user_id", user_id=session["user_id"])
        for dictionary in password:
            user_password = dictionary["hash"]
        if not request.form.get("old_password"):
            return apology("must provide old password", 403)
        if not request.form.get("new_password"):
            return apology("must provide new password", 403)
        if not request.form.get("confirm_new_password") or request.form.get("new_password") != request.form.get("confirm_new_password"):
            return apology("must confirm new password", 403)
        if check_password_hash(user_password, request.form.get("old_password")) == True:
            db.execute("UPDATE 'users' SET 'hash' = :new_password WHERE id == :user_id", new_password=generate_password_hash(request.form.get("new_password")), user_id=session["user_id"])
            return redirect("/login")
        else:
            return apology("invalid old password", 403)
    else:
        return render_template("change_password.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
