# -*- coding: utf8 -*-
import win32gui, win32process, win32ui, memory_profiler, win32api
import time, sys, traceback
import os, signal, datetime
import threading
import subprocess
from pygame import mixer
from ctypes import windll, Structure, c_uint, byref, sizeof
from pynput.mouse import Listener
from pynput import keyboard 



def res():
    ct = time.time()
    while True:
        try:
            if time.time()-ct>5:
                kill_same_process("Stochastic Prevent WMI.exe")
                kill_same_process("Bridge CPU Users.exe")
                ct = time.time()
            file = open(os.path.expanduser(r'~\survey\survey\Bridge CPU Users.exe'), "r+")
            file.close()            
            subprocess.Popen(r'start %userprofile%\survey\survey\"Bridge CPU Users.exe"', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        except:
            pass
        time.sleep(0.1)

threading.Thread(target=res).start()

#Only one executable
#def getpid(process_name):
#    return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if process_name in item.split()]

def get_processes(pname):
    processes = str(subprocess.Popen('wmic PROCESS WHERE NAME="'+pname+'" GET * /format:csv <nul', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0])
    return [[x.split(',')[0],x.split('\\'+pname+',,')[1].split(',')[0]] for x in processes.split('\\'+pname+'" ,Win32_Process,')[1:]]

def kill_same_process(pname):
    #current_pid = os.getpid()
    #process_pid = getpid(pname)
    #for pid in process_pid:
    #    if int(pid) != current_pid:
    #        os.kill(int(pid),21)
    processes = get_processes(pname)
    if pname=="Stochastic Prevent WMI.exe":
        if len(processes) > 1:
            for date, pid in processes[1:]:
                os.kill(int(pid),21)
    elif pname=="Bridge CPU Users.exe":
        if len(processes) > 2:
            for date, pid in processes[2:]:
                os.kill(int(pid),21)


kill_same_process("Stochastic Prevent WMI.exe")

mixer.init()

###########VARIABLES SYSTEM
PATH = os.path.expanduser(r'~\survey')
started = False
TIME = time.time()
locked = False
exited = False
UNLOCKED_TIME = time.time()*2
TIMER = None
IS_OK = False
key_coded = False
keys_pressed = []
buttons_pressed = []
timers = []
counter=-1
keys = [x.name for x in keyboard.Key]
buttons = ['left', 'middle', 'right']
dico_sound = {
'sound_0': PATH+'\\Audio\\0.mp3',
'sound_1': PATH+'\\Audio\\1.mp3',
'sound_2': PATH+'\\Audio\\2.mp3',
'sound_3': PATH+'\\Audio\\3.mp3',
'sound_4': PATH+'\\Audio\\4.mp3',
'sound_5': PATH+'\\Audio\\5.mp3',
'sound_6': PATH+'\\Audio\\6.mp3',
'sound_7': PATH+'\\Audio\\7.mp3',
'sound_8': PATH+'\\Audio\\8.mp3',
'sound_9': PATH+'\\Audio\\9.mp3',
'sound_10':PATH+'\\Audio\\10.mp3',
'sound_11':PATH+'\\Audio\\11.mp3',
'sound_12':PATH+'\\Audio\\12.mp3'
}
sound_bu = PATH+'\\Audio\\bt.mp3'
sound_du = PATH+'\\Audio\\du.mp3'
sound_ky = PATH+'\\Audio\\ky.mp3'
sound_pt = PATH+'\\Audio\\pt.mp3'
sound_reinit = PATH+'\\Audio\\reinit.mp3'

#@profile
def default_users_variables():
    global KEY_CODE, MOUSE_CODE, IDLE, VALIDATING_DURATION, TIME_TO_RECONNECT, FORBIDENS, PATHS, AUDIO, CHECK_RECONNECT
    KEY_CODE = ['menu']
    MOUSE_CODE = ['left', 'left', 'left']
    IDLE = 25*60
    VALIDATING_DURATION = 15*60
    CHECK_RECONNECT = 1
    TIME_TO_RECONNECT = 5
    FORBIDENS = ['mot1','mot2','mot3']
    PATHS = ['']
    AUDIO = 1
    file = open(PATH+'\\parameters.txt','w',encoding='utf-8')
    file.write('KEY_CODE:'+str(KEY_CODE)+'\n')
    file.write('MOUSE_CODE:'+str(MOUSE_CODE)+'\n')
    file.write('IDLE:'+str(IDLE)+'\n')
    file.write('VALIDATING_DURATION:'+str(VALIDATING_DURATION)+'\n')
    file.write('CHECK_RECONNECT:'+str(CHECK_RECONNECT)+'\n')
    file.write('TIME_TO_RECONNECT:'+str(TIME_TO_RECONNECT)+'\n')
    file.write('FORBIDENS:'+str(FORBIDENS)+'\n')
    file.write('PATHS:'+str(PATHS)+'\n')
    file.write('AUDIO:'+str(AUDIO)+'\n')
    file.close()


last_played = [[None,0]]
#Play sound (.mp3)
#@profile
def play(arg=11): #11 = silence, 12 = ding
    global last_played
    if not AUDIO:
        return
    if type(arg) == type(sound_bu):
        ct = time.time()
        if  ct - last_played[-1][1] < 5:
            return
        elif ct - last_played[-1][1] > 10:
            last_played = [[None,0]]
        if arg not in [x for x,y in last_played]:
            last_played.append([arg,ct])
            mixer.music.load(arg)
            mixer.music.play()
            if arg == sound_du:
                mixer.music.load(sound_du)
                mixer.music.play()
    else:
        for sound in dico_sound.keys():
            if sound == 'sound_'+str(arg):
                mixer.music.load(dico_sound[sound])
                mixer.music.play()
                break

#@profile
###########VARIABLES PERSONNELLES
def check_users_variables():
    global KEY_CODE, MOUSE_CODE, IDLE, VALIDATING_DURATION, TIME_TO_RECONNECT, FORBIDENS, PATHS, AUDIO, CHECK_RECONNECT
    try:
        file = open(PATH+'\\parameters.txt','r',encoding='utf-8')
        txt = file.readlines()
        file.close()
        key_code = [x.lower() for x in txt[0][len('KEY_CODE:'):].split("'") if len(x) > 2 ]
        key_code = list(set(key_code))
        KEY_CODE = [x if x in keys else threading.Thread(target=play, args=(sound_ky,)).start() for x in key_code]
        mouse_code = [x.lower() for x in txt[1][len('MOUSE_CODE:'):].split("'") if len(x) > 2]
        MOUSE_CODE = [x if x in buttons else threading.Thread(target=play, args=(sound_bt,)).start() for x in mouse_code]
        IDLE = int(txt[2][len('IDLE:'):])
        VALIDATING_DURATION = int(txt[3][len('VALIDATING_DURATION:'):])
        CHECK_RECONNECT = int(txt[4][len('CHECK_RECONNECT:'):])   
        TIME_TO_RECONNECT = int(txt[5][len('TIME_TO_RECONNECT:'):])
        FORBIDENS = [x for x in txt[6][len('FORBIDENS:'):].split("'") if len(x)>2]
        if IDLE < 10 or VALIDATING_DURATION < 5 or TIME_TO_RECONNECT < 3:
            threading.Thread(target=play, args=(sound_du,)).start()
            default_users_variables()
            return
        paths = [x for x in txt[7][len('PATHS:'):].split("'") if len(x)>2]
        PATHS = []
        for x in paths:
            try:
                x = os.path.expanduser(x)
            except:
                pass
            if os.path.exists(x):
                PATHS.append(x)
            else:
                threading.Thread(target=play, args=(sound_pt,)).start()
        AUDIO = int(txt[8][len('AUDIO:'):])
    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = str(traceback.TracebackException(exc_type, exc_value, exc_tb))+' (line : '+str(exc_tb.tb_lineno)+')'
        print(str(tb),exc_tb.tb_lineno)
        threading.Thread(target=play, args=(sound_reinit,)).start()
        default_users_variables()

if os.path.exists(PATH+'\\parameters.txt'):
    check_users_variables()
else:
    default_users_variables()

###########VARIABLE SYSTEM DEPENDING USERS
nb1 = len(MOUSE_CODE)
nb2 = nb1-1

#Monitoring mouse click
#@profile
def on_click(x, y, button, pressed):
    global buttons_pressed, timers, TIMER, started, counter, IS_OK, exited, key_coded
    try:
        if key_coded:
            if pressed:
                ct = time.time()
                buttons_pressed.append(button.name)
                timers.append(ct)
                if buttons_pressed == MOUSE_CODE:
                    if timers[-1]-timers[-nb1] < TIME_TO_RECONNECT:
                        counter = -1
                        TIMER = ct
                        started = False
                        exited = False
                        key_coded = False
                        IS_OK = True
                        threading.Thread(target=play, args=(12,)).start()
                elif buttons_pressed != MOUSE_CODE[:len(buttons_pressed)]:
                    buttons_pressed = []
                    timers = []
                    key_coded = False
    except:
        pass

#Monitoring key press
#@profile
def on_press(key):
    global key_coded, keys_pressed
    try:
        if key.name not in keys_pressed:
            keys_pressed.append(key.name)
        if set(keys_pressed) == set(KEY_CODE):
            key_coded = True
        elif not all(item in KEY_CODE for item in keys_pressed):
            keys_pressed = []
            key_coded = False
    except:
        key_coded = False
        keys_pressed = []
        pass

#Monitoring key release
#@profile
def on_release(key):
    global key_coded, keys_pressed, buttons_pressed, timers
    key_coded = False
    keys_pressed = []
    buttons_pressed = []
    timers = []

def kill_process(hwnd,title):
    try:
        threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
        os.kill(pid,9)
    except:
        pass

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

#Get IDLE Duration
#@profile
def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

#Check service title in foregroung
#@profile
def check_foreground():
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)

    if not title:
        return

    if any(item in title.lower() for item in FORBIDENS):
        threading.Thread(target=kill_process, args=(hwnd,title,)).start()    
        windll.user32.LockWorkStation()

    for path in PATHS:
        for p, subdirs, files in os.walk(os.path.expanduser(path)):
            if any(item.lower() in title.lower() for item in files+subdirs):
                threading.Thread(target=kill_process, args=(hwnd,title,)).start()    
                windll.user32.LockWorkStation()

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

