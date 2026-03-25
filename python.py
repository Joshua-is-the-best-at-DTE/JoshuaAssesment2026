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
    cart = session.get('cart', [])
    cart.append(ID)
    session['cart'] = cart
    return redirect(request.referrer or url_for('home'))

@app.route("/remove_from_cart/<int:ID>")
def remove_from_cart(ID):
    cart = session.get('cart', [])
    if ID in cart:
        cart.remove(ID)
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('cart'))

@app.route("/cart")
def cart():
    cart_ids = session.get('cart', [])
    products_in_cart = []
    
    if cart_ids:
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            placeholders = ','.join(['?'] * len(cart_ids))
            query = f"SELECT Product_name, Image, Prices, Product_info, Product_ID FROM Products WHERE Product_ID IN ({placeholders})"
            cursor.execute(query, cart_ids)
            results = cursor.fetchall()
            
            for item in results:
                products_in_cart.append({
                    "name": item[0],
                    "image": item[1],
                    "price": item[2],
                    "info": item[3],
                    "id": item[4]
                })
    total_price = sum(float(item['price']) for item in products_in_cart)

    return render_template("cart.html", PRODUCTS=products_in_cart, TOTAL=total_price)

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