#!/bin/bash

if [ ! $( id -u ) -eq 0 ]; then
  echo Bitte als root ausführen!
  exit
fi


if [ ! -d "/home/pi" ]
  then
    echo Kann nur auf einem Raspberry Pi installiert werden!
    exit
fi

if [ $(dirname $0) != "." ]; then
  echo Bitte vorher ins installverzeichnis wechseln!
  exit
fi

#Pre Boot Modifications
sudo echo -e "max_usb_current=1\nhdmi_group=2\nhdmi_mode=1\nhdmi_mode=87\nhdmi_cvt 1024 600 6 0 0 0 >> /boot/config.txt"

#Uninstall unused software
sudo apt -y remove --purge libreoffice* wolfram-engine minecraft-pi sonic-pi python3-numpy smartsim timidity scratch nuscratch python3-pygame python-pygame python-tk python-picraft bluej claws-mail greenfoot nodered geany xpdf
sudo apt -y autoremove
sudo apt update
sudo apt -y upgrade

#Usefull tool for missing packages
sudo apt -y install command-not-found
sudo update-command-not-found

#Hiding mouse pointer
sudo apt -y install unclutter

#Remove warning when starting any gtk+ application
sudo apt -y install at-spi2-core

#Install packages for the Python PyQt graphical user interface
sudo apt -y install qt5-default pyqt5-dev pyqt5-dev-tools
sudo apt -y install python3-pyqt5
sudo apt -y install python3-pyqt5.qtwebkit

#Modifications on Bootloader
#ip=10.27.210.71::10.27.64.1:255.255.0.0:rpi:eth0:off
#sudo sh -c "echo dtoverlay=gpio-poweroff,active_low="y"\ndtoverlay=gpio-shutdown,gpio_pin=20 >> /boot/config.txt"

sudo sed -i 's/$/ logo.nologo consoleblank=0 vt.global_cursor_default=0/' /boot/cmdline.txt
sudo sed -i 's/console=tty./console=tty3/g' /boot/cmdline.txt
sudo sed -i 's/#kernel.printk = . . . ./kernel.printk = 0 0 0 0/g' /etc/sysctl.conf
sudo sed -i 's/ExecStart=-\/sbin\/agetty --autologin pi --noclear \%I \$TERM/ExecStart=-\/sbin\/agetty --skip-login --noclear --noissue --login-options \"-f pi\" \%I \$TERM/' /etc/systemd/system/autologin@.service
sudo sed -i 's/session    optional   pam_lastlog.so/#session    optional   pam_lastlog.so/' /etc/pam.d/login
sudo sed -i 's/session    optional   pam_motd.so/#session    optional   pam_motd.so/' /etc/pam.d/login

#Edit Autostart LXDE-pi fuer Cursor hiden (idle TIME)
echo -e "@Infoscreen /usr/share/infoscreen\n@unclutter -idle 0" > /home/pi/.config/lxsession/LXDE-pi/autostart

### SSH Configuration
#Activate SSH Server
#
sudo apt -y install ssh
sudo /etc/init.d/ssh start
sudo update-rc.d ssh defaults
#
#Allow Root Permissions via SSH
sudo sh -c "sed -i -e 's/PermitRootLogin without-password/PermitRootLogin yes/g' /etc/ssh/sshd_config"
###

#Install Skript etc
sudo mkdir -p /usr/share/infoscreen
sudo cp -r ../src/python/GUI_Test/Infoscreen.py /usr/bin/Infoscreen
sudo cp ../src/python/GUI_Test/* /usr/share/infoscreen
sudo rm /usr/share/infoscreen/Infoscreen.py

#Install Splash Infoscreen
sudo cp -r ../src/bootloader/raspberry_pi /usr/share/plymouth/themes
sudo plymouth-set-default-theme raspberry_pi
sudo cp -r ./plymouth-quit.service.d /etc/systemd/system
sudo systemctl daemon-reload

#Remove Sudo Rights for User
sudo rm /etc/sudoers.d/010.pi-nopasswd

sudo reboot
