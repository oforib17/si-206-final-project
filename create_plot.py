import matplotlib.pyplot as plt
import numpy as np

def get_data_from_file(filename):
    data = []
    file_obj = open(filename, "r")

    for line in file_obj:
        data.append(line)

    data = data[1:]

    for i in range(len(data)):
        data[i] = data[i].split()
    
    return data

def create_bar_chart_averages(data, region):
    cities = []
    avg_temps = []
    max_temps = []
    min_temps = []

    for datum in data:
        # Get average temps and city names
        temp = ""
        city = ""
        temp_start_index = 0
        for i in range(len(datum)):
            if not datum[i+1].isalpha():
                avg_temps.append(float(datum[i+1]))
                temp_start_index = i+1
                break
            else:
                temp += datum[i]

        # City names formatting
        for char in temp:
            if char.isupper():
                city = city + " " + char.upper()
            else:
                city = city + char
        
        city = city[1:]
        cities.append(city)

        # Get mins and maxes
        max_temps.append(float(datum[temp_start_index+1]))
        min_temps.append(float(datum[temp_start_index+2]))

    
    plt.bar(cities, avg_temps)

    # error bar for ranges
    for i in range(len(cities)):
        plt.errorbar(x = i, y = avg_temps[i], yerr = [[avg_temps[i] - min_temps[i]], [max_temps[i] - avg_temps[i]]], fmt = 'none', capsize = 5, color = "black")
    
    plt.title(f'Average Temperatures for {region} Cities Across the Past 10 Days (With Ranges)', fontsize = 16)
    plt.xlabel('City', fontsize = 12)
    plt.ylabel('Temperature (°F)', fontsize = 12)

def main():
    e = get_data_from_file("european_weather_summary.txt")
    u = get_data_from_file("us_weather_summary.txt")

    plt.figure(0)
    create_bar_chart_averages(e, "European")

    plt.figure(1)
    create_bar_chart_averages(u, "American")

    plt.show()

if __name__ == "__main__":
    main()
