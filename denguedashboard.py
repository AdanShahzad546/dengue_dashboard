import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Dengue Analysis Dashboard", layout="wide")

# Title
st.title("🦟 Dengue Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("OpenDengue_V1.2.csv", parse_dates=["calendar_start_date", "calendar_end_date"])
    df = df.rename(columns={
        "calendar_start_date": "Start Date",
        "calendar_end_date": "End Date",
        "adm_0_name": "Country",
        "adm_1_name": "Region",
        "dengue_total": "Cases"
    })
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
countries = st.sidebar.multiselect("Select Country", options=df["Country"].unique(), default=["Pakistan"])
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2010-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2023-12-31"))

# Filter data based on selections
mask = (
    df["Country"].isin(countries) &
    (df["Start Date"] >= pd.to_datetime(start_date)) &
    (df["End Date"] <= pd.to_datetime(end_date))
)
filtered_df = df[mask]

# Display data
st.subheader("Filtered Dengue Cases")
st.dataframe(filtered_df[["Start Date", "End Date", "Country", "Region", "Cases"]])

# Time series plot
st.subheader("Dengue Cases Over Time")
time_series = filtered_df.groupby("Start Date")["Cases"].sum().reset_index()
fig = px.line(time_series, x="Start Date", y="Cases", title="Dengue Cases Over Time")
st.plotly_chart(fig, use_container_width=True)

# Bar chart by region
st.subheader("Dengue Cases by Region")
region_data = filtered_df.groupby("Region")["Cases"].sum().reset_index()
fig2 = px.bar(region_data, x="Region", y="Cases", title="Dengue Cases by Region")
st.plotly_chart(fig2, use_container_width=True)
