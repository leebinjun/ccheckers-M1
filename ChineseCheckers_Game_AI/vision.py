from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
import cv2
import time

import colorsys  

from utils import get_feature


my_board_list = [(480, 40), (458, 80), (502, 80), (436, 120), (480, 120), (524, 120), (414, 160), (458, 160), (502, 160), (546, 160), (392, 200), (436, 200), (480, 200), (524, 200), (568, 200), (370, 240), (414, 240), (458, 240), (502, 240), (546, 240), (590, 240), (348, 280), (392, 280), (436, 280), (480, 280), (524, 280), (568, 280), (612, 280), (326, 320), (370, 320), (414, 320), (458, 320), (502, 320), (546, 320), (590, 320), (634, 320), (304, 360), (348, 360), (392, 360), (436, 360), (480, 360), (524, 360), (568, 360), (612, 360), (656, 360), (326, 400), (370, 400), (414, 400), (458, 400), (502, 400), (546, 400), (590, 400), (634, 400), (348, 440), (392, 440), (436, 440), (480, 440), (524, 440), (568, 440), (612, 440), (370, 480), (414, 480), (458, 480), (502, 480), (546, 480), (590, 480), (392, 520), (436, 520), (480, 520), (524, 520), (568, 520), (414, 560), (458, 560), (502, 560), (546, 560), (436, 600), (480, 600), (524, 600), (458, 640), (502, 640), (480, 680)]

alist_board = [(0, 0), (0, 1), (1, 0), (0, 2), (1, 1), (2, 0), (0, 3), (1, 2), (2, 1), (3, 0), (0, 4), (1, 3), (2, 2), (3, 1), (4, 0), (0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (0, 6), (1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0), (0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0), (0, 8), (1, 7), (2, 6), (3, 5), (4, 4), (5, 3), (6, 2), (7, 1), (8, 0), (1, 8), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1), (2, 8), (3, 7), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (3, 8), (4, 7), (5, 6), (6, 5), (7, 4), (8, 3), (4, 8), (5, 7), (6, 6), (7, 5), (8, 4), (5, 8), (6, 7), (7, 6), (8, 5), (6, 8), (7, 7), (8, 6), (7, 8), (8, 7), (8, 8)]

def pos_to_id(x, y):
    tmp = (x, y)
    if tmp in my_board_list:
        id = my_board_list.index(tmp)
        # print("id", id)
        ret = alist_board[id]
    else:
        ret = None
    # print("ret:", ret)
    return ret

def perTrans(img, points = [(33, 235), (309, 403), (317, 99), (596, 248)]):
    # points: U L D R 4 points
    dst = np.float32([[0,0],[0,399],[399,0],[399,399]])
    src = np.float32(points)
    M = cv2.getPerspectiveTransform(src, dst)
    T = cv2.warpPerspective(img,M,(400,400))
    ROI = np.zeros((400,400,3),np.uint8)
    ROI[0:,0:400] = T
    return ROI

def get_dominant_color(image):  
    max_score = 0.0001  
    dominant_color = (10,10,10)  
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]):  
        # 转为HSV标准  
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]  
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)  
        y = (y-16.0)/(235-16)  
  
        #忽略高亮色  
        if y > 0.9:  
            continue  
        score = (saturation+0.1)*count  
        if score > max_score:  
            max_score = score  
            dominant_color = (r,g,b)  
    return dominant_color



dd = 10
x, y = 50, 50

def get_pos_states(alist):
    global cap

    x, y = alist[0], alist[1]
    # print("x, y:", x, y)
    ret,img = cap.read()
    cv2.imshow("imag",img)
    img_trans = perTrans(img)
    cv2.imshow("perTrans_rst",img_trans)
    
    if pos_to_id(x, y) == None:
        return 0
    # print("get_pos_states:", x, y)
    x_t, y_t = pos_to_id(x, y)
    x_t, y_t = 15+45*x_t, 13+46*y_t
    roi = img_trans[y_t-10:y_t+10, x_t-10:x_t+10, :]

    cv2.imwrite(r"C:\Users\SadAngel\Desktop\myworkplace\test1.jpg", roi) 
    
    img_path = r"C:\Users\SadAngel\Desktop\myworkplace\test1.jpg"
    
    f1, f2, f3, f4, f5 = list(get_feature(img_path))[:5]
    print(f1, f2, f3, f4, f5)

    # 此处应该转格式
    roi = Image.open(r"C:\Users\SadAngel\Desktop\myworkplace\test1.jpg") 

    image = roi.convert('RGB')  
    x, y, z = get_dominant_color(image)
    if x > 150 :
    #x , y , z = hsv_caculate(x,y,z)
    # if x > 170 and (y > 100 or z > 100): 
        print(x, y, z, 'checker')
        # print(alist[0], alist[1])
        result = 'Checker' 
        return 1
    else:
        # print(x, y, z, 'null')
        result = 'Null' 
        return 2
    
    return 0


cap = cv2.VideoCapture(0)
ret,img = cap.read()



def no_hand():
    global cap
    ret,img = cap.read()
    img = perTrans(img)
    cnt = 0
    
    for [x,y] in my_board_list:
        x_t, y_t = pos_to_id(x, y)
        x_t, y_t = 15+45*x_t, 13+46*y_t
        if get_pos_states([x,y]) == 2: #Null
            cv2.circle(img, (x_t,y_t), 10, (0,255,0), 5)
            # plt.scatter(x_t, y_t, c = 'b')
        elif get_pos_states([x,y]) == 1: #Checker
            cv2.circle(img, (x_t,y_t), 10, (255,0,0), 5)
            # plt.scatter(x_t, y_t, c = 'r')
            cnt += 1
    #cv2.imshow("no_hand", img)
    ch = cv2.waitKey(1)
    print("running", cnt)
    if cnt == 10:
        return True
    else:
        return False





if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    ret,img = cap.read()
    while ret is True:
        
        cv2.imshow("imag",img)
        ret, img = cap.read()
        
        ch = cv2.waitKey(5)
        if ch == ord('c') :
            break
        if ch == ord('s') :
            print("save photo")
            cv2.imwrite(r"C:\Users\SadAngel\Desktop\myworkplace\CCAI\Data\origin\test"+str(time.time())+'.jpg', img)
            cv2.imwrite(r"C:\Users\SadAngel\Desktop\myworkplace\CCAI\Data\origin\test"+str(time.time())+'.jpg', img_trans)

        # vision test
        if ch == ord('t') :
            for i in my_board_list[:10]:
                print(get_pos_states(i))


    cv2.destroyAllWindows()









