# WEB SERVER HONEYPOT IN PYTHON
---

## INSTALLATION

1. Clone this repository
2. Install dependencies:
  * `pip3 install -r requirements.txt`

## SETUP

1. Re-route ports to your listening port (default is 8080)
  * Re-route incoming port 80 requests (HTTP) to port 8080 (the server's listening port)
    * `sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
  * Re-route incoming port 443 requests (HTTPS) to port 8080 (the server's listening port)
    * `sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
  * **Delete these rules**
    * `sudo iptables -t nat --line-numbers -n -L`

---

## Generate Self-Signed Certificate for Fake Web Server
execute in **honeypot/server_root/vars/keys**
```
openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 21 -nodes -out cert.pem -keyout key.pem; chmod 700 *.pem
```

### Features
- HTTPS Server with SSL certificate verified by **Let's Encrypt**

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
