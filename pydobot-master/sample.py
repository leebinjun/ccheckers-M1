import time
from glob import glob

from pydobot import Dobot


from mypack.myglob import board_list
print(board_list)
# available_ports = glob('com6')  # mask for OSX Dobot port
# print(available_ports)
# if len(available_ports) == 0:
#     print('no port found for Dobot Magician')
#     exit(1)

device = Dobot(port='com6', verbose=False)
time.sleep(0.5)
device.speed(1)
alist = device._get_pose()
print("alist:", alist)
a = 99
device.go(250.0, 0.0, 130.0)

while 1:

    a = input("input act:")

    # 001 move test
    # device.go(250.0, 0.0, 100.0)
    # rsp = device.go(250.0, 0.0, 130.0)
    if int(a) == 1:
        device.speed(1)
        device.go(250.0, 0.0, 100)

    if int(a) == 2:
        device.speed(10)
        device.set_jumpHeight(jumpHeight = 20)
        device.go(250.0, 10.0, 100, mode=0x00)

    if int(a) == 3:
        x = input("input act x:")
        y = input("input act y:")
        z = input("input act z:")
        device.speed(1)
        device.go(int(x), int(y), int(z))

    # 运动范围 
    # x  155 - 350
    #  174 +18 +18 +18  246 +18 +18 300 318
    # y  
    #  15.5  31  +15.5  62 +15.5  93 +15.5  124
    # 
    if int(a) == 4:
        num = input("input act list num:")
        x, y = board_list[int(num)]
        device.speed(1)
        device.go(x, y, 65)


    # 002 suck tese
    # device.foo_suck_1()
    # device.foo_suck_2()
    # device.suck(1)
    # time.sleep(3)
    # device.suck(0)
    if int(a) == 17:
        device.foo_suck_close()

    if int(a) == 18:
        device.foo_suck_open()  


    # device.speed(10)
    # device.go(250.0, 0.0, 0.0)
    # time.sleep(2)
    if int(a) == 999:
        print("break")
        break



device.close()
