def insert_dummy_data_psi_stats_resource_pressure():
    try:
        insert_query = """
        INSERT INTO l3_cache_stats
        (pid, tid, stat_type, full_avg, some_avg, recorded_at, avg10, avg60, avg300, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 'rcu_preempt', 3, 25200, 0, 100, now),
            # Insert dummy data specific to l3_cache_stats table
        ]
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")