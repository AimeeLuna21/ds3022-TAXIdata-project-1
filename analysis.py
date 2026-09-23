import duckdb
import logging
import matplotlib.pyplot as plt

# Set up logging so that the analysis results
# are saved in analysis.log.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='analysis.log'
)

# Create a logger for the analysis script.
logger = logging.getLogger(__name__)


def analyze_data():
    """
    Connect to the DuckDB database and calculate
    the required CO2 analysis results for Yellow
    and Green taxi trips.
    """

    # Start with no database connection.
    # This lets the finally block safely close the connection.
    con = None

    try:
        # Connect to the existing DuckDB database.
        con = duckdb.connect(
            database='emissions.duckdb',
            read_only=False
        )

        logger.info("Connected to DuckDB instance")
        print("Connected to DuckDB instance")

        def analyze_data():

            con = duckdb.connect(
            database='emissions.duckdb',
            read_only=False
        )

        # STEP 1: Find the largest single CO2-producing trip.

        # Find the Yellow trip with the highest CO2 output.
        yellow_largest = con.execute("""
            SELECT
                trip_co2_kgs,
                trip_distance,
                pickup_time,
                dropoff_time
            FROM yellow_trips
            ORDER BY trip_co2_kgs DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW largest carbon-producing trip: "
            f"{yellow_largest[0]:.2f} kg CO2 "
            f"({yellow_largest[1]:.2f} miles)"
        )

        logger.info(
            f"YELLOW largest carbon-producing trip: "
            f"{yellow_largest[0]:.2f} kg CO2 "
            f"({yellow_largest[1]:.2f} miles)"
        )

        # Find the Green trip with the highest CO2 output.
        green_largest = con.execute("""
            SELECT
                trip_co2_kgs,
                trip_distance,
                pickup_time,
                dropoff_time
            FROM green_trips
            ORDER BY trip_co2_kgs DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN largest carbon-producing trip: "
            f"{green_largest[0]:.2f} kg CO2 "
            f"({green_largest[1]:.2f} miles)"
        )

        logger.info(
            f"GREEN largest carbon-producing trip: "
            f"{green_largest[0]:.2f} kg CO2 "
            f"({green_largest[1]:.2f} miles)"
        )

        # STEP 2: Find the most and least carbon-heavy hours.

        # DuckDB EXTRACT(HOUR) gives hours from 0-23.
        # The assignment asks for hours numbered 1-24,
        # so we add 1 to the hour when displaying the results.
        # We group by the original hour so the calculations
        # are still based on the correct hour from the data.

        # Find the Yellow hour with the highest average CO2 per trip.
        yellow_heaviest_hour = con.execute("""
            SELECT
                hour_of_day + 1 AS hour_of_day,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY hour_of_day
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW heaviest hour of day: "
            f"{yellow_heaviest_hour[0]} "
            f"with an average of {yellow_heaviest_hour[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW heaviest hour of day: "
            f"{yellow_heaviest_hour[0]} "
            f"with an average of {yellow_heaviest_hour[1]:.2f} kg CO2 per trip"
        )

        # Find the Yellow hour with the lowest average CO2 per trip.
        yellow_lightest_hour = con.execute("""
            SELECT
                hour_of_day + 1 AS hour_of_day,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY hour_of_day
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW lightest hour of day: "
            f"{yellow_lightest_hour[0]} "
            f"with an average of {yellow_lightest_hour[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW lightest hour of day: "
            f"{yellow_lightest_hour[0]} "
            f"with an average of {yellow_lightest_hour[1]:.2f} kg CO2 per trip"
        )

        # Find the Green hour with the highest average CO2 per trip.
        green_heaviest_hour = con.execute("""
            SELECT
                hour_of_day + 1 AS hour_of_day,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY hour_of_day
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN heaviest hour of day: "
            f"{green_heaviest_hour[0]} "
            f"with an average of {green_heaviest_hour[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN heaviest hour of day: "
            f"{green_heaviest_hour[0]} "
            f"with an average of {green_heaviest_hour[1]:.2f} kg CO2 per trip"
        )

        # Find the Green hour with the lowest average CO2 per trip.
        green_lightest_hour = con.execute("""
            SELECT
                hour_of_day + 1 AS hour_of_day,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY hour_of_day
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN lightest hour of day: "
            f"{green_lightest_hour[0]} "
            f"with an average of {green_lightest_hour[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN lightest hour of day: "
            f"{green_lightest_hour[0]} "
            f"with an average of {green_lightest_hour[1]:.2f} kg CO2 per trip"
        )

        # STEP 3: Find the most and least carbon-heavy days of the week.

        # DuckDB EXTRACT(DAYOFWEEK) stores Sunday as 0
        # and Saturday as 6.
        # We use CASE to convert these numbers into day names.

        # Find the Yellow day with the highest average CO2 per trip.
        yellow_heaviest_day = con.execute("""
            SELECT
                CASE day_of_week
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                END AS day_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY day_of_week
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW heaviest day of week: "
            f"{yellow_heaviest_day[0]} "
            f"with an average of {yellow_heaviest_day[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW heaviest day of week: "
            f"{yellow_heaviest_day[0]} "
            f"with an average of {yellow_heaviest_day[1]:.2f} kg CO2 per trip"
        )

        # Find the Yellow day with the lowest average CO2 per trip.
        yellow_lightest_day = con.execute("""
            SELECT
                CASE day_of_week
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                END AS day_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY day_of_week
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW lightest day of week: "
            f"{yellow_lightest_day[0]} "
            f"with an average of {yellow_lightest_day[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW lightest day of week: "
            f"{yellow_lightest_day[0]} "
            f"with an average of {yellow_lightest_day[1]:.2f} kg CO2 per trip"
        )

        # Find the Green day with the highest average CO2 per trip.
        green_heaviest_day = con.execute("""
            SELECT
                CASE day_of_week
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                END AS day_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY day_of_week
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN heaviest day of week: "
            f"{green_heaviest_day[0]} "
            f"with an average of {green_heaviest_day[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN heaviest day of week: "
            f"{green_heaviest_day[0]} "
            f"with an average of {green_heaviest_day[1]:.2f} kg CO2 per trip"
        )

        # Find the Green day with the lowest average CO2 per trip.
        green_lightest_day = con.execute("""
            SELECT
                CASE day_of_week
                    WHEN 0 THEN 'Sunday'
                    WHEN 1 THEN 'Monday'
                    WHEN 2 THEN 'Tuesday'
                    WHEN 3 THEN 'Wednesday'
                    WHEN 4 THEN 'Thursday'
                    WHEN 5 THEN 'Friday'
                    WHEN 6 THEN 'Saturday'
                END AS day_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY day_of_week
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN lightest day of week: "
            f"{green_lightest_day[0]} "
            f"with an average of {green_lightest_day[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN lightest day of week: "
            f"{green_lightest_day[0]} "
            f"with an average of {green_lightest_day[1]:.2f} kg CO2 per trip"
        )

        # STEP 4: Find the most and least carbon-heavy weeks of the year.

        # Find the Yellow week with the highest average CO2 per trip.
        yellow_heaviest_week = con.execute("""
            SELECT
                week_of_year,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY week_of_year
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW heaviest week of year: "
            f"{yellow_heaviest_week[0]} "
            f"with an average of {yellow_heaviest_week[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW heaviest week of year: "
            f"{yellow_heaviest_week[0]} "
            f"with an average of {yellow_heaviest_week[1]:.2f} kg CO2 per trip"
        )

        # Find the Yellow week with the lowest average CO2 per trip.
        yellow_lightest_week = con.execute("""
            SELECT
                week_of_year,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY week_of_year
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW lightest week of year: "
            f"{yellow_lightest_week[0]} "
            f"with an average of {yellow_lightest_week[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW lightest week of year: "
            f"{yellow_lightest_week[0]} "
            f"with an average of {yellow_lightest_week[1]:.2f} kg CO2 per trip"
        )

        # Find the Green week with the highest average CO2 per trip.
        green_heaviest_week = con.execute("""
            SELECT
                week_of_year,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY week_of_year
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN heaviest week of year: "
            f"{green_heaviest_week[0]} "
            f"with an average of {green_heaviest_week[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN heaviest week of year: "
            f"{green_heaviest_week[0]} "
            f"with an average of {green_heaviest_week[1]:.2f} kg CO2 per trip"
        )

        # Find the Green week with the lowest average CO2 per trip.
        green_lightest_week = con.execute("""
            SELECT
                week_of_year,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY week_of_year
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN lightest week of year: "
            f"{green_lightest_week[0]} "
            f"with an average of {green_lightest_week[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN lightest week of year: "
            f"{green_lightest_week[0]} "
            f"with an average of {green_lightest_week[1]:.2f} kg CO2 per trip"
        )

        # STEP 5: Find the most and least carbon-heavy months of the year.

        # Use month numbers from 1-12 and convert them to
        # month names so the results are easier to read.

        # Find the Yellow month with the highest average CO2 per trip.
        yellow_heaviest_month = con.execute("""
            SELECT
                CASE month_of_year
                    WHEN 1 THEN 'January'
                    WHEN 2 THEN 'February'
                    WHEN 3 THEN 'March'
                    WHEN 4 THEN 'April'
                    WHEN 5 THEN 'May'
                    WHEN 6 THEN 'June'
                    WHEN 7 THEN 'July'
                    WHEN 8 THEN 'August'
                    WHEN 9 THEN 'September'
                    WHEN 10 THEN 'October'
                    WHEN 11 THEN 'November'
                    WHEN 12 THEN 'December'
                END AS month_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY month_of_year
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW heaviest month of year: "
            f"{yellow_heaviest_month[0]} "
            f"with an average of {yellow_heaviest_month[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW heaviest month of year: "
            f"{yellow_heaviest_month[0]} "
            f"with an average of {yellow_heaviest_month[1]:.2f} kg CO2 per trip"
        )

        # Find the Yellow month with the lowest average CO2 per trip.
        yellow_lightest_month = con.execute("""
            SELECT
                CASE month_of_year
                    WHEN 1 THEN 'January'
                    WHEN 2 THEN 'February'
                    WHEN 3 THEN 'March'
                    WHEN 4 THEN 'April'
                    WHEN 5 THEN 'May'
                    WHEN 6 THEN 'June'
                    WHEN 7 THEN 'July'
                    WHEN 8 THEN 'August'
                    WHEN 9 THEN 'September'
                    WHEN 10 THEN 'October'
                    WHEN 11 THEN 'November'
                    WHEN 12 THEN 'December'
                END AS month_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM yellow_trips
            GROUP BY month_of_year
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"YELLOW lightest month of year: "
            f"{yellow_lightest_month[0]} "
            f"with an average of {yellow_lightest_month[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"YELLOW lightest month of year: "
            f"{yellow_lightest_month[0]} "
            f"with an average of {yellow_lightest_month[1]:.2f} kg CO2 per trip"
        )

        # Find the Green month with the highest average CO2 per trip.
        green_heaviest_month = con.execute("""
            SELECT
                CASE month_of_year
                    WHEN 1 THEN 'January'
                    WHEN 2 THEN 'February'
                    WHEN 3 THEN 'March'
                    WHEN 4 THEN 'April'
                    WHEN 5 THEN 'May'
                    WHEN 6 THEN 'June'
                    WHEN 7 THEN 'July'
                    WHEN 8 THEN 'August'
                    WHEN 9 THEN 'September'
                    WHEN 10 THEN 'October'
                    WHEN 11 THEN 'November'
                    WHEN 12 THEN 'December'
                END AS month_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY month_of_year
            ORDER BY average_co2 DESC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN heaviest month of year: "
            f"{green_heaviest_month[0]} "
            f"with an average of {green_heaviest_month[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN heaviest month of year: "
            f"{green_heaviest_month[0]} "
            f"with an average of {green_heaviest_month[1]:.2f} kg CO2 per trip"
        )

        # Find the Green month with the lowest average CO2 per trip.
        green_lightest_month = con.execute("""
            SELECT
                CASE month_of_year
                    WHEN 1 THEN 'January'
                    WHEN 2 THEN 'February'
                    WHEN 3 THEN 'March'
                    WHEN 4 THEN 'April'
                    WHEN 5 THEN 'May'
                    WHEN 6 THEN 'June'
                    WHEN 7 THEN 'July'
                    WHEN 8 THEN 'August'
                    WHEN 9 THEN 'September'
                    WHEN 10 THEN 'October'
                    WHEN 11 THEN 'November'
                    WHEN 12 THEN 'December'
                END AS month_name,
                AVG(trip_co2_kgs) AS average_co2
            FROM green_trips
            GROUP BY month_of_year
            ORDER BY average_co2 ASC
            LIMIT 1;
        """).fetchone()

        print(
            f"GREEN lightest month of year: "
            f"{green_lightest_month[0]} "
            f"with an average of {green_lightest_month[1]:.2f} kg CO2 per trip"
        )

        logger.info(
            f"GREEN lightest month of year: "
            f"{green_lightest_month[0]} "
            f"with an average of {green_lightest_month[1]:.2f} kg CO2 per trip"
        )

        # STEP 6: Create a plot of total CO2 by month.

        # Get the total Yellow CO2 for each month.
        yellow_monthly = con.execute("""
            SELECT
                month_of_year,
                SUM(trip_co2_kgs) AS total_co2
            FROM yellow_trips
            GROUP BY month_of_year
            ORDER BY month_of_year;
        """).fetchall()

        # Get the total Green CO2 for each month.
        green_monthly = con.execute("""
            SELECT
                month_of_year,
                SUM(trip_co2_kgs) AS total_co2
            FROM green_trips
            GROUP BY month_of_year
            ORDER BY month_of_year;
        """).fetchall()

        # Create lists of months and total CO2 values for plotting.
        months = [row[0] for row in yellow_monthly]
        yellow_co2 = [row[1] for row in yellow_monthly]
        green_co2 = [row[1] for row in green_monthly]

        # Use month names for the x-axis.
        month_names = [
            'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August',
            'September', 'October', 'November', 'December'
        ]

        # Create the line plot.
        plt.figure(figsize=(10, 6))

        plt.plot(
            month_names,
            yellow_co2,
            marker='o',
            label='Yellow Taxi'
        )

        plt.plot(
            month_names,
            green_co2,
            marker='o',
            label='Green Taxi'
        )

        plt.xlabel('Month')
        plt.ylabel('Total CO2 (kg)')
        plt.title('Total CO2 Output by Month')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot as a PNG file.
        plt.savefig('co2_by_month.png')
        plt.close()

        print("Created CO2-by-month plot: co2_by_month.png")
        logger.info("Created CO2-by-month plot: co2_by_month.png")




    except Exception as e:
        # Print and log any errors that occur during analysis.
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

    finally:
        # Close the database connection when the script finishes.
        if con is not None:
            con.close()
            logger.info("Closed DuckDB connection")


# Run the analysis when the script is executed.
if __name__ == "__main__":
    analyze_data()