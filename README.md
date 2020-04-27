# WEB SERVER HONEYPOT IN PYTHON
## CS422 - Networks Final Project

### Requirements
- `pip3 install -r requirements.txt`

- Re-route incoming port 80 requests to port 8080 (the server's listening port)
  - `sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
- Re-route incoming port 443 requests to port 8080 (the server's listening port)
  - `sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
- Delete these rules
  - `sudo iptables -t nat --line-numbers -n -L`

- execute in **honeypot/server_root/vars/keys** for a self-signed certificate (for fake web server):
`openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 21 -nodes -out cert.pem -keyout key.pem`
`chmod 700 *.pem`

### Features
- HTTPS Server
  - Verified by **Let's Encrypt**

- Full-fledged directory browsing
  - Put all files in server_root/htdocs
  - Put all icons in server_root/icons
  - Put all scripts in server_root/cgi-bin

- Supported file extensions
  - *.txt  *.png  *.jpg  *.gif  *.ico  *.svg  *.xml  *.html  *.py  *.mp4

- Support for 14 HTTP response codes
  - 200, 301, 400, 401, 403, 403.6, 404, 405, 413, 414, 500, 501, 504, 505

- Logging
  - Uses remote SQL database for later analysis
  - Able to define trusted IPs in `vars/database_api.py`

- Blacklisting
  - User-defined text file to add custom IPs (`vars/blacklist.txt`)
  - Python script to scan the remote SQL database and blacklist IPs that have requested the same URI 10+ times in 3 seconds
    - `vars/update_blacklist.py` is run automatically
  - HTTP Response Code **403.6** used for telling client that IP has been banned

- Lures attackers
  - Fake SSL server keys and certificates located in the server
  - Fake README.md, python webserver, keys, and server icons files in root directory
    - Makes it look like the web server is inadvertently serving the parent directory of the root