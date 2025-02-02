from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

# Configure Chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
driver = webdriver.Chrome(options=options)

# Global Variables
href = []  # Store href links
Route_Names = []  # Store route names
Route_Links = []  # Align route names with bus details
Bus_Name = []
Bus_Type = []
Departing_Time = []
Duration_Time = []
Reaching_Time = []
Star_Rating = []
Price = []
Seat_Availability = []

# Function to extract all href links and route names on the current page
def get_all_links_and_routes():
    elements = driver.find_elements(By.CLASS_NAME, "route")
    for element in elements:
        link = element.get_attribute("href")
        route_name = element.text.strip()
        if link and link not in href:
            href.append(link)
            Route_Names.append(route_name)  # Add the route name for each href link

# List of links for different bus services
bus_urls = [

    "https://www.redbus.in/online-booking/pepsu/",
    "https://www.redbus.in/online-booking/ksrtc-kerala/",
    "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/",
    "https://www.redbus.in/online-booking/west-bengal-transport-corporation",
    "https://www.redbus.in/online-booking/astc/",
    "https://www.redbus.in/online-booking/ktcl/",
    "https://www.redbus.in/online-booking/wbtc-ctc/",
    "https://www.redbus.in/online-booking/kaac-transport",
    "https://www.redbus.in/travels/nbstc",
    "https://www.redbus.in/online-booking/chandigarh-transport-undertaking-ctu",
    "https://www.redbus.in/online-booking/jksrtc",
     "https://www.redbus.in/online-booking/tsrtc/"
]

# Iterate through each URL and scrape the data
for bus_url in bus_urls:
    try:
        # Open the website
        driver.get(bus_url)
        time.sleep(3)

        # Wait until the pagination container is visible
        pagination_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'DC_117_paginationTable'))
        )

        # Get the total number of pages
        page_elements = pagination_container.find_elements(By.CLASS_NAME, 'DC_117_pageTabs')
        num_pages = len(page_elements)
        print(f"Total pages for {bus_url}: {num_pages}")

        # Iterate over each page and collect href links and route names
        for i in range(num_pages):
            try:
                # Re-locate the pagination container and elements after each page change
                pagination_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'DC_117_paginationTable'))
                )
                page_elements = pagination_container.find_elements(By.CLASS_NAME, 'DC_117_pageTabs')

                # Click on the page number
                print(f"Clicking page {i + 1}")
                actions = ActionChains(driver)
                actions.move_to_element(page_elements[i]).click().perform()

                # Wait for the page to load
                time.sleep(5)
                get_all_links_and_routes()  # Collect all links and route names on the current page

            except Exception as e:
                print(f"Error processing page {i + 1} for {bus_url}: {e}")

        # Visit each link and scrape bus details
        for idx, link in enumerate(href):
            try:
                print(f"Navigating to: {link}")
                driver.get(link)
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "button"))
                ).click()
                time.sleep(5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for buses to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "travels.lh-24.f-bold.d-color"))
                )

                # Extract bus data
                bus_names = [
                    bus.text for bus in driver.find_elements(By.CLASS_NAME, "travels.lh-24.f-bold.d-color")
                ]
                Bus_Name.extend(bus_names)

                # Align Route_Links with the number of buses
                Route_Links.extend([Route_Names[idx]] * len(bus_names))

                # Extract other data
                Bus_Type.extend(
                    [bt.text for bt in driver.find_elements(By.CLASS_NAME, "bus-type.f-12.m-top-16.l-color.evBus")]
                )
                Departing_Time.extend(
                    [dt.text for dt in driver.find_elements(By.CLASS_NAME, "dp-time.f-19.d-color.f-bold")]
                )
                Duration_Time.extend(
                    [dr.text for dr in driver.find_elements(By.CLASS_NAME, "dur.l-color.lh-24")]
                )
                Reaching_Time.extend(
                    [rt.text for rt in driver.find_elements(By.CLASS_NAME, "bp-time.f-19.d-color.disp-Inline")]
                )
                Price.extend(
                    [
                        float(pr.text.strip().replace("₹", "").replace(",", ""))
                        for pr in driver.find_elements(By.CLASS_NAME, "f-19.f-bold")
                        if pr.text.strip().replace("₹", "").replace(",", "").isdigit()
                    ]
                )
                Seat_Availability.extend(
                    [
                        int(div.text.split()[0])
                        for div in driver.find_elements(By.CLASS_NAME, "seat-left")
                    ]
                )
                Star_Rating.extend(
                    [
                        float(span.text.strip())
                        for span in driver.find_elements(By.TAG_NAME, "span")
                        if span.text.strip().replace(".", "", 1).isdigit() and 0.0 <= float(span.text.strip()) <= 5.0
                    ]
                )

                # Random delay between requests
                time.sleep(10)

            except Exception as e:
                print(f"Error scraping link {link}: {e}")

        href.clear()
        Route_Names.clear()

    except Exception as e:
        print(f"Error processing URL {bus_url}: {e}")

