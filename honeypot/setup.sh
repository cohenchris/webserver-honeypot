#!/bin/bash

echo "--------- INSTALLING DEPENDENCIES ---------"
echo

sudo apt-get update
sudo apt-get upgrade -y

# Install package dependencies
declare -a pkgs=(
  python3.8-dev
  python3.8
  python3-pip
  mysql-server*
  mysql-client*
  virtualenv
)
for pkg in ${pkgs[@]}
do
  sudo apt-get install $pkg -y
done

# Activate virtual environment
python3.8 -m venv honeyenv
source honeyenv/bin/activate

# Install python dependencies
pip3 install -r requirements.txt

# Change permission of forbidden.txt
if [[ -r "server_root/htdocs/forbidden.txt" ]]; then
  echo
  echo "** Changing permission of 'forbidden.txt' **"
  chmod -r server_root/htdocs/forbidden.txt
fi

echo
echo "-------------------------------------------"
echo
echo
echo "---------- SQL DATABASE CREATION ----------"
echo

read -p "Enter a username for your MySQL Database: " username
read -sp "Enter a secure password: " pass
echo
ret=$(sudo mysql -e "CREATE USER '$username'@'localhost' IDENTIFIED BY '$pass';")

while [[ $ret -ne 0 ]]; do
  read -sp "Failed. Enter a MORE secure password: " pass
  ret=$(sudo mysql -e "CREATE USER '$username'@'localhost' IDENTIFIED BY '$pass';")
done

sudo mysql -e "GRANT ALL PRIVILEGES ON * . * TO '$username'@'localhost';" >> /dev/null
sudo mysql -u $username -p$pass -e "FLUSH PRIVILEGES;" > /dev/null  2>&1
mysql -u $username -p$pass -e "CREATE DATABASE webserver_logs;" > /dev/null 2>&1

echo "Created database 'webserver_logs'"

echo
echo "-------------------------------------------"
echo
echo
echo "-------------- NETWORK SETUP --------------"
echo

echo "Redirecting port 80 requests to server listening port 8080"
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

echo "Redirecting port 443 requests to server listening port 8080"
sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8080

echo
echo "-------------------------------------------"
echo
echo
echo "--------------- FINAL SETUP ---------------"
echo

# Create fake keys and auth file
echo "Creating fake server keys and auth file in server_root/vars/keys"
mkdir server_root/vars/keys
cd server_root/vars/keys
openssl req -newkey rsa:4096 -nodes -sha512 -x509 -days 21 -nodes -out cert.pem -keyout key.pem
chmod 700 *.pem
echo "YWRtaW46cGFzc3dvcmQ=" > auth.txt    # base64 encoding for 'admin:password'
cd ../../../

sleep 1

echo
read -p "Enter an IP to host this webserver: " ip
echo "#!/bin/bash

source honeyenv/bin/activate
python3.8 honeypot_server.py $ip 8080" > ./start_webserver.sh
chmod +x start_webserver.sh

echo
echo "===== TO START WEB SERVER ====="
echo

mkdir vars/keys
echo "In 'vars/keys:"
echo "  Put your full-chain certificate in      'fullchain.pem'"
echo "  Put your private key in                 'privkey.pem'"
echo "  Put your base64-encoded auth creds in   'auth.txt'"

echo 

echo "In 'vars/constants.py':"
echo "  Fill in USERNAME with previously entered MySQL username"
echo "  Fill in PASSWORD with previously entered MySQL password"
echo "  Fill in WEBSITE_URL with your https:// URL to redirect to on 301 error"
echo "  Add to KNOWN_USERS if you desire"

echo

echo "AFTER THE ABOVE HAS BEEN COMPLETED:"
echo "  Execute 'python3.8 vars/database_api.py create'"
echo "  Start the server using ./start_webserver.sh"
