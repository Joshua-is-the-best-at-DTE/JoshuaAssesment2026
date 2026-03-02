from flask import Flask, render_template, request
import sqlite3

database = 'Databases/products.db'
app = Flask(__name__)

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
            "image": item[3],
            "info": item[5],
            "price": item[4]
        })

    return render_template("index.html", PRODUCTS = products)

if __name__ == "__main__":
    app.run(debug=True)