import os

from flask import Flask, g, jsonify, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from time import gmtime, strftime
import time
from helpers import login_required, register_db_name, SQL
import shutil

# Configure application
app = Flask(__name__)

# State the database name
register_db_name('eshop.db')


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
    query = """SELECT * FROM products WHERE active = "True" AND category = "Laptops" """
    laptops = SQL(query, )
    query = """SELECT * FROM products WHERE active = "True" AND category = "Smartphones" """
    smartphones = SQL(query, )
    return render_template('index.html', smartphones=smartphones, laptops=laptops)


@app.route('/product/<int:product_id>')
def product(product_id):
    query = """SELECT * FROM products WHERE id = ? AND active = "True" """
    product = SQL(query, (product_id,))[0]
    return render_template('product.html', product=product)


@app.route('/update_cart', methods=["POST"])
def update_cart():
    if 'user_id' not in session:
        return "not_logged_in"
    product_id = int(request.form.get('productId'))
    action = request.form.get('action')
    if (action == 'delete'):
        query = """ DELETE FROM cart
                    WHERE user_id = ? AND product_id = ?"""
        SQL(query, (session["user_id"], product_id,))
        for i in range(len(session['cart'])):
            if session['cart'][i]['id'] == product_id:
                del session['cart'][i]
                break
        return "Cart updated successfully!"

    if (action == 'increase'):
        change = 1
    elif (action == 'decrease'):
        change = -1
    query = """SELECT quantity FROM cart
                WHERE user_id = ? AND product_id = ?"""
    quantity = (SQL(query, (session["user_id"], product_id,)))[0][0]
    query = """UPDATE cart SET quantity = ?
                WHERE user_id = ? AND product_id = ?"""
    quantity += change
    SQL(query, (quantity, session["user_id"], product_id,))
    for i in range(len(session['cart'])):
        if session['cart'][i]['id'] == product_id:
            session['cart'][i]['quantity'] = quantity

    return "Cart updated successfully!"


@app.route('/cart', methods=["GET", "POST"])
def cart():
    # Add a product to the cart
    if request.method == "POST":
        if 'user_id' not in session:
            return "not_logged_in"
        product_id = int(request.form.get('jsdata'))
        query = """SELECT title, price, img_route FROM products WHERE id = ? AND active = "True" """
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
                if session['cart'][i]['id'] == product_id:
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
                'img_route': product_info[2]
            })
        updated_cart = session.get('cart', [])
        return {
            "message": "Product added to cart successfully!",
            "cart": updated_cart}

    if 'user_id' not in session:
        return redirect('/login')
    shipping_cost = 9.99
    total_cost = shipping_cost
    for i in range(len(session['cart'])):
        total_cost += session['cart'][i]['quantity'] * session['cart'][i]['price']
    return render_template('cart.html', total_cost=total_cost, shipping_cost=shipping_cost)


@app.route('/category/<category>')
def category(category):
    query = """SELECT * FROM products WHERE category = ? AND active = "True" """
    products = SQL(query, (category,))
    print(products)
    return render_template('category.html', products=products)


@app.route('/orders')
def orders():
    query = """SELECT * FROM orders WHERE user_id = ? """
    orders = (SQL(query, (session['user_id'],)))

    query = """SELECT P.img_route, P.title, OP.quantity, P.price FROM orderss_products AS OP, products AS P
                WHERE OP.order_id = ? AND
                      OP.product_id = P.id AND
                      active = "True"
            """
    products = {}
    for order in orders:
        order_id = order['id']
        products[order_id] = SQL(query, (order_id,))
    return render_template('orders.html', orders=orders, products=products)


@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect('/login')
    the_date = strftime("%a, %d %b %Y %H:%M:%S",
                        time.localtime())
    shipping_cost = request.args.get("shipping_cost")
    total_cost = request.args.get("total_cost")
    query = """INSERT INTO orders (user_id, the_date, shipping_cost, total_cost) VALUES(?, ?, ?, ?)"""
    SQL(query, (session['user_id'], the_date, shipping_cost, total_cost,))
    query = """SELECT id FROM orders WHERE the_date = ?"""
    order_id = (SQL(query, (the_date,)))[0][0]
    for product in session['cart']:
        query = """INSERT INTO orderss_products (order_id, product_id, quantity) VALUES(?, ?, ?)"""
        SQL(query, (order_id, product['id'], product['quantity']))

    query = """DELETE FROM CART WHERE user_id = ?"""
    SQL(query, (session['user_id'],))
    session['cart'].clear()
    flash("Order successful!")
    return redirect('/')


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
            flash("All fields must be filled")
            return redirect("/login")
        if confirmation != password:
            flash("Password and confirmation must match")
            return redirect("/login")

        query = """INSERT INTO users (username, hash, access) VALUES(?, ?, ?)"""
        SQL(query, (username, generate_password_hash(password), "user",))
        flash("Registration successful!")
        return redirect("/login")
    else:
        return render_template("register.html")


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
            flash("You must provide username")
            return redirect("/")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("You must provide the password")
            return redirect("/")

        query = """SELECT * FROM users WHERE username = ?"""
        rows = SQL(query, (username,))

        # Ensure username exists and password is correct
        if not check_password_hash(
                rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/or password")
            return redirect("/")

        # Remember which user has logged in
        session['username'] = request.form.get("username")
        session["user_id"] = rows[0]["id"]
        session["cart"] = []
        query = """SELECT product_id, quantity FROM cart
                    WHERE user_id = ?"""
        id_quantity = SQL(query, (session["user_id"], ))
        for i in range(len(id_quantity)):
            query = """SELECT title, price, img_route FROM products WHERE id = ? AND active = "True" """
            product_info = (SQL(query, (id_quantity[i][0],)))[0]
            session['cart'].append({
                'id': id_quantity[i][0],
                'title': product_info[0],
                'price': product_info[1],
                'quantity': id_quantity[i][1],
                'img_route': product_info[2]
            })
        flash("login successful!")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    # Redirect user to login form
    flash('Logged out successfully.')
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