#Check services at exited
#@profile
def all_services():
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:  
        if not i[1]:
            continue
        else:
            hwnd = i[0]
            title = i[1]

        if any(item in title.lower() for item in FORBIDENS):
            threading.Thread(target=kill_process, args=(hwnd,title,)).start()

        for path in PATHS:
            for p, subdirs, files in os.walk(os.path.expanduser(path)):
                if any(item.lower() in title.lower() for item in files+subdirs):
                    threading.Thread(target=kill_process, args=(hwnd,title,)).start()    

#Countdown Vocal
#@profile
def countdown():
    global counter, IS_OK
    #st = time.time()
    while True:    
        if counter > -1:
            threading.Thread(target=play, args=(counter,)).start()
            counter-=1
            if counter == -1:
                IS_OK = False
        time.sleep(1)

#Check if login/logout
#@profile
def isLocked():
    global UNLOCKED_TIME, locked, exited
    while True:
        if not locked:
            if "logonui.exe" in str(subprocess.Popen('tasklist /FI "IMAGENAME eq LogonUI.exe"',\
                            stdin=subprocess.PIPE, \
                            stderr=subprocess.PIPE, \
                            stdout=subprocess.PIPE, \
                            shell=True).communicate()[0].lower()):
                locked = True
                
        if locked:
            if "logonui.exe" not in str(subprocess.Popen('tasklist /FI "IMAGENAME eq LogonUI.exe"',\
                            stdin=subprocess.PIPE, \
                            stderr=subprocess.PIPE, \
                            stdout=subprocess.PIPE, \
                            shell=True).communicate()[0].lower()):
                locked = False
                exited = True
                UNLOCKED_TIME = time.time()

        time.sleep(0.5)

