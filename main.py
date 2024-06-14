import flet as ft
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import mysql.connector
from datetime import datetime
from l3_cache_stats import insert_dummy_data_l3_cache_stats 
from memory_management_events_tracing import insert_dummy_data_memory_management_events_tracing 
from paging_operations import insert_dummy_data_paging_operations 
from swap_io_overhead import insert_dummy_data_swap_io_overhead 
from user_space_memory_alloc_and_dealloc import insert_dummy_data_user_space_memory_alloc_and_dealloc 
from vm_stats import  insert_dummy_data_vm_stats 
from psi_stats_resource_pressure import insert_dummy_data_psi_stats_resource_pressure 
# Set Matplotlib to use the Agg backend
plt.switch_backend('Agg')

# Establish MySQL connection
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

def create_table_l3_cache_stats():
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS l3_cache_stats (
            pid INT,
            tid INT,
            name VARCHAR(255),
            cpu FLOAT,
            reference INT,
            misses INT,
            hit_rate FLOAT,
            recorded_at DATETIME
        )"""
        db_cursor.execute(create_query)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_table_paging_operations():
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS paging_operations (
            pid INT,
            tid INT,
            name VARCHAR(255),
            page_fauts INT,
            refaults INT,
            swap_ins INT,
            swap_outs INT,
            recorded_at DATETIME
        )"""
        db_cursor.execute(create_query)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_table_swap_io_overhead():
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS swap_io_overhead (
            pid INT,
            tid INT,
            command VARCHAR(255), 
            read_bytes INT, 
            write_bytes INT,
            read_mb_s INT, 
            write_mb_s FLOAT, 
            recorded_at DATETIME
        )"""
        db_cursor.execute(create_query)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_table_user_space_memory_alloc_and_dealloc():
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS user_space_memory_alloc_and_dealloc (
            recorded_at DATETIME,
            pid INT,
            tid INT,
            action VARCHAR(255),
            count INT
        )"""
        db_cursor.execute(create_query)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_table_vm_stats():
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS vm_stats (
            pid INT,
            tid INT,
            rss INT, 
            pss INT,
            process_name VARCHAR(255),
            total_memory VARCHAR(255), 
            used_memory VARCHAR(255), 
            free_memory VARCHAR(255), 
            available_memory VARCHAR(255),
            recorded_at DATETIME
        )"""
        db_cursor.execute(create_query)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_table_memory_management_events_tracing():
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS memory_management_events_tracing (
            pid INT,
            tid INT,
            field VARCHAR(255),
            type VARCHAR(255),
            null VARCHAR(255),
            key VARCHAR(255),
            default VARCHAR(255), 
            extra VARCHAR(255),
            recorded_at DATETIME
        )"""
        db_cursor.execute(create_query)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def create_table_psi_stats_resource_pressure():
    try:
        create_query = """
        CREATE TABLE IF NOT EXISTS psi_stats_resource_pressure (
            pid INT,
            tid INT,
            stat_type VARCHAR(255), 
            full_avg VARCHAR(255), 
            some_avg VARCHAR(255), 
            recorded_at DATETIME, 
            avg10 FLOAT, 
            avg60 FLOAT, 
            avg300 FLOAT, 
            total INT
        )"""
        db_cursor.execute(create_query)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
# Define create_table functions for other tables similarly

# Define insert_dummy_data functions for other tables similarly
def fetch_column_data(table, column):
    try:
        if table:
            db_cursor.execute(f"SELECT {column} FROM {table}")
            return db_cursor.fetchall()
        return []
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    

def generate_line_graph(data, column):
    fig, ax = plt.subplots()
    ax.plot(range(len(data)), [d[0] for d in data], marker='o')
    ax.set_xlabel('Index')
    ax.set_ylabel(column)
    ax.set_title(f'{column} Data')

    # Save plot to a bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode plot to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return image_base64
    # Function remains the same

