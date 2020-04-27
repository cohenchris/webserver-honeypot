import sys

import mysql.connector

from constants import COLUMNS, DB_CONFIG, TABLE


"""
    Prints the entire log table
"""
def main():
    table = ""
    try:
        cnxn = mysql.connector.connect(**DB_CONFIG)
        cursor = cnxn.cursor()

        if cursor is None:
            print("504", end='')
            return "504"

        cursor.execute("SELECT * from " + TABLE)

        rows = cursor.fetchall()
        table += ("-"*50 + " SERVER LOGS " + "-"*50 + "\n")
        table += "  " + "#".ljust(3) + "date".ljust(12) + "time".ljust(17) + "hostname".ljust(20) + "ip_addr".ljust(15) + "port".ljust(7) + "protocol".ljust(10) + "request\n"
        table += ("-"*113 + "\n")
        for row in rows:
            table += "  " + str(row[0]).ljust(3)       # entry number
            curr_date = str(row[1]).split()[0]
            curr_time = str(row[1]).split()[1]
            table += curr_date.ljust(12)               # date
            table += curr_time.ljust(17)               # time
            table += str(row[2]).ljust(20)             # hostame
            table += str(row[3]).ljust(15)             # ip
            table += str(row[4]).ljust(7)              # port
            protocol = row[5].split(" ")[-1]
            request = ' '.join(row[5].split(" ")[:-1])
            table += str(protocol).ljust(10)           # protocol
            table += str(request)                      # request

            table += '  \n'
            row = cursor.fetchone()
        table += ("-"*113 + "\n")
        cursor.close()
        cnxn.close()
    except Exception as e:
        table += "ERROR: Unable to print table\n"
        table += f"\t{e}"
    print(table)

if __name__ == "__main__":
    main()
