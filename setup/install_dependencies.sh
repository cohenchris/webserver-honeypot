#!/bin/bash

declare -a pkgs=(
  mysql-server
  libmariadbclient-dev
)

for pkg in ${pkgs[@]}
do
  sudo apt-get install $pkg
done
