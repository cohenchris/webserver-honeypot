from database_api import connect, TABLE
import pprint
from datetime import datetime


"""
    Analyzes the server logs and updates the blacklist in blacklist.txt
"""
def update_blacklist(log_table):
    start_time = datetime.strptime(log_table[0]["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
    for log in log_table:
        time = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
        difference = str(time - start_time)
        hours = difference.split(":")[0]
        mins = difference.split(":")[1]
        secs = difference.split(":")[2].split(".")[0]

        print(f"{hours}  {mins}  {secs}")
        #pprint.pprint(str(log), width=200)


"""
    Fetches table and puts it in a list of dictionaries

    log_table = [{
                    num :       <entry_num>,
                    timestamp:  <entry_timestamp>,
                    username:   <associated_username>,
                    ip:         <client_ip>,
                    port:       <client_port>,
                    request:    <client_request>
                 }, ...]
"""
def main():
    log_table = []
    try:
        cursor = connect()
        if cursor is None:
            print("UNABLE TO CONNECT TO SQL SERVER")
            return

        cursor.execute("SELECT * from " + TABLE)
        row = cursor.fetchone()
        while row:
            curr_entry = {}
            curr_entry["num"] = str(row[0])
            curr_entry["timestamp"] = str(row[1])
            curr_entry["username"] = str(row[2])
            curr_entry["ip"] = str(row[3])
            curr_entry["port"] = str(row[4])
            curr_entry["request"] = str(row[5])
            log_table.append(curr_entry)
            row = cursor.fetchone()

        update_blacklist(log_table)
    except Exception as e:
        print("ERROR: Unable to fetch table")
        print(f"\t{e}")

if __name__ == "__main__":
    main()