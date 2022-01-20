import time
import frida

def fridaSpawn(packageName):
    device = frida.get_usb_device()
    pid = device.spawn([packageName])
    device.resume(pid)
    return pid

# 获取可导出的 Activitys
def getExportedActivitys(session):
    with open(".//script//get_exported_activitys.js", "r", encoding="utf-8") as f:
        script = session.create_script(f.read())
    script.on("message", exported_activitys_handler)  # 注册消息处理函数
    script.load()
    time.sleep(3) # 为了让脚本执行完，获取全局变量 activitys

def exported_activitys_handler(message, payload):
    global activitys
    print(message)
    activitys = []
    if message["type"] == "send":
        activitys = message["payload"]
    return activitys

# 启动 Activity
def startActivity(session, activity):
    with open(".//script//start_activity.js", "r", encoding="utf-8") as f:
        script = session.create_script(f.read())
    script.on("message", my_message_handler)  # 注册消息处理函数
    script.load()
    script.post({"activity": activity})

# 获取拒绝服务的 Activity 列表
def activitysDosTest(packageName):
    dos_activity = []
    pid = fridaSpawn(packageName)
    session = frida.get_usb_device().attach(pid)
    getExportedActivitys(session)
    for activity in activitys:
        startActivity(session, activity)
        time.sleep(3)
        try:
            frida.get_usb_device().attach(pid)
        except Exception as e:
            dos_activity.append(activity)
            pid = fridaSpawn(packageName)
            session = frida.get_usb_device().attach(pid)
            print(e)
    # print(dos_activity)
    return dos_activity



# 获取可导出的 service
def getExportedServices(session):
    with open(".//script//get_exported_services.js", "r", encoding="utf-8") as f:
        script = session.create_script(f.read())
    script.on("message", exported_services_handler)  # 注册消息处理函数
    script.load()
    time.sleep(3) # 为了让脚本执行完，获取全局变量 services

def exported_services_handler(message, payload):
    global services
    print(message)
    services = []
    if message["type"] == "send":
        services = message["payload"]
    return services

# 启动 service
def startService(session, service):
    with open(".//script//start_service.js", "r", encoding="utf-8") as f:
        script = session.create_script(f.read())
    script.on("message", my_message_handler)  # 注册消息处理函数
    script.load()
    script.post({"service": service})

# 获取拒绝服务的 service 列表
def servicesDosTest(packageName):
    dos_service = []
    pid = fridaSpawn(packageName)
    session = frida.get_usb_device().attach(pid)
    getExportedServices(session)
    for service in services:
        startService(session, service)
        time.sleep(3)
        try:
            frida.get_usb_device().attach(pid)
        except Exception as e:
            dos_service.append(service)
            pid = fridaSpawn(packageName)
            session = frida.get_usb_device().attach(pid)
            print(e)
    # print(dos_service)
    return dos_service



# 获取可导出的 Receivers
def getExportedReceivers(session):
    with open(".//script//get_exported_receivers.js", "r", encoding="utf-8") as f:
        script = session.create_script(f.read())
    script.on("message", exported_receivers_handler)  # 注册消息处理函数
    script.load()
    time.sleep(3) # 为了让脚本执行完，获取全局变量 receivers

def exported_receivers_handler(message, payload):
    global receivers
    print(message)
    receivers = []
    if message["type"] == "send":
        receivers = message["payload"]
    return receivers

# 启动 recevice
def startReceiver(session, receiver):
    with open(".//script//start_receiver.js", "r", encoding="utf-8") as f:
        script = session.create_script(f.read())
    script.on("message", my_message_handler)  # 注册消息处理函数
    script.load()
    script.post({"receiver": receiver})

# 获取拒绝服务的 receivers 列表
def receiversDosTest(packageName):
    dos_receiver = []
    pid = fridaSpawn(packageName)
    session = frida.get_usb_device().attach(pid)
    getExportedReceivers(session)
    for receiver in receivers:
        startReceiver(session, receiver)
        time.sleep(3) # 等待脚本执行完成
        try:
            frida.get_usb_device().attach(pid)
        except Exception as e:
            dos_receiver.append(receiver)
            pid = fridaSpawn(packageName)
            session = frida.get_usb_device().attach(pid)
            print(e)
    # print(dos_receiver)
    return dos_receiver


def initEpList(packageName):
    pid = fridaSpawn(packageName)
    session = frida.get_usb_device().attach(pid)
    getExportedActivitys(session)
    getExportedServices(session)
    getExportedReceivers(session)

def my_message_handler(message, payload):
    print(message)
    # print(payload)
