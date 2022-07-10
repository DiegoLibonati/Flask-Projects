from flask import Flask, jsonify, request, abort
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'system'
mysql = MySQL(app)

@app.route('/api/customers')
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM customers')
    data = cur.fetchall()
    result = []
    for row in data:
        content = {
        'id':row[0],
        'firstname': row[1],
        'lastname': row[2],
        'email': row[3],
        'phone': row[4],
        'address': row[5],
         }
        result.append(content)

    return jsonify(result)

@app.route('/api/customers', methods=['POST'])
@cross_origin()
def saveCustomer():
    cur = mysql.connection.cursor()
    consulta = cur.execute('SELECT * FROM customers WHERE email LIKE %s', [request.json['email']])
    
    if consulta == 0:
        cur.execute("INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `phone`, `address`) VALUES (NULL, %s, %s, %s, %s,%s );", (request.json['firstname'],request.json['lastname'],request.json['email'],request.json['phone'],request.json['address'])) 
    else:
        return abort(400)
    
    cur.connection.commit()
    return 'Cliente guardado'

@app.route('/api/customers/<int:id_customer>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id_customer):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM `customers` WHERE `customers`.`id` = {str(id_customer)};")
    cur.connection.commit()
    return 'Cliente eliminado'

@app.route('/api/customers', methods=['PUT'])
@cross_origin()
def editCustomer():
    cur = mysql.connection.cursor()
    cur.execute('UPDATE `customers` SET `firstname`=%s, `lastname`=%s, `email`=%s, `phone`=%s, `address`=%s WHERE `customers`.`id` = %s', (request.json['firstname'],request.json['lastname'],request.json['email'],request.json['phone'],request.json['address'], request.json['id'])) 
    cur.connection.commit()
    return 'Cliente guardado y editado'

if __name__ == '__main__':
    app.run(None,5000, True)