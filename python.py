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
        # 1. Get the category from the URL (e.g., ?category=aparel)
    selected_cat = request.args.get('category', 'all').lower()
    
    products = []
    # 2. Loop through all products from your DB
    for item in get_all_products():
        # Based on your image: 
        # item[0]=Name, item[1]=Keywords, item[2]=ID, item[3]=Image, item[4]=Price, item[5]=Info
        db_keywords = item[1].lower() if item[1] else ""

        # 3. Logic: Show if 'all' is picked OR if the category is IN the keywords string
        if selected_cat == 'all' or selected_cat in db_keywords:
            products.append({
                "name": item[0],
                "id": item[2],
                "image": item[3],
                "info": item[5],
                "price": item[4]
            })

    return render_template("index.html", PRODUCTS = products)

@app.route("/cart")
def cart():
    products = []
    for item in get_all_products():
        products.append({
            "name": item[0],
            "image": item[3],
            "info": item[5],
            "price": item[4]
        })

    return render_template("cart.html", PRODUCTS = products)

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
        cursor.execute("SELECT Product_name, Image, Prices, Product_info FROM Products WHERE Product_ID = ?", (ID,))
        results = cursor.fetchone()
    return render_template("productpage.html", PRODUCT = results)

if __name__ == "__main__":
    app.run(debug=True)

