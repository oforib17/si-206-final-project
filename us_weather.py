import json
import requests as r
import sqlite3

# Limit the number of items to be inserted per run
MAX_ITEMS_PER_RUN = 25

def load_data(cities: list) -> list:
    API_KEY = "a866133410144d0792b4a13053d33aec"
    weather_data = []

    for location in cities:
        city = location["city"]
        state = location["state"]
        params = {"key": API_KEY, "start_date" : "2024-12-02", "end_date": "2024-12-12", "units" : "I"}

        response = r.get(f"https://api.weatherbit.io/v2.0/history/daily?city={city},{state}&country=US", params=params).json()
        weather_data.append({"city": city, "state": state, "data": response['data']})
    
    return weather_data

def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USCities (
                    cityid INTEGER PRIMARY KEY,
                    city TEXT,
                    state TEXT,
                    UNIQUE(city, state)  -- Ensure no duplicate cities
                )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS USWeatherData (
                    weatherid INTEGER PRIMARY KEY,
                    cityid INTEGER,
                    date DATE,
                    temp REAL,
                    max_temp REAL,
                    min_temp REAL,
                    precipitation REAL,
                    UNIQUE(cityid, date),  -- Ensure no duplicate weather records for the same date
                    FOREIGN KEY (cityid) REFERENCES USCities (cityid)
                )''')
    
    conn.commit()

def input_sql_data(conn, data):
    cur = conn.cursor()
    inserted_items = 0

    for city_info in data:
        if inserted_items >= MAX_ITEMS_PER_RUN:
            break

        city = city_info['city']
        state = city_info['state']

        cur.execute('''INSERT OR IGNORE INTO USCities (city, state)
                    VALUES (?, ?)''', (city, state))

        cur.execute('SELECT cityid FROM USCities WHERE city = ? AND state = ?', (city, state))
        cityid = cur.fetchone()[0]

        for day in city_info['data']:
            if inserted_items >= MAX_ITEMS_PER_RUN:
                break

            date = day.get('datetime')
            cur.execute('SELECT COUNT(*) FROM USWeatherData WHERE cityid = ? AND date = ?', (cityid, date))
            if cur.fetchone()[0] == 0:
                cur.execute('''INSERT INTO USWeatherData (cityid, date, temp, max_temp, min_temp, precipitation)
                               VALUES (?, ?, ?, ?, ?, ?)''', (
                                cityid,
                                date,
                                day.get('temp', 0.0),
                                day.get('max_temp', 0.0),
                                day.get('min_temp', 0.0),
                                day.get('precip', 0.0)
                ))

                inserted_items += 1

    conn.commit()
    print(f"Inserted {inserted_items} new weather data items.")

def main():
    locations = [{"city": "New York City", "state": "NY"},
                 {"city": "Los Angeles", "state": "CA"},
                 {"city": "Chicago", "state": "IL"},
                 {"city": "Houston", "state": "TX"},
                 {"city": "Phoenix", "state": "AZ"},
                 {"city": "Philadelphia", "state": "PA"},
                 {"city": "San Antonio", "state": "TX"},
                 {"city": "San Diego", "state": "CA"},
                 {"city": "Dallas", "state": "TX"},
                 {"city": "Jacksonville", "state": "FL"}]

    weather_data = load_data(locations)

    conn = sqlite3.connect('Weather.db')
    create_tables(conn)
    input_sql_data(conn, weather_data)
    conn.close()

if __name__ == "__main__":
    main() 
