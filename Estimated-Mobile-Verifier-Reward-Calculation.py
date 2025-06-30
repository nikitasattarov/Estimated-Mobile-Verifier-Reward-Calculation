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

def boost_coef_integral_calculation(bl, br, xl, xr, yd, yu, k):
    dx = xr - xl
    expk = math.exp(k)
    term1 = (yu - yd) * dx * (
        math.exp(k * (br - xl) / dx) - math.exp(k * (bl - xl) / dx)
    )
    term2 = k * (br - bl) * (yd * expk - yu)
    return (term1 + term2) / (k * (expk - 1.0))

def boost_coef_calculation(dl, dr, x1, x2, x3, x4, y1, y2, y3, y4, k1, k2, k3):
    bc = 0.0

    if x1 <= dl <= x2:
        if x1 <= dr <= x2:
            bc = boost_coef_integral_calculation(dl, dr, x1, x2, y1, y2, k1)
        elif x2 < dr <= x3:
            bc = (
                boost_coef_integral_calculation(dl, x2, x1, x2, y1, y2, k1)
                + boost_coef_integral_calculation(x2, dr, x2, x3, y2, y3, k2)
            )
        elif x3 < dr <= x4:
            bc = (
                boost_coef_integral_calculation(dl, x2, x1, x2, y1, y2, k1)
                + boost_coef_integral_calculation(x2, x3, x2, x3, y2, y3, k2)
                + boost_coef_integral_calculation(x3, dr, x3, x4, y3, y4, k3)
            )

    elif x2 < dl <= x3:
        if x2 < dr <= x3:
            bc = boost_coef_integral_calculation(dl, dr, x2, x3, y2, y3, k2)
        elif x3 < dr <= x4:
            bc = (
                boost_coef_integral_calculation(dl, x3, x2, x3, y2, y3, k2)
                + boost_coef_integral_calculation(x3, dr, x3, x4, y3, y4, k3)
            )

    elif x3 < dl <= x4:
        if x3 < dr <= x4:
            bc = boost_coef_integral_calculation(dl, dr, x3, x4, y3, y4, k3)

    return bc

def calculate_sum_boost_coefficients(lst, x1, x2, x3, x4, y1, y2, y3, y4, k1, k2, k3):
    total = sum(lst)
    cumulative = 0.0
    result = []

    for value in lst:
        left_border = cumulative / total
        cumulative += value
        right_border = cumulative / total
        bc = boost_coef_calculation(
            left_border, right_border,
            x1, x2, x3, x4,
            y1, y2, y3, y4,
            k1, k2, k3
        )
        result.append(bc)

    return result

def calc_mv_rew_per_sec(t, K_r_mv, T, K_M, u_M):
    return K_r_mv * T * (1 + K_M) * (math.exp(-u_M * t) - math.exp(-u_M * (t + 1)))

K_r_mv = 0.225
K_M = 1e-5
tau = 2e9
T = 1.04e10
x1, x2, x3, x4 = 0.0, 0.3, 0.7, 1.0
y1, y2, y3, y4 = 0.0, 0.066696948409, 2.0, 8.0
k1, k2, k3 = 10.0, 1.894163612445, 17.999995065464
max_mamaboard_component_index_list = list(range(39))
user_max_index = 0
delta_mv_e = 1e5

u_M = -1 / tau * math.log(K_M / (K_M + 1))

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

with open("mbndictprev.json", 'r', encoding='utf-8') as f:
    mbn_dict_prev = {int(k): v for k, v in json.load(f).items()}

with open("gdictprev.json", 'r', encoding='utf-8') as f:
    g_dict_prev = {int(k): v for k, v in json.load(f).items()}

mbn_dict_prev[user_max_index] = mbn_dict_prev[user_max_index] + 1

g_dict_prev[user_max_index] = g_dict_prev[user_max_index] + math.log(user_max_height)

mbn_lst_prev = [value for key, value in sorted(mbn_dict_prev.items(), key=lambda item: item[0])]

g_lst_prev = [value for key, value in sorted(g_dict_prev.items(), key=lambda item: item[0])]

boost_coef_lst = calculate_sum_boost_coefficients(mbn_lst_prev, x1, x2, x3, x4, y1, y2, y3, y4, k1, k2, k3)

g_boost_sum_value = sum(ai * bi for ai, bi in zip(g_lst_prev, boost_coef_lst))

u_mv_e = user_max_height * boost_coef_lst[user_max_index] / g_boost_sum_value

st.write(u_mv_e)

t = days_to_seconds(days)

mv_rew_per_sec = calc_mv_rew_per_sec(t, K_r_mv, T, K_M, u_M)

st.write(mv_rew_per_sec)

user_reward = delta_mv_e * mv_rew_per_sec * u_mv_e

st.write(user_reward)
