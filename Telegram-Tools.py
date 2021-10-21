#!/usr/bin/env python3
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.sync import TelegramClient
import configparser, os, sys, csv, random, time, traceback

# Set color
red="\033[1;31m"
green="\033[1;32m"

# Features menu
os.system("clear")
print(green + """
[1] 导出小组成员
[2] 添加用户到小组
[3] 发送消息给用户
""")
menu_item = int(input("\033[0m请输入对应的数字: "))

# Read config file
config = configparser.RawConfigParser()
config.read("config.txt")

try:
	api_id = config["config"]["id"]
	api_hash = config["config"]["hash"]
	phone = config["config"]["phone"]
	client = TelegramClient(phone, api_id, api_hash)
except KeyError:
	os.system("clear")
	print(red + "请按照正确格式编辑config.txt文件\n")
	sys.exit(1)

# Verify account
client.connect()
if not client.is_user_authorized():
	client.send_code_request(phone)
	os.system("clear")
	client.sign_in(phone, input(green + "[+] 请输入Telegram的验证码: " + red))
	
os.system("clear")

# Export group memebrs
if menu_item == 1:
	chats = []
	groups = []
	
	result = client(GetDialogsRequest(
				offset_date=None,
				offset_id=0,
				offset_peer=InputPeerEmpty(),
				limit=200,
				hash = 0
			))
	chats.extend(result.chats)
	for i in chats:
		try:
			if i.megagroup== True:
				groups.append(i)
		except:
			continue

	print(green + "[+] 请选择需要获取成员的小组: " + red)
	for i, g in enumerate(groups):
		print(green + "[" + str(i) + "]" + " - " + g.title)
	g_index = input(green+"[+] 请输入对应的数字: "+red)
	target_group = groups[int(g_index)]
	
	print(green + "[+] 获取小组成员中 ...")
	time.sleep(1)
	all_participants = []
	all_participants = client.get_participants(target_group, aggressive=True)
	
	print(green + "[+] 正在保存文件 ...")
	time.sleep(1)
	# Save file
	with open("小组成员.csv", "w", encoding="UTF-8") as f:
		writer = csv.writer(f, delimiter=",", lineterminator="\n")
		writer.writerow(["username", "user id", "access hash", "name", "group", "group id"])
		for user in all_participants:
			username = user.username or ""
			first_name = user.first_name or ""
			last_name = user.last_name or ""
			name= (first_name + ' ' + last_name).strip()
			writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
	print(green + "[+] 已成功获取小组!")

# Add users to the group
elif menu_item == 2:
	print("需要设置最大延迟时间和最小延迟时间（秒为单位），然后随机取中间的值\n")
	max_time = int(input("请输入最大延迟时间: " + red))
	min_time = int(input("\033[0m请输入最小延迟时间: " + red))
	os.system("clear")
	users = []
	# Get file
	with open(sys.argv[1], encoding="UTF-8") as f:
		rows = csv.reader(f, delimiter=",", lineterminator="\n")
		next(rows, None)
		for row in rows:
			user = {
				"username": row[0],
				"id": int(row[1]),
				"access_hash": int(row[2]),
				"name": row[3],
			}
			users.append(user)
			
	chats = []
	groups = []
	result = client(GetDialogsRequest(
		offset_date=None,
		offset_id=0,
		offset_peer=InputPeerEmpty(),
		limit=900,
		hash=0
	))
	chats.extend(result.chats)
	for i in chats:
		try:
			if i.megagroup == True:
				groups.append(i)
		except:
			continue
		
	print("\033[0m选择需要添加成员的小组: \n")
	for i, group in enumerate(groups):
		print(green + str(i) + " - " + group.title)
	g_index = input("\033[0m\n请输入对应的数字: ")
	target_group = groups[int(g_index)]
	target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
	os.system("clear")
	print(green + "[1] 通过username添加成员\n[2] 通过user id添加成员")
	mode = int(input("\033[0m\n请输入对应的数字: "))
	for user in users:
		rand_time = random.randrange(min_time, max_time)
		try:
			print("添加 {}".format(user["id"]))
			if mode == 1:
				if user["username"] == "":
					continue
				user_to_add = client.get_input_entity(user["username"])
			elif mode == 2:
				user_to_add = InputPeerUser(user["id"], user["access_hash"])
			else:
				sys.exit("输入错误")
			client(InviteToChannelRequest(target_group_entity, [user_to_add]))
			print("等待 {} 秒 ...".format(rand_time))
			time.sleep(rand_time)
		except PeerFloodError:
			print(red+"[!] 账号已受限 \n[!] 脚本已停止运行 \n[!] 请稍后再试")
			client.disconnect()
			sys.exit()
		except UserPrivacyRestrictedError:
			print("这个用户设置了隐私权限，不允许邀请加入小组，已跳过...")
			print("等待 {} 秒 ...".format(rand_time))
			time.sleep(rand_time)
		except:
			traceback.print_exc()
			print("未知错误")
			continue

# Send message to users
elif menu_item == 3:
	print("需要设置最大延迟时间和最小延迟时间（秒为单位），然后随机取中间的值\n")
	max_time = int(input("请输入最大延迟时间: " + red))
	min_time = int(input("\033[0m请输入最小延迟时间: " + red))
	os.system("clear")
	class send_sms():
			users = []
			with open(sys.argv[1], encoding="UTF-8") as f:
				rows = csv.reader(f,delimiter=",",lineterminator="\n")
				next(rows, None)
				for row in rows:
					user = {
						"username": row[0],
						"id": int(row[1]),
						"access_hash": int(row[2]),
						"name": row[3],
					}
					users.append(user)
			print(green + "[1] 通过user id发送信息\n[2] 通过username发送信息")
			mode = int(input(green + "请输入对应的数字: " + red))
			message = input(green + "[+] 请输入需要发送的消息: " + red)
			for user in users:
				rand_time = random.randrange(min_time, max_time)
				if mode == 1:
					receiver = InputPeerUser(user['id'],user['access_hash'])
				elif mode == 2:
					if user['username'] == "":
						continue
					receiver = client.get_input_entity(user['username'])
				else:
					print(red+"[!] 输出错误...")
					client.disconnect()
					sys.exit()
				try:
					print(green+"[+] 发送信息给:", user['name'])
					client.send_message(receiver, message.format(user['name']))
					print(green+"[+] 等待 {} 秒".format(rand_time))
					time.sleep(rand_time)
				except PeerFloodError:
					print(red+"[!] 账号已受限 \n[!] 脚本已停止运行 \n[!] 请稍后再试")
					client.disconnect()
					sys.exit()
				except Exception as e:
					print(red+"[!] 出现错误:", e)
					print(red+"[!] 正在尝试继续 ...")
					continue
			client.disconnect()
			print("完成！消息已发送给所有用户")
	send_sms()
	
else:
	sys.exit("输入错误")
	
