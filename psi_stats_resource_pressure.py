from asyncio.windows_events import NULL
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
def insert_dummy_data_psi_stats_resource_pressure():
    try:
        insert_query = """
        INSERT INTO psi_stats_resource_pressure
        (pid, tid, stat_type, full_avg, some_avg, recorded_at, avg10, avg60, avg300, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 'cpu ',NULL, NULL ,now, 0.00, 0.00, 0.00, 0), (1748, 1748, 'memory', NULL, NULL ,now, 0.00, 0.00, 0.00, 11958),
                (652, 652, 'cpu', NULL, NULL ,now, 0.00, 0.00, 0.00, 0),
                (4790, 4790, 'memory', NULL, NULL ,now, 0.00, 0.00, 0.00, 15100),
                (7121, 7121, 'cpu', NULL, NULL ,now, 0.00, 0.00, 0.00, 0),
                (22, 22, 'memory', NULL, NULL ,now,0.00, 0.00, 0.00, 15100), (7121, 7121, 'cpu' , NULL, NULL , now , 0.00, 0.00, 0.00, 0), (8572, 8572, 'memory' , NULL, NULL ,now, 0.00, 0.00, 0.00, 15100), (8432, 8432 , 'cpu' , NULL, NULL ,now, 0.00, 0.00, 0.00, 0), (7121, 7121, 'memory' , NULL, NULL ,now, 0.00, 0.00, 0.00, 16240), (130, 130 , 'cpu' , NULL, NULL ,now, 0.00, 0.00, 0.00, 0), (70, 70, 'memory' , NULL, NULL,now, 0.00, 0.00, 0.00, 0)
]
        
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")