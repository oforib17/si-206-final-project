import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Read US and European data
    us_data = pd.read_csv("us_weather_summary.txt", sep="\t")
    europe_data = pd.read_csv("european_weather_summary.txt", sep="\t")

    us_data["Region"] = "US"
    europe_data["Region"] = "Europe"

    data = pd.concat([us_data, europe_data], ignore_index=True)

    # rename the columns
    data = data.rename(columns={"Avg Temp": "Average Temp", "Highest Temp": "Max Temp", "Lowest Temp": "Min Temp"})

    plt.figure(figsize=(12, 6))

    # Bar chart
    sns.barplot(
        x="City", 
        y="Average Temp", 
        hue="Region", 
        data=data, 
        errorbar=None,  
    )

    # Adding error bars for min/max temperatures
    for i, row in data.iterrows():
        city_idx = i  
        avg_temp = row["Average Temp"]
        min_temp = row["Min Temp"]
        max_temp = row["Max Temp"]

        # plot the error bar
        plt.errorbar(
            x=city_idx, 
            y=avg_temp, 
            yerr=[[avg_temp - min_temp], [max_temp - avg_temp]], 
            fmt='none', 
            capsize=5, 
            color="black"
        )

    # make the plot look better
    plt.title("Average Temperatures in US and European Cities (with Ranges)", fontsize=16)
    plt.xlabel("City", fontsize=12)
    plt.ylabel("Temperature (°F)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Region")
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig("comparative_temperatures_bar_chart.png")
    plt.show()

if __name__ == "__main__":
    main() 