#!/bin/bash

forbidden="./honeypot/http_root/htdocs/forbidden.txt"

if [[ -r $forbidden ]]; then
  chmod -r $forbidden
else
  chmod +r $forbidden
fi
