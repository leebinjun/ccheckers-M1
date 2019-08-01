[![CircleCI](https://circleci.com/gh/luismesas/pydobot.svg?style=svg)](https://circleci.com/gh/luismesas/pydobot)

Python library for Dobot Magician
===

Based on Communication Protocol V1.0.4 (_latest version [here](http://dobot.cc/download-center/dobot-magician.html)_)


Installation
---

```
pip install pydobot
```

Samples
---

```python
import time
from glob import glob

from pydobot import Dobot

available_ports = glob('/dev/cu*usb*')  # mask for OSX Dobot port
if len(available_ports) == 0:
    print('no port found for Dobot Magician')
    exit(1)

device = Dobot(port=available_ports[0])

time.sleep(0.5)
device.speed(100)
device.go(250.0, 0.0, 25.0)
device.speed(10)
device.go(250.0, 0.0, 0.0)
time.sleep(2)
device.close()

```


bug
****************************************************************************get new move.
*************************************mouse_pos: (568, 200)
Traceback (most recent call last):
  File "c:/Users/SadAngel/Desktop/myworkplace/ChineseCheckers_Game_AI-master/main.py", line 158, in <module>
    game_intro()
  File "c:/Users/SadAngel/Desktop/myworkplace/ChineseCheckers_Game_AI-master/main.py", line 79, in game_intro
    button("Start", 250, 350, 100, 50, light_red, red, "Start")
  File "c:/Users/SadAngel/Desktop/myworkplace/ChineseCheckers_Game_AI-master/main.py", line 53, in button
    game_loop()
  File "c:/Users/SadAngel/Desktop/myworkplace/ChineseCheckers_Game_AI-master/main.py", line 125, in game_loop
    if get_pos_states(i) == 1:
  File "c:\Users\SadAngel\Desktop\myworkplace\ChineseCheckers_Game_AI-master\vision.py", line 70, in get_pos_states
    x_t, y_t = pos_to_id(x, y)
TypeError: 'NoneType' object is not iterable