# Telegram-Tools
Telegram 小工具。

# 说明
[English](README.md) | [中文](README-zh.md)


# 功能
1. 导出小组成员
2. 添加用户到小组
3. 发送消息给用户

# 设置 API
1. 打开 [https://my.telegram.org](https://my.telegram.org) 并登陆。
2. 点击 API development tools 并且输入相关信息。
<img src="Instructions/1.png" width="550px">

3. 在config.txt文件填入api_id, api_hash和电话号码

# 安装依赖
### Windows
1. 打开命令提示符并且输入 ```python3```，然后会打开微软商店。
<img src="Instructions/2.png" width="750px">

2. 安装 Python
3. 输入命令 ```python3 -m pip install telethon``` 或者 ```pip3 install telethon``` 来安装 telethon.

### macOS
1. 在 Terminal 输入命令 ```brew install python3```.
2. 输入命令 ```python3 -m pip install telethon``` 或者 ```pip3 install telethon``` 来安装 telethon.

# 使用方法
```python3 Telegram-Tools.py```

如果要使用添加用户到小组或者发送消息给用户功能，需要设置csv文件

```python3 Telegram-Tools.py xxxxx.csv```
