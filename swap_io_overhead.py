import mysql.connector
from datetime import datetime
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="#03gks03#",
        database="mobile"
    )
    db_cursor = db_connection.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    db_connection = None
    db_cursor = None
def insert_dummy_data_swap_io_overhead():
    try:
        insert_query = """
        INSERT INTO swap_io_overhead
        (pid, tid, command, read_bytes, write_bytes, read_mb_s, write_mb_s, recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 'kworker/u16:4', 0, 0, 0, 0, now),
            (652, 652, 'ib_io_wr-3', 0, 102400, 0, 0.167969, now),
            (4790, 4790, 'jbd2/sda2-8', 0, 32768, 0, 0.167969, now),
            (7121, 7121, 'kworker/5:1H', 0, 16384, 0, 0.167969, now),
            (22, 22, 'jbd2/sda4-8', 0, 20480, 0, 0.167969, now)
            # Insert dummy data specific to l3_cache_stats table
        ]
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")