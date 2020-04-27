#!/bin/bash

forbidden="honeypot/server_root/htdocs/forbidden.txt"

if [[ -r $forbidden ]]; then
  echo "changed"
  chmod -r $forbidden
else
  chmod +r $forbidden
fi
