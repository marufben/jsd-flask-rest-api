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

if __name__ == '__main__':
    app.run(debug=True)