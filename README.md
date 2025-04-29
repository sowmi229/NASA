# NASA
NASA Near-Earth Object (NEO) Tracking & Insights
A Streamlit web application to explore and analyze data about asteroids and near-Earth objects (NEOs) using an interactive dashboard powered by SQL queries and data filters.

🚀 Features
📊 Query Dashboard: Execute 20 pre-defined analytical SQL queries on NASA's NEO dataset.

🔍 Filter Dashboard: Filter asteroids using interactive widgets (e.g., size, velocity, magnitude, dates).

🌌 Stylized UI: Clean and engaging interface with space-themed backgrounds.

💾 Downloadable Results: Export query results to CSV directly from the interface.

🧠 Technologies Used
Streamlit – Python web app framework

Pandas – Data manipulation

MySQL – Relational database backend

streamlit-option-menu – Sidebar navigation

🗃️ Database Schema
Two MySQL tables assumed:

asteroids – Includes asteroid metadata such as name, estimated diameter, magnitude, hazardous flag, etc.

close_approach – Includes close approach details such as date, miss distance, and velocity.

📦 Setup Instructions

Set Up the MySQL Database

Create a database called nasa

Import the required tables: asteroids and close_approach

Adjust the credentials in get_connection():

python
Copy
Edit
host="localhost",
user="your_user",
password="your_password",
database="nasa"
Run the App

bash
Copy
Edit
streamlit run app.py
📁 File Structure
text
Copy
Edit
nasa-neo-tracker/
│
├── app.py                # Main Streamlit application
├── README.md             # This file
├── requirements.txt      # Required Python packages
└── ...                   # Other supporting files
✅ Example Queries Supported
Asteroids approaching Earth most frequently

Average approach velocity per asteroid

Top 10 fastest asteroids

Hazardous asteroids with multiple approaches

Month with most approaches
...and more (20+ pre-built queries)

