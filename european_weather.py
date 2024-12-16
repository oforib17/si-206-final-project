import json
import requests as r
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# Limit the number of items to be inserted per run
MAX_ITEMS_PER_RUN = 25

def load_data(cities: list) -> list:
    API_KEY = "WAAQYCJVRT25ZVRML3WDCSU24"
    weather_data = []

    for location in cities:
        city = location["city"]
        country = location["country"]
        params = {"key": API_KEY, "include": "days"}

        response = r.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city},{country}/last9days", params=params).json()
        weather_data.append({"city": city, "country": country, "data": response})
    
    return weather_data


def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Cities (
                    cityid INTEGER PRIMARY KEY,
                    city TEXT,
                    country TEXT,
                    UNIQUE(city, country)  -- Ensure no duplicate cities
                )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS WeatherData (
                    weatherid INTEGER PRIMARY KEY,
                    cityid INTEGER,
                    datetime DATE,
                    description TEXT,
                    tempmax REAL,
                    tempmin REAL,
                    temp REAL,
                    feelslikemax REAL,
                    feelslikemin REAL,
                    feelslike REAL,
                    UNIQUE(cityid, datetime),  -- Ensure no duplicate weather records for the same datetime
                    FOREIGN KEY (cityid) REFERENCES Cities (cityid)
                )''')
    
    conn.commit()


def input_sql_data(conn, data):
    cur = conn.cursor()
    inserted_items = 0

    for city_info in data:
        if inserted_items >= MAX_ITEMS_PER_RUN:
            break

        city = city_info['city']
        country = city_info['country']

        # Insert city into Cities table if not exists
        cur.execute('''
        INSERT OR IGNORE INTO Cities (city, country)
        VALUES (?, ?)
        ''' , (city, country))

        cur.execute('SELECT cityid FROM Cities WHERE city = ? AND country = ?', (city, country))
        cityid = cur.fetchone()[0]

        for day in city_info['data']['days']:
            if inserted_items >= MAX_ITEMS_PER_RUN:
                break

            datetime_value = day.get('datetime')
            # Check if this specific weather data already exists
            cur.execute('SELECT COUNT(*) FROM WeatherData WHERE cityid = ? AND datetime = ?', (cityid, datetime_value))
            if cur.fetchone()[0] == 0:
                cur.execute('''
                INSERT INTO WeatherData (cityid, datetime, description, tempmax, tempmin, temp, feelslikemax, feelslikemin, feelslike)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''' , (
                    cityid,
                    datetime_value,
                    day.get('description', 'No description'),
                    day.get('tempmax', 0.0),
                    day.get('tempmin', 0.0),
                    day.get('temp', 0.0),
                    day.get('feelslikemax', 0.0),
                    day.get('feelslikemin', 0.0),
                    day.get('feelslike', 0.0)
                ))

                inserted_items += 1

    conn.commit()
    print(f"Inserted {inserted_items} new weather data items.")


def main():
    locations = [{"city": "Moscow", "country": "Russia"},
                 {"city": "London", "country": "UK"},
                 {"city": "Saint Petersburg", "country": "Russia"},
                 {"city": "Berlin", "country": "Germany"},
                 {"city": "Madrid", "country": "Spain"},
                 {"city": "Kyiv", "country": "Ukraine"},
                 {"city": "Rome", "country": "Italy"},
                 {"city": "Paris", "country": "France"},
                 {"city": "Bucharest", "country": "Romania"},
                 {"city": "Minsk", "country": "Belarus"}]

    weather_data = load_data(locations)

    conn = sqlite3.connect('Weather.db')  
    create_tables(conn)
    input_sql_data(conn, weather_data)
    conn.close()
    

if __name__ == "__main__":
    main()  
