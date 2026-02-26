import sqlite3

database = 'Databases/products.db'

def print_all_products():
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        sql = "SELECT * FROM products;"
        cursor.execute(sql)
        results = cursor.fetchall()
        for Product_name in results:
            print(f'Product name: {Product_name[0]} - Price: ${Product_name[4]}.00')

if __name__ == "__main__":
    print_all_products()