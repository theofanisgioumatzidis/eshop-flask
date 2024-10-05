import os

from flask import Flask, g, jsonify, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, euro, register_db_name, SQL

# Configure application
app = Flask(__name__)

# State the database name
register_db_name('eshop.db')

# Custom filter
app.jinja_env.filters["euro"] = euro

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    print(session['cart'][0])
    query = """SELECT * FROM products"""
    products = SQL(query, ())
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product(product_id):
    try:
        username = session["username"]
    except:
        username = ""
    query = """SELECT * FROM products WHERE id = ?"""
    product = SQL(query, (product_id,))[0]
    return render_template('product.html', product=product, username=username)

@app.route('/cart', methods=["GET", "POST"])
def cart():
    if session.get("user_id") is None:
        return jsonify({'message': 'Failed to add product to cart. Login first.','color': 'red'})

    # Add a product to the cart
    if request.method == "POST":
        product_id = int(request.form.get('jsdata'))
        print(product_id)
        query = """SELECT title, price, img_route FROM products WHERE id = ?"""
        product_info = (SQL(query, (product_id,)))[0]
        quantity = 1

        try:
            query = """SELECT quantity FROM cart
                    WHERE user_id = ? AND product_id = ?"""
            quantity = (SQL(query, (session["user_id"], product_id,)))[0][0]
            query = """UPDATE cart SET quantity = ?
                    WHERE user_id = ? AND product_id = ?"""
            quantity += 1
            SQL(query, (quantity, session["user_id"], product_id,))
            for i in range(len(session['cart'])):
                if session['cart'][i]['id'] == product_id :
                    session['cart'][i]['quantity'] += 1
        except:
            query = """INSERT INTO cart (user_id, product_id, quantity)
                    VALUES (?,?,?)"""
            SQL(query, (session["user_id"], product_id, quantity,))
            session['cart'].append({
                        'id': product_id,
                        'title': product_info[0],
                        'price': product_info[1],
                        'quantity': quantity,
                        'img_route': product_info[1]
                    })
        # flash('Product added successfully.')
        # Return a response
        return "Product added to cart successfully!"

    try:
        username = session["username"]
    except:
        username = ""
    return render_template('cart.html', cart=session['cart'], username=username)


@app.route('/smartphones')
def smartphones():
    return render_template('product.html', product=product_info)

@app.route('/laptops')
def laptops():
    return render_template('product.html', product=product_info)

@app.route('/buy')
def buy():
    return render_template('product.html', product=product_info)

@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        username = session["username"]
        return redirect('/')
    except:
        pass
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Validate submission
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            return apology("All fields must be filled")
        if confirmation != password:
            return apology("Password and confirmation must match")

        try:
            # Remember registrant
            query = """INSERT INTO users (username, hash, access) VALUES(?, ?, ?)"""
            SQL(query, (username, generate_password_hash(password),"user",))
        except:
            return apology("Name already in use from another user")
        flash("Registration successful!")
        return redirect("/login")
    else:
        try:
            username = session["username"]
        except:
            username = ""
        return render_template("register.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        username = session["username"]
        return redirect('/')
    except:
        pass

    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        query = """SELECT * FROM users WHERE username = ?"""
        rows = SQL(query, (username,))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session['username'] = request.form.get("username")
        session["user_id"] = rows[0]["id"]
        session["cart"] = []
        query = """SELECT product_id, quantity FROM cart
                    WHERE user_id = ?"""
        id_quantity = SQL(query, (session["user_id"], ))
        for i in range(len(id_quantity)):
            query = """SELECT title, price, img_route FROM products WHERE id = ?"""
            product_info = (SQL(query, (id_quantity[i][0],)))[0]
            session['cart'].append({
                        'id': id_quantity[i][0],
                        'title': product_info[0],
                        'price': product_info[1],
                        'quantity': id_quantity[i][1],
                        'img_route': product_info[2]
                    })
        # Redirect user to home page
        flash(
            f"login successful!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        try:
            username = session["username"]
        except:
            username = ""
        return render_template("login.html", username=username)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash('Logged out successfully.')
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
