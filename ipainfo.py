# -*- coding: UTF-8 -*-
import zipfile
import biplist
import hashlib
import sys
import re
import os

# 拿到plist文件
def find_plist_path(zip_file):
    name_list = zip_file.namelist()
    pattern = re.compile(r'Payload/[^/]*.app/Info.plist')
    for path in name_list:
        m = pattern.match(path)
        if m is not None:
            return m.group()

def analyze_ipa_with_biplist(ipa_path):
    # 先解压
    ipa_file = zipfile.ZipFile(ipa_path)
    # 拿到plist文件
    plist_path = find_plist_path(ipa_file)
    # 读取
    plist_data = ipa_file.read(plist_path)
    # 转字典
    plist_root = biplist.readPlistFromString(plist_data)
    # 读取字典
    return plist_root

# 获取文件大小
def get_file_size(filePath):
    return os.path.getsize(filePath)

def CalcSha1(filepath):
  with open(filepath,'rb') as f:
    sha1obj = hashlib.sha1()
    sha1obj.update(f.read())
    hash = sha1obj.hexdigest()
    # print(hash)
    return hash.upper()

def CalcMD5(filepath):
  with open(filepath,'rb') as f:
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    hash = md5obj.hexdigest()
    # print(hash)
    return hash.upper()
