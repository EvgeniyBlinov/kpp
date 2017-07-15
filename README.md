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
