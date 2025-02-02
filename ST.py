import streamlit as st
import pandas as pd

# Title and introduction
st.set_page_config(page_title="Bus Finder", layout="wide")
st.title("🚌Bus Finder")
st.markdown("Explore all available buses and find the best recommendation based on **star rating**, **price**, **seat availability**, and **duration**. 🚍")

# Load the dataset
df = pd.read_csv("bus_services_data.csv")

# Check required columns
required_columns = ["Link Route", "Seat Availability", "Star Rating", "Price", "Duration Time"]
if not all(col in df.columns for col in required_columns):
    st.error(f"Missing required columns. Ensure your CSV contains {required_columns}.")
    st.stop()

# Helper function to convert '6h 30m' to float hours
def duration_to_hours(duration):
    hours, minutes = 0, 0
    if "h" in duration:
        hours = int(duration.split("h")[0])
        if "m" in duration:
            minutes = int(duration.split("h")[1].replace("m", "").strip())
    elif "m" in duration:
        minutes = int(duration.replace("m", "").strip())
    return hours + minutes / 60

# Apply conversion
df["Duration (hours)"] = df["Duration Time"].apply(duration_to_hours)

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Filter by Route
route_filter = st.sidebar.selectbox("Filter by Route", options=["All"] + sorted(df["Link Route"].unique().tolist()))
if route_filter != "All":
    df = df[df["Link Route"] == route_filter]

# Filter by Star Rating
min_rating, max_rating = st.sidebar.slider("Filter by Star Rating", 0.0, 5.0, (0.0, 5.0), 0.5)

# Filter by Price
min_price, max_price = int(df["Price"].min()), int(df["Price"].max())

if min_price == max_price:
    st.sidebar.warning("Price filter is not available because all prices are the same.")
    min_price, max_price = min_price, min_price  # Disable filtering
else:
    min_price, max_price = st.sidebar.slider(
        "Filter by Price",
        min_price,
        max_price,
        (min_price, max_price)
    )

# Filter by Duration
min_duration, max_duration = st.sidebar.slider(
    "Filter by Duration (hours)",
    float(df["Duration (hours)"].min()),
    float(df["Duration (hours)"].max()),
    (float(df["Duration (hours)"].min()), float(df["Duration (hours)"].max())),
    step=0.5
)

# Apply filters
filtered_df = df[
    (df["Star Rating"] >= min_rating) &
    (df["Star Rating"] <= max_rating) &
    (df["Price"] >= min_price) &
    (df["Price"] <= max_price) &
    (df["Duration (hours)"] >= min_duration) &
    (df["Duration (hours)"] <= max_duration)
]

st.write(filtered_df)

# Recommend the best bus
if not filtered_df.empty:
    best_bus = (
        filtered_df.sort_values(
            by=["Star Rating", "Seat Availability", "Price", "Duration (hours)"],
            ascending=[False, False, True, True]
        ).iloc[0]
    )

    st.subheader("⭐ Recommended Bus")
    st.markdown(f"""
    - **Bus Name**: {best_bus['Bus Name']}
    - **Bus Route**: {best_bus['Link Route']}
    - **Star Rating**: {best_bus['Star Rating']}
    - **Price**: ₹ {best_bus['Price']}
    - **Seat Availability**: {best_bus['Seat Availability']}
    - **Duration**: {best_bus['Duration Time']}
    """)
else:
    st.info("No buses available to recommend based on the selected criteria.")
