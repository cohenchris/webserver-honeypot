#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import pyodbc
import sys

TABLE = "logfile"
COLUMNS = "(username, ip, port, request, filename)"

KNOWN_USERS = {
    "127.0.0.1"     :   "localhost",
    "73.103.85.242" :   "Chris Cohen"
}

def get_username(ip):
    return KNOWN_USERS[ip] if ip in KNOWN_USERS else None

"""
    Connect to SQL server hosted by Azure
    Returns cursor
"""
def connect():
    # Set up server connection
    connectString = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:cohenwebserver-logs.database.windows.net,1433;Database=webserver-logs;Uid=cohenchris;Pwd=ChRiS245;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    try:
        cnxn = pyodbc.connect(connectString)
    except Exception as e:
        print("ERROR: Unable to connect to SQL Server.")
        print("\t", e)
        sys.exit()

    return cnxn.cursor()

"""
    Adds entry to the SQL table
"""
def log(ip, port, request, filename):
    cursor = connect()
    username = get_username(ip)
    vals = f"('{username}', '{ip}', {port}, '{request}', '{filename}')" if username is not None else f"(NULL, '{ip}', {port}, '{request}', '{filename}')"
    query = f"""
            INSERT INTO {TABLE} {COLUMNS}
            VALUES {vals};
            """
    try:
        print(query)
        cursor.execute(query)
        cursor.commit()
    except Exception as e:
        print(f"ERROR: Failed to add entry ({ip}, {port}, {request}, {filename})")
        print("\t", e)

"""
    Prints the entire table that's passed in
"""
def print_table():
    try:
        cursor = connect()
        cursor.execute("SELECT * from " + TABLE)
        row = cursor.fetchone()
        print("------------------------ ENTIRE TABLE ------------------------")
        print("| #\t   hostname\t   ip_addr\t port\t  req\tfile |")
        print("--------------------------------------------------------------")
        while row:
            print('| ' + '\t'.join(str(row).split(',')).strip('()') + ' |')
            row = cursor.fetchone()
        print("--------------------------------------------------------------")
    except Exception as e:
        print("ERROR: Unable to print table")
        print("\t", e)

"""
    Creates a new SQL table with name TABLE on the database
"""
def create_log_table():
    cursor = connect()

    try:
        cursor.execute(f"""
        CREATE TABLE {TABLE}
        (
            num         int NOT NULL IDENTITY(1, 1),
            username    varchar(30),
            ip          varchar(15) NOT NULL,
            port        int NOT NULL,
            request     varchar(10) NOT NULL,
            filename    varchar(30) NOT NULL
        );
        """
        )
        cursor.commit()
    except Exception as e:
        print("ERROR: Unable to create table.")
        print("\t", e)

if __name__ == "__main__":
    print_table()
