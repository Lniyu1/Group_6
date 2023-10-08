import wx
import wx.adv
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from itertools import cycle
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx.grid as gridlib


app_frame = None
accident_data = None
left_grid = None
current_screen = None
search_bar = None


def load_data(data_path):
    try:
        data = pd.read_csv(data_path)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None


def create_home_screen(app_frame):

    home_sizer = wx.BoxSizer(wx.VERTICAL)


    search_sizer = wx.BoxSizer(wx.HORIZONTAL)


    search_panel, search_bar = create_search_bar(app_frame)


    search_sizer.Add(search_panel, 1, wx.ALL | wx.EXPAND, 5)


    search_button = wx.Button(app_frame, wx.ID_ANY, "Search")
    search_button.Bind(wx.EVT_BUTTON, on_search_enter)

    search_sizer.Add(search_button, 0, wx.ALL, 5)


    home_sizer.Add(search_sizer, 0, wx.EXPAND)


    splitter = wx.SplitterWindow(app_frame, wx.ID_ANY)


    global left_panel
    global right_panel

    left_panel, left_grid = create_left_panel(splitter, accident_data)
    right_panel = create_right_panel(splitter)


    splitter.SplitVertically(left_panel, right_panel)
    splitter.SetMinimumPaneSize(100)

    home_sizer.Add(splitter, 1, wx.EXPAND)


    tools_button = wx.Button(app_frame, wx.ID_ANY, "Tools")
    tools_button.Bind(wx.EVT_BUTTON, open_tools_dialog)

    home_sizer.Add(tools_button, 0, wx.ALL, 5)

    app_frame.SetSizer(home_sizer)


def create_search_bar(parent):
    search_panel = wx.Panel(parent, wx.ID_ANY)
    search_sizer = wx.BoxSizer(wx.HORIZONTAL)

    global search_bar
    search_bar = wx.TextCtrl(search_panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)


    search_bar.SetMinSize((100, -1))

    search_sizer.Add(search_bar, 1, wx.ALL | wx.EXPAND, 5)

    search_panel.SetSizerAndFit(search_sizer)

    search_bar.Bind(wx.EVT_TEXT_ENTER, on_search_enter)

    return search_panel, search_bar


def on_search_enter(event):
    global left_grid
    search_text = search_bar.GetValue() if search_bar else ""

    if not search_text:
        populate_grid(left_grid, accident_data)
    else:

        selected_columns = [col for col in accident_data.columns if search_text.lower() in col.lower()]

        if not selected_columns:

            left_grid.ClearGrid()
        else:

            filtered_data = accident_data[selected_columns]
            populate_grid(left_grid, filtered_data)



def create_left_panel(parent, data):
    global left_grid
    global left_panel

    left_panel = wx.Panel(parent, wx.ID_ANY, style=wx.BORDER_SUNKEN)


    left_sizer = wx.BoxSizer(wx.VERTICAL)


    left_grid = gridlib.Grid(left_panel)


    if data is not None:
        populate_grid(left_grid, data)


    left_sizer.Add(left_grid, 1, wx.EXPAND)

    left_sizer.AddSpacer(10)


    buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)


    create_button = wx.Button(left_panel, wx.ID_ANY, "Create")
    create_button.Bind(wx.EVT_BUTTON, on_create_data)
    buttons_sizer.Add(create_button, 0, wx.ALL, 5)


    save_button = wx.Button(left_panel, wx.ID_ANY, "Save")
    save_button.Bind(wx.EVT_BUTTON, on_save_data)
    buttons_sizer.Add(save_button, 0, wx.ALL, 5)


    delete_button = wx.Button(left_panel, wx.ID_ANY, "Delete")
    delete_button.Bind(wx.EVT_BUTTON, on_delete_data)
    buttons_sizer.Add(delete_button, 0, wx.ALL, 5)

    left_sizer.Add(buttons_sizer, 0, wx.CENTER)


    left_panel.SetSizerAndFit(left_sizer)

    return left_panel, left_grid


