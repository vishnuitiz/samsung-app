from asyncio.windows_events import NULL
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
def insert_dummy_data_memory_management_events_tracing():
    try:
        insert_query = """
        INSERT INTO memory_management_events_tracing
        (pid,tid,event_type,proces_name,total_memory_gb,available_memory_gb, used_memory_gb ,memory_percent_used ,total_swap_gb , total_swap_gb_1 ,swap__percent_used,recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 'Memory/Swap Usage',NULL,15.3964, 11.5906, 2.90557,24.7,46.2559,0,0,now),
            (652, 652, 'Memory/Swap Usage',NULL,15.3964, 11.5914, 2.90479,24.7,46.2559,0,0,now),
            (4790, 4790, 'Memory/Swap Usage',NULL,15.3964, 10.6707, 3.6364,30.7,46.2559,0,0,now),
            (7121, 7121, 'Memory/Swap Usage',NULL,15.3964, 10.6781, 3.59831,30.6,46.2559,0,0,now),
            (22, 22, 'Memory/Swap Usage',NULL,15.3964, 10.9382, 3.4544,29,46.2559,0,0,now),
            # Insert dummy data specific to l3_cache_stats table
        ]
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")