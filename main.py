from flask import Flask,render_template,request
import json
import sqlite3
from sqlite3 import Error
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
conn = create_connection('progdb.db')
table_creator = "CREATE TABLE IF NOT EXISTS drugs(name VARCHAR(246), brand VARCHAR(246), date DATE, price FLOAT, quantity FLOAT, PRIMARY KEY(name,brand))"
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
execute_query(conn,table_creator)

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/getall',methods=['GET'])
def showall():
    conn = create_connection('progdb.db')
    cursor = conn.cursor()
    try:
        table_creator = "CREATE TABLE IF NOT EXISTS drugs(name VARCHAR(246), brand VARCHAR(246), date DATE, price FLOAT, quantity FLOAT, PRIMARY KEY(name,brand))"
        cursor.execute(table_creator)
        conn.commit()
    except:
        print("ERROR")
    query = "SELECT * FROM drugs ORDER BY name"
    cursor.execute(query)
    ans = cursor.fetchall()
    return json.dumps(ans)

@app.route('/sendinfo/<string:details>',methods=['POST','GET'])
def processdetails(details):
    err = ''
    conn = create_connection('progdb.db')
    if request.method == 'GET':
        details = json.loads(details)
        print(details)
        cursor = conn.cursor()
        if details["name"] != '':
            query = f"INSERT INTO drugs(name,brand,date,price,quantity) VALUES ('{details['name'].lower()}','{details['brand']}','{details['date']}','{(details['price'])}','{details['quantity']}')"
            try:
                cursor.execute(query)
                conn.commit()
                print("Successfully added to database")
            except Error as e:
                err = f'The error {e} occured'
                print(err)
        query = "SELECT * FROM drugs ORDER BY name"
        cursor = conn.cursor()
        cursor.execute(query)
        ans = cursor.fetchall()
        return json.dumps(ans)
        
        


@app.route('/removeinfo/<string:details>',methods=['POST','GET'])
def removedetails(details):
    conn = create_connection('progdb.db')
    if request.method == 'POST':
        details = json.loads(details)
        cursor = conn.cursor()
        query = f"DELETE FROM drugs WHERE name = '{details['name']}' and brand = '{details['brand']}'"
        cursor.execute(query)
        conn.commit()
        print("Successfully deleted from database")
        return render_template("index.html")
    else: 
        return json.dumps("Succesfully removed entry")

@app.route('/searchinfo/<string:details>',methods=['POST','GET'])
def searchdetails(details):
    conn = create_connection('progdb.db')
    if request.method == 'POST':
        return render_template("index.html")
    else:
        details = json.loads(details)
        cursor = conn.cursor()
        if details["brand"] == None:
            query = f"SELECT name,brand,price FROM drugs WHERE name = '{details['name']}' and quantity != '0';"
        else:
            query = f"SELECT * FROM drugs WHERE name = '{details['name']}' and brand = '{details['brand']}';"
        cursor.execute(query)
        ans = cursor.fetchall()
        return json.dumps(ans)

@app.route('/deleteall',methods=['POST'])
def deletetable():
    if request.method == 'POST':
        conn = create_connection('progdb.db')
        cursor = conn.cursor()
        query = "DROP table IF EXISTS drugs"
        cursor.execute(query)
        conn.commit()
        query = "CREATE TABLE IF NOT EXISTS drugs(name VARCHAR(246), brand VARCHAR(246), date DATE, price FLOAT, quantity FLOAT, PRIMARY KEY(name,brand))"
        cursor.execute(query)
        conn.commit()
        return render_template("index.html")

@app.route('/updateinfo/<string:details>',methods=['POST','GET'])
def updatetable(details):
    if request.method == 'GET':
        conn = create_connection('progdb.db')
        cursor = conn.cursor()
        details = json.loads(details)
        keys = list(details.keys())
        keys.remove('name')
        keys.remove('brand')
        quest = ""
        for i in keys:
            if details[i] != '':
                quest = quest + i + " = " + f"'{details[i]}'" + ","
        quest = quest[:-1]
        query = f"UPDATE drugs SET {quest} WHERE name = '{details['name']}' and brand = '{details['brand']}'"
        cursor.execute(query)
        conn.commit()
        query = f"SELECT * FROM drugs WHERE name = '{details['name']}' and brand = '{details['brand']}'"
        cursor.execute(query)
        ans=cursor.fetchall()
        #print(ans)
        return json.dumps(ans)


#Special API call for just doctor

        
# main driver function
if __name__ == '__main__':
    app.run(debug=True)
