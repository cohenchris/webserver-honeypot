#!/bin/bash

declare -a pkgs=(
  python3.8
  python3-pip
  mysql-server
  libmariadbclient-dev
  virtualenv
)

for pkg in ${pkgs[@]}
do
  sudo apt-get install $pkg
done