def on_create_data(event):

    dlg = wx.TextEntryDialog(app_frame, "Enter column names to create a bar chart (comma-separated):",
                             "Create Bar Chart")
    if dlg.ShowModal() == wx.ID_OK:
        search_input = dlg.GetValue()
        search_columns = [col.strip() for col in
                          search_input.split(',')]  # Split input by comma and remove leading/trailing spaces

        if not search_columns:
            wx.MessageBox("No column names entered. Please try again.", "Error", wx.OK | wx.ICON_ERROR)
            return


        selected_columns = [col for col in accident_data.columns if
                            any(search_col.lower() in col.lower() for search_col in search_columns)]

        if not selected_columns:
            wx.MessageBox("No matching columns found. Please try different search terms.", "No Match",
                          wx.OK | wx.ICON_INFORMATION)
            return


        x_label = wx.TextEntryDialog(app_frame, "Enter the x-axis label:", "X-axis Label", style=wx.OK | wx.CANCEL)
        if x_label.ShowModal() == wx.ID_OK:
            x_label_value = x_label.GetValue()


            y_label = wx.TextEntryDialog(app_frame, "Enter the y-axis label:", "Y-axis Label", style=wx.OK | wx.CANCEL)
            if y_label.ShowModal() == wx.ID_OK:
                y_label_value = y_label.GetValue()


                title = wx.TextEntryDialog(app_frame, "Enter the chart title:", "Chart Title", style=wx.OK | wx.CANCEL,
                                           value="Bar Chart")
                if title.ShowModal() == wx.ID_OK:
                    title_value = title.GetValue()


                    filtered_data = accident_data[selected_columns]


                    fig = create_bar_chart(filtered_data, x_label_value, y_label_value, title_value, selected_columns)


                    update_right_panel_with_bar_chart(filtered_data, x_label_value, y_label_value, title_value,
                                                      selected_columns)

    dlg.Destroy()


def on_save_data(event):

    wx.MessageBox("Data has been saved.", "Save Data", wx.OK | wx.ICON_INFORMATION)


def on_delete_data(event):

    wx.MessageBox("Data has been deleted.", "Delete Data", wx.OK | wx.ICON_INFORMATION)


def create_right_panel(parent, fig=None):
    global right_panel
    right_panel = wx.Panel(parent, wx.ID_ANY, style=wx.BORDER_SUNKEN)

    if fig:

        canvas = FigureCanvas(right_panel, -1, fig)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.EXPAND | wx.ALL, 5)


        right_panel.SetSizerAndFit(sizer)

    return right_panel


def update_right_panel_with_bar_chart(data, x_label, y_label, title, columns):

    right_panel.DestroyChildren()


    fig = create_bar_chart(data, x_label, y_label, title, columns)


    canvas = FigureCanvas(right_panel, -1, fig)


    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(canvas, 1, wx.EXPAND | wx.ALL, 5)
    right_panel.SetSizerAndFit(sizer)


    right_panel.Refresh()


def open_tools_dialog(event):
    global current_screen


    dialog = wx.Dialog(app_frame, wx.ID_ANY, "Tools Dialog", size=(400, 300))


    button1 = wx.Button(dialog, wx.ID_ANY, "Load Data")
    button2 = wx.Button(dialog, wx.ID_ANY, "Graphing Data")
    back_button = wx.Button(dialog, wx.ID_ANY, "Back to Main Page")  # Added "Back" button


    button1.Bind(wx.EVT_BUTTON, show_screen1)
    button2.Bind(wx.EVT_BUTTON, show_screen2)
    back_button.Bind(wx.EVT_BUTTON, show_main_page)


    button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    button_sizer.Add(button1, 0, wx.ALL, 5)
    button_sizer.Add(button2, 0, wx.ALL, 5)
    button_sizer.Add(back_button, 0, wx.ALL, 5)  # Add the "Back" button to the sizer


    dialog.SetSizerAndFit(button_sizer)


    dialog.ShowModal()
    dialog.Destroy()


def show_main_page(event):
    global current_screen
    if current_screen:
        current_screen.Hide()
    create_home_screen(app_frame)
    current_screen = None


def show_screen1(event):
    global current_screen
    if current_screen:
        current_screen.Hide()
    current_screen = DataLoadScreen(app_frame)
    current_screen.Show()


