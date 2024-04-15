#!/bin/bash

if [[ "$EUID" -ne 0 ]]; then
  echo "Please run this script as root." 1>&2
  exit 1
fi

# Ensure default user shell timeout is 900 seconds or less

cp /etc/bash.bashrc /etc/bash.bashrc.bak
cp /etc/profile /etc/profile.bak

tmoutbash=$(grep -cP '^TMOUT=600$' /etc/bash.bashrc)
if [ $tmoutbash -eq 0 ];
then
	printf '\n%s\n' 'TMOUT=600' >> /etc/bash.bashrc
fi

tmoutprof=$(grep -cP '^TMOUT=600$' /etc/profile)
if [ $tmoutprof -eq 0 ];
then
	printf '\n%s\n' 'TMOUT=600' >> /etc/profile
fi

#Ensure SSH X11 forwarding is disabled

cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sed -i "s/^X11Forwarding.*yes/X11Forwarding no/" /etc/ssh/sshd_config

# Disable IPv6

cp /etc/default/grub /etc/default/grub.bak
sed -i "s/^GRUB_CMDLINE_LINUX=\"\"/GRUB_CMDLINE_LINUX=\"ipv6.disable=1\"/" /etc/default/grub
update-grub