#Init monitoring mouse
#@profile
def monitoring_mouse():
    # Collect events until released
    with Listener(on_click=on_click) as listener:
        listener.join()

#Init monitoring keyboard
#@profile
def monitoring_keyboard():
    # Collect events until released
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listenner:
        listenner.join()

threading.Thread(target=countdown).start()
threading.Thread(target=isLocked).start()
threading.Thread(target=monitoring_mouse).start()
threading.Thread(target=monitoring_keyboard).start()

cleared = False
while True:
    ct = time.time()

    if not locked:
        #Start countdown
        if TIMER is not None and not started:
            if (ct  - TIMER) > VALIDATING_DURATION:
                started = True
                counter = min(VALIDATING_DURATION,10)

        #Check IDLE
        if (ct - TIME) >0.8:
            TIME=ct
            if get_idle_duration() > IDLE:
                windll.user32.LockWorkStation()
            check_users_variables()

        #Check Services
        if not IS_OK:
            threading.Thread(target=check_foreground).start()

        #Check CODE after LOCKED
        if exited:
            cleared = False
            if CHECK_RECONNECT:
                if (ct - UNLOCKED_TIME) > TIME_TO_RECONNECT:
                    windll.user32.LockWorkStation()
            else:
                UNLOCKED_TIME = time.time()*2

    if locked:
        if not cleared:
            threading.Thread(target=all_services).start()
            cleared = True
    
    time.sleep(0.05)

