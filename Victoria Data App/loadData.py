import pandas as pd
import matplotlib.pyplot as plt

def create_bar_chart(data, labels, title, x_label, y_label):
    plt.bar(labels, data)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def load_data(data_path):
    try:
        data = pd.read_csv(data_path)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None

def tabulate_data(data, page_size=10):
    if data is not None:
        pd.set_option('display.max_columns', 25)
        total_rows = len(data)
        current_page = 1
        while True:
            print(data.head(page_size))  # Display the first 'page_size' rows
            print(f"Page {current_page} of {total_rows // page_size + 1}")

            if len(data) <= page_size:
                break

            user_input = input("Press 'Enter' to view the next page, 'p' for previous page, 'q' to quit: ")

            if user_input.lower() == 'q':
                break
            elif user_input.lower() == 'p':
                if current_page > 1:
                    current_page -= 1
                    data = data.iloc[:(current_page - 1) * page_size]
                else:
                    print("You are already on the first page.")
            else:
                if current_page * page_size < total_rows:
                    current_page += 1
                    data = data.iloc[current_page * page_size:]
                else:
                    print("You have reached the end of the dataset.")
    else:
        print("No data to tabulate.")

def search_data(data, keywords):
    if data is not None:
        # Search in column names
        matching_columns = [col for col in data.columns if any(keyword in col for keyword in keywords)]

        if matching_columns:
            print("Matching columns:", matching_columns)
            for col_name in matching_columns:
                print(f"Column: {col_name}\n{data[col_name]}\n")
        else:
            print("No matching columns found.")
    else:
        print("No data to search.")

def main():

    data = [10, 20, 30, 40, 50]
    labels = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']

    create_bar_chart(data, labels, 'Sample Bar Chart', 'Categories', 'Values')

    # Define the path to the dataset
    dataset_path = "Crash Statistics Victoria.csv"

    # Load the data
    accident_data = load_data(dataset_path)

    # Tabulate the data
    tabulate_data(accident_data)

    # Get search keywords from the user
    keywords = input("Enter search keywords (comma-separated): ").split(",")

    # Perform the search in column names
    print("Searching for keywords in column names:", keywords)
    search_data(accident_data, keywords)

if __name__ == "__main__":
    main()
