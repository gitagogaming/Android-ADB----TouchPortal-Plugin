
commands = {
    "Turn Off Screen": "input keyevent 223",
    "Turn On Screen": "input keyevent 224",
   # "Power Button Toggle": "input keyevent 26",
    "Swipe to Unlock": "input swipe 300 1000 300 500",   ## start x, end x, start y, end y
    "Input Text": "input text (text here)",
  # "Increase Volume": "input keyevent 24",
  # "Decrease Volume": "input keyevent 25",
  #  "Take Picture": "input keyevent 27",  # input keyevent KEYCODE_CAMERA"
  #  "Toggle Mute Volume": "input keyevent 164",
  #  "Home Key": "input keyevent 3",
  #  "Return Key": "input keyevent 4",
  #  "Menu": "input keyevent 82",
    "Switch Applications": "input keyevent 187",
   # "Calendar": "input keyevent 208" ,
 #  "Reduce Screen Brightness": "input keyevent 220",
 #   "Increase Screen Brightness": "input keyevent 221",
 #   "Voice Assistant": "input keyevent 231",
 #  "Device Model": "getprop ro.product.model",
 #  "Screen Size": "wm size",
 #  "Screen Density": "wm density",
 #   "Android Version": "getprop ro.build.version.release",
    "CPU INFO": "cat /proc/cpuinfo",   ### use func above to pull details needed like processor, 
  #  "MEM INFO": "cat /proc/meminfo",
   # "Screenshot Device": "exec-out screencap -p> sc.png",
    "Pull Image to PC": "screencap -p /sdcard/sc.png",  ##  doesnt quite work?
    "Screen Record Phone": "screenrecord /sdcard/filename.mp4",   ## -- "--bit-rate 2000" "--time-limit 60" "--size 300x300"
    "Reboot Device": "reboot",

}

# X1 = WHERE TO START HORIZTONALLY
# X2 = ACTUALLY Y1 - WHERE TO START VERTICALLY



