# DS3022 - Data Project 1

## Project Overview

This project uses NYC Taxi Trip Record data from 2024 to calculate and analyze CO2 emissions from Yellow and Green taxi trips.

The pipeline uses Python and DuckDB to:

1. Load the 2024 Yellow Taxi, Green Taxi, and vehicle emissions data.
2. Clean the taxi trip data.
3. Transform the cleaned data by calculating CO2 emissions, average speed, and time-based variables.
4. Analyze CO2 emissions by trip, hour, day, week, and month.
5. Generate a plot showing total monthly CO2 emissions for Yellow and Green taxis.

The project uses the NYC Taxi Trip Record Data provided by the New York City Taxi and Limousine Commission.

## Project Structure

The main pipeline is divided into four stages:

### `load.py`

Loads the 2024 taxi trip data into DuckDB tables.

The script creates:

* `yellow_trips`
* `green_trips`
* `vehicle_emissions`

The vehicle emissions table is loaded from `data/vehicle_emissions.csv`.

The script also reports the raw number of rows loaded for each table.

### `clean.py`

Cleans the Yellow and Green taxi trip tables.

The following records are removed:

* Duplicate trips
* Trips with 0 passengers
* Trips with 0 miles
* Trips longer than 100 miles
* Trips lasting more than 24 hours

The script also verifies that these conditions no longer exist after cleaning.

### `transform.py`

Adds the following variables to the cleaned trip tables:

* `trip_co2_kgs` — CO2 produced by each trip in kilograms
* `avg_mph` — average speed of the trip in miles per hour
* `hour_of_day` — hour when the trip began
* `day_of_week` — day when the trip began
* `week_of_year` — week when the trip began
* `month_of_year` — month when the trip began

CO2 is calculated using a real-time lookup from the `vehicle_emissions` table rather than using hard-coded emission values.

The transformations are performed using Python-based DuckDB SQL commands.

### `analysis.py`

Analyzes the transformed data for both Yellow and Green taxis.

The script reports:

* The largest individual CO2-producing trip
* The average CO2 per trip for each hour of the day
* The average CO2 per trip for each day of the week
* The average CO2 per trip for each week of the year
* The average CO2 per trip for each month of the year

It also creates `co2_by_month.png`, which compares total monthly CO2 emissions for Yellow and Green taxis.

## How to Run the Pipeline

The project requires Python and the packages listed in `requirements.txt`.

First, install the required packages:

```bash
pip install -r requirements.txt
```

Then run each stage in order:

```bash
python load.py
python clean.py
python transform.py
python analysis.py
```

The scripts should be run in this order because each stage uses the database created or modified by the previous stage.

Running `analysis.py` creates:

```text
co2_by_month.png
```

The scripts also create separate log files for each stage:

```text
load.log
clean.log
transform.log
analysis.log
```

These log files are excluded from Git.

## Design Decisions

### DuckDB

DuckDB was used because the taxi dataset contains millions of records. DuckDB allows the project to perform SQL-based transformations and analysis without loading the entire dataset into pandas.

### Selecting Columns

Only the columns needed for the assignment were retained from the original taxi data. This reduces the amount of data stored and makes the database easier to work with.

### CO2 Calculation

CO2 emissions are calculated using the `vehicle_emissions` lookup table:

```text
trip_distance × co2_grams_per_mile ÷ 1000
```

This produces CO2 in kilograms.

The emission value is looked up from the database using the taxi type instead of being hard-coded into the transformation queries.

### Average Speed

Average speed is calculated as:

```text
trip distance ÷ trip duration in hours
```

A `NULLIF` is used when calculating the duration so that a zero-duration trip does not cause a division-by-zero error.

### Time Variables

DuckDB date/time extraction functions are used to create the hour, day, week, and month variables directly from `pickup_time`.

DuckDB's hour values range from 0–23, while the assignment asks for hours 1–24. The analysis therefore displays the hour as the DuckDB hour plus one.

### Memory Management

The taxi data contains tens of millions of rows. The cleaning stage uses DuckDB's memory and temporary-directory settings so that large operations can be processed without exceeding the available memory.

## Analysis Results

The final analysis produced the following results.

### Largest CO2-Producing Trip

| Taxi Type |      CO2 |    Distance |
| --------- | -------: | ----------: |
| Yellow    | 37.95 kg | 99.86 miles |
| Green     | 34.75 kg | 99.28 miles |

### Heaviest and Lightest Hour

| Taxi Type | Heaviest Hour |  Average CO2 | Lightest Hour |  Average CO2 |
| --------- | ------------: | -----------: | ------------: | -----------: |
| Yellow    |             6 | 2.32 kg/trip |            19 | 1.14 kg/trip |
| Green     |             6 | 1.60 kg/trip |            19 | 0.92 kg/trip |

### Heaviest and Lightest Day

| Taxi Type | Heaviest Day |  Average CO2 | Lightest Day |  Average CO2 |
| --------- | ------------ | -----------: | ------------ | -----------: |
| Yellow    | Sunday       | 1.46 kg/trip | Saturday     | 1.22 kg/trip |
| Green     | Sunday       | 1.12 kg/trip | Tuesday      | 1.00 kg/trip |

### Heaviest and Lightest Week

| Taxi Type | Heaviest Week |  Average CO2 | Lightest Week |  Average CO2 |
| --------- | ------------: | -----------: | ------------: | -----------: |
| Yellow    |            35 | 1.47 kg/trip |            51 | 1.17 kg/trip |
| Green     |            35 | 1.39 kg/trip |             3 | 0.94 kg/trip |

### Heaviest and Lightest Month

| Taxi Type | Heaviest Month |  Average CO2 | Lightest Month |  Average CO2 |
| --------- | -------------- | -----------: | -------------- | -----------: |
| Yellow    | August         | 1.40 kg/trip | February       | 1.23 kg/trip |
| Green     | August         | 1.15 kg/trip | January        | 0.97 kg/trip |

## Plot

The project includes the required monthly CO2 plot:

`co2_by_month.png`

The plot contains two series, one for Yellow Taxi trips and one for Green Taxi trips, with month on the x-axis and total CO2 emissions in kilograms on the y-axis.

Yellow Taxi totals are substantially larger because the dataset contains many more Yellow Taxi trips than Green Taxi trips.

## Files Not Committed

The local DuckDB database and log files are required while running the pipeline but are not committed to the repository.

The `.gitignore` excludes:

```text
*.parquet
*.log
*.duckdb
```

This keeps large data files, local database files, and generated logs out of the Git repository.

## Scope

This project covers the required 2024 data.

The optional extensions covering the full 2015–2024 period and DBT-based transformations were not completed

