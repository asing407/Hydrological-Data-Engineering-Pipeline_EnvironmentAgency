# How to install this project on your laptop.

# Hydrological Data Engineering Pipeline (ETL)

## Overview
This project is a simple, file-based ETL (Extract, Transform, Load) data engineering pipeline built in Python. It access hydrological data via the UK Environment Agency's Hydrological Data Explorer API, an d transforms the nested JSON responses, and loads the data into a local SQLite database using a Star Schema design.

The pipeline is designed to be **idempotent**, meaning it can be run multiple times to fetch new data without duplicating existing historical records.

## Architecture & Schema
* **Extract:** Connects to the API and fetches the 10 most recent readings for specific parameters (e.g., Dissolved Oxygen, Conductivity) at station `E64999A` (HIPPER_PARK ROAD BRIDGE).
* **Transform:** Flattens the nested JSON data and dynamically appends measurement units to the parameter names (e.g., `Dissolved Oxygen (%)` vs `Dissolved Oxygen (mg/L)`) to ensure data integrity.
* **Load:** Loads the data into a local SQLite database (`hydrology.db`) using a 
**Star Schema**:
  * **Dimension Table:** `stations`
  * **Fact Table:** `measurements`

## Prerequisites
* Python 3.8 or higher installed on your machine.
* Git (optional, for cloning the repository).

## Installation & Setup
To ensure the project runs cleanly on your machine (Windows, Mac, or Linux), it is recommended to use a virtual environment.



1. **Clone the repository (or extract the zip file) and navigate into the folder:**
   ```bash
   cd DataEngineerJob

# 2. Create a virtual environment:

On Windows: python -m venv venv

On Mac/Linux: python3 -m venv venv

# 3. Activate the virtual environment:

On Windows: venv\Scripts\activate

On Mac/Linux: source venv/bin/activate

# 4. Install the required dependencies:

pip install -r requirements.txt


# run pipeline

python main.py

# view the results of database. 
python view_results.py

# after viewing the result, run the tests. 

pytest -v