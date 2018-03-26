# Mods on Raspbian for the Kiosk functionality

- [Pre-boot modifications](#pre-boot-modifications)
- [Software installations](#software-installations)
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

```shell
sudo apt update
sudo apt install command-not-found
sudo update-command-not-found
```

```shell
sudo apt install xserver-xorg-input-evdev
sudo mv /usr/share/X11/xorg.conf.d/40-libinput.conf /usr/share/X11/xorg.conf.d/40-libinput.conf_bak
reboot
```

```shell
sudo apt remove --purge libreoffice* wolfram-engine minecraft-pi sonic-pi python3-numpy smartsim timidity scratch nuscratch python3-pygame python-pygame python-tk python-picraft bluej claws-mail greenfoot nodered geany xpdf
sudo apt autoremove
sudo apt upgrade
```
##Activate SSH Server

For current Raspbian versions the ssh server is already installed. Just activate it:

```
sudo raspi-config
```

Select SSH and reboot.

For older versions the installation has to be done manually. Install, start and enable automatic start:

```
sudo apt-get install ssh
sudo /etc/init.d/ssh start
sudo update-rc.d ssh defaults
```

##Allow root permission via SSH

Login as user pi:

```
pi:raspberry
```

Set a new password for user "root". There is no password set by default.

```
sudo passwd
```

Call configurations for the SSH server

```
sudo nano /etc/ssh/sshd_config
```

Search for the following code block..

```
# Authentication:
LoginGraceTime 120
PermitRootLogin without-password
StrictModes yes
```
..and change like this:

```
# Authentication:
LoginGraceTime 120
PermitRootLogin yes
StrictModes yes
```

To save changes press STRG-X and enter two times.
Reboot afterwards

```
sudo reboot
```


##Connect to Raspberry

Get the IP of the pi:

```
hostname -I
```

Connect via terminal (Linux/MacOS) ..
(-Y allows the usage of graphical applications)

```
ssh -Y pi@IP
```
.. or Putty (Windows).

When a host key WARNING appears, the latest key has to be removed (it was generated in antoher session from the last person that accessed a pi from this computer).

So follow the instructions and delete the host key:

```
ssh-keygen -f "../.ssh/kown_hosts" -R IP
``` 

Where IP is the adress of the computer that should access the pi and .. is the path to the configuration file.

Close the connection afterwards:

```
exit
```
