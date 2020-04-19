#!/usr/bin/python3
# CGI-BIN for webserver
import cgitb
cgitb.enable()

import pyodbc
import sys

TABLE = "logfile"
COLUMNS = "(username, ip, port, request)"


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
        return None

    return cnxn.cursor()


"""
    Prints the entire log table
"""
def main():
    table = ""
    try:
        cursor = connect()
        if cursor is None:
            return "UNABLE TO CONNECT TO SQL SERVER"

        cursor.execute("SELECT * from " + TABLE)
        row = cursor.fetchone()
        table += ("------------------------------------------ SERVER LOGS ------------------------------------------\n")
        table += ("| #\tdate\t\ttime\t\thostname\tip_addr\t\tport\treq\t\t|\n")
        table += ("-------------------------------------------------------------------------------------------------\n")
        while row:
            table += '  '
            for val in range(len(row) - 1):
                if val == 1:
                    curr_date = str(row[val]).split()[0]
                    curr_time = str(row[val]).split()[1]
                    table += f"{curr_date}\t{curr_time}\t"
                else:
                    table += str(row[val]) + '\t'
            table += row[-1]
            table += '  \n'
            row = cursor.fetchone()
        table += ("-------------------------------------------------------------------------------------------------\n")
    except Exception as e:
        table += "ERROR: Unable to print table\n"
        table += f"\t{e}"
    
    print(table)

if __name__ == "__main__":
    main()