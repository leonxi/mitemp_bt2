[English](./README.md) | 简体中文

# 小米 米家蓝牙温湿度计2

[![GitHub Release][releases-shield]][releases]
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

这是一个Home Assistant自定义组件，用于 Home Assistant 通过 蓝牙适配器 直接集成 小米 米家蓝牙温湿度计 (LYWSDCGQ/01ZM) 和 米家蓝牙温湿度计2 (LYWSD03MMC)。

不需要蓝牙网关。

| LYWSD03MMC | LYWSDCGQ/01ZM |
| ---------------------- | ---------------------- |
| ![LYWSD03MMC](/pictures/LYWSD03MMC.jpg) | ![LYWSDCGQ/01ZM](/pictures/LYWSDCGQ01ZM.jpg) |

## 必要条件

* 已支持和测试版本 HassOS 4.13 (HassOS Release-4 build 13 (Stable))
  * 注意: 版本HassOS 4.14 存在蓝牙缺陷，蓝牙设备无法连接.
  * 其它版本有待大家提交测试报告
* 需要在带有蓝牙适配器的设备上运行，已经在树莓派 (Raspberry PI 3 Model B) 上测试成功
  * 其它硬件有待大家提交测试报告

## 支持的设备

| Name                   | Model                  | Model no. |
| ---------------------- | ---------------------- | --------- |
| 小米 米家蓝牙温湿度计  |  | LYWSDCGQ/01ZM |
| 小米 米家蓝牙温湿度计2  |  | LYWSD03MMC  |

## 功能

### 米家蓝牙温湿度计 (LYWSDCGQ/01ZM)

- Attributes
  - `temperature`
  - `humidity`
  - `battery`

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

## 待处理事项

- 集成选项
  - 增加自动发现选项，控制自动发现(启用/禁用)
  - 增加周期选项，控制读取蓝牙设备数据周期(默认15分钟)，避免频繁访问蓝牙设备，造成蓝牙设备耗电高
- 已知问题
  - 安装集成的时候，无法每次都显示扫描到的设备，并设置所在区域
  - 设备区域和名称无法设置和修改 (已解决)

[releases-shield]: https://img.shields.io/github/release/leonxi/mitemp_bt2.svg
[releases]: https://github.com/leonxi/mitemp_bt2/releases
