import sqlite3

def write_data_to_file(query, filename):
    conn = sqlite3.connect('Weather.db')
    cur = conn.cursor()

    # Execute the query
    cur.execute(query)

    # Fetch all results
    rows = cur.fetchall()

    # Write the results to a text file
    with open(filename, 'w') as f:
        # Write header row
        f.write("City\tRegion\tAvg Temp\tHighest Temp\tLowest Temp\n")

        # Loop through each row
        for row in rows:
            row_str = ""  # Initialize an empty string to build the row
            
            # Loop through each value in the row
            for value in row:
                # Convert each value to string and add a tab between them
                row_str += str(value) + "\t"
            
            # Remove the trailing tab and add a newline at the end of the row
            row_str = row_str.rstrip("\t") + "\n"
            
            # Write the row to the file
            f.write(row_str)
    
    conn.close()

def main():
    # Example: Write European cities average temperatures to a file
    write_data_to_file("""
    SELECT 
        C.city,
        C.country,
        AVG(W.temp) AS avg_temp,
        MAX(W.tempmax) AS highest_temp,
        MIN(W.tempmin) AS lowest_temp
    FROM 
        EuropeanCities C
    INNER JOIN 
        EuropeanWeatherData W
    ON 
        C.cityid = W.cityid
    GROUP BY 
        C.city, C.country;
""", "european_weather_summary.txt")

    # Example: Write US cities average temperatures to a file
    write_data_to_file("""
    SELECT 
        C.city,
        C.state,
        AVG(W.temp) AS avg_temp,
        MAX(W.max_temp) AS highest_temp,
        MIN(W.min_temp) AS lowest_temp
    FROM 
        USCities C
    INNER JOIN 
        USWeatherData W
    ON 
        C.cityid = W.cityid
    GROUP BY 
        C.city, C.state;
""", "us_weather_summary.txt")

if __name__ == "__main__":
    main()  
