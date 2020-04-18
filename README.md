# HONEYPOT IN PYTHON
## CS422 - Networks Final Project
=================================

#### Requirements
- PYODBC
  - `pip3 install --user pyodbc`

- [Microsoft ODBC Driver 17 for MySQL](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017#ubuntu17)

- server.pem in the `honeypot/` directory
  - `openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes`
