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
                    2000, 3000, 10000, 10000, 15000, 40000, 50000, 60000, 80000, 90000, 100000, 160000, 180000, 240000, \
                    12000, 40000, 40000, 60000, 160000, 200000, 240000, 320000, 360000, 400000, 640000, 720000, 960000]

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




