#!/bin/bash

if [ ! $( id -u ) -eq 0 ]; then
  echo Must be run as root
  exit
fi

if [ -z "$1" ]
  then
    echo Bitte IP Adresse als Argument uebergeben
    exit
fi

if [ ! -d "/home/pi" ]
  then
    echo Kann nur auf einem Raspberry Pi installiert werden
    exit
fi

chk_root

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

#Fix Touchscreen pointing device
sudo apt -y install xserver-xorg-input-evdev
sudo mv /usr/share/X11/xorg.conf.d/40-libinput.conf /usr/share/X11/xorg.conf.d/40-libinput.conf_bak

#Remove warning when starting any gtk+ application
sudo apt -y install at-spi2-core

#Install packages for the Python PyQt graphical user interface
sudo apt install -y qt5-default pyqt5-dev pyqt5-dev-tools
sudo apt install -y python3-pyqt5
sudo apt install -y python3-pyqt5.qtwebkit

#Modifications on Bootloader
#ip=10.27.210.71::10.27.64.1:255.255.0.0:rpi:eth0:off
#sudo sh -c "echo dtoverlay=gpio-poweroff,active_low="y"\ndtoverlay=gpio-shutdown,gpio_pin=20 >> /boot/config.txt"

sudo sh -c "sed -i 's/$/ logo.nologo consoleblank=0 vt.global_cursor_default=0/' /boot/cmdline.txt"
sudo sh -c "sed -i 's/console=tty./console=tty3/g' /boot/cmdline.txt"
sudo sh -c "sed -i 's/#kernel.printk = . . . ./kernel.printk = 0 0 0 0/g' /etc/sysctl.conf"
sudo sh -c "sed -i 's/ExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM/ExecStart=-/sbin/agetty --skip-login --noclear --noissue --login-options "-f pi" %I $TERM/' /etc/systemd/system/autologin@.service"
sudo sh -c "sed -i 's/session    optional   pam_lastlog.so/#session    optional   pam_lastlog.so/' /etc/pam.d/login"
sudo sh -c "sed -i 's/session    optional   pam_motd.so/#session    optional   pam_motd.so/' /etc/pam.d/login"

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
sudo mv ./html/Infoscreen.py /usr/bin/Infoscreen
sudo mv ./html/* /usr/share/infoscreen
sudo rmdir ./html

#Install Splash Infoscreen
sudo cp -r ./splashscreen/raspberry_pi /usr/share/plymouth/themes
sudo plymouth-set-default-theme raspberry_pi
sudo cp -r ./plymouth-quit.service.d /etc/systemd/system
sudo systemctl daemon-reload

#Remove Sudo Rights for User
sudo rm /etc/sudoers.d/010.pi-nopasswd

sudo reboot
