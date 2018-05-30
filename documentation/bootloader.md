# Modified Plymouth boot splashscreen

Boot splash screens on Raspbian are currently displayed by plymouth.  
Plymouth is an application that runs very early in the boot process
(even before the root filesystem is mounted!) that provides a graphical
boot animation while the boot process happens in the background.
Plymouth themes are usually written in C but Plymouth also ships a script parser
which can be used to create simple boot splash screens.

- [Developing Plymouth splash screens](#developing-plymouth-splash-screens)
- [Installing the splash screen from this repository](#installing-the-splash-screen-from-this-repository)
- [Further reading](#further-reading)

## Developing Plymouth splash screens

An animation for plymouth can be created with the help of the 3D tool [blender](https://www.blender.org/download/).

To develop your own plymouth script install the following packages.

```shell
$ sudo apt install plymouth-themes
$ sudo apt install plymouth-x11
```

A sample script can now be found in */usr/share/plymouth/themes/script*.

```shell
$ sudo plymouth-set-default-theme script
$ cp <src/bootloder/test_plymouth.sh> .
$ ./test_plymouth.sh
```

Refer to [further reading](#further-reading) for more information on the scripting syntax.

## Installing the splash screen from this repository

1. Render the pngs from the blender project.
2. Remove the leading "0" from the file names. In linux with `rename -n 's/^0*//' *` (remove the `-n` switch for "dry run" when satisfied with the results).
3. Execute the following commands.
 
```shell
$ sudo cp -r <src/bootloder/raspberry_pi> /usr/share/plymouth/themes
$ sudo cp <image_folder>/* /usr/share/plymouth/themes/raspberry_pi
$ sudo plymouth-set-default-theme raspberry_pi
$ sudo cp -r <src/bootloder/plymouth-quit.service.d> /etc/systemd/system 
$ sudo systemctl daemon-reload
```

## Further reading

- [Plymouth scripting guide](http://brej.org/blog/?p=158)
- [Plymouth scripting Syntax](https://www.freedesktop.org/wiki/Software/Plymouth/Scripts/)
- [Plymouth git repository](https://github.com/sergeysova/plymouth)