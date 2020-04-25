import sys
import pyodbc

TABLE = "logfile"
COLUMNS = "(username, ip, port, request)"


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
    except Exception:
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
            print("504", end='')
            return "504"

        cursor.execute("SELECT * from " + TABLE)
        row = cursor.fetchone()
        table += ("-"*50 + " SERVER LOGS " + "-"*50 + "\n")
        table += "  "
        table += "#".ljust(3)
        table += "date".ljust(12)
        table += "time".ljust(17)
        table += "hostname".ljust(20)
        table += "ip_addr".ljust(15)
        table += "port".ljust(7)
        table += "request\n"
        table += ("-"*113 + "\n")
        while row:
            table += '  '
            table += str(row[0]).ljust(3)              # entry number
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

if __name__ == "__main__":
    main()