class DataLoadScreen(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)


        sizer = wx.BoxSizer(wx.VERTICAL)


        loading_label = wx.StaticText(self, label="Loading dataset... Please wait.")
        sizer.Add(loading_label, 0, wx.ALL | wx.CENTER, 10)


        dataset_path = "Crash Statistics Victoria.csv"
        data = load_data(dataset_path)

        if data is not None:

            data_grid = gridlib.Grid(self)
            populate_grid(data_grid, data)
            sizer.Add(data_grid, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizerAndFit(sizer)


def show_screen2(event):
    global current_screen
    if current_screen:
        current_screen.Hide()
    current_screen = CalendarAndDatasetScreen(app_frame)
    current_screen.Show()


class CalendarAndDatasetScreen(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        sizer = wx.BoxSizer(wx.HORIZONTAL)


        left_panel = wx.Panel(self)
        left_sizer = wx.BoxSizer(wx.VERTICAL)


        calendar = wx.adv.CalendarCtrl(left_panel, wx.ID_ANY, wx.DefaultDateTime, style=wx.adv.CAL_SHOW_HOLIDAYS)
        left_sizer.Add(calendar, 1, wx.EXPAND | wx.ALL, 10)

        left_panel.SetSizer(left_sizer)


        create_right_panel(self)

        sizer.Add(left_panel, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizerAndFit(sizer)


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
    menu_bar.Append(tools_menu, "Tools")

    # Windows Menu
    windows_menu = wx.Menu()
    windows_menu.Append(wx.ID_ANY, "Window 1")
    menu_bar.Append(windows_menu, "Windows")

    # Help Menu
    help_menu = wx.Menu()
    help_menu.Append(wx.ID_ABOUT, "About")
    menu_bar.Append(help_menu, "Help")

    return menu_bar


def on_create_bar_chart(event):

    dlg = wx.TextEntryDialog(app_frame, "Enter column names to search for (comma-separated):", "Search Columns")
    if dlg.ShowModal() == wx.ID_OK:
        search_input = dlg.GetValue()
        search_columns = [col.strip() for col in
                          search_input.split(',')]

        if not search_columns:
            wx.MessageBox("No column names entered. Please try again.", "Error", wx.OK | wx.ICON_ERROR)
            return


        selected_columns = [col for col in accident_data.columns if
                            any(search_col.lower() in col.lower() for search_col in search_columns)]

        if not selected_columns:
            wx.MessageBox("No matching columns found. Please try different search terms.", "No Match",
                          wx.OK | wx.ICON_INFORMATION)
            return


        x_label = wx.TextEntryDialog(app_frame, "Enter the x-axis label:", "X-axis Label", style=wx.OK | wx.CANCEL)
        if x_label.ShowModal() == wx.ID_OK:
            x_label_value = x_label.GetValue()


            y_label = wx.TextEntryDialog(app_frame, "Enter the y-axis label:", "Y-axis Label", style=wx.OK | wx.CANCEL)
            if y_label.ShowModal() == wx.ID_OK:
                y_label_value = y_label.GetValue()


                title = wx.TextEntryDialog(app_frame, "Enter the chart title:", "Chart Title", style=wx.OK | wx.CANCEL,
                                           value="Bar Chart")
                if title.ShowModal() == wx.ID_OK:
                    title_value = title.GetValue()


                    filtered_data = accident_data[selected_columns]


                    fig = create_bar_chart(filtered_data, x_label_value, y_label_value, title_value, selected_columns)


                    update_right_panel_with_bar_chart(filtered_data, x_label_value, y_label_value, title_value,
                                                      selected_columns)

    dlg.Destroy()


def create_bar_chart(data: pd.DataFrame, x_label: str, y_label: str, title: str, columns: List[str]):
    if data is None or columns is None or not columns:
        raise ValueError("Invalid input data or columns")

    for column in columns:
        if column not in data.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame")

    selected_data = data[columns]

    fig, ax = plt.subplots()


    cmap = plt.colormaps['tab10']

    color_cycle = cycle(cmap.colors)

    for column in columns:
        color = next(color_cycle)
        ax.bar(column, selected_data.iloc[0][column], color=color)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    return fig


def populate_grid(grid, data, num_rows=150):

    if data is not None:

        grid.ClearGrid()

        data = data.head(num_rows)
        rows, cols = data.shape


        if not grid.GetNumberRows():
            grid.CreateGrid(rows, cols)
            for i, col in enumerate(data.columns):
                grid.SetColLabelValue(i, col)

        for i, row in data.iterrows():
            for j, value in enumerate(row):
                grid.SetCellValue(i, j, str(value))


def main():
    global app_frame
    global accident_data
    global left_grid


    dataset_path = "Crash Statistics Victoria.csv"


    accident_data = load_data(dataset_path)


    app = wx.App(False)
    app_frame = wx.Frame(None, wx.ID_ANY, "Victoria Dataset App", size=(800, 800))

    menu_bar = create_menu_bar()
    app_frame.SetMenuBar(menu_bar)


    create_home_screen(app_frame)


    app_frame.Show()

    app.MainLoop()


if __name__ == "__main__":
    main()
