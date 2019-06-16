# ETAfly

[软件说明](./software/README.md) |
[硬件说明](./hardware/README.md) |
[机械结构说明](./graphic_model/README.md)

## 1、飞控
[![Badge](https://img.shields.io/badge/link-996.icu-%23FF4D5B.svg)](https://996.icu/#/en_US)
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)
[![Slack](https://img.shields.io/badge/slack-996icu-green.svg)](https://join.slack.com/t/996icu/shared_invite/enQtNTg4MjA3MzA1MzgxLWQyYzM5M2IyZmIyMTVjMzU5NTE5MGI5Y2Y2YjgwMmJiMWMxMWMzNGU3NDJmOTdhNmRlYjJlNjk5ZWZhNWIwZGM)

---

| 硬件 | 描述 |
| -- | -- |
|芯片型号| TM4C123G |
|CPU| Cortex-M4 |
|主频| 80MHz |
|FLASH| 256KB |
|RAM|  32KB |
|EEPROM|  2KB |
|单元| FPU、DSP |


![测试图](https://img-blog.csdnimg.cn/20190616200215386.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NDkyOTMy,size_16,color_FFFFFF,t_70)




## 2、目录说明
```
+——Underwater_vehicle
|--------+ docs: 【设计参考文档】
|--------+ hardware:【相关电路设计】      
|            ├──README.md

|--------+ software:【相关软件设计】
|            ├──README.md
|			 └──ETAfly  【主要系统控制程序】
|--------+ machine-vision:【机器视觉】
|            ├──README.md
|			 └──OpenMV  【主要视觉识别】
|--------+ mechanical-structure:【机械结构】
|--------+ README.md
```

## 3、软件结构
```


```

## 4、硬件结构


```
+——ETAfly
|--------+──DC 12V 【Power management】 
|--------+──TM4C123G 【Control-Center】                  
|        │       └──【Normal Peripherals】
|        │       ├── LED [GPIO]   
|        │       ├── KEY [GPIO]  
|        │       ├── Dial Switch [GPIO]   
|        │       ├── OLED [Software SPI]       
|        │       ├── Voltage Detection [ADC]             
|        │       ├── Bluetooth [UART]       
|        │       ├── USB [USB]
|        │       └──......  
|        │       └── 【Important Peripherals】
|        │       ├── Magnetometer [I2C]
|        │       ├── Gyroscope [I2C]   
|        │       ├── OpenMV [UART]
|        │       └──...... 
|--------+── Devices
|        ├── Motor [PWM]
|        ├── Raspberry Pi CAMERAs 
|        └──...... 
```






## 5、ETAfly 的进展
- [X] 电路设计

	
- [X] 控制程序


- [X] 视觉
	- [ ] OpenMV

	- [ ] 树莓派
		- [ ] OpenCV


- [X] 机械结构






#### 使用说明

- 暂无添加

#### 参与贡献

- Fork 本仓库
- 新建 Feat_xxx 分支
- 提交代码
- 新建 Pull Request





