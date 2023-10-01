import pandas as pd

keywords = input("Enter search keywords (comma-separated): ").split(",")


data_types = {
    "OBJECTID": object,
    "ACCIDENT_NO": object,
    "ABS_CODE": object,
    "ACCIDENT_STATUS": object,
    "ACCIDENT_DATE": object,
    "ACCIDENT_TIME": object,
    "ALCOHOLTIME": object,
    "ACCIDENT_TYPE": object,
    "DAY_OF_WEEK": object,
    "DCA_CODE": object,
    "HIT_RUN_FLAG": object,
    "LIGHT_CONDITION": object,
    "POLICE_ATTEND": object,
    "ROAD_GEOMETRY": object,
    "SEVERITY": object,
    "SPEED_ZONE": object,
    "RUN_OFFROAD": object,
    "NODE_ID": object,
    "LONGITUDE": object,
    "LATITUDE": object,
    "NODE_TYPE": object,
    "LGA_NAME": object,
    "REGION_NAME": object,
    "VICGRID_X": object,
    "VICGRID_Y": object,
    "TOTAL_PERSONS": object,
    "INJ_OR_FATAL": object,
    "FATALITY": object,
    "SERIOUSINJURY": object,
    "OTHERINJURY": object,
    "NONINJURED": object,
    "MALES": object,
    "FEMALES": object,
    "BICYCLIST": object,
    "PASSENGER": object,
    "DRIVER": object,
    "PEDESTRIAN": object,
    "PILLION": object,
    "MOTORIST": object,
    "UNKNOWN": object,
    "PED_CYCLIST_5_12": object,
    "PED_CYCLIST_13_18": object,
    "OLD_PEDESTRIAN": object,
    "OLD_DRIVER": object,
    "YOUNG_DRIVER": object,
    "ALCOHOL_RELATED": object,
    "UNLICENCSED": object,
    "NO_OF_VEHICLES": object,
    "HEAVYVEHICLE": object,
    "PASSENGERVEHICLE": object,
    "MOTORCYCLE": object,
    "PUBLICVEHICLE": object,
    "DEG_URBAN_NAME": object,
    "DEG_URBAN_ALL": object,
    "LGA_NAME_ALL": object,
    "REGION_NAME_ALL": object,
    "SRNS": object,
    "SRNS_ALL": object,
    "RMA": object,
    "RMA_ALL": object,
    "DIVIDED": object,
    "DIVIDED_ALL": object,
    "STAT_DIV_NAME": object
}

column_names = [
    "OBJECTID", "ACCIDENT_NO", "ABS_CODE", "ACCIDENT_STATUS", "ACCIDENT_DATE", "ACCIDENT_TIME",
    "ALCOHOLTIME", "ACCIDENT_TYPE", "DAY_OF_WEEK", "DCA_CODE", "HIT_RUN_FLAG", "LIGHT_CONDITION",
    "POLICE_ATTEND", "ROAD_GEOMETRY", "SEVERITY", "SPEED_ZONE", "RUN_OFFROAD", "NODE_ID", "LONGITUDE",
    "LATITUDE", "NODE_TYPE", "LGA_NAME", "REGION_NAME", "VICGRID_X", "VICGRID_Y", "TOTAL_PERSONS",
    "INJ_OR_FATAL", "FATALITY", "SERIOUSINJURY", "OTHERINJURY", "NONINJURED", "MALES", "FEMALES",
    "BICYCLIST", "PASSENGER", "DRIVER", "PEDESTRIAN", "PILLION", "MOTORIST", "UNKNOWN", "PED_CYCLIST_5_12",
    "PED_CYCLIST_13_18", "OLD_PEDESTRIAN", "OLD_DRIVER", "YOUNG_DRIVER", "ALCOHOL_RELATED", "UNLICENCSED",
    "NO_OF_VEHICLES", "HEAVYVEHICLE", "PASSENGERVEHICLE", "MOTORCYCLE", "PUBLICVEHICLE", "DEG_URBAN_NAME",
    "DEG_URBAN_ALL", "LGA_NAME_ALL", "REGION_NAME_ALL", "SRNS", "SRNS_ALL", "RMA", "RMA_ALL", "DIVIDED",
    "DIVIDED_ALL", "STAT_DIV_NAME"
]

def load_data(data_path, data_types):
    try:
        data = pd.read_csv(data_path, dtype=data_types)
        return data
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None

def tabulate_data(data):
    if data is not None:
        pd.set_option('display.max_columns', None)
        print(data)
    else:
        print("No data to tabulate.")

def search_data(data, keywords):
    if data is not None:
        filter_condition = data.apply(lambda row: any(keyword in str(row) for keyword in keywords), axis=1)
        filtered_data = data[filter_condition]

        if not filtered_data.empty:
            tabulate_data(filtered_data)
        else:
            print("No matching entries found.")
    else:
        print("No data to search.")


dataset_path = "Crash Statistics Victoria.csv"


accident_data = load_data(dataset_path, data_types)


tabulate_data(accident_data)


keywords = input("Enter search keywords (comma-separated): ").split(",")


search_data(accident_data, keywords)


