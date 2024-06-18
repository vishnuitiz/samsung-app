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
def insert_dummy_data_vm_stats():
    try:
        insert_query = """
        INSERT INTO vm_stats
        (pid, tid, rss, pss, process_name, total_memory, used_memory, free_memory, available_memory, recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 1988, 158, 'fusermount3', "15Gi", "2.8Gi", "8.6Gi", "11Gi", now),
            (16, 16, 1760, 235, 'sh', "15Gi", "2.8Gi", "8.6Gi", "11Gi", now),
            (16, 16, 2072, 239, 'acpid', "15Gi", "2.8Gi", "8.6Gi", "11Gi", now),
            (16, 16, 3012, 326, 'cron', "15Gi", "2.8Gi", "8.6Gi", "11Gi", now),
            (16, 16, 1440, 348, 'avahi-daemon', "15Gi", "2.8Gi", "8.6Gi", "11Gi", now),
            # Insert dummy data specific to l3_cache_stats table
        ]
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
