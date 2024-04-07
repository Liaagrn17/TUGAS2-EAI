from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'penjualan_barang'
mysql = MySQL(app)


@app.route('/')
def root():
    return 'Selamat Datang di Tutorial Restful API'

@app.route('/barang', methods=['GET', 'POST'])
def barang():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM BARANG')

        column_names = [i[0] for i in cursor.description]
        
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        return jsonify(data)

        cursor.close()
    
    elif request.method == 'POST':
        #get data from request
        nama_barang = request.json['nama_barang']
        harga = request.json['harga']
        stok = request.json['stok']
        
        #open connection and insert to db
        cursor = mysql.connection.cursor()
        sql = 'INSERT INTO BARANG (nama_barang, harga, stok) VALUES (%s, %s, %s)'
        val = (nama_barang, harga, stok)
        cursor.execute(sql, val)

        mysql.connection.commit()

        return jsonify({'message': 'data added successfully!'})
        cursor.close()
    
@app.route('/detailbarang', methods=['GET'])
def detailbarang():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = 'SELECT * FROM BARANG WHERE id_barang = %s'
        val = (request.args['id'],)
        cursor.execute(sql, val)

        column_names = [i[0] for i in cursor.description]
            
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        return jsonify(data)

        cursor.close()

@app.route('/deletebarang', methods=['DELETE'])
def deletebarang():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = 'DELETE FROM barang WHERE id_barang = %s'
        val = (request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()

        return jsonify({'message': 'data deleted successfully!'})
        cursor.close()

@app.route('/editbarang', methods=['PUT'])
def editbarang():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = 'UPDATE barang SET nama_barang=%s, harga=%s, stok=%s WHERE id_barang = %s'
        val = (data['nama_barang'], data['harga'], data['stok'], request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()
        return jsonify({'message': 'Data updated successfuly!'})
        cursor.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7004, debug=True)

