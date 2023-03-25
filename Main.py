import requests
import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connect to MySQL database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='abcd1234',
    database='dashboard_jds'
)

# API endpoint for storing data to MySQL database
@app.route('/store_data', methods=['GET'])
def store_data():
    # Retrieve data from API endpoint
    url = 'https://data.jabarprov.go.id/api-backend/bigdata/dinkes/od_17107_jumlah_balita_berdasarkan_kategori_balita_gizi_buruk?limit=250'
    response = requests.get(url)
    data = response.json()

    # Store data to MySQL database
    mycursor = mydb.cursor()
    mycursor.execute("TRUNCATE TABLE balita_gizi_buruk")
    sql = "INSERT INTO balita_gizi_buruk (kode_provinsi, nama_provinsi, kode_kabupaten_kota, nama_kabupaten_kota, kategori_gizi_buruk, jumlah_balita, satuan, tahun) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"
    for row in data['data']:
        values = (row['kode_provinsi'], 
        row['nama_provinsi'], 
        row['kode_kabupaten_kota'], 
        row['nama_kabupaten_kota'], 
        row['kategori_gizi_buruk'], 
        row['jumlah_balita'], 
        row['satuan'], 
        row['tahun'])
        mycursor.execute(sql, values)
    mydb.commit()

    return 'Data stored to MySQL database'

# API endpoint for storing data to MySQL database
@app.route('/get-data-balita-gizi-buruk', methods=['GET'])
def get_data_balita_gizi_buruk():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM balita_gizi_buruk")
    result = mycursor.fetchall()

# Menampilkan data
    data = []
    for row in result:
        row_list = {
            'nama_kabupaten_kota':row[4],
            'kategori_gizi_buruk':row[5],
            'jumlah_balita':row[6],
            'tahun':row[8]
        }
        data.append(row_list)
    return jsonify({'data': data})

@app.route('/get-data-kategori-gizi-buruk-by-tahun', methods=['GET'])
def get_data_kategori_gizi_buruk_by_tahun():
    token = request.headers.get('Authorization')
    if not verify_token(token):
        return jsonify({'message': 'Unauthorized Access'}), 401
    mycursor = mydb.cursor()
    mycursor.execute("select tahun, kategori_gizi_buruk ,SUM(jumlah_balita) as jumlah from dashboard_jds.balita_gizi_buruk group by kategori_gizi_buruk, tahun order by tahun asc")
    result = mycursor.fetchall()

# Menampilkan data
    data = []
    for row in result:
        row_list = {
            'kategori_gizi_buruk':row[1],
            'jumlah_balita':row[2],
            'tahun':row[0]
        }
        data.append(row_list)
    return jsonify({'data': data})
@app.route('/get-data-jumlah-gizi-buruk-kabupaten-kota-bytahun', methods=['GET'])
def get_data_jumlah_gizi_buruk_kabupaten_kota_bytahun():   
    token = request.headers.get('Authorization')
    if not verify_token(token):
        return jsonify({'message': 'Unauthorized Access'}), 401
    mycursor = mydb.cursor()
    mycursor.execute("select nama_kabupaten_kota, SUM(jumlah_balita) as jumlah, tahun from dashboard_jds.balita_gizi_buruk group by `nama_kabupaten_kota` , tahun order by nama_kabupaten_kota, tahun")
    result = mycursor.fetchall()

# Menampilkan data
    data = []
    for row in result:
        row_list = {
            'nama_kabupaten_kota':row[0],
            'tahun':row[2],
            'jumlah_balita_gizi_buruk':row[1]
        }
        data.append(row_list)
    return jsonify({'data': data})

#Function Verifiy token statis
def verify_token(token):
    if token == "xYEq9m2f8C8X4F9fZvp2QbndsPfESunN":
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)