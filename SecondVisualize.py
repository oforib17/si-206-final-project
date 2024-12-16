import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Read US and European data
    us_data = pd.read_csv("us_weather_summary.txt", sep="\t")
    europe_data = pd.read_csv("european_weather_summary.txt", sep="\t")

    print("US Data Columns:", us_data.columns)
    print("European Data Columns:", europe_data.columns)

    us_data["Region"] = "US"
    europe_data["Region"] = "Europe"

    # Combine us and european data
    data = pd.concat([us_data, europe_data], ignore_index=True)

    print("Combined Data Columns:", data.columns)

    # rename columns
    data = data.rename(columns={"Avg Temp": "Average Temp", "Highest Temp": "Max Temp", "Lowest Temp": "Min Temp"})

    # make the data suitable for plotting a heatmap with pandas function
    heatmap_data = data.pivot(index="City", columns="Region", values="Average Temp")

    # plot heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", linewidths=0.5)

    # make the plot look good
    plt.title("Heatmap of Average Temperatures in US and European Cities", fontsize=16)
    plt.xlabel("Region", fontsize=12)
    plt.ylabel("City", fontsize=12)
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig("temperature_heatmap.png")
    plt.show()

if __name__ == "__main__":
    main()

