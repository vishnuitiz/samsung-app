def insert_dummy_data_paging_operations():
    try:
        insert_query = """
        INSERT INTO paging_operations
        (pid, tid,page_fauts,refaults,swap_ins,swap_outs, recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 'rcu_preempt', 3, 25200, 0, 100, now),
            # Insert dummy data specific to l3_cache_stats table
        ]
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")