# Print Collected Data
print("Collected Data Summary:")
print(f"Route Names: {Route_Links}")
print(f"Bus Names: {Bus_Name}")
print(f"Bus Types: {Bus_Type}")
print(f"Departure Times: {Departing_Time}")
print(f"Durations: {Duration_Time}")
print(f"Reaching Times: {Reaching_Time}")
print(f"Star Ratings: {Star_Rating}")
print(f"Prices: {Price}")
print(f"Seat Availability: {Seat_Availability}")

# Close the browser
driver.quit()
import psycopg2

# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "GEsH@30122005"  # Replace with your password
DB_HOST = "localhost"
DB_PORT = "5432"  # Default PostgreSQL port



# SQL to create tables
CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS bus_names (
        id SERIAL PRIMARY KEY,
        bus_name VARCHAR(255) NOT NULL
    );
    ""","""
    CREATE TABLE IF NOT EXISTS link_routes (
        id SERIAL PRIMARY KEY,
        link_route VARCHAR(255) NOT NULL
    );
    """
    """
    CREATE TABLE IF NOT EXISTS bus_types (
        id SERIAL PRIMARY KEY,
        bus_type VARCHAR(255) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS deeparting_times (
    id SERIAL PRIMARY KEY,
    deeparting_time TIME NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS duration_times (
        id SERIAL PRIMARY KEY,
        duration_time VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS reeaching_times (
        id SERIAL PRIMARY KEY,
        reeaching_time TIME NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS star_ratings (
        id SERIAL PRIMARY KEY,
        star_rating NUMERIC(3, 1)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS prices (
        id SERIAL PRIMARY KEY,
        price NUMERIC(10, 2) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS seat_availabilities (
        id SERIAL PRIMARY KEY,
        seat_availability INTEGER NOT NULL
    );
    """
]

def create_tables():
    """Function to create tables in the database."""
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()

        # Create each table
        for sql in CREATE_TABLES_SQL:
            cursor.execute(sql)
            print(f"Table created or already exists: {sql.split()[2]}")

        connection.commit()
        print("All tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_data():
    """Function to insert data into tables."""
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()

        # Insert data into tables
        for i in range(len(Bus_Name)):
            cursor.execute("INSERT INTO bus_names (bus_name) VALUES (%s);", (Bus_Name[i],))
            cursor.execute("INSERT INTO link_routes (link_route) VALUES (%s);", (Route_Links[i],))
            cursor.execute("INSERT INTO bus_types (bus_type) VALUES (%s);", (Bus_Type[i],))
            cursor.execute("INSERT INTO deeparting_times (deeparting_time) VALUES (%s);", (Departing_Time[i],))
            cursor.execute("INSERT INTO duration_times (duration_time) VALUES (%s);", (Duration_Time[i],))
            cursor.execute("INSERT INTO reeaching_times (reeaching_time) VALUES (%s);", (Reaching_Time[i],))
            cursor.execute("INSERT INTO star_ratings (star_rating) VALUES (%s);", (Star_Rating[i],))
            cursor.execute("INSERT INTO prices (price) VALUES (%s);", (Price[i],))
            cursor.execute("INSERT INTO seat_availabilities (seat_availability) VALUES (%s);", (Seat_Availability[i],))
            print(f"Inserted row {i + 1}")

        connection.commit()
        print("All data inserted successfully!")

    except Exception as e:
        print(f"Error inserting data: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Create tables
create_tables()

# Insert data into tables
insert_data()



import csv


# Function to write collected data to a CSV file
def write_data_to_csv():
    # Define the header row
    header = [
        "Bus Name","Link Route", "Bus Type", "Departing Time", "Duration Time",
        "Reaching Time", "Star Rating", "Price", "Seat Availability"
    ]

    # Prepare the data by zipping all lists together
    data = zip(Bus_Name,Route_Links, Bus_Type, Departing_Time, Duration_Time,
               Reaching_Time, Star_Rating, Price, Seat_Availability)

    # Write to CSV
    with open('bus_services_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write header
        writer.writerows(data)  # Write data rows

    print("Data has been successfully written to bus_services_data.csv")


# Call the function to write the data to CSV
write_data_to_csv()

