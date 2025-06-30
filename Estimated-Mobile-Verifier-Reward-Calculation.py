import math
import json
import numpy as np
import matplotlib.pyplot as plt 
import streamlit as st
import pandas as pd
from decimal import Decimal, getcontext, ROUND_HALF_UP

getcontext().prec = 150

def dec(number):
    return(Decimal(str(number)))

def days_to_seconds(days):
    return days * 60 * 60 * 24



new_mamaboard_list = [1500, 5000, 5000, 7500, 20000, 25000, 30000, 40000, 45000, 50000, 80000, 90000, 120000, \
                    3000, 10000, 10000, 15000, 40000, 50000, 60000, 80000, 90000, 100000, 160000, 180000, 240000, \
                    12000, 40000, 40000, 60000, 160000, 200000, 240000, 320000, 360000, 400000, 640000, 720000, 960000]

max_mamaboard_component_index_list = list(range(39))
user_max_index = 0

st.title("Estimated Mobile Verifier Reward Calculation")

max_mamaboard_comp = st.selectbox(
    "Select the most recently purchased Mamaboard component:",
    (
        "Battery Power",
        "Network Card",
        "Power Supply",
        "Video Card",
        "RAM",
        "Monitor",
        "IPMI",
        "HDD",
        "UPS",
        "CPU",
        "Fiber Optical Interface",
        "M2NVME",
        "ASIC board"
    ),
    index=0
)

max_mamaboard_lvl = st.selectbox(
    "Select the level of the most recently purchased Mamaboard component:",
    (
        1,
        2,
        3
    ),
    index=0
)

days = st.number_input(
        label = r'Enter the number of days from network launch to epoch start', 
        help = r"The number of days is in $ \lbrack 1, 23148 \rbrack $", 
        value = 100, 
        format = "%i",
        min_value = 1,
        max_value = 23148
        )

user_max_height = st.number_input(
        label = r'Enter the maximum block height reached during the epoch', 
        help = r"The maximum block height is in $ \lbrack 5, 10000 \rbrack $", 
        value = 50, 
        format = "%i",
        min_value = 5,
        max_value = 10000
        )

if max_mamaboard_lvl == 1:
    sublist_max_mamaboard_component_index = max_mamaboard_component_index_list[:13]

if max_mamaboard_lvl == 2:
    sublist_max_mamaboard_component_index = max_mamaboard_component_index_list[13:26]

if max_mamaboard_lvl == 3:
    sublist_max_mamaboard_component_index = max_mamaboard_component_index_list[-13:]

if max_mamaboard_comp == "Battery Power":
    user_max_index = sublist_max_mamaboard_component_index[0]

if max_mamaboard_comp == "Network Card":
    user_max_index = sublist_max_mamaboard_component_index[1]

if max_mamaboard_comp == "Power Supply":
    user_max_index = sublist_max_mamaboard_component_index[2]

if max_mamaboard_comp == "Video Card":
    user_max_index = sublist_max_mamaboard_component_index[3]

if max_mamaboard_comp == "RAM":
    user_max_index = sublist_max_mamaboard_component_index[4]

if max_mamaboard_comp == "Monitor":
    user_max_index = sublist_max_mamaboard_component_index[5]

if max_mamaboard_comp == "IPMI":
    user_max_index = sublist_max_mamaboard_component_index[6]

if max_mamaboard_comp == "HDD":
    user_max_index = sublist_max_mamaboard_component_index[7]

if max_mamaboard_comp == "UPS":
    user_max_index = sublist_max_mamaboard_component_index[8]

if max_mamaboard_comp == "CPU":
    user_max_index = sublist_max_mamaboard_component_index[9]

if max_mamaboard_comp == "Fiber Optical Interface":
    user_max_index = sublist_max_mamaboard_component_index[10]

if max_mamaboard_comp == "M2NVME":
    user_max_index = sublist_max_mamaboard_component_index[11]

if max_mamaboard_comp == "ASIC board":
    user_max_index = sublist_max_mamaboard_component_index[12]

with open("mbnlistprev.json", 'r', encoding='utf-8') as f:
        mbndictprev = json.load(f)

st.write(mbndictprev)