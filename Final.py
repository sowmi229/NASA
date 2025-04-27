import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import mysql.connector
from datetime import datetime

# Function to connect to MySQL database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="sowmiya",
        password="tiger",
        database="nasa"
    )

# Function to execute SQL query and return results as DataFrame
def run_query(query):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(results)

# App title
st.title("NASA Near-Earth Object (NEO) Tracking & Insights")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Queries", "Filters"],
        icons=["house", "info-circle"],
        menu_icon="cast",
        default_index=0
    )

# Home Page
if selected == "Queries":
    st.title("\U0001F320 Asteroid Data Explorer")
    st.write("Explore near-Earth objects in style!")

    # Background Image
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Question Selector
    option = st.selectbox("Select a question to query:", [
        "1) Count how many times each asteroid has approached Earth",
        "2) Average velocity of each asteroid over multiple approaches",
        "3) List top 10 fastest asteroids",
        "4) Find potentially hazardous asteroids that have approached Earth more than 3 times",
        "5) Find the month with the most asteroid approaches",
        "6) Get the asteroid with the fastest ever approach speed",
        "7) Sort asteroids by maximum estimated diameter (descending)",
        "8) Asteroids whose closest approach is getting nearer over time",
        "9) Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
        "10) List names of asteroids that approached Earth with velocity > 50,000 km/h",
        "11) Count how many approaches happened per month",
        "12) Find asteroid with the highest brightness (lowest magnitude value)",
        "13) Get number of hazardous vs non-hazardous asteroids",
        "14) Find asteroids that passed closer than the Moon (< 1 LD), with date and distance",
        "15) Find asteroids that came within 0.05 AU",
        "16) Find the average estimated diameter for hazardous vs non-hazardous asteroids",
        "17) Which asteroid had the longest time gap between two approaches?",
        "18) Display all asteroid approaches on a specific date",
        "19) Count how many unique asteroids approached Earth in each year",
        "20) List asteroids that approached Earth on weekends"
    ])

    # SQL query definitions
    queries = {
        "1": """SELECT a.name, COUNT(c.neo_reference_id) AS approach_count FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id GROUP BY a.name;""",
        "2": """SELECT a.name, AVG(c.relative_velocity_kmph) AS average_velocity FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id GROUP BY a.name;""",
        "3": """SELECT a.name, MAX(c.relative_velocity_kmph) AS max_velocity FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id GROUP BY a.name ORDER BY max_velocity DESC LIMIT 10;""",
        "4": """SELECT a.name, COUNT(c.neo_reference_id) AS approach_count FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id WHERE a.is_potentially_hazardous_asteroid = TRUE GROUP BY a.name HAVING approach_count > 3;""",
        "5": """SELECT EXTRACT(MONTH FROM close_approach_date) AS approach_month, COUNT(*) AS approach_count FROM close_approach GROUP BY approach_month ORDER BY approach_count DESC LIMIT 1;""",
        "6": """SELECT a.name, MAX(c.relative_velocity_kmph) AS fastest_velocity FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id GROUP BY a.name ORDER BY fastest_velocity DESC LIMIT 1;""",
        "7": """SELECT a.name, a.estimated_diameter_max_km FROM asteroids a ORDER BY a.estimated_diameter_max_km DESC;""",
        "8": """SELECT a.name, c.close_approach_date, c.miss_distance_km FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id ORDER BY c.close_approach_date, c.miss_distance_km ASC;""",
        "9": """SELECT a.name, c.close_approach_date, c.miss_distance_km FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id;""",
        "10": """SELECT a.name FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id WHERE c.relative_velocity_kmph > 50000;""",
        "11": """SELECT EXTRACT(MONTH FROM close_approach_date) AS approach_month, COUNT(*) AS approach_count FROM close_approach GROUP BY approach_month;""",
        "12": """SELECT a.name, a.absolute_magnitude_h FROM asteroids a ORDER BY a.absolute_magnitude_h ASC LIMIT 1;""",
        "13": """SELECT SUM(CASE WHEN a.is_potentially_hazardous_asteroid = TRUE THEN 1 ELSE 0 END) AS hazardous_count, SUM(CASE WHEN a.is_potentially_hazardous_asteroid = FALSE THEN 1 ELSE 0 END) AS non_hazardous_count FROM asteroids a;""",
        "14": """SELECT a.name, c.close_approach_date, c.miss_distance_lunar FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id WHERE c.miss_distance_lunar < 1;""",
        "15": """SELECT a.name, c.close_approach_date, c.astronomical FROM asteroids a JOIN close_approach c ON a.id = c.neo_reference_id WHERE c.astronomical < 0.05;""",
        "16": """SELECT is_potentially_hazardous_asteroid, AVG((estimated_diameter_min_km + estimated_diameter_max_km) / 2) AS avg_estimated_diameter_km FROM asteroids GROUP BY is_potentially_hazardous_asteroid;""",
        "17": """SELECT neo_reference_id, name, MAX(DATEDIFF(close_approach_date, LAG(close_approach_date) OVER (PARTITION BY neo_reference_id ORDER BY close_approach_date))) AS max_gap_days FROM close_approach JOIN asteroids ON close_approach.neo_reference_id = asteroids.id;""",
        "18": """SELECT ca.neo_reference_id, a.name, ca.close_approach_date, ca.relative_velocity_kmph, ca.miss_distance_km FROM close_approach ca JOIN asteroids a ON ca.neo_reference_id = a.id WHERE ca.close_approach_date = '2024-01-01';""",
        "19": """SELECT YEAR(close_approach_date) AS year, COUNT(DISTINCT neo_reference_id) AS unique_asteroids FROM close_approach GROUP BY YEAR(close_approach_date) ORDER BY year;""",
        "20": """SELECT ca.neo_reference_id, a.name, ca.close_approach_date FROM close_approach ca JOIN asteroids a ON ca.neo_reference_id = a.id WHERE DAYOFWEEK(close_approach_date) IN (1, 7);"""
    }

    selected_num = option.split(")")[0]
    query = queries.get(selected_num, "")

    if st.button("Submit"):
        if query:
            df = run_query(query)
            if df.empty:
                st.warning("No data found for the selected query.")
            else:
                st.success(f"Query returned {len(df)} rows.")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, "asteroid_data.csv", "text/csv")
        else:
            st.error("Please select a valid option.")
