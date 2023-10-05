import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from itertools import cycle
from matplotlib.cm import get_cmap


def load_data(data_path):
    try:
        data = pd.read_csv(data_path)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None


def create_bar_chart(data: pd.DataFrame, x_label: str, y_label: str, title: str, columns: List[str]):
    if data is None or columns is None or not columns:
        raise ValueError("Invalid input data or columns")

    for column in columns:
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame")

    selected_data = data[columns]

    fig, ax = plt.subplots()

    # Use a predefined colormap to automatically generate colors
    cmap = get_cmap('tab10')  # You can change the colormap as needed

    # Create a cycle iterator to loop through the colors
    color_cycle = cycle(cmap.colors)

    for column in columns:
        color = next(color_cycle)
        ax.bar(column, selected_data.iloc[0][column], color=color)  # Assign a color to each bar

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    return fig


def main():
    # Define the path to the dataset
    dataset_path = "Crash Statistics Victoria.csv"

    # Load the data
    accident_data = load_data(dataset_path)

    # Get column names for the bar chart from the user
    columns = input("Enter column names for the bar chart (comma-separated): ").split(",")

    if not columns:
        print("No columns entered. Exiting.")
        return

    # Create a bar chart based on the selected columns
    x_label = input("Enter the x-axis label: ")
    y_label = input("Enter the y-axis label: ")
    title = input("Enter the chart title: ")

    chart = create_bar_chart(accident_data, x_label, y_label, title, columns)
    plt.show()  # Display the chart


if __name__ == "__main__":
    main()
