import duckdb
import logging

# RAW DATA
#  ↓
# remove duplicates
#  ↓
# remove 0-passenger trips
#  ↓
# remove 0-mile trips
#  ↓
# remove trips > 100 miles
#  ↓
# remove trips > 24 hours
#  ↓
# CLEAN DATA

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='clean.log'
)

logger = logging.getLogger(__name__)


def clean_data():

    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(
            database='emissions.duckdb',
            read_only=False
        )

                # Allow DuckDB to use disk space when operations need more memory
        con.execute("SET memory_limit='2GB'")
        con.execute("SET temp_directory='tmp_duckdb'")

        logger.info("Connected to DuckDB instance")

        # STEP 1: Remove duplicate trips
        # Create a temporary table containing only unique Yellow taxi trips
        con.execute("""
            CREATE OR REPLACE TABLE yellow_trips_clean AS
            SELECT DISTINCT *
            FROM yellow_trips;
        """)

        # Replace the original Yellow table with the cleaned table
        con.execute("""
            DROP TABLE yellow_trips;
            ALTER TABLE yellow_trips_clean RENAME TO yellow_trips;
        """)

        yellow_count = con.execute(
            "SELECT COUNT(*) FROM yellow_trips"
        ).fetchone()[0]

        print(f"Yellow rows after removing duplicates: {yellow_count}")
        logger.info(
            f"Yellow rows after removing duplicates: {yellow_count}"
        )

        # STEP 1 Remove duplicate Green taxi trips
        con.execute("""
            CREATE OR REPLACE TABLE green_trips_clean AS
            SELECT DISTINCT *
            FROM green_trips;
        """)

        con.execute("""
            DROP TABLE green_trips;
            ALTER TABLE green_trips_clean RENAME TO green_trips;
        """)

        green_count = con.execute(
            "SELECT COUNT(*) FROM green_trips"
        ).fetchone()[0]

        print(f"Green rows after removing duplicates: {green_count}")
        logger.info(
            f"Green rows after removing duplicates: {green_count}"
        )

        # Verify that no duplicate Yellow trips remain
        yellow_total = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
        """).fetchone()[0]

        yellow_unique = con.execute("""
            SELECT COUNT(DISTINCT (
                VendorID,
                pickup_time,
                dropoff_time,
                passenger_count,
                trip_distance
            ))
            FROM yellow_trips
        """).fetchone()[0]

        print(f"Yellow total rows: {yellow_total}")
        print(f"Yellow unique rows: {yellow_unique}")
        print(f"Yellow duplicate check: {yellow_total - yellow_unique}")


        # Verify that no duplicate Green trips remain
        green_total = con.execute("""
            SELECT COUNT(*) FROM green_trips
        """).fetchone()[0]

        green_unique = con.execute("""
            SELECT COUNT(DISTINCT (
                VendorID,
                pickup_time,
                dropoff_time,
                passenger_count,
                trip_distance
            ))
            FROM green_trips
        """).fetchone()[0]

        print(f"Green total rows: {green_total}")
        print(f"Green unique rows: {green_unique}")
        print(f"Green duplicate check: {green_total - green_unique}")

        # STEP 2: remove 0-passenger trips

        # Check how many Yellow trips have 0 passengers before deleting
        before = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE passenger_count = 0
        """).fetchone()[0]

        print(f"Yellow 0-passenger trips before delete: {before}")
        logger.info(f"Yellow 0-passenger trips before delete: {before}")

        # Remove Yellow trips with 0 passengers
        con.execute("""
            DELETE FROM yellow_trips
            WHERE passenger_count = 0
        """)

        # Check that no Yellow trips with 0 passengers remain
        after = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE passenger_count = 0
        """).fetchone()[0]

        print(f"Yellow 0-passenger trips after delete (verify): {after}")
        logger.info(
            f"Yellow 0-passenger trips after delete (verify): {after}"
        )


        # Check how many Green trips have 0 passengers before deleting
        before = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE passenger_count = 0
        """).fetchone()[0]

        print(f"Green 0-passenger trips before delete: {before}")
        logger.info(f"Green 0-passenger trips before delete: {before}")

        # Remove Green trips with 0 passengers
        con.execute("""
            DELETE FROM green_trips
            WHERE passenger_count = 0
        """)

        # Check that no Green trips with 0 passengers remain
        after = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE passenger_count = 0
        """).fetchone()[0]

        print(f"Green 0-passenger trips after delete (verify): {after}")
        logger.info(
            f"Green 0-passenger trips after delete (verify): {after}"
        )

        # STEP 3: remove 0-mile trips

        # Check how many Yellow trips have 0 miles
        before = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE trip_distance = 0
        """).fetchone()[0]

        print(f"Yellow 0-mile trips before delete: {before}")
        logger.info(f"Yellow 0-mile trips before delete: {before}")

        # Remove Yellow trips with 0 miles
        con.execute("""
            DELETE FROM yellow_trips
            WHERE trip_distance = 0
        """)

        # Verify that no Yellow 0-mile trips remain
        after = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE trip_distance = 0
        """).fetchone()[0]

        print(f"Yellow 0-mile trips after delete: {after}")
        logger.info(f"Yellow 0-mile trips after delete: {after}")


        # Check how many Green trips have 0 miles
        before = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE trip_distance = 0
        """).fetchone()[0]

        print(f"Green 0-mile trips before delete: {before}")
        logger.info(f"Green 0-mile trips before delete: {before}")

        # Remove Green trips with 0 miles
        con.execute("""
            DELETE FROM green_trips
            WHERE trip_distance = 0
        """)

        # Verify that no Green 0-mile trips remain
        after = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE trip_distance = 0
        """).fetchone()[0]

        print(f"Green 0-mile trips after delete: {after}")
        logger.info(f"Green 0-mile trips after delete: {after}")

        # STEP 4: trips over 100 miles

        # Yellow trips
        before = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE trip_distance > 100
        """).fetchone()[0]

        print(f"Yellow - Before delete: {before}")

        con.execute("""
            DELETE FROM yellow_trips
            WHERE trip_distance > 100
        """)

        after = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE trip_distance > 100
        """).fetchone()[0]

        print(f"Yellow - After delete (verify): {after}")


        # Green trips
        before = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE trip_distance > 100
        """).fetchone()[0]

        print(f"Green - Before delete: {before}")

        con.execute("""
            DELETE FROM green_trips
            WHERE trip_distance > 100
        """)

        after = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE trip_distance > 100
        """).fetchone()[0]

        print(f"Green - After delete (verify): {after}")

        # STEP 5: trips over 1 day

        # Yellow trips
        before = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
        """).fetchone()[0]

        print(f"Yellow - Before delete: {before}")

        con.execute("""
            DELETE FROM yellow_trips
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
        """)

        after = con.execute("""
            SELECT COUNT(*) FROM yellow_trips
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
        """).fetchone()[0]

        print(f"Yellow - After delete (verify): {after}")


        # Green trips
        before = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
        """).fetchone()[0]

        print(f"Green - Before delete: {before}")

        con.execute("""
            DELETE FROM green_trips
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
        """)

        after = con.execute("""
            SELECT COUNT(*) FROM green_trips
            WHERE date_diff('second', pickup_time, dropoff_time) > 86400
        """).fetchone()[0]

        print(f"Green - After delete (verify): {after}")

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

    finally:
        if con is not None:
            con.close()


if __name__ == "__main__":
    clean_data()