# About Page
elif selected == "Filters":
    #st.title("ℹ️ Filters Dashboard")
    #st.write("This dashboard allows you to explore NASA's Near-Earth Object (NEO) data.")
    space_background = """
 <style>
 body {
    background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
 }

 div.stApp {
    background-color: rgba(0, 0, 0, 0.5);  /* Dark overlay for readability */
 }
 </style>
 """
    st.markdown(space_background, unsafe_allow_html=True)
    # --- Function to load data from database
    @st.cache_data
    def load_data():
        conn = get_connection()
        asteroids = pd.read_sql("SELECT * FROM asteroids", conn)
        close_approach = pd.read_sql("SELECT * FROM close_approach", conn)
        conn.close()
        return asteroids, close_approach

    # --- Load data
    asteroids, close_approach = load_data()

    # --- Title
    st.markdown("<h1 style='text-align: center;'>🚀 NASA Asteroid Tracker 🛰️</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # --- Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        magnitude = st.slider("Min Magnitude", 0.0, 35.0, (13.8, 32.61))
        min_diameter = st.slider("Min Estimated Diameter (km)", 0.0, 5.0, (0.0, 4.62))
        max_diameter = st.slider("Max Estimated Diameter (km)", 0.0, 12.0, (0.0, 10.33))

    with col2:
        velocity = st.slider("Relative_velocity_kmph Range", 0.0, 180000.0, (1418.21, 173071.83))
        astronomical = st.slider("Astronomical Unit", 0.0, 0.5, (0.0, 0.5))
        hazardous = st.selectbox("Only Show Potentially Hazardous", ("Both", "Yes", "No"))

    with col3:
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
        end_date = st.date_input("End Date", datetime(2024, 1, 7))

        # Convert to pandas Timestamp
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        

    if st.button("Filter"):
        # --- Merge two tables
        data = asteroids.merge(close_approach, left_on="id", right_on="neo_reference_id")
        data['close_approach_date'] = pd.to_datetime(data['close_approach_date'])
        # --- Apply Filters
        data = data[
            (data['mag'] >= magnitude[0]) & (data['mag'] <= magnitude[1]) &
            (data['estimated_diameter_min_km'] >= min_diameter[0]) & (data['estimated_diameter_min_km'] <= min_diameter[1]) &
            (data['estimated_diameter_max_km'] >= max_diameter[0]) & (data['estimated_diameter_max_km'] <= max_diameter[1]) &
            (data['relative_velocity_kmph'] >= velocity[0]) & (data['relative_velocity_kmph'] <= velocity[1]) &
            (data['astronomical'] >= astronomical[0]) & (data['astronomical'] <= astronomical[1]) &
            (data['close_approach_date'] >= start_date) & (data['close_approach_date'] <= end_date)
        ]

        if hazardous == "Yes":
            data = data[data['is_potentially_hazardous_asteroid'] == 1]
        elif hazardous == "No":
            data = data[data['is_potentially_hazardous_asteroid'] == 0]

        st.markdown("### Filtered Asteroids")
        st.dataframe(data.head(500), use_container_width=True)
