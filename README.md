# Raspberry Pi 3 powered kiosk

- [Introduction](#introduction)
  - [Scope](#scope)
  - [Audience](#audience)
  - [Documentation](#documentation)
  - [Acronyms](#acronyms)
- [1. Components](#1-components)
- [2. Milestones (Roadmap)](#2-milestones-roadmap)
- [3. Software](#3-software)
- [4. Hardware](#4-hardware)
- [5. Power consumption](#5-power-consumption)
- [Appendix](#appendix)
  - [Useful webpages](#useful-webpages)

## Introduction

### Scope

This repository shows the work in progress of the TI project summer 2018 no. 6. 

### Audience

This document should be a guide for future participants in the project. 

### Documentation

* [Automatic TOC generation](http://tableofcontent.eu/)
* [General form](https://docs.gitlab.com/ee/user/markdown.html)
* [Table generator](http://www.tablesgenerator.com/markdown_tables)
* Markdown editor 
	- Windows & Linux: [Ghostwriter](https://wereturtle.github.io/ghostwriter/)
	- MacOS: [Macdown](https://macdown.uranusjr.com/)

### Acronyms

**OS** Operating System

## 1. Components


| Unit         | Component                                                                          |
|:-------------|:----------------------------------------------------------------------------------:|
| Compute unit | Raspberry Pi 3 B                                                                   |
| Screen       | [Waveshare 10.1" HDMI LCD(H)](https://www.waveshare.com/wiki/10.1inch_HDMI_LCD_(H))|
| OS           | [Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/)                |

## 2. Milestones (Roadmap)

- [x] Building development system
- [x] Putting touchscreen into operation
- [x] Creating standby logic
    - [x] Concept
    - [x] Design
    - [x] Test
- [x] Hosting a fullscreen application
	- [x] Implement button functionality
		- [x] Build button test setup
		- [x] Create python software drivers
		- [x] Solder buttons
	- [x] Set up GUI
		- [x] Implement GUI
		- [x] Test GUI on the Raspberry 
	- [x] Integration
- [x] Creating a case
	- [x] Concept
	- [x] Design
	- [x] Manufacture
	- [x] Paint
- [x] Integrating admin access
- [ ] Writing setup-bashscript

## 3. Software

- Modifications on the OS can be found in [this](documentation/mods.md) document.
- The application development is descibend in [this](documentation/app.md) document.
- The documentation for the modified bootloader can be found [here](documentation/bootloader.md).

## 4. Hardware

- Everything concerning hardware is described in [this](documentation/hw.md) document.

## 5. Power consumption

|Nominal Voltage|Measured Current|Consumed Power|
|---------------|----------------|--------------|
|12V            |~0.5A           |~6W           |

## Appendix

### Useful webpages
  
[Add a power button to the Raspberry](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi)
[Original project descripton (DE)](http://www.netzmafia.de/skripten/hardware/RasPi/Projekt-Kiosk/)  
[Pi 3 Kiosk (DE)](https://itrig.de/index.php?/archives/2309-Raspberry-Pi-3-Kiosk-Chromium-Autostart-im-Vollbildmodus-einrichten.html)  
[Various Information on the Raspberry Pi (DE)](http://www.elektronik-kompendium.de/sites/raspberry-pi/index.htm)  


