import pandas as pd

from ..database.dao import get_devices, get_ID_devices, retrieve_n_occupancy_observations


def create_ID_devices_options():

    IDs_devices, bind = get_ID_devices()
    IDs_devices = pd.read_sql(IDs_devices.statement, bind)["ID"].to_list()
    IDs_devices.sort()

    return IDs_devices


def create_table_dataframe():
    devices_table, bind = get_devices()
    df_devices = pd.read_sql(devices_table.statement, bind)

    df_devices.sort_values('ID', inplace=True, ignore_index=True)

    df_devices["max_people_alert"] = df_devices["max_people"].apply(lambda x: int(x*0.9))

    return df_devices


def set_table_columns(df):
    columns = list(df.columns)
    columns.remove("max_people_alert")

    return [{"name": i, "id": i} for i in columns]




def create_occupancy_dataframe(ID_device):

    occupancy_sql, bind = retrieve_n_occupancy_observations(ID_device, 100)
    occupancy_record = pd.read_sql(occupancy_sql.statement, bind)

    return occupancy_record