# monthly plotting
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import july
from july.utils import date_range
import pandas as pd

df=pd.read_csv("C:/Users/yash1/Desktop/Data Analyst/week 16 sql/data.csv")
data=df['amount_spend']
## Create data
dates = date_range("2020-01-01", "2020-12-31")


## Create a figure with a single axes
fig, ax = plt.subplots(figsize=(30, 20))
## Tell july to make a plot in a specific axes
july.heatmap(
    dates=dates,
    data=data,
    cmap='github',
    month_grid=True,
    horizontal=True,
    value_label=True,
    date_label=False,
    weekday_label=True,
    month_label=True,
    year_label=True,
    colorbar=True,
    fontfamily="monospace",
    fontsize=15,
    title="Daily Spending",
    ax=ax   ## <- Tell July to put the heatmap in that Axes
)

st.pyplot(fig) 