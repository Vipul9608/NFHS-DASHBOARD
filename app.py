import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Setup
# ---------------------------------
st.set_page_config(page_title="NFHS Dashboard", layout="wide")

st.title("📊 National Family Health Survey Dashboard")
st.write("Interactive Dashboard for Exploring Health Indicators in India")

# ---------------------------------
# Load Data
# ---------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey.xlsx")
    return df

df = load_data()

# ---------------------------------
# Sidebar Filters
# ---------------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox(
    "Select State / UT",
    df["India/States/UTs"].unique()
)

survey = st.sidebar.selectbox(
    "Select Survey",
    df["Survey"].unique()
)

area = st.sidebar.selectbox(
    "Select Area",
    df["Area"].unique()
)

# Filter Data
filtered_df = df[
    (df["India/States/UTs"] == state) &
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

# ---------------------------------
# Indicator Selection
# ---------------------------------
numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

indicator = st.selectbox(
    "Select Health Indicator",
    sorted(numeric_columns)
)

# ---------------------------------
# KPI Section
# ---------------------------------
st.subheader("📌 Selected Indicator Value")

if not filtered_df.empty:
    value = filtered_df[indicator].values[0]
    st.metric(label=indicator, value=round(value, 2))
else:
    st.warning("No data available")

# ---------------------------------
# Comparison Chart Across States
# ---------------------------------
st.subheader("📊 State-wise Comparison")

comparison_df = df[
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

fig = px.bar(
    comparison_df,
    x="India/States/UTs",
    y=indicator,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# Trend Across Surveys
# ---------------------------------
st.subheader("📈 Trend Across Surveys")

trend_df = df[
    (df["India/States/UTs"] == state) &
    (df["Area"] == area)
]

fig2 = px.line(
    trend_df,
    x="Survey",
    y=indicator,
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------
# Raw Data
# ---------------------------------
st.subheader("📄 Data Table")
st.dataframe(filtered_df)
