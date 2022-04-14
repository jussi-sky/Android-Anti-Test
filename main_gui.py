# -*- coding: utf-8 -*-
# Jussi

import threading
from tkinter import *
import windnd
from androguard.core.bytecodes.apk import APK
from android_dos import *
from ipainfo import *
from run_shell import *
from config import *

def getApkPath(files):
    try:
        apk_path_Text.delete(1.0, END)
        apk_path_Text.insert(1.0, files[-1].decode("gbk"))
    except Exception as e:
        print(e)
        apk_path_Text.delete(1.0, END)
        apk_path_Text.insert(1.0, "\tGet apk path false!\n")



def signApk():
    apk_path = apk_path_Text.get(1.0, END).strip().replace("\n","")
    # print(apk_path)

    rootPath = os.path.split(os.path.realpath(__file__))[0]
    keystore = os.path.join(rootPath, 'tools\\debug.jks')
    pswd = '123456'
    newApkPath = os.path.splitext(apk_path)[0]

    cmd = 'java -jar %s\\tools\\apksigner.jar sign --ks %s --in %s --out %s_resign.apk --ks-pass pass:%s' % \
          (rootPath, keystore, apk_path, newApkPath, pswd)
    # print(cmd)
    return_code, data = run(cmd)
    # print('return code:', return_code, '\ndata:', data)
    try:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tApk sign false!")



def getApkInfo():
    packageName = ""
    debuggable = False
    allowBackup = True

    apk_path = apk_path_Text.get(1.0, END).strip().replace("\n", "")
    try:
        apk = APK(apk_path)
        appName = apk.get_app_name()
        packageName = apk.get_package()
        androidVersionName = apk.get_androidversion_name()
        minSdkVersion = apk.get_min_sdk_version()
        maxSdkVersion = apk.get_max_sdk_version()

        application = apk.find_tags_from_xml("AndroidManifest.xml", "application")
        if application != []:
            debuggable = application[0].attrib.get("{http://schemas.android.com/apk/res/android}debuggable")
            if debuggable == None:
                debuggable = False
            allowBackup = application[0].attrib.get("{http://schemas.android.com/apk/res/android}allowBackup")
            if allowBackup == None:
                allowBackup = True

        apkByte = open(apk.get_filename(), "rb").read()
        m = hashlib.md5()
        m.update(apkByte)
        apkMd5 = m.hexdigest()
        m = hashlib.sha1()
        m.update(apkByte)
        apkSha1 = m.hexdigest()
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\t应用名:" + str(appName) + "\n")
        print_win.insert(END, "\t包名:" + str(packageName) + "\n")
        print_win.insert(END, "\t入口:" + str(apk.get_main_activity()) + "\n")
        print_win.insert(END, "\t版本:" + str(androidVersionName) + "\n")
        print_win.insert(END, "\t开启调试:" + str(debuggable) + "\n")
        print_win.insert(END, "\t允许备份:" + str(allowBackup) + "\n")
        print_win.insert(END, "\t文件大小:" + str(os.path.getsize(apk.get_filename())) + "\n")
        print_win.insert(END, "\tSDK版本 minSdkVersion:" + str(minSdkVersion) + "\n")
        print_win.insert(END, "\tSDK版本 targetSdkVersion:" + str(maxSdkVersion) + "\n")
        print_win.insert(END, "\t使用V1签名:" + str(apk.get_certificates_v1() != []) + "\n")
        print_win.insert(END, "\t使用V2签名:" + str(apk.get_certificates_v2() != []) + "\n")
        print_win.insert(END, "\t使用V3签名:" + str(apk.get_certificates_v3() != []) + "\n")
        print_win.insert(END, "\tApk文件MD5:" + apkMd5 + "\n")
        print_win.insert(END, "\tApk文件SHA1:" + apkSha1 + "\n")
        print_win.insert(END, "\t*****************************************\n")
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tGet apk info false!\n")
    return packageName



def setProxy():
    cmd = "adb shell settings put global http_proxy " + http_proxy
    return_code, data = run(cmd)
    try:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
        getProxy()
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tSet porxy false!\n")



