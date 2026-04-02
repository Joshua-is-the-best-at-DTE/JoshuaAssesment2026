from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

database = 'Databases/products.db'
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_all_products():
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        sql = "SELECT * FROM products;"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

@app.route("/")
def home():
    products = []
    for item in get_all_products():
        products.append({
            "name": item[0],
            "id": item[2],
            "image": item[3],
            "info": item[5],
            "price": item[4]
        })
    selected_cat = request.args.get('category', 'all').lower()
    products = []
    for item in get_all_products():
        db_keywords = item[1].lower() if item[1] else ""
        if selected_cat == 'all' or selected_cat in db_keywords:
            products.append({
                "name": item[0],
                "id": item[2],
                "image": item[3],
                "info": item[5],
                "price": item[4]
            })
    return render_template("index.html", PRODUCTS = products)

@app.route("/add_to_cart/<int:ID>")
def add_to_cart(ID):
    cart = session.get('cart', {})
    if isinstance(cart, list):
        cart = {}
    str_id = str(ID)
    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1
    session['cart'] = cart
    session.modified = True
    return redirect(request.referrer or url_for('home'))

@app.route("/remove_from_cart/<int:ID>")
def remove_from_cart(ID):
    cart = session.get('cart', {})
    str_id = str(ID)
    if str_id in cart:
        cart.pop(str_id)
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('cart'))

@app.route("/cart")
def cart():
    cart_dict = session.get('cart', {})
    products_in_cart = []
    total_price = 0
    if cart_dict:
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            ids = [int(i) for i in cart_dict.keys()]
            placeholders = ','.join(['?'] * len(ids))
            query = f"SELECT Product_name, Image, Prices, Product_info, Product_ID FROM Products WHERE Product_ID IN ({placeholders})"
            cursor.execute(query, ids)
            results = cursor.fetchall()
            for item in results:
                p_id = str(item[4])
                quantity = cart_dict[p_id]
                price = float(item[2])
                subtotal = price * quantity
                total_price += subtotal
                products_in_cart.append({
                    "name": item[0],
                    "image": item[1],
                    "price": price,
                    "info": item[3],
                    "quantity": quantity,
                    "subtotal": subtotal,
                    "id": item[4]
                })
    return render_template("cart.html", PRODUCTS=products_in_cart, TOTAL="{:.2f}".format(total_price))

@app.route("/increase_quantity/<int:ID>")
def increase_quantity(ID):
    cart = session.get('cart', {})
    str_id = str(ID)
    if str_id in cart:
        cart[str_id] += 1
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route("/decrease_quantity/<int:ID>")
def decrease_quantity(ID):
    cart = session.get('cart', {})
    str_id = str(ID)
    if str_id in cart:
        if cart[str_id] > 1:
            cart[str_id] -= 1
        else:
            cart.pop(str_id)
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart'))

@app.route("/pro2")
def pro2():
    products = []
    for item in get_all_products():
        products.append({
            "name": item[0],
            "image": item[3],
            "info": item[5],
            "price": item[4]
        })
    return render_template("productpage.html", PRODUCTS = products)

@app.route("/pro/<int:ID>")
def pro(ID):
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        cursor.execute("SELECT Product_name, Image, Prices, Product_info, Product_ID FROM Products WHERE Product_ID = ?", (ID,))
        results = cursor.fetchone()
    return render_template("productpage.html", PRODUCT=results)

@app.route("/paid")
def paid():
    return render_template("paid.html")

if __name__ == "__main__":
    app.run(debug=True)