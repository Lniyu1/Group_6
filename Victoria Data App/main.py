import wx
import wx.grid as gridlib
import pandas as pd
import matplotlib.pyplot as plt


# Define global variables for the wx.Frame and wx.grid.Grid objects
app_frame = None
data_grid = None
search_bar = None
accident_data = None  # Global variable to store the dataset
notebook = None

def load_data(data_path):
    try:
        data = pd.read_csv(data_path)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None


def create_search_bar():
    global search_bar
    search_bar = wx.TextCtrl(app_frame, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
    search_bar.Bind(wx.EVT_TEXT_ENTER, on_search_enter)
    return search_bar


def on_search_enter(event):
    search_text = search_bar.GetValue()

    if not search_text:
        # If the search text is empty, display the full dataset
        populate_grid(accident_data)
    else:
        # Filter the dataset based on the search_text
        filtered_data = accident_data[
            accident_data.apply(lambda row: any(search_text.lower() in str(cell).lower() for cell in row), axis=1)]

        # Populate the grid with the filtered data
        populate_grid(filtered_data)


def create_data(event):
    global notebook
    if notebook is not None:
        create_tab = wx.Panel(notebook)
        create_text = wx.TextCtrl(create_tab, wx.ID_ANY, "Enter your create data here", style=wx.TE_MULTILINE)
        create_button = wx.Button(create_tab, wx.ID_ANY, "Create Data")
        create_button.Bind(wx.EVT_BUTTON, on_create_data)

        create_sizer = wx.BoxSizer(wx.VERTICAL)
        create_sizer.Add(create_text, 1, wx.EXPAND | wx.ALL, 5)
        create_sizer.Add(create_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        create_tab.SetSizer(create_sizer)

        notebook.AddPage(create_tab, "Create Data")

def on_create_data(event):
    global accident_data

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



def save_data():
    pass


def delete_data():
    pass


def populate_grid(data, num_rows=25):
    if data is not None and data_grid is not None:
        data_grid.ClearGrid()
        data = data.head(num_rows)
        rows, cols = data.shape
        data_grid.CreateGrid(rows, cols)

        for i, col in enumerate(data.columns):
            data_grid.SetColLabelValue(i, col)

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                data_grid.SetCellValue(i, j, str(value))


def create_menu_bar():
    menu_bar = wx.MenuBar()

    # File Menu
    file_menu = wx.Menu()
    file_menu.Append(wx.ID_OPEN, "Open")
    file_menu.Append(wx.ID_EXIT, "Exit")
    menu_bar.Append(file_menu, "File")

    # Edit Menu
    edit_menu = wx.Menu()
    edit_menu.Append(wx.ID_CUT, "Cut")
    edit_menu.Append(wx.ID_COPY, "Copy")
    edit_menu.Append(wx.ID_PASTE, "Paste")
    menu_bar.Append(edit_menu, "Edit")

    # Options Menu
    options_menu = wx.Menu()
    options_menu.Append(wx.ID_PREFERENCES, "Preferences")
    menu_bar.Append(options_menu, "Options")

    # Tools Menu
    tools_menu = wx.Menu()
    tools_menu.Append(wx.ID_ANY, "Tool 1")
    tools_menu.Append(wx.ID_ANY, "Tool 2")
    menu_bar.Append(tools_menu, "Tools")

    # Windows Menu
    windows_menu = wx.Menu()
    windows_menu.Append(wx.ID_ANY, "Window 1")
    windows_menu.Append(wx.ID_ANY, "Window 2")
    menu_bar.Append(windows_menu, "Windows")

    # Help Menu
    help_menu = wx.Menu()
    help_menu.Append(wx.ID_ABOUT, "About")
    menu_bar.Append(help_menu, "Help")

    return menu_bar


def main():
    global app_frame
    global data_grid
    global search_bar
    global accident_data
    global notebook

    # Define the path to the dataset
    dataset_path = "Crash Statistics Victoria.csv"

    # Load the data
    accident_data = load_data(dataset_path)

    # Initialize the wxPython app
    app = wx.App(False)
    app_frame = wx.Frame(None, wx.ID_ANY, "Dataset Viewer", size=(800, 600))

    # Create the menu bar
    menu_bar = create_menu_bar()
    app_frame.SetMenuBar(menu_bar)

    # Create a wx.grid.Grid within the frame
    data_grid = gridlib.Grid(app_frame)
    app_frame.Bind(wx.EVT_CLOSE, on_close)

    # Create the search bar (TextCtrl)
    search_bar = create_search_bar()

    # Create the notebook with the parent as app_frame
    notebook = wx.Notebook(app_frame, wx.ID_ANY)

    # Create the "Create" button
    create_button = wx.Button(app_frame, wx.ID_ANY, "Create")
    app_frame.Bind(wx.EVT_BUTTON, create_data, create_button)

    # Create the "Save" button
    save_button = wx.Button(app_frame, wx.ID_ANY, "Save")
    app_frame.Bind(wx.EVT_BUTTON, save_data, save_button)

    # Create the "Delete" button
    delete_button = wx.Button(app_frame, wx.ID_ANY, "Delete")
    app_frame.Bind(wx.EVT_BUTTON, delete_data, delete_button)

    # Create a sizer to arrange the buttons horizontally
    button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    button_sizer.Add(create_button, 0, wx.ALL, 5)
    button_sizer.Add(save_button, 0, wx.ALL, 5)
    button_sizer.Add(delete_button, 0, wx.ALL, 5)

    # Create a sizer to arrange the grid and buttons vertically
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    main_sizer.Add(search_bar, 0, wx.ALL | wx.EXPAND, 5)  # Add the search bar
    main_sizer.Add(data_grid, 1, wx.EXPAND)
    main_sizer.Add(button_sizer, 0, wx.CENTER)

    app_frame.SetSizer(main_sizer)

    # Populate the grid with the loaded dataset
    populate_grid(accident_data)

    # Make the frame visible
    app_frame.Show()

    app.MainLoop()


def on_close(event):
    global app_frame
    app_frame.Destroy()

def on_notebook_change(event):
    # Handle notebook page change event here
    pass


if __name__ == "__main__":
    main()
