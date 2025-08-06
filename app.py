from flask import render_template, Flask, request,jsonify
import mysql.connector
from datetime import datetime ,timedelta
from requests_api import fetch_and_store_earthquake_data

app = Flask(__name__)

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'varunkumar',
    database = 'earthquake_data'
)

cursor = db.cursor(dictionary=True)

fetch_and_store_earthquake_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_earthquakes')
def get_earthquakes():
    hours = int(request.args.get('hours', 1))
    cutoff_time = datetime.now() - timedelta(hours=hours)
    cursor.execute("SELECT latitude, longitude, magnitude, location, time FROM earthquake WHERE time >= %s", (cutoff_time,))
    results = cursor.fetchall()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