def clearProxy():
    cmd = "adb shell settings put global http_proxy :0"
    return_code, data = run(cmd)
    try:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
        getProxy()
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tClose porxy false!\n")



def getProxy():
    cmd = "adb shell settings get global http_proxy"
    return_code, data = run(cmd)
    try:
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tget porxy false!\n")


def getCurrentActivity():

    # android < 8.1
    # cmd = "adb shell dumpsys activity | grep \"mFocusedActivity\""

    # android >= 8.1
    cmd = "adb shell dumpsys activity | grep \"mResume\""
    return_code, data = run(cmd)
    try:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\t" + str(data) + "\n")
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tGet current activity false!\n")

def pushFrida():
    cmd = "adb push " + frida_server + " /data/local/tmp"
    return_code, data = run(cmd)
    try:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
    except:
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tFrida push false!\n")

    cmd = "adb shell su -c 'chmod +x /data/local/tmp/hluda*'"
    return_code, data = run(cmd)
    try:
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tFrida chmod false!\n")



def startFrida():
    cmd = "adb shell su -c '/data/local/tmp/hluda-server-14.2.2-android-arm64'"
    return_code, data = run(cmd)
    # print('return code:', return_code, '\ndata:', data)
    try:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
    except Exception as e:
        print(e)
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tFrida start false!\n")



def killFrida():
    cmd = "adb shell su -c 'pkill -9 hluda-server'"
    return_code, data = run(cmd)
    # print('return code:', return_code, '\ndata:', data)
    try:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
    except:
        print_win.delete(1.0, END)
        print_win.insert(1.0, "\tFrida kill false!\n")



def startGadget():
    try:
        packageName = getApkInfo()
        cmd = "adb shell su -c \'echo " + packageName + " > /data/local/tmp/app.list\'"
        # print(cmd)
        return_code, data = run(cmd)
        cmd_fordward = "adb forward tcp:27042 tcp:26000"
        return_code, data = run(cmd_fordward)
        # print('return code:', return_code, '\ndata:', data)
        # print_win.delete(1.0, END)
        print_win.insert(END, "\n\t*****************************************\n")
        print_win.insert(END, "\tReturn code:" + str(return_code) + "\n")
        print_win.insert(END, "\tData:" + str(data) + "\n")
    except Exception as e:
        print(e)
        getApkInfo()
        print_win.insert(END, "\tFrida gadget start false!\n")



def androidDos():
    try:
        packageName = getApkInfo()
        # print_win.delete(1.0, END)
        print_win.insert(END, "\n\t*****************************************\n")
        initEpList(packageName)
        dos_activitys = activitysDosTest(packageName)
        print_win.insert(END, "\tDOS Activity:\n")
        for dos_activity in dos_activitys:
            print_win.insert(END, '\t' + str(dos_activity) + '\n')
        print_win.insert(END, '\n')

        dos_services = servicesDosTest(packageName)
        print_win.insert(END, "\tDOS Service:\n")
        for dos_service in dos_services:
            print_win.insert(END, '\t' + str(dos_service) + '\n')
        print_win.insert(END, '\n')

        dos_receivers = receiversDosTest(packageName)
        print_win.insert(END, "\tDOS Receiver:\n")
        for dos_receiver in dos_receivers:
            print_win.insert(END, '\t' + str(dos_receiver) + '\n')
        print_win.insert(END, "\n\t*****************************************\n")
    except Exception as e:
        print(e)
        print_win.insert(END, "\trun android dos false!\n")



def get_ipa_info():
    ipa_path = apk_path_Text.get(1.0, END).strip().replace("\n", "")
    if ipa_path[-4:] == ".ipa":
        plist_root = analyze_ipa_with_biplist(ipa_path)
        fsize = get_file_size(ipa_path)
        try:
            print_win.delete(1.0, END)
            print_win.insert(END, "\t*****************************************\n")
            print_win.insert(END, "\t文件名:" + plist_root['CFBundleDisplayName'] + "\n")
            print_win.insert(END, "\t进程名:" + plist_root['CFBundleName'] + "\n")
            print_win.insert(END, "\t包名:" + plist_root['CFBundleIdentifier'] + "\n")
            print_win.insert(END, "\t版本号:" + plist_root['CFBundleShortVersionString'] + "\n")
            print_win.insert(END, "\t文件大小:" + str(fsize) + "\n")
            print_win.insert(END, "\tMD5:" + CalcMD5(ipa_path) + "\n")
            print_win.insert(END, "\tSHA1:" + CalcSha1(ipa_path) + "\n")
        except Exception as e:
            print(e)
            print_win.delete(1.0, END)
            print_win.insert(1.0, "\tGet ipa info false!\n")
    else:
        print_win.delete(1.0, END)
        print_win.insert(END, "\t*****************************************\n")
        print_win.insert(END, "\tThe file suffix is not ipa !\n")



