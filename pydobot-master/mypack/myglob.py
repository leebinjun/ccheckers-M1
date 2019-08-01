board_list = [(246, -124.0), (237, -108.5), (255, -108.5), (228, -93.0), (246, -93.0), (264, -93.0), (219, -77.5), (237, -77.5), (255, -77.5), (273, -77.5), (138, -62.0), (156, -62.0), (174, -62.0), (192, -62.0), (210, -62.0), (228, -62.0), (246, -62.0), (264, -62.0), (282, -62.0), (300, -62.0), (318, -62.0), (336, -62.0), (354, -62.0), (147, -46.5), (165, -46.5), (183, -46.5), (201, -46.5), (219, -46.5), (237, -46.5), (255, -46.5), (273, -46.5), (291, -46.5), (309, -46.5), (327, -46.5), (345, -46.5), (156, -31.0), (174, -31.0), (192, -31.0), (210, -31.0), (228, -31.0), (246, -31.0), (264, -31.0), (282, -31.0), (300, -31.0), (318, -31.0), (336, -31.0), (165, -15.5), (183, -15.5), (201, -15.5), (219, -15.5), (237, -15.5), (255, -15.5), (273, -15.5), (291, -15.5), (309, -15.5), (327, -15.5), (174, 0.0), (192, 0.0), (210, 0.0), (228, 0.0), (246, 0.0), (264, 0.0), (282, 0.0), (300, 0.0), (318, 0.0), (165, 15.5), (183, 15.5), (201, 15.5), (219, 15.5), (237, 15.5), (255, 15.5), (273, 15.5), (291, 15.5), (309, 15.5), (327, 15.5), (156, 31.0), (174, 31.0), (192, 31.0), (210, 31.0), (228, 31.0), (246, 31.0), (264, 31.0), (282, 31.0), (300, 31.0), (318, 31.0), (336, 31.0), (147, 46.5), (165, 46.5), (183, 46.5), (201, 46.5), (219, 46.5), (237, 46.5), (255, 46.5), (273, 46.5), (291, 46.5), (309, 46.5), (327, 46.5), (345, 46.5), (138, 62.0), (156, 62.0), (174, 62.0), (192, 62.0), (210, 62.0), (228, 62.0), (246, 62.0), (264, 62.0), (282, 62.0), (300, 62.0), (318, 62.0), (336, 62.0), (354, 62.0), (219, 77.5), (237, 77.5), (255, 77.5), (273, 77.5), (228, 93.0), (246, 93.0), (264, 93.0), (237, 108.5), (255, 108.5), (246, 124.0)]

'''
#初始化全部棋盘
def init_board_list_M1():
# 运动范围 
# x  155 - 350
#  174 +18 +18 +18  246 +18 +18 300 318
# y  
#  15.5  31  +15.5  62 +15.5  93 +15.5  124
    board_list = []

    dd_x = 9
    dd_a = 246
    dd_y = 15.5

    for i in range(0, 4):
        for j in range(i+1):
            board_list.append((dd_a - dd_x * i + 2 * dd_x * j, -124 + dd_y * i))
    for i in range(4, 9):
        for j in range(17-i):
            board_list.append((dd_a - dd_x * (16-i) + 2 * dd_x * j, -124 + dd_y * i))
    for i in range(9, 13):
        for j in range(i+1):
            board_list.append((dd_a - dd_x * i + 2 * dd_x * j, -124 + dd_y * i))
    for i in range(13, 17):
        for j in range(17-i):
            board_list.append((dd_a - dd_x * (16-i) + 2 * dd_x * j, - 124 + dd_y * i))

    return board_list

print(init_board_list_M1())
print(len(init_board_list_M1()))
a = len(init_board_list_M1())
alist = init_board_list_M1()
print(alist[int(a/2)])

'''