Redbus Data Scraping and Filtering with Streamlit Application
Project Overview

The "Redbus Data Scraping and Filtering with Streamlit Application" project aims to automate the collection of bus travel data from the Redbus website using Selenium. This data includes bus routes, schedules, prices, seat availability, and other key information. The scraped data is then stored in a PostgreSQL database and visualized using a Streamlit-based web application, enabling users to filter and analyze bus travel options efficiently.

Approach
Web Scraping with Selenium
Automates browsing through Redbus pages.
Extracts key details such as bus name, type, departure and arrival times, duration, prices, and seat availability.
Implements dynamic pagination handling to navigate through multiple pages.
Uses delays and randomized waits to avoid bot detection.
Data Storage in PostgreSQL
Scraped data is structured and stored in PostgreSQL tables.
Tables include bus_names, link_routes, bus_types, departing_times, duration_times, reaching_times, star_ratings, prices, and seat_availabilities.
Python's psycopg2 library is used to create tables and insert data.
Data Export to CSV
Extracted data is also saved as a CSV file to allow additional analysis and backups.
Interactive Data Filtering with Streamlit
Streamlit application reads the CSV data and provides an interactive dashboard.
Users can filter buses based on route, star rating, price range, seat availability, and duration.
A recommendation system suggests the best bus based on multiple factors.
Code Explanation

1. Web Scraping with Selenium

Initialization:
Chrome WebDriver is set up with custom options to prevent automatic closure.
The script navigates to Redbus URLs provided in a list.

Pagination Handling:
The script extracts bus details from multiple pages of each Redbus URL.
Uses Selenium to interact with pagination buttons dynamically.

Data Extraction:
Scrapes details like bus name, type, departure time, duration, and seat availability using class selectors.
Stores data in Python lists for further processing.

Error Handling:
Includes exception handling to avoid crashes due to missing elements or page load issues.

2. Data Storage in PostgreSQL

Database Connection:
Uses psycopg2 to connect to PostgreSQL.

Table Creation:
Defines SQL commands to create structured tables for storing the extracted data.

Data Insertion:
Iterates through scraped data and inserts it into respective tables.
Converts values like price and ratings to appropriate SQL data types.

3. Data Export to CSV

Uses Python’s csv module to store the extracted bus details in a structured CSV file.
Ensures proper formatting of values to maintain data integrity.

4. Streamlit Application for Data Filtering

Loading Data:
Reads the CSV file into a Pandas DataFrame.

User Interface:
Uses Streamlit components like sidebar filters and data tables to display bus information.

Filtering Functionality:
Enables users to filter buses based on:
Route selection.
Star rating range.
Price range.
Duration range.

Recommendation System:
Sorts buses by best star rating, seat availability, price, and duration.
Displays the best available option.

Conclusion
This project provides a streamlined way to collect and analyze Redbus travel data. By leveraging Selenium for automation, PostgreSQL for structured storage, and Streamlit for visualization, it delivers a comprehensive tool for bus travelers and transportation analysts. Future enhancements can include:
API integration for real-time data updates.
More advanced machine learning models for bus recommendations.
Integration with Google Maps for route optimization.
