English | [简体中文](./README_zh-CN.md)

# Xiaomi Mijia BLE Temperature Hygrometer 2

[![GitHub Release][releases-shield]][releases]
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This is a custom component for home assistant to use bluetooth adapter directly integrate the Xiaomi Mijia BLE Temperature Hygrometer (LYWSDCGQ/01ZM) and Mijia BLE Temperature Hygrometer 2 (LYWSD03MMC).

No Bluetooth Gateway required.

| LYWSD03MMC | LYWSDCGQ/01ZM |
| ---------------------- | ---------------------- |
| ![LYWSD03MMC](/pictures/LYWSD03MMC.jpg) | ![LYWSDCGQ/01ZM](/pictures/LYWSDCGQ01ZM.jpg) |

## Requirements

* Supported & tested on HassOS 4.13 (HassOS Release-4 build 13 (Stable))
  * Warning: HassOS 4.14 has BLE bugs need fix, BLE devices can not be connected.
  * Other versions need to be tested
* Hardware need bluetooth adapter and be actived, tested on Raspberry PI 3 Model B
  * Other hardwares need to be tested

## Supported devices

| Name                   | Model                  | Model no. |
| ---------------------- | ---------------------- | --------- |
| Xiaomi Mijia BLE Temperature Hygrometer  |  | LYWSDCGQ/01ZM |
| Xiaomi Mijia BLE Temperature Hygrometer 2  |  | LYWSD03MMC  |

## Features

### Mijia BLE Temperature Hygrometer (LYWSDCGQ/01ZM)

- Attributes
  - `temperature`
  - `humidity`
  - `battery`

### Mijia BLE Temperature Hygrometer 2 (LYWSD03MMC)

- Attributes
  - `temperature`
  - `humidity`
  - `battery`

## Install

You can install this custom component by adding this repository ([https://github.com/leonxi/mitemp_bt2](https://github.com/leonxi/mitemp_bt2/)) to [HACS](https://hacs.xyz/) in the settings menu of HACS first. You will find the custom component in the integration menu afterwards, look for 'Xiaomi Mijia BLE Temperature Hygrometer 2 Integration'. Alternatively, you can install it manually by copying the custom_component folder to your Home Assistant configuration folder.


## Setup

```yaml
# configuration.yaml

sensor:
  - platform: mitemp_bt2
    mac: 'A4:C1:38:AA:AA:AA'
    mode: 'LYWSD03MMC'
    name: book room
    period: 60
  - platform: mitemp_bt2
    mac: 'A4:C1:38:FF:FF:FF'
    mode: 'LYWSD03MMC'
    name: living room
    period: 60
```

Configuration variables:
- **mac** (*Required*): The MAC of your device.
- **mode** (*Optional*): The mode of your device. Default LYWSD03MMC
- **name** (*Optional*): The name of your device.
- **period** (*Optional*): The scan period of your device. Default 300 seconds.

## Panel Sample

  ![LYWSD03MMC_PANEL_SHOW](/pictures/sample_panel_1.png)

## Todo

- Integration Options
  - Add auto discovery option, to control enable or disable discovery
  - Add period option, to control period of fetching devices' data, default period is 15 minutes. Avoid frequent access to Bluetooth devices, resulting in high power consumption of them.
- Known issues
  - When installation, discoverred devices can not be displayed, and set their own areas.
  - In devices list, area can not be modified.

[releases-shield]: https://img.shields.io/github/release/leonxi/mitemp_bt2.svg
[releases]: https://github.com/leonxi/mitemp_bt2/releases
