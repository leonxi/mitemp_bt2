[English](./README.md) | 简体中文

# 小米 米家蓝牙温湿度计2

[![GitHub Release][releases-shield]][releases]

这是一个Home Assistant自定义组件，用于集成小米 米家蓝牙温湿度计2 (LYWSD03MMC)。

![LYWSD03MMC](/pictures/LYWSD03MMC.jpg)
![LYWSDCGQ/01ZM](/pictures/LYWSDCGQ01ZM.jpg)

## 支持的设备

| Name                   | Model                  | Model no. |
| ---------------------- | ---------------------- | --------- |
| 小米 米家蓝牙温湿度计  |  | LYWSDCGQ/01ZM |
| 小米 米家蓝牙温湿度计2  |  | LYWSD03MMC  |

## 功能

### 米家蓝牙温湿度计2 (LYWSD03MMC)

- Attributes
  - `temperature`
  - `humidity`
  - `battery`

## 安装

你可以先在HACS设置菜单中，把这个库 ([https://github.com/leonxi/mitemp_bt2](https://github.com/leonxi/mitemp_bt2/)) 添加到 [HACS](https://hacs.xyz/) . 你将在集成菜单中找到定制组件，然后查找关键字 'Xiaomi Mijia BLE Temperature Hygrometer 2 Integration' 进行添加. 或者, 也可以通过将该自定义组件的 custom_component 文件夹，复制到 Home Assistant 的 config 文件夹.

## 设置

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

配置变量:
- **mac** (*Required*): The MAC of your device.
- **mode** (*Optional*): The mode of your device. Default LYWSD03MMC
- **name** (*Optional*): The name of your device.
- **period** (*Optional*): The scan period of your device. Default 300 seconds.

## 面板显示

  ![LYWSD03MMC_PANEL_SHOW](/pictures/sample_panel_1.png)
