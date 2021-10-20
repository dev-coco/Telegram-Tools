# Telegram-Tools
Telegram tools.

# Explanation
[English](README.md) | [中文](README-zh.md)


# Features
1. Export group memebrs
2. Add users to the group
3. Send message to users

# Setup API
1. Open [https://my.telegram.org](https://my.telegram.org) and login.
2. Click on API development tools and fill the required fields.
<img src="Instructions/1.png" width="550px">

3. Fill in api_id, api_hash, moble number in the config.txt file.

# Dependencies
### Windows
1. Open Command Prompt and enter ```python3```, then will open Microsoft Store.
<img src="Instructions/2.png" width="750px">

2. Install Python
3. Enter command ```python3 -m pip install telethon``` or ```pip3 install telethon``` to install telethon.

### macOS
1. Enter ```brew install python3``` in the Terminal.
2. Enter command ```python3 -m pip install telethon``` or ```pip3 install telethon``` to install telethon.

# Instructions
```python3 Telegram-Tools.py```

If you want to use the Add users to the group or Send message to users feature, you need to set up the csv file.

```python3 Telegram-Tools.py xxxxx.csv```
