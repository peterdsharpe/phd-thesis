# Set up general imports and locate data sources
import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p
import pandas as pd
from scipy import interpolate, ndimage
import copy
from tqdm import tqdm

timestamp_0 = 539330432

raw_time_takeoff = 577
raw_time_landing = 840

t_max = raw_time_landing - raw_time_takeoff

data_sources = {
    "airspeed"  : ("../data/flight3_airspeed_validated_0.csv", "calibrated_airspeed_m_s"),
    "barometer" : ("../data/flight3_sensor_baro_0.csv", "pressure"),
    "baro_alt"  : ("../data/flight3_vehicle_air_data_0.csv", "baro_alt_meter"),
    "gps_alt_mm": ("../data/flight3_vehicle_gps_position_0.csv", "alt"),
    "voltage"   : ("../data/flight3_battery_status_1.csv", "voltage_v"),
    "current"   : ("../data/flight3_battery_status_1.csv", "current_a"),
}

def simple_read(name):
    source = data_sources[name][0]
    colname = data_sources[name][1]

    df = pd.read_csv(source)

    raw_time = (df["timestamp"].values - timestamp_0) / 1e6
    data = df[colname].values

    mask = (raw_time > raw_time_takeoff) & (raw_time < raw_time_landing)

    time = raw_time[mask] - raw_time_takeoff
    data = data[mask]

    return time, data

import graphviz

gv_settings = dict(
    graph_attr=dict(
        rankdir='TB',
        nodesep='0.1',
        bgcolor='#FFFFFF',
        splines='ortho',
    ),
    node_attr=dict(
        shape='box',
        style='rounded,filled',
        fillcolor='#E9F1F7',
        fontname='Helvetica',
        fontsize='10',
        color='#333333',
    ),
    edge_attr=dict(
        arrowhead='vee',
        arrowtail='none',
        fontname='Helvetica',
        fontsize='10',
        color='#555555',
    ),
)