import sqlite3

db = sqlite3.connect('products.db')
cursor = db.cursor()
sql = "SELECT * FROM ;"
cursor.execute(sql)
results = cursor.fetchall()
print(results)

db.close