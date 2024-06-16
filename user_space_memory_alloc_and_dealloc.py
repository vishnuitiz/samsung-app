import mysql.connector
from datetime import datetime
try:
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vi@270902",
        database="num"
    )
    db_cursor = db_connection.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    db_connection = None
    db_cursor = None
def insert_dummy_data_user_space_memory_alloc_and_dealloc():
    try:
        insert_query = """
        INSERT INTO l3_cache_stats
        (recorded_at, pid, tid, action, count)
        VALUES (%s, %s, %s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 'rcu_preempt', 3, 25200, 0, 100, now),
            # Insert dummy data specific to l3_cache_stats table
        ]
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")