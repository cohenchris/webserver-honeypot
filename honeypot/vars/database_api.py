import sys

import mysql.connector

try:
    from .constants import COLUMNS, DB_CONFIG, IGNORED_REQUESTS, KNOWN_USERS, TABLE
except:
    from constants import COLUMNS, DB_CONFIG, IGNORED_REQUESTS, KNOWN_USERS, TABLE


"""
    Adds entry to the SQL table
"""
def log(ip, port, request):
    # Ignore any requests that are in IGNORED_REQUESTS
    for req in IGNORED_REQUESTS:
        if req in request:
            return

    cnxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnxn.cursor()

    username = KNOWN_USERS[ip] if ip in KNOWN_USERS else None
    vals = f"('{username}', '{ip}', {port}, '{request}')" if username is not None else f"(NULL, '{ip}', {port}, '{request}')"
    query = (f"""
            INSERT INTO {TABLE} {COLUMNS}
            VALUES {vals};
            """)
    try:
        cursor.execute(query, vals)
        cnxn.commit()
        cursor.close()
        cnxn.close()
    except Exception as e:
        print(f"ERROR: Failed to add entry ({ip}, {port}, {request})")
        print("\t", e)


"""
    Creates a new SQL table with name TABLE on the database
"""
def create_table():
    cnxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnxn.cursor()

    try:
        cursor.execute(f"""
        CREATE TABLE {TABLE} (
            num         int AUTO_INCREMENT PRIMARY KEY,
            timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            username    varchar(30),
            ip          varchar(15) NOT NULL,
            port        int NOT NULL,
            request     varchar(128) NOT NULL
        );
        """
        )
        cursor.close()
        cnxn.close()
    except Exception as e:
        print("ERROR: Unable to create table.")
        print("\t", e)

"""
    Deletes the SQL table with name TABLE on the database
"""
def delete_table():
    cnxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnxn.cursor()

    try:
        cursor.execute(f"DROP TABLE {TABLE}")
        cursor.close()
        cnxn.close()
    except Exception as e:
        print("ERROR: Unable to delete table.")
        print("\t", e)


if __name__ == "__main__":
    if sys.argv[1] == "create":
        create_table()
    elif sys.argv[1] == "delete":
        delete_table()
    else:
        print("""Usage: python3 database_api <option>
        OPTIONS:
        create  -  creates a new log table in the database
        delete  -  deletes the log table in the database
        """)
