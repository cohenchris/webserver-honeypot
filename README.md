# **HTTPS WEB SERVER HONEYPOT**
---
# Installation and Setup

1. Clone this repository
2. Install dependencies: `pip3 install -r requirements.txt`
### Ports
3. Port Forward ports 80 and 443 on your local router
4. Re-route HTTP and HTTPS requests to the server's listening port (default is 8080)
    * Re-route incoming port 80 requests (HTTP) to port 8080 (the server's listening port)
      * `sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
    * Re-route incoming port 443 requests (HTTPS) to port 8080 (the server's listening port)
      * `sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080`
    * **DELETE RULES**
      * `sudo iptables -t nat --line-numbers -n -L`
### Personal Credentials
5. Enter personal database and website details in `vars/constants.py`
    * USERNAME to local MySQL Server
    * PASSWORD to local MySQL Server
    * DATABSE name in local MySQL Server
    * WEBSITE URL to serve
### Fake Web Server
6. Copy over your website SSL keys, SSL certificate, and authentication file
    * Put full-chain certificate in `vars/security/fullchain.pem`
    * Put private key in `vars/security/privkey.pem`
    * Put base64 encoded authentication string in the form of **user:password** in `vars/security/auth.txt`
7. Generate Self-Signed Certificate for Fake Web Server
    * execute in **honeypot/server_root/vars/keys**
    * `openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 21 -nodes -out cert.pem -keyout key.pem; chmod 700 *.pem;`

# Features

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
  - Uses MySQL database for later analysis
  - Able to define trusted IPs in `vars/database_api.py`

- Blacklisting
  - User-editable text file to add custom IPs to ban (`vars/blacklist.txt`)
  - Python script scans the MySQL database and blacklist IPs that have requested the same URI 10+ times in 3 seconds
    - `vars/update_blacklist.py` runs and will ban IPs automatically
  - HTTP Response Code **403.6** used for telling client that IP has been banned

- Lures attackers
  - Fake SSL server keys and certificates located in the server root directory
    - Looks like a vulnerability to attackers
  - Fake Python webserver and README.md located in the server root directory
    - Makes it look like the web server is inadvertently serving the parent directory of the root