def my_message_handler(message, payload):
    print(message)
    print(payload)
    if message["type"] == "send":
        data = message["payload"]
        print_win.insert(END, str(data) + "\n")



def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()



def gui_start():

    global root, apk_path_Text, print_win
    root = Tk()              #实例化出一个父窗口
    root.title("APP Anti Test @Jussi (严禁用于非授权的测试及非法用途)")
    root.geometry('1000x800+10+10')

    # apk path
    apk_name_label = Label(root, text="Apk Path:", height=2)
    apk_name_label.grid(row=0, column=0, sticky=W)

    apk_path_Text = Text(root, width=90, height=2)
    apk_path_Text.grid(row=0, column=1, columnspan=10, sticky=W)

    windnd.hook_dropfiles(root, func=getApkPath)

    # apk info
    apk_info_button = Button(root, text="ApkInfo", bg="lightblue", width=10, command=lambda:thread_it(getApkInfo))
    apk_info_button.grid(row=15, column=1, sticky=W)

    # apk sign
    apksigner_button = Button(root, text="ApkSigner", bg="lightblue", width=10, command=lambda:thread_it(signApk))
    apksigner_button.grid(row=15, column=2, sticky=W)

    # set proxy
    set_proxy_button = Button(root, text="SetProxy", bg="lightblue", width=10, command=lambda: thread_it(setProxy))
    set_proxy_button.grid(row=15, column=3, sticky=W)

    # clear proxy
    clear_proxy_button = Button(root, text="ClearProxy", bg="lightblue", width=10, command=lambda: thread_it(clearProxy))
    clear_proxy_button.grid(row=15, column=4, sticky=W)

    # get current Activity
    get_Activity_button = Button(root, text="CurActivity", bg="lightblue", width=10, command=lambda: thread_it(getCurrentActivity))
    get_Activity_button.grid(row=15, column=5, sticky=W)

    # frida push
    frida_push_button = Button(root, text="frida-push", bg="lightblue", width=10, command=lambda: thread_it(pushFrida))
    frida_push_button.grid(row=25, column=1, sticky=W)

    # frida start
    frida_start_button = Button(root, text="frida-start", bg="lightblue", width=10, command=lambda:thread_it(startFrida))
    frida_start_button.grid(row=25, column=2, sticky=W)

    # frida kill
    frida_kill_button = Button(root, text="frida-kill", bg="lightblue", width=10, command=lambda:thread_it(killFrida))
    frida_kill_button.grid(row=25, column=3, sticky=W)

    # frida gadget start
    gadget_start_button = Button(root, text="gadget-strat", bg="lightblue", width=10, command=lambda:thread_it(startGadget))
    gadget_start_button.grid(row=25, column=4, sticky=W)

    # android DOS
    android_DOS = Button(root, text="android-Dos", bg="lightblue", width=10, command=lambda:thread_it(androidDos))
    android_DOS.grid(row=25, column=5, sticky=W)

    # get ipa info
    ipa_info = Button(root, text="ipaInfo", bg="lightblue", width=10, command=lambda:thread_it(get_ipa_info))
    ipa_info.grid(row=35, column=1, sticky=W)

    # print windows
    apk_name_label = Label(root, text="Print Windows:")
    apk_name_label.grid(row=99, column=0, sticky=W)

    print_win = Text(root, width=90, height=36)
    print_win.grid(row=100, column=1, columnspan=10, sticky=W)

    root.mainloop()

if __name__ == "__main__":
    gui_start()
