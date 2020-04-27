# **HTTPS WEB SERVER HONEYPOT**
---
# Installation and Setup

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
    * WEBSITE URL to serve
6. Copy over your website SSL keys, SSL certificate, and authentication file
    * Put full-chain certificate in `vars/keys/cert.pem`
    * Put private key in `vars/keys/key.pem`
    * Put authentication string in the form of **user:password** in `vars/keys/auth.txt`
        * Encode this in base64

# Features

- HTTPS Server with SSL certificate verified by [**Let's Encrypt**](https://letsencrypt.org/)

- Full-fledged directory browsing
  - Put all files in `htdocs/`
  - Put all icons in `icons/`
  - Put all scripts in `cgi-bin/`

- Supported file extensions
  - *.txt  *.png  *.jpg  *.gif  *.ico  *.svg  *.xml  *.html  *.py  *.mp4

- Support for 13 HTTP response codes
  - 200, 301, 400, 401, 403, 404, 405, 413, 414, 500, 501, 504, 505