# Mods on Raspbian for the Kiosk functionality

- [Pre-boot modifications](#pre-boot-modifications)
- [Software installations](#software-installations)
- [Modifications on the bootloader](#modifications-on-the-bootloader)
- [Activate SSH Server](#activate-ssh-server)
- [Allow root permission via SSH](#allow-root-permission)
- [Connect to Raspberry](#connect-to-rasperry)

## Pre-boot modifications

Added the following to the config.txt on the FAT partition of the SD card

```
max_usb_current=1
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 1024 600 6 0 0 0
```

## Software installations

Very useful tool for missing packages

```shell
sudo apt update
sudo apt install command-not-found
sudo update-command-not-found
```

Fix touchscreen pointing device

```shell
sudo apt install xserver-xorg-input-evdev
sudo mv /usr/share/X11/xorg.conf.d/40-libinput.conf /usr/share/X11/xorg.conf.d/40-libinput.conf_bak
reboot
```

Uninstall stuff that is not needed

```shell
sudo apt remove --purge libreoffice* wolfram-engine minecraft-pi sonic-pi python3-numpy smartsim timidity scratch nuscratch python3-pygame python-pygame python-tk python-picraft bluej claws-mail greenfoot nodered geany xpdf
sudo apt autoremove
sudo apt upgrade
```

Remove warning when starting any gtk+ application

```shell
sudo apt install at-spi2-core
```

Install packages for the Python PyQt graphical user interface

```
sudo apt-get update
sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
sudo apt-get install python3-pyqt5
sudo apt-get install python3-pyqt5.qtwebkit
reboot
```

## Modifications on the bootloader

In this section, devicetree overlays are used. For more information on the devicetree, check [this webpage](https://www.raspberrypi.org/documentation/configuration/device-tree.md).

First activate the GPIO-poweroff overlay which acts as feedback for the power board. Then activate the GPIO-shutdown overlay in order to be able to shutdown the PI with the click of a button.
Currently, the GPIO-poweroff overlay leaves the system with a kernel panic at the end of the power cycle because something tries to kill the init task. However this should not be a problem, as the storage is unmounted before.
Finally, the bootloader should not display any kind of messages.

```shell
sudo mount -t auto /dev/mmcblk0p1 /mnt/
sudo sh -c "echo dtoverlay=gpio-poweroff,active_low="y"\ndtoverlay=gpio-shutdown,gpio_pin=20 >> /mnt/config.txt"
sudo sh -c "sed -i 's/$/ logo.nologo consoleblank=0 vt.global_cursor_default=0/' /mnt/cmdline.txt"
sudo sh -c "sed -i 's/console=tty./console=tty3/g' /mnt/cmdline.txt"
sudo umount /mnt
sudo sh -c "sed -i 's/#kernel.printk = . . . ./kernel.printk = 0 0 0 0/g' /etc/sysctl.conf"
sudo sh -c "sed -i 's/ExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM/ExecStart=-/sbin/agetty --skip-login --noclear --noissue --login-options "-f pi" %I $TERM/' /etc/systemd/system/autologin@.service"
sudo sh -c "sed -i 's/session    optional   pam_lastlog.so/#session    optional   pam_lastlog.so/' /etc/pam.d/login"
sudo sh -c "sed -i 's/session    optional   pam_motd.so/#session    optional   pam_motd.so/' /etc/pam.d/login"
sudo plymouth-set-default-theme spinfinity
```

## Activate SSH Server

For current Raspbian versions the ssh server is already installed. Just activate it:

```shell
sudo raspi-config
```

Select SSH and reboot.

For older versions the installation has to be done manually. Install, start and enable automatic start:

```shell
sudo apt-get install ssh
sudo /etc/init.d/ssh start
sudo update-rc.d ssh defaults
```

## Allow root permission via SSH

Login as user pi:

```shell
pi:raspberry
```

Set a new password for user "root". There is no password set by default.

```shell
sudo passwd
```

Call configurations for the SSH server

```shell
sudo nano /etc/ssh/sshd_config
```

Search for the following code block..

```shell
# Authentication:
LoginGraceTime 120
PermitRootLogin without-password
StrictModes yes
```
..and change like this:

```shell
# Authentication:
LoginGraceTime 120
PermitRootLogin yes
StrictModes yes
```

To save changes press STRG-X and enter two times.
Reboot afterwards

```shell
sudo reboot
```


## Connect to Raspberry

Get the IP of the pi:

```shell
hostname -I
```

Connect via terminal (Linux/MacOS) ..
(-Y allows the usage of graphical applications)

```shell
ssh -Y pi@IP
```
.. or Putty (Windows).

When a host key WARNING appears, the latest key has to be removed (it was generated in another session from the last person that accessed a pi from this computer).

So follow the instructions and delete the host key:

```shell
ssh-keygen -f "../.ssh/kown_hosts" -R IP
``` 

Where IP is the adress of the computer that should access the pi and .. is the path to the configuration file.

Close the connection afterwards:

```shell
exit
```
