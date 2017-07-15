# kpp
kernel custom parameters parser

## Install

!!! IMPORTANT - save you current grub.cfg

```sh
cp /boot/grub/grub.cfg /boot/grub/grub.cfg.work
```

```sh
sudo -s -- <<EOC
wget -O /usr/local/bin/kpp https://raw.githubusercontent.com/EvgeniyBlinov/kpp/master/kpp.py?t=`date +%s` &&
chmod +x /usr/local/bin/kpp &&
/usr/local/bin/kpp -c 'scenario=job;scenario=media' > /etc/grub.d/05_linux_kpp
update-grub
EOC
```

## My usage example

```sh
cat ~/.config/lxsession/Lubuntu/autostart
@/home/user/myscripts/startup.sh

cat /home/user/myscripts/startup.sh
#! /bin/bash
setxkbmap -option terminate:ctrl_alt_bksp
xmodmap -e "remove lock = Caps_Lock"
[ "xjob" == "x$(kpp -e scenario)" ] && {
/usr/bin/x-www-browser &
/usr/bin/skype &
lxterminal -e 'vim -S ~/.vimsession.vim' &
lxterminal -e 'export EDITOR=vim;mc' &
lxterminal -e 'export EDITOR=vim;echo "Enter root pass:";su -' &
}

[ "xmedia" == "x$(kpp -e scenario)" ] && {
/usr/bin/kodi &
}
```
