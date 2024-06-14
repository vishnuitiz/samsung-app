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

def insert_dummy_data_l3_cache_stats():
    try:
        insert_query = """
        INSERT INTO l3_cache_stats
        (pid, tid, name, cpu, reference, misses, hit_rate, recorded_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        now = datetime.now()
        dummy_data = [
            (16, 16, 'rcu_preempt', 3, 25200, 0, 100, now),
            (1748, 1748,'gnome_shell',7, 935400, 12, 90.5, now),
                (652, 652,'systemd-oomd',2, 417000, 5, 97.5, now),
                (4790, 4790,'grafana_server',1, 21500, 8, 93.0,now),
                (7121, 7121,'ib_dict_stats',0, 3300, 6, 96.8, now),
                (22, 22, 'migration/1',7, 900,1, 94.2, now), 
                (7121, 7121,"ib_io_rd-1",0, 15500 , 0, 100, now), 
                (8572, 8572, "kworker/7:1",7, 71900, 0, 100, now), 
                (8432, 8432 , "kworker/u16:0",7, 20400, 0, 100, now), 
                (7121, 7121, "ib_log_flush",4, 151800, 0, 100, now), 
                (130, 130 , "kworker/7:1H", 7, 1600, 0, 100, now), 
                (70, 70, "kcompactd0",0, 5800, 0, 100, now),
                (7944, 7944, "isolated Web Co" ,3,49400, 0, 100, now), 
                (7121, 7121 , "ib_log_checkpt" ,2,9400, 0, 100, now), 
                (17, 17, "migration/0" ,0,1400, 0, 100, now), 
                (28, 28, "migration/2" ,2,1300, 0, 100, now), 
                (6731, 6731, "threaded-ml" ,3,21800, 0, 100, now), 
                (758, 758, "thermald",1,26400, 0, 100, now),
                (9131, 9131, "kworker/4:2",4,5900, 0, 100, now),
                (1576, 1576, "alsa_sink_ALC32" ,3, 3397400, 0, 100, now), 
                (52, 52, "migration/6" ,6, 1400, 0, 100, now), 
                (40, 40, "migration/4" ,4,900, 0, 100, now), 
                (7944, 7944, "Timer" ,0,33500, 0, 100, now), 
                (1908, 1908, "ibus_daemon" ,3,63800, 0, 100, now),
                (4790, 4790, "grafana_server" ,0,18600, 0, 100, now), 
                (7121, 7121, "ib_io_rd-2" ,2,18800, 0, 100, now), 
                (9929, 9929, "kworker/u16:1" ,7, 26100, 0, 100, now),
                (148,148, "kworker/5:1H" ,5,8000, 0, 100, now), 
                (2060,2060, "gdbus" ,1,13700, 0, 100, now),
                (7437,7437, "IPC I/O parent" ,3,11200, 0, 100, now),
                (7121,7121, "ib_clone_gtid" ,3,34900, 0, 100, now),
                (715, 715,"acnid",2,4600, 0, 100, now)
            # Insert dummy data specific to l3_cache_stats table
        ]
        db_cursor.executemany(insert_query, dummy_data)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")