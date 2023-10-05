import pandas as pd
import matplotlib.pyplot as plt


def load_data(data_path):
    try:
        data = pd.read_csv(data_path)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None


def highlight_matches(val, keywords):
    for keyword in keywords:
        if keyword.lower() in str(val).lower():
            return 'background-color: yellow'
    return ''


def tabulate_data(data, page_size=10, keywords=None):
    if data is not None:
        pd.set_option('display.max_columns', 25)

        if keywords:
            display_data = data.head(page_size).style.applymap(lambda x: highlight_matches(x, keywords),
                                                               subset=data.columns[1:])
            print(display_data)
        else:
            while True:
                print(data.head(page_size))  # Display the first 'page_size' rows

                if len(data) <= page_size:
                    break

                user_input = input("Press 'Enter' to view the next page, 'q' to quit: ")

                if user_input.lower() == 'q':
                    break

                data = data.iloc[page_size:]  # Move to the next page
    else:
        print("No data to tabulate.")


def search_data(data, keywords):
    if data is not None:
        # Search in column names
        matching_columns = [col for col in data.columns if any(keyword in col for keyword in keywords)]

        if matching_columns:
            print("Matching columns:", matching_columns)
            # Display the data for matching columns
            for col_name in matching_columns:
                print(data[col_name])
        else:
            print("No matching columns found.")
    else:
        print("No data to search.")


def create_bar_chart(data, x_label, y_label, title):
    plt.figure(figsize=(10, 6))  # Adjust the figure size if needed
    plt.bar(data[x_label], data[y_label])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Ensure the labels fit within the figure
    plt.show()


def main():
    # Define the path to the dataset
    dataset_path = "Crash Statistics Victoria.csv"

    # Load the data
    accident_data = load_data(dataset_path)

    # Get search keywords from the user
    keywords = input("Enter search keywords (comma-separated): ").split(",")

    # Tabulate the data
    tabulate_data(accident_data, keywords=keywords)

    # Perform the search in column names
    print("Searching for keywords in column names:", keywords)
    search_data(accident_data, keywords)

    # Create a bar chart based on user input
    x_label = input("Enter the x-axis label: ")
    y_label = input("Enter the y-axis label: ")
    title = input("Enter the chart title: ")

    # Filter and aggregate data as needed for the bar chart
    chart_data = accident_data.groupby(x_label)[y_label].count().reset_index()

    # Create the bar chart
    create_bar_chart(chart_data, x_label, y_label, title)


if __name__ == "__main__":
    main()
