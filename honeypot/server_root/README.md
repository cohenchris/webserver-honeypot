# WEBSERVER HONEYPOT IN PYTHON
## CS422 - Networks Final Project

### Requirements
- Unix ODBC   `sudo apt-get install unixodbc unixodbc-dev freetds-dev tdsodbc`
- PYODBC      `pip3 install --user pyodbc`

- [Microsoft ODBC Driver 17 for MySQL](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017#ubuntu17)

- execute in **keys/** for a self-signed certificate:
`openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 21 -nodes -out cert.pem -keyout key.pem`
`chmod 700 *.pem`

### Features
- SSL Server

- Full-fledged directory browsing
  - Put all files in htdocs/
  - Put all icons in icons/
  - Put all scripts in cgi-bin/

- Supported file extensions
  - *.txt  *.png  *.jpg  *.gif  *.svg  *.xml  *.html  *.py  *.mp4

- Support for 12 HTTP response codes
  - 200, 400, 401, 403, 404, 405, 413, 414, 500, 501, 504, 505
