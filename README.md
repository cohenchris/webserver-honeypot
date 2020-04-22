# WEBSERVER HONEYPOT IN PYTHON
## CS422 - Networks Final Project

### Requirements
- PYODBC      `pip3 install --user pyodbc`

- [Microsoft ODBC Driver 17 for MySQL](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017#ubuntu17)

- execute in **honeypot/vars/** for a self-signed certificate:
`openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 21 -nodes -out cert.pem -keyout key.pem`
`chmod 700 *.pem`

### Features
- SSL Server

- Full-fledged directory browsing

- Support for 12 HTTP response codes
  - 200, 400, 401, 403, 404, 405, 413, 414, 500, 501, 504, 505

- Logging
  - Uses remote SQL database for later analysis
  - Able to define trusted IPs in `vars/constants.py`

- Blacklisting
  - User-defined text file to add custom IPs (`vars/blacklist.txt`)
  - Python script to scan the remote SQL database and blacklist IPs that have requested the same URI 10+ times in 5 seconds
    - `vars/update_blacklist.py` Runs on server startup (or manually)

- Lures attackers
  - Fake SSL server keys and RSA private keys located in the server
  - 