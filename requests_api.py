# earthquake_fetcher.py

import requests
import mysql.connector
import datetime

def fetch_and_store_earthquake_data():
    # Connect to MySQL
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='varunkumar',
        database='earthquake_data'
    )
    cursor = db.cursor()

    # Parameters for USGS API
    parameters = {
        'format': 'geojson',
        "starttime": '2025-04-01',
        "endtime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "minmagnitude": 3.5
    }

    response = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query", params=parameters)

    if response.status_code == 200:
        data = response.json()
        for i in data['features']:
            mag = i["properties"]['mag']
            place = i["properties"]['place']
            time = i["properties"]['time']
            coords = i["geometry"]["coordinates"]
            longitude = coords[0]
            latitude = coords[1]
            readable_time = datetime.datetime.fromtimestamp(time / 1000).strftime("%Y-%m-%d %H:%M:%S")

            if mag and mag > 4:
                if 'of' in place:
                    area, location = place.split("of", 1)
                    area = area.strip()
                    location = location.strip()
                else:
                    area = ''
                    location = place.strip()

                if ',' in location:
                    country = location.split(',')[-1].strip()
                else:
                    country = location

                sql = "INSERT INTO earthquake (magnitude, location, area, time, country, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (mag, location, area, readable_time, country, latitude, longitude)
                cursor.execute(sql, values)

        db.commit()
        print("Data Inserted Successfully")
    else:
        print("Error:", response.status_code)

    cursor.close()
    db.close()
