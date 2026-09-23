import duckdb
import logging


# Set up logging so that important information and errors
# from the transformation process are saved in transform.log.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='transform.log'
)

# Create a logger that we can use to record information
# while the transformation script is running.
logger = logging.getLogger(__name__)


def transform_data():
    """
    Connect to the DuckDB database and transform the
    cleaned Yellow and Green trip tables.

    The transformations will add calculated columns for:
    - CO2 produced per trip
    - average speed
    - hour of day
    - day of week
    - week of year
    - month of year
    """

    # Start with no database connection.
    # This allows the finally block to safely check
    # whether a connection was created before closing it.
    con = None

    try:
        # Connect to the existing DuckDB database.
        # read_only=False allows us to modify the tables
        # by adding the new transformation columns.
        con = duckdb.connect(database='emissions.duckdb',read_only=False)
        logger.info("Connected to DuckDB instance")
    

        # STEP 1: Calculate CO2 produced by each trip.
        # The CO2 value comes from the vehicle_emissions lookup table.
        # Join each trip table to the appropriate vehicle type instead of hard-coding the CO2 value.
        
        # Formula:trip_distance * co2_grams_per_mile / 1000
        # Dividing by 1000 converts grams of CO2 to kilograms.

        # Add the trip_co2_kgs column to the Yellow trips table.
        con.execute("""
            ALTER TABLE yellow_trips
            ADD COLUMN IF NOT EXISTS trip_co2_kgs DOUBLE;
        """)

        # Calculate CO2 for each Yellow taxi trip.
        # The FROM clause looks up the CO2 grams per mile for a yellow taxi from the vehicle_emissions table.
        con.execute("""
            UPDATE yellow_trips
            SET trip_co2_kgs =
                trip_distance * emissions.co2_grams_per_mile / 1000
            FROM vehicle_emissions AS emissions
            WHERE emissions.vehicle_type = 'yellow_taxi';
        """)

        # Add the trip_co2_kgs column to the Green trips table.
        con.execute("""
            ALTER TABLE green_trips
            ADD COLUMN IF NOT EXISTS trip_co2_kgs DOUBLE;
        """)

        # Calculate CO2 for each Green taxi trip.
        # The FROM clause looks up the CO2 grams per mile for a green taxi
        # from the vehicle_emissions table.
        con.execute("""
            UPDATE green_trips
            SET trip_co2_kgs =
                trip_distance * emissions.co2_grams_per_mile / 1000
            FROM vehicle_emissions AS emissions
            WHERE emissions.vehicle_type = 'green_taxi';
        """)

        print("Calculated trip_co2_kgs for Yellow and Green trips")
        logger.info("Calculated trip_co2_kgs for Yellow and Green trips")


        # STEP 2: Calculate average miles per hour.
        # Average speed is calculated by dividing the trip distance by the trip duration in hours.
        # date_diff('second', pickup_time, dropoff_time) gives the trip duration in seconds.

        # Dividing by 3600 converts seconds to hours.
        # NULLIF prevents a divide-by-zero error if a trip has a duration of exactly 0 seconds.

        # Add the avg_mph column to the Yellow trips table.
        con.execute("""
            ALTER TABLE yellow_trips
            ADD COLUMN IF NOT EXISTS avg_mph DOUBLE;
        """)

        # Calculate average miles per hour for Yellow trips.
        con.execute("""
            UPDATE yellow_trips
            SET avg_mph =
                trip_distance /
                NULLIF(
                    date_diff('second', pickup_time, dropoff_time) / 3600.0,
                    0
                );
        """)

        # Add the avg_mph column to the Green trips table.
        con.execute("""
            ALTER TABLE green_trips
            ADD COLUMN IF NOT EXISTS avg_mph DOUBLE;
        """)

        # Calculate average miles per hour for Green trips.
        con.execute("""
            UPDATE green_trips
            SET avg_mph =
                trip_distance /
                NULLIF(
                    date_diff('second', pickup_time, dropoff_time) / 3600.0,
                    0
                );
        """)

        print("Calculated avg_mph for Yellow and Green trips")
        logger.info("Calculated avg_mph for Yellow and Green trips")

        # STEP 3: Extract the hour of the day.
        
        # EXTRACT(HOUR FROM pickup_time) gets the hour when the trip started.
        
        # The result will be a number from 0 to 23.

        # Add the hour_of_day column to the Yellow trips table.
        con.execute("""
            ALTER TABLE yellow_trips
            ADD COLUMN IF NOT EXISTS hour_of_day INTEGER;
        """)

        # Extract the pickup hour for Yellow trips.
        con.execute("""
            UPDATE yellow_trips
            SET hour_of_day = EXTRACT(HOUR FROM pickup_time);
        """)

        # Add the hour_of_day column to the Green trips table.
        con.execute("""
            ALTER TABLE green_trips
            ADD COLUMN IF NOT EXISTS hour_of_day INTEGER;
        """)

        # Extract the pickup hour for Green trips.
        con.execute("""
            UPDATE green_trips
            SET hour_of_day = EXTRACT(HOUR FROM pickup_time);
        """)

        print("Calculated hour_of_day for Yellow and Green trips")
        logger.info("Calculated hour_of_day for Yellow and Green trips")

        # STEP 4: Extract the day of the week.
        
        # EXTRACT(DAYOFWEEK FROM pickup_time) gets the
        # day of the week when the trip started.

        # Add the day_of_week column to the Yellow trips table.
        con.execute("""
            ALTER TABLE yellow_trips
            ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
        """)

        # Extract the day of the week for Yellow trips.
        con.execute("""
            UPDATE yellow_trips
            SET day_of_week = EXTRACT(DAYOFWEEK FROM pickup_time);
        """)

        # Add the day_of_week column to the Green trips table.
        con.execute("""
            ALTER TABLE green_trips
            ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
        """)

        # Extract the day of the week for Green trips.
        con.execute("""
            UPDATE green_trips
            SET day_of_week = EXTRACT(DAYOFWEEK FROM pickup_time);
        """)

        print("Calculated day_of_week for Yellow and Green trips")
        logger.info("Calculated day_of_week for Yellow and Green trips")

        # STEP 5: Extract the week of the year.
        
        # EXTRACT(WEEK FROM pickup_time) gets the week number for the date when the trip started.

        # Add the week_of_year column to the Yellow trips table.
        con.execute("""
            ALTER TABLE yellow_trips
            ADD COLUMN IF NOT EXISTS week_of_year INTEGER;
        """)

        # Extract the week of the year for Yellow trips.
        con.execute("""
            UPDATE yellow_trips
            SET week_of_year = EXTRACT(WEEK FROM pickup_time);
        """)

        # Add the week_of_year column to the Green trips table.
        con.execute("""
            ALTER TABLE green_trips
            ADD COLUMN IF NOT EXISTS week_of_year INTEGER;
        """)

        # Extract the week of the year for Green trips.
        con.execute("""
            UPDATE green_trips
            SET week_of_year = EXTRACT(WEEK FROM pickup_time);
        """)

        print("Calculated week_of_year for Yellow and Green trips")
        logger.info("Calculated week_of_year for Yellow and Green trips")

        # STEP 6: Extract the month of the year.
        
        # EXTRACT(MONTH FROM pickup_time) gets the month when the trip started.
        
        # The result will be a number from 1 to 12.

        # Add the month_of_year column to the Yellow trips table.
        con.execute("""
            ALTER TABLE yellow_trips
            ADD COLUMN IF NOT EXISTS month_of_year INTEGER;
        """)

        # Extract the month for Yellow trips.
        con.execute("""
            UPDATE yellow_trips
            SET month_of_year = EXTRACT(MONTH FROM pickup_time);
        """)

        # Add the month_of_year column to the Green trips table.
        con.execute("""
            ALTER TABLE green_trips
            ADD COLUMN IF NOT EXISTS month_of_year INTEGER;
        """)

        # Extract the month for Green trips.
        con.execute("""
            UPDATE green_trips
            SET month_of_year = EXTRACT(MONTH FROM pickup_time);
        """)

        print("Calculated month_of_year for Yellow and Green trips")
        logger.info("Calculated month_of_year for Yellow and Green trips")


    except Exception as e:
        # If something goes wrong, print the error
        # and also save it to the log file.
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

    finally:
        # Close the database connection when the script
        # finishes, whether it succeeds or encounters an error.
        if con is not None:
            con.close()
            logger.info("Closed DuckDB connection")


# This makes sure the transformation function runs
# when we execute "python transform.py" from the terminal.
if __name__ == "__main__":
    transform_data()
