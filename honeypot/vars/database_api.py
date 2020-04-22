import sys

import pyodbc

TABLE = "logfile"
COLUMNS = "(username, ip, port, request)"

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
    driver = "{ODBC Driver 17 for SQL Server}"
    server = "tcp:cohenwebserver-logs.database.windows.net,1433"
    db = "webserver-logs"
    uid = "cohenchris"
    pw = "ChRiS245"
    extras = "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=10;"
    # AWS
    #connectString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=cohen-webserver.cdvgeueymc21.us-east-2.rds.amazonaws.com,3306;DATABASE=cohen_webserver_logs;UID=admin;PWD=honeypot69;'
    # AZURE
    connectString = f'Driver={driver};Server={server};Database={db};Uid={uid};Pwd={pw};{extras}'
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
def log(ip, port, request):
    cursor = connect()

    username = get_username(ip)
    vals = f"('{username}', '{ip}', {port}, '{request}')" if username is not None else f"(NULL, '{ip}', {port}, '{request}')"
    query = f"""
            INSERT INTO {TABLE} {COLUMNS}
            VALUES {vals};
            """
    try:
        cursor.execute(query)
        cursor.commit()
    except Exception as e:
        print(f"ERROR: Failed to add entry ({ip}, {port}, {request})")
        print("\t", e)

"""
    Prints the entire log table
"""
def print_table():
    table = ""
    try:
        cursor = connect()
        if cursor is None:
            print("UNABLE TO CONNECT TO SQL SERVER")
            return "UNABLE TO CONNECT TO SQL SERVER"

        cursor.execute("SELECT * from " + TABLE)
        row = cursor.fetchone()
        table += ("-"*50 + " SERVER LOGS " + "-"*50 + "\n")
        table += "  " + "#".ljust(3) + "date".ljust(12) + "time".ljust(17) + "hostname".ljust(20) + "ip_addr".ljust(15) + "port".ljust(7) + "request\n"
        table += ("-"*113 + "\n")
        while row:
            table += "  " + str(row[0]).ljust(3)       # entry number
            curr_date = str(row[1]).split()[0]
            curr_time = str(row[1]).split()[1]
            table += curr_date.ljust(12)               # date
            table += curr_time.ljust(17)               # time
            table += str(row[2]).ljust(20)             # hostame
            table += str(row[3]).ljust(15)             # ip
            table += str(row[4]).ljust(7)              # port
            table += str(row[5])                       # request

            table += '  \n'
            row = cursor.fetchone()
        table += ("-"*113 + "\n")
    except Exception as e:
        table += "ERROR: Unable to print table\n"
        table += f"\t{e}"
    print(table)


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
            timestamp   DATETIME NOT NULL DEFAULT(GETDATE()),
            username    varchar(30),
            ip          varchar(15) NOT NULL,
            port        int NOT NULL,
            request     varchar(128) NOT NULL,
        );
        """
        )
        cursor.commit()
    except Exception as e:
        print("ERROR: Unable to create table.")
        print("\t", e)

if __name__ == "__main__":
    print_table()
