# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:59:32 2020

@author: Gebruiker
"""


import winput, time
import ctypes
import win32clipboard
import threading
import win32ui

def getCurrentForegroundWindow():
    return win32ui.GetForegroundWindow().GetWindowText()

def isSlackSelected():
    return "Slack" in getCurrentForegroundWindow()

def checkClipBoard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText("Yoink")
    win32clipboard.CloseClipboard()
    while True:
        time.sleep(1./120)
        try:
            win32clipboard.OpenClipboard()
            curClip = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            if "@" in curClip:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText("Oops, forgot to lock again? luckily for you, I locked the PC before someone could ctf ;)")
                win32clipboard.CloseClipboard()
                ctypes.windll.user32.LockWorkStation()
        except Exception:
            pass
            
        

chars = [0,0]
def keyboard_callback( event ):
    global chars
    #if event.vkCode == winput.VK_ESCAPE: # quit on pressing escape
    #    winput.stop()
    if event.vkCode != chars[-1]:
        chars[0] = chars[1]
        chars[1] = event.vkCode
    if chars == [161,50] or chars == [160,50]:
        chars = [0,0]
        ctypes.windll.user32.LockWorkStation()
    if 165 in chars or 164 in chars:
        chars = [0,0]
        ctypes.windll.user32.LockWorkStation()
        
#print("Press escape to quit")
    
# hook input
winput.hook_keyboard( keyboard_callback )

thread_clipboard = threading.Thread(target=checkClipBoard, args=())
thread_clipboard.start()
# enter message loop
try:
    while 1:
        time.sleep(1./120)
        msg = (winput.get_message())
        if msg:
            break
except KeyboardInterrupt:
    pass

# remove input hook
winput.unhook_keyboard()