def create_dedicated_page_l3_cache_stats(label, table):
    def dedicated_page(page):
        def on_time_stamp_click(e):
            # Adjust this function to fetch data from the paging_operations table
            tid_data = fetch_column_data(table, "recorded_at")
            print("Timestamp data fetched:", tid_data)
            image_base64 = generate_line_graph(tid_data, "recorded_at")
            display_data(image_base64, tid_data, "TID Data")

        def on_pid_click(e):
            # Adjust this function to fetch data from the paging_operations table
            pid_data = fetch_column_data(table, "pid")
            print("PID data fetched:", pid_data)
            image_base64 = generate_line_graph(pid_data, "pid")
            display_data(image_base64, pid_data, "PID Data")

        def display_data(image_base64, table_data, title):
            page.controls.clear()
            image = ft.Image(src_base64=image_base64, width=600, height=400)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Index")),
                    ft.DataColumn(ft.Text(title)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(str(value[0])))])
                    for idx, value in enumerate(table_data)
                ],
            )

            page.add(
                ft.Column([
                    ft.Text(value=label, size=30),
                    image,
                    table,
                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/"), width=200, height=50)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        generate_button = ft.ElevatedButton(text="Generate Stats", on_click=lambda e: insert_dummy_data_l3_cache_stats(table),
                                            width=200, height=50)
        time_stamp_button = ft.ElevatedButton(text="Time Stamp", on_click=on_time_stamp_click, width=200, height=50)
        pid_button = ft.ElevatedButton(text="PID", on_click=on_pid_click, width=200, height=50)

        page.add(
            ft.Column([
                ft.Text(value=label, size=30),
                ft.Container(content=generate_button, alignment=ft.alignment.center),
                ft.Container(content=time_stamp_button, alignment=ft.alignment.center),
                ft.Container(content=pid_button, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return dedicated_page

def create_dedicated_page_paging_operations(label, table):
    def dedicated_page(page):
        def on_time_stamp_click(e):
            # Adjust this function to fetch data from the paging_operations table
            tid_data = fetch_column_data(table, "recorded_at")
            print("Timestamp data fetched:", tid_data)
            image_base64 = generate_line_graph(tid_data, "recorded_at")
            display_data(image_base64, tid_data, "TID Data")

        def on_pid_click(e):
            # Adjust this function to fetch data from the paging_operations table
            pid_data = fetch_column_data(table, "pid")
            print("PID data fetched:", pid_data)
            image_base64 = generate_line_graph(pid_data, "pid")
            display_data(image_base64, pid_data, "PID Data")

        def display_data(image_base64, table_data, title):
            page.controls.clear()
            image = ft.Image(src_base64=image_base64, width=600, height=400)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Index")),
                    ft.DataColumn(ft.Text(title)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(str(value[0])))])
                    for idx, value in enumerate(table_data)
                ],
            )

            page.add(
                ft.Column([
                    ft.Text(value=label, size=30),
                    image,
                    table,
                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/"), width=200, height=50)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        generate_button = ft.ElevatedButton(text="Generate Stats", on_click=lambda e: insert_dummy_data_paging_operations(table),
                                            width=200, height=50)
        time_stamp_button = ft.ElevatedButton(text="Time Stamp", on_click=on_time_stamp_click, width=200, height=50)
        pid_button = ft.ElevatedButton(text="PID", on_click=on_pid_click, width=200, height=50)

        page.add(
            ft.Column([
                ft.Text(value=label, size=30),
                ft.Container(content=generate_button, alignment=ft.alignment.center),
                ft.Container(content=time_stamp_button, alignment=ft.alignment.center),
                ft.Container(content=pid_button, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return dedicated_page

def create_dedicated_page_swap_io_overhead(label, table):
    def dedicated_page(page):
        def on_time_stamp_click(e):
            # Adjust this function to fetch data from the paging_operations table
            tid_data = fetch_column_data(table, "recorded_at")
            print("Timestamp data fetched:", tid_data)
            image_base64 = generate_line_graph(tid_data, "recorded_at")
            display_data(image_base64, tid_data, "TID Data")

        def on_pid_click(e):
            # Adjust this function to fetch data from the paging_operations table
            pid_data = fetch_column_data(table, "pid")
            print("PID data fetched:", pid_data)
            image_base64 = generate_line_graph(pid_data, "pid")
            display_data(image_base64, pid_data, "PID Data")

        def display_data(image_base64, table_data, title):
            page.controls.clear()
            image = ft.Image(src_base64=image_base64, width=600, height=400)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Index")),
                    ft.DataColumn(ft.Text(title)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(str(value[0])))])
                    for idx, value in enumerate(table_data)
                ],
            )

            page.add(
                ft.Column([
                    ft.Text(value=label, size=30),
                    image,
                    table,
                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/"), width=200, height=50)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        generate_button = ft.ElevatedButton(text="Generate Stats", on_click=lambda e: insert_dummy_data_swap_io_overhead(table),
                                            width=200, height=50)
        time_stamp_button = ft.ElevatedButton(text="Time Stamp", on_click=on_time_stamp_click, width=200, height=50)
        pid_button = ft.ElevatedButton(text="PID", on_click=on_pid_click, width=200, height=50)

        page.add(
            ft.Column([
                ft.Text(value=label, size=30),
                ft.Container(content=generate_button, alignment=ft.alignment.center),
                ft.Container(content=time_stamp_button, alignment=ft.alignment.center),
                ft.Container(content=pid_button, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return dedicated_page

def create_dedicated_page_user_space_memory_alloc_and_dealloc(label, table):
    def dedicated_page(page):
        def on_time_stamp_click(e):
            # Adjust this function to fetch data from the paging_operations table
            tid_data = fetch_column_data(table, "recorded_at")
            print("Timestamp data fetched:", tid_data)
            image_base64 = generate_line_graph(tid_data, "recorded_at")
            display_data(image_base64, tid_data, "TID Data")

        def on_pid_click(e):
            # Adjust this function to fetch data from the paging_operations table
            pid_data = fetch_column_data(table, "pid")
            print("PID data fetched:", pid_data)
            image_base64 = generate_line_graph(pid_data, "pid")
            display_data(image_base64, pid_data, "PID Data")

        def display_data(image_base64, table_data, title):
            page.controls.clear()
            image = ft.Image(src_base64=image_base64, width=600, height=400)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Index")),
                    ft.DataColumn(ft.Text(title)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(str(value[0])))])
                    for idx, value in enumerate(table_data)
                ],
            )

            page.add(
                ft.Column([
                    ft.Text(value=label, size=30),
                    image,
                    table,
                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/"), width=200, height=50)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        generate_button = ft.ElevatedButton(text="Generate Stats", on_click=lambda e: insert_dummy_data_user_space_memory_alloc_and_dealloc(table),
                                            width=200, height=50)
        time_stamp_button = ft.ElevatedButton(text="Time Stamp", on_click=on_time_stamp_click, width=200, height=50)
        pid_button = ft.ElevatedButton(text="PID", on_click=on_pid_click, width=200, height=50)

        page.add(
            ft.Column([
                ft.Text(value=label, size=30),
                ft.Container(content=generate_button, alignment=ft.alignment.center),
                ft.Container(content=time_stamp_button, alignment=ft.alignment.center),
                ft.Container(content=pid_button, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return dedicated_page

def create_dedicated_page_vm_stats(label, table):
    def dedicated_page(page):
        def on_time_stamp_click(e):
            # Adjust this function to fetch data from the paging_operations table
            tid_data = fetch_column_data(table, "recorded_at")
            print("Timestamp data fetched:", tid_data)
            image_base64 = generate_line_graph(tid_data, "recorded_at")
            display_data(image_base64, tid_data, "TID Data")

        def on_pid_click(e):
            # Adjust this function to fetch data from the paging_operations table
            pid_data = fetch_column_data(table, "pid")
            print("PID data fetched:", pid_data)
            image_base64 = generate_line_graph(pid_data, "pid")
            display_data(image_base64, pid_data, "PID Data")

        def display_data(image_base64, table_data, title):
            page.controls.clear()
            image = ft.Image(src_base64=image_base64, width=600, height=400)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Index")),
                    ft.DataColumn(ft.Text(title)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(str(value[0])))])
                    for idx, value in enumerate(table_data)
                ],
            )

            page.add(
                ft.Column([
                    ft.Text(value=label, size=30),
                    image,
                    table,
                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/"), width=200, height=50)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        generate_button = ft.ElevatedButton(text="Generate Stats", on_click=lambda e: insert_dummy_data_vm_stats(table),
                                            width=200, height=50)
        time_stamp_button = ft.ElevatedButton(text="Time Stamp", on_click=on_time_stamp_click, width=200, height=50)
        pid_button = ft.ElevatedButton(text="PID", on_click=on_pid_click, width=200, height=50)

        page.add(
            ft.Column([
                ft.Text(value=label, size=30),
                ft.Container(content=generate_button, alignment=ft.alignment.center),
                ft.Container(content=time_stamp_button, alignment=ft.alignment.center),
                ft.Container(content=pid_button, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return dedicated_page

def create_dedicated_page_memory_management_events_tracing(label, table):
    def dedicated_page(page):
        def on_time_stamp_click(e):
            # Adjust this function to fetch data from the paging_operations table
            tid_data = fetch_column_data(table, "recorded_at")
            print("Timestamp data fetched:", tid_data)
            image_base64 = generate_line_graph(tid_data, "recorded_at")
            display_data(image_base64, tid_data, "TID Data")

        def on_pid_click(e):
            # Adjust this function to fetch data from the paging_operations table
            pid_data = fetch_column_data(table, "pid")
            print("PID data fetched:", pid_data)
            image_base64 = generate_line_graph(pid_data, "pid")
            display_data(image_base64, pid_data, "PID Data")

        def display_data(image_base64, table_data, title):
            page.controls.clear()
            image = ft.Image(src_base64=image_base64, width=600, height=400)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Index")),
                    ft.DataColumn(ft.Text(title)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(str(value[0])))])
                    for idx, value in enumerate(table_data)
                ],
            )

            page.add(
                ft.Column([
                    ft.Text(value=label, size=30),
                    image,
                    table,
                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/"), width=200, height=50)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        generate_button = ft.ElevatedButton(text="Generate Stats", on_click=lambda e: insert_dummy_data_memory_management_events_tracing(table),
                                            width=200, height=50)
        time_stamp_button = ft.ElevatedButton(text="Time Stamp", on_click=on_time_stamp_click, width=200, height=50)
        pid_button = ft.ElevatedButton(text="PID", on_click=on_pid_click, width=200, height=50)

        page.add(
            ft.Column([
                ft.Text(value=label, size=30),
                ft.Container(content=generate_button, alignment=ft.alignment.center),
                ft.Container(content=time_stamp_button, alignment=ft.alignment.center),
                ft.Container(content=pid_button, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return dedicated_page

def create_dedicated_page_psi_stats_resource_pressure(label, table):
    def dedicated_page(page):
        def on_time_stamp_click(e):
            # Adjust this function to fetch data from the paging_operations table
            tid_data = fetch_column_data(table, "recorded_at")
            print("Timestamp data fetched:", tid_data)
            image_base64 = generate_line_graph(tid_data, "recorded_at")
            display_data(image_base64, tid_data, "TID Data")

        def on_pid_click(e):
            # Adjust this function to fetch data from the paging_operations table
            pid_data = fetch_column_data(table, "pid")
            print("PID data fetched:", pid_data)
            image_base64 = generate_line_graph(pid_data, "pid")
            display_data(image_base64, pid_data, "PID Data")

        def display_data(image_base64, table_data, title):
            page.controls.clear()
            image = ft.Image(src_base64=image_base64, width=600, height=400)
            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Index")),
                    ft.DataColumn(ft.Text(title)),
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(idx))), ft.DataCell(ft.Text(str(value[0])))])
                    for idx, value in enumerate(table_data)
                ],
            )

            page.add(
                ft.Column([
                    ft.Text(value=label, size=30),
                    image,
                    table,
                    ft.ElevatedButton(text="Back", on_click=lambda e: page.go("/"), width=200, height=50)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            page.update()

        generate_button = ft.ElevatedButton(text="Generate Stats", on_click=lambda e: insert_dummy_data_psi_stats_resource_pressure(table),
                                            width=200, height=50)
        time_stamp_button = ft.ElevatedButton(text="Time Stamp", on_click=on_time_stamp_click, width=200, height=50)
        pid_button = ft.ElevatedButton(text="PID", on_click=on_pid_click, width=200, height=50)

        page.add(
            ft.Column([
                ft.Text(value=label, size=30),
                ft.Container(content=generate_button, alignment=ft.alignment.center),
                ft.Container(content=time_stamp_button, alignment=ft.alignment.center),
                ft.Container(content=pid_button, alignment=ft.alignment.center)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    return dedicated_page

# Define similar create_dedicated_page functions for other tables
# Define similar create_dedicated_page functions for other tables
# Define similar create_dedicated_page functions for other tables
# Define similar create_dedicated_page functions for other tables
# Define similar create_dedicated_page functions for other tables
# Define similar create_dedicated_page functions for other tables
# Define similar create_dedicated_page functions for other tables



# Define create_dedicated_page functions for other tables similarly

def main_page(page):
    def on_button_click_l3_cache_stats(e):
        create_table_l3_cache_stats()
        insert_dummy_data_l3_cache_stats()
        create_dedicated_page_l3_cache_stats("L3 Cache Stats", "l3_cache_stats")(page)
    def on_button_click_paging_operations(e):
        create_table_paging_operations()
        insert_dummy_data_paging_operations()
        create_dedicated_page_paging_operations("PagingOperation", "paging_operations")(page)
    def on_button_click_swap_io_overhead(e):
        create_table_swap_io_overhead()
        insert_dummy_data_swap_io_overhead()
        create_dedicated_page_swap_io_overhead("swap io overhead", "swap_io_overhead")(page)
    def on_button_click_user_space_memory_alloc_and_dealloc(e):
        create_table_user_space_memory_alloc_and_dealloc()
        insert_dummy_data_user_space_memory_alloc_and_dealloc()
        create_dedicated_page_user_space_memory_alloc_and_dealloc("user space memory alloc and dealloc", "user_space_memory_alloc_and_dealloc")(page)
    def on_button_click_vm_stats(e):
        create_table_vm_stats()
        insert_dummy_data_vm_stats()
        create_dedicated_page_vm_stats("vm stats", "vm_stats")(page)
    def on_button_click_memory_management_events_tracing(e):
        create_table_memory_management_events_tracing()
        insert_dummy_data_memory_management_events_tracing()
        create_dedicated_page_memory_management_events_tracing("memory management events tracing", "memory_management_events_tracing")(page)
    def on_button_click_psi_stats_resource_pressure(e):
        create_table_psi_stats_resource_pressure()
        insert_dummy_data_psi_stats_resource_pressure()
        create_dedicated_page_psi_stats_resource_pressure("psi stats resource pressure", "psi_stats_resource_pressure")(page)                    
    # Define on_button_click functions for other tables similarly

    button_labels = [
        "L3 Cache Stats",
        "Paging Operations",
        "swap_io_overhead",
        "user_space_memory_alloc_and_dealloc",
        "vm_stats",
        "memory_management_events_tracing",
        "psi_stats_resource_pressure"
        # Add other button labels here
    ]

    button_actions = [
        on_button_click_l3_cache_stats,
        on_button_click_paging_operations,
        on_button_click_swap_io_overhead,
        on_button_click_user_space_memory_alloc_and_dealloc,
        on_button_click_vm_stats,
        on_button_click_memory_management_events_tracing,
        on_button_click_psi_stats_resource_pressure,
        # Add other button actions here
    ]

    buttons = [ft.ElevatedButton(text=label, on_click=action, width=200, height=50) for label, action in zip(button_labels, button_actions)]

    page.add(ft.Column(buttons, alignment=ft.MainAxisAlignment.START))

def main(page: ft.Page):
    def on_route_change(e):
        page.controls.clear()
        if page.route == "/":
            main_page(page)
        else:
            label = page.route.replace('_', ' ').strip('/')
            table = label.replace(' ', '_').lower()
            create_dedicated_page_l3_cache_stats(label, table)(page)
            create_dedicated_page_paging_operations(label, table)(page)
            create_dedicated_page_swap_io_overhead(label, table)(page)
            create_dedicated_page_user_space_memory_alloc_and_dealloc(label, table)(page)
            create_dedicated_page_memory_management_events_tracing(label, table)(page)
            create_dedicated_page_vm_stats(label, table)(page)
            create_dedicated_page_psi_stats_resource_pressure(label, table)(page)
        page.update()

    page.on_route_change = on_route_change
    page.go("/")

ft.app(target=main)
