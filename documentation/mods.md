# Mods on Raspbian for the Kiosk functionality

- [Pre-boot modifications](#pre-boot-modifications)
- [Software installations](#software-installations)

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

```
sudo apt install command-not-found
sudo apt-file update
sudo update-command-not-found
```

```
sudo apt install xserver-xorg-input-evdev
sudo mv /usr/share/X11/xorg.conf.d/40-libinput.conf /usr/share/X11/xorg.conf.d/40-libinput.conf_bak
reboot
```