from datetime import datetime

import numpy as np

from constants import BLACKLIST
from database_api import TABLE, connect


def get_ip(candidate):
    return candidate["ip"]

def get_req(candidate):
    return candidate["request"]


"""
    Analyzes the server logs and updates the blacklist in blacklist.txt
"""
def analyze_blacklist(log_table):
    blacklist = []

    for i in range(len(log_table)):
        start_time = datetime.strptime(log_table[i]["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
        candidates = []
        j = i + 1

        # Find candidates in the log table that are within 5 seconds of start_time
        if j < len(log_table):
            time = datetime.strptime(log_table[j]["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
            secs = (time - start_time).total_seconds()
        while secs <= 5 and j < len(log_table):
            candidates.append(log_table[j])
            j = j + 1
            if j < len(log_table):
                time = datetime.strptime(log_table[j]["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
                secs = (time - start_time).total_seconds()

        ##### FIND UNIQUE IPs AND COUNT EACH OCCURRENCE. IF MORE THAN 10 (WITH THE SAME REQUEST), ADD TO BLACKLIST #####

        # If there are less than 10 candidates for this entry, there's no way that it will be blacklisted
        if len(candidates) < 10:
            continue

        # Split the array of candidates into subarrays of entries with like IPs
        sorted_candidates = sorted(candidates, key=get_ip)
        split_arr = []
        for i in range(len(sorted_candidates)):
            subarr = []
            start = sorted_candidates[i]
            while i < len(sorted_candidates) and start["ip"] == sorted_candidates[i]["ip"]:
                subarr.append(sorted_candidates[i])
                i = i + 1
            split_arr.append(subarr)

        # If all of the requests are the same, then the ip corresponding to the entries in the array 'subarr' needs to be blacklisted
        split_arr = [subarr for subarr in split_arr if min(subarr, key=get_req) == max(subarr, key=get_req)]
        [blacklist.append(subarr[0]["ip"]) for subarr in split_arr if subarr[0]["ip"] not in blacklist]

    with open(BLACKLIST, "r") as blist:
        content = blist.readlines()
    content = [line.strip() for line in content]
    
    [blacklist.append(line) for line in content if line not in blacklist]
    with open(BLACKLIST, "w") as blist:
        [blist.write(ip + "\n") for ip in blacklist]



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
def update_blacklist():
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
        analyze_blacklist(log_table)
    except Exception as e:
        print("ERROR: Unable to fetch table")
        print(f"\t{e}")

if __name__ == "__main__":
    update_blacklist()
