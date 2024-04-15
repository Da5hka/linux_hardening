#!/bin/bash

chown root:root /etc/motd
chmod 644 /etc/motd
echo "Hardened by Security Team." > /etc/motd