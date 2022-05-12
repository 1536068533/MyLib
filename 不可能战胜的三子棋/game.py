import pygame
import random
import os
import time
import datetime
import re
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from common import *
from sprite import *

WINDOW_X = 800  # 游戏窗口宽度
WINDOW_Y = 800  # 游戏窗口高度
image_width = 180  # 圆圈和叉叉的宽度
image_high = 180  # 圆圈和叉叉的高度
x, y, r, d = 83, 73, 226, 233  # x，y分别是左上叉叉的初始横坐标和纵坐标，r是从左上到中上的叉叉的距离，d是从左上到左边的叉叉的距离

cross_image = pygame.image.load('images/叉叉.png')  # 加载叉叉图
cross = pygame.transform.scale(cross_image, (image_width, image_high))  # 拉伸叉叉图使其适应棋盘的方框
circle_image = pygame.image.load('images/圈圈.png')  # 加载圆圈图
circle = pygame.transform.scale(circle_image, (image_width, image_high))  # 拉伸圆圈图使其适应棋盘的方框
cross_disappear_image = pygame.image.load('images/叉叉消失.png')  # 加载叉叉消失图
cross_disappear = pygame.transform.scale(cross_disappear_image, (image_width, image_high))  # 拉伸叉叉消失图使其适应棋盘的方框
circle_disappear_image = pygame.image.load('images/圈圈消失.png')  # 加载圆圈消失图
circle_disappear = pygame.transform.scale(circle_disappear_image, (image_width, image_high))  # 拉伸圆圈消失图使其适应棋盘的方框

pwd = os.path.dirname(__file__)
log_file = os.path.join(pwd, 'log.txt')  # 日志文件绝对路径
with open(log_file, mode='w', encoding='utf-8') as stream:  # 清空日志，并在第一行写上开始游戏的时间
    stream.write("游戏开始时间：" + datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒') + "\n")
    stream.write("'o'表示AI，'x'表示玩家\n")
coord = [[' ' for j in range(3)] for i in range(3)]  # coord初始化，coord和log函数中的status变量配合使用，用于打印到log文件中


def initialization_log():
    '''
    日志初始化函数，用于将这里的日志初始化
    :return: 无
    '''
    coord = [[' ' for j in range(3)] for i in range(3)]  # coord初始化，coord和log函数中的status变量配合使用，用于打印到log文件中
    '''日志初始化'''
    with open(log_file, mode='w', encoding='utf-8') as stream:  # 清空日志，并在第一行写上开始游戏的时间
        stream.write("游戏开始时间：" + datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒') + "\n")
        stream.write("'o'表示AI，'x'表示玩家\n")


def player(window, pos):
    '''
    传入一个对象和坐标，在对应的格子中渲染上叉叉的图片
    :param window: pygame的游戏窗口对象
    :param pos: 坐标
    :return: 玩家已落子返回1，玩家点击位置不在判断范围中返回0
    '''
    for i in range(3):
        for j in range(3):  # 为传入的坐标参数，利用循环判断出叉叉应该出现的位置
            if x + r * j <= pos[0] <= (x + image_width) + r * j and y + d * i <= pos[1] <= (
                    y + image_high) + d * i and (i, j) not in get_all_record():
                window.blit(cross, (x + r * j, y + d * i))
                add_player_record((i, j))
                log((i, j), 'x')
                union_all_record()
                pygame.display.update()  # 刷新游戏画面
                cheer(window, cross, cross_disappear, get_player_record())  # 调用cheer函数判断是否已获胜
                return 1
    return 0


def AI(window):
    '''
    玩家先手时调用的函数，打法先抢中心点，抢不到优先防守，随后在防守中寻求进攻机会
    :param window: pygame的窗口对象
    :return: 无
    '''

    def judge(record):
        '''
        根据传入的集合，判断应该在哪落子，尽可能取得胜利
        :param record: 传AI_record则判断是否将要取得胜利，传player_record则判断如何阻止玩家取胜
        :return: 如果落子了返回1，否则返回0
        '''
        # 判断斜线是否将要连成一线，如果是，下在空缺位置
        count = 0
        for i in range(3):  # 判断从左上连到右下是否将要连成一线，如果是，就把棋子下在空缺位置
            if (i, i) in record:
                count += 1
            else:
                choice = (i, i)
        else:
            if count == 2 and choice not in get_all_record():  # 当该斜线已有两个落子并且有空缺位置
                return choice;
        j = 2  # y坐标
        count = 0  # 初始化
        for i in range(3):  # 判断从右上连到左下是否将要连成一线，如果是，就把棋子下在空缺位置
            if (i, j) in record:
                count += 1
            else:
                choice = (i, j)
            j -= 1
        else:
            if count == 2 and choice not in get_all_record():  # 当该斜线已有两个落子并且有空缺位置
                return choice

        for i in range(3):  # 纵横检查判断
            if (i, 0) in record and (i, 1) in record and (i, 2) not in get_all_record():
                return (i, 2)
            elif (i, 0) in record and (i, 2) in record and (i, 1) not in get_all_record():
                return (i, 1)
            elif (i, 1) in record and (i, 2) in record and (i, 0) not in get_all_record():
                return (i, 0)
            elif (0, i) in record and (1, i) in record and (2, i) not in get_all_record():
                return (2, i)
            elif (0, i) in record and (2, i) in record and (1, i) not in get_all_record():
                return (1, i)
            elif (1, i) in record and (2, i) in record and (0, i) not in get_all_record():
                return (0, i)
        return 0

    choice = judge(get_AI_record())
    if len(get_player_record()) == 1 and (1, 1) not in get_player_record():  # 当AI先手或玩家第一颗棋子没有下在中心时，下在中心处
        window.blit(circle, (x + r, y + d))
        add_AI_record((1, 1))
        log((1, 1), 'o')
    elif len(get_player_record()) <= 2 and (1, 1) in get_player_record():
        # 当玩家第一颗棋子下在中心位置时，AI第一次下随机下在四角中的一个，第二次下检查玩家是否将要连成三子，及时阻止，否则随机下在角落处
        danger = judge(get_player_record())
        if danger:  # 检查危险，玩家是否将要连成三子，及时阻止
            window.blit(circle, (x + r * danger[1], y + d * danger[0]))
            add_AI_record(danger)
            log(danger, 'o')
        else:
            while True:
                corner = (2 if random.randint(0, 1) == 1 else 0, 2 if random.randint(0, 1) == 1 else 0)
                if corner not in get_all_record():
                    window.blit(circle, (x + r * corner[1], y + d * corner[0]))
                    add_AI_record(corner)
                    log(corner, 'o')
                    break
    elif choice:  # 当AI快要连成3子时，立即连成三子
        window.blit(circle, (x + r * choice[1], y + d * choice[0]))
        add_AI_record(choice)
        log(choice, 'o')
    elif choice == 0:
        try:
            defend = judge(get_player_record())  # 当玩家快要连成3子时，及时阻止
            window.blit(circle, (x + r * defend[1], y + d * defend[0]))
            add_AI_record(defend)
            log(defend, 'o')
        except Exception:
            # 利用随机数选择空缺位置落子，假设下一步下这个地方，是否能促进AI将要连成三子
            hypothesis = set()
            hypothesis.update(get_all_record())
            # hypothesis猜想，随机出来的位置都填入这个集合中
            break_out = 0  # 用于跳出多层循环
            while True:
                m = random.randint(0, 2)
                n = random.randint(0, 2)
                if (m, n) not in hypothesis:
                    hypothesis.add((m, n))
                    if judge(get_AI_record().union({(m, n)})):  # 假设下一步下这个地方，能促进AI将要连成三子，就下这个地方
                        window.blit(circle, (x + r * n, y + d * m))
                        add_AI_record((m, n))
                        log((m, n), 'o')
                        break
                if len(hypothesis) == 9:
                    # 如果hypothesis集合长度为9
                    # 说明每个可能都试过了，下一步找不到能促进AI将要连成三子的地方，就随机下一个空位置
                    while True:
                        m = random.randint(0, 2)
                        n = random.randint(0, 2)
                        if (m, n) not in get_all_record():
                            window.blit(circle, (x + r * n, y + d * m))
                            add_AI_record((m, n))
                            log((m, n), 'o')
                            break_out = 1
                            break
                        if len(get_all_record()) == 9:  # 如果all_record集合长度为9说明棋盘已经满了，直接跳出循环
                            break_out = 1
                            break
                if break_out == 1:  # 跳出多层循环
                    break
    union_all_record()
    pygame.display.update()  # 刷新游戏画面
    cheer(window, circle, circle_disappear, get_AI_record())  # 调用cheer函数判断是否已获胜


def AI_aggressive(window):
    '''
    当AI先手时，调用这个函数，开局进攻性较强，之后的战略和AI函数相同
    :param window: pygame的窗口对象
    :return: 无
    '''
    if len(get_all_record()) == 0:  # 第一颗棋先下在中心
        window.blit(circle, (x + r, y + d))
        add_AI_record((1, 1))
        log((1, 1), 'o')
    elif len(get_player_record()) == 1:  # 当玩家下了第一颗棋的时候
        player_pos = pop_player_record()  # 删除元素时会返回该元素，利用这点获取集合中唯一一个元素
        if player_pos in {(0, 0), (0, 2), (2, 0), (2, 2)}:  # 如果玩家第一颗棋下在角落，则AI下在其对角
            choice = (player_pos[0] ^ 2, player_pos[1] ^ 2)  # 按位异或，让0变2,2变0
            window.blit(circle, (x + r * choice[1], y + d * choice[0]))
            add_AI_record(choice)
            log(choice, 'o')
        else:  # 如果玩家第一颗棋下在上或下或左或右
            pos_choice = [0, 2]  # 让m、n只能随机到0或2
            m = pos_choice[random.randint(0, 1)]
            n = pos_choice[random.randint(0, 1)]
            window.blit(circle, (x + r * n, y + d * m))
            add_AI_record((m, n))
            log((m, n), 'o')
        add_player_record(player_pos)  # 把刚刚删除的元素放回去
    else:
        AI(window)  # 之后的战略和AI函数相同

    union_all_record()
    pygame.display.update()  # 刷新游戏画面


def referee(record):
    '''
    裁判函数，判断输赢
    :param record: 传入对应的玩家记录集合，判断该玩家是否获胜
    :return: 如果判断出已获胜，返回获胜列表，对应三棋子坐标，如果没有获胜且棋盘还有空缺位置则返回0，如果平局返回-1
    '''
    winner = list()
    for i in range(3):  # 横向扫描判断是否连成三子
        for j in range(3):
            if (i, j) in record:
                winner.append((i, j))
            else:
                winner = []
                break
        else:
            return winner

    for i in range(3):
        for j in range(3):
            if (j, i) in record:
                winner.append((j, i))
            else:
                winner = []
                break
        else:
            return winner

    for i in range(3):
        if (i, i) in record:
            winner.append((i, i))
        else:
            winner = []
            break
    else:
        return winner

    if (2, 0) in record and (1, 1) in record and (0, 2) in record:
        return [(0, 2), (1, 1), (2, 0)]
    if len(get_all_record()) == 9:
        return -1
    return 0


def generalduty_gif(window, pwd, frames, cycle_index=1):
    '''
    通用的gif函数
    :param window: pygame的游戏窗口对象
    :param pwd: 存放gif的目录
    :param frames: 每秒帧数
    :param cycle_index:循环次数，默认gif只循环1次
    :return: 无
    '''
    file_list = os.listdir(pwd)  # 搜索pwd目录下的所有文件名并保存为列表
    try:
        file_type = re.search(r'.\w+$', file_list[0]).group()  # 如果search没匹配到结果返回None，None.group()就会报错
    except Exception as err:
        print(err)
        print("gif目录中没有搜索到符合正则表达式的结果\n请检查存放gif素材的目录，或检查代码中的generalduty_gif函数")
    clock = pygame.time.Clock()  # 游戏时钟对象
    for i in range(cycle_index):
        for j in range(len(file_list)):
            clock.tick(frames)  # 每秒运行帧数
            gif_image = pygame.image.load(pwd + str(j) + file_type)
            gif = pygame.transform.scale(gif_image, (WINDOW_X, WINDOW_Y))
            window.blit(gif, (0, 0))
            get_sound_button().update(window, get_sound_status())  # 刷新音量按钮
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 保证在gif循环里也能随时退出
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    get_mouse().update()  # 刷新鼠标精灵位置
                    if pygame.sprite.collide_mask(get_sound_button(), get_mouse()):  # 判断是否在设置音量
                        if get_sound_status():
                            set_sound_status(0)
                        else:
                            set_sound_status(1)


def happy_gif(window):
    '''
    加载表达开心的gif，并且可以随时开关背景音乐和关闭游戏窗口
    :param window: pygame的游戏窗口对象
    :return: 无
    '''
    clock = pygame.time.Clock()  # 游戏时钟对象
    for m in range(3):
        for n in range(27):
            clock.tick(30)  # 每秒运行30帧
            happy_image = pygame.image.load('gif/开心/' + str(n) + '.jpg')  # 加载'开心'gif图
            happy = pygame.transform.scale(happy_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
            window.blit(happy, (0, 0))
            happy_txt = pygame.image.load('images/嘻嘻嘻.PNG')
            happy_txt_size = happy_txt.get_size()
            window.blit(happy_txt, (WINDOW_X / 2 - happy_txt_size[0] / 2, WINDOW_Y * 0.75))
            get_sound_button().update(window, get_sound_status())  # 刷新音量按钮
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 保证在gif循环里也能随时退出
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    get_mouse().update()  # 刷新鼠标精灵位置
                    if pygame.sprite.collide_mask(get_sound_button(), get_mouse()):  # 判断是否在设置音量
                        if get_sound_status():
                            set_sound_status(0)
                        else:
                            set_sound_status(1)


def daze_gif(window):
    '''
    加载表达面容呆滞的gif，并且可以随时开关背景音乐和关闭游戏窗口
    :param window: pygame的游戏窗口对象
    :return: 无
    '''
    clock = pygame.time.Clock()  # 游戏时钟对象
    for m in range(10):
        for n in range(5):
            clock.tick(20)  # 每秒运行20帧
            daze_image = pygame.image.load('gif/呆/' + str(n) + '.png')  # 加载'呆'gif图
            daze = pygame.transform.scale(daze_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
            window.blit(daze, (0, 0))
            tie_txt = pygame.image.load('images/平局.PNG')
            window.blit(tie_txt, (WINDOW_X * 0.8, WINDOW_Y * 0.3))
            get_sound_button().update(window, get_sound_status())  # 刷新音量按钮
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 保证在gif循环里也能随时退出
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    get_mouse().update()  # 刷新鼠标精灵位置
                    if pygame.sprite.collide_mask(get_sound_button(), get_mouse()):  # 判断是否在设置音量
                        if get_sound_status():
                            set_sound_status(0)
                        else:
                            set_sound_status(1)


def cheer(window, image, image_disappear, player):
    '''
    胜利欢呼函数
    通过判断referee返回的类型，如果是列表说明获胜了
    获胜则让连成3子的地方闪烁
    :param window: pygame的游戏窗口对象
    :param player: 传入玩家棋局数据，player_record或AI_record集合
    :return: 无
    '''
    result = referee(player)  # 获胜返回列表，对应三棋子坐标，没获胜且棋盘还有空缺位置则返回0，如果平局返回-1
    if type(result) is list:  # 获胜时让连成3子的地方闪烁
        for i in range(3):
            for i in range(3):
                window.blit(image_disappear, (x + r * result[i][1], y + d * result[i][0]))
            pygame.display.update()  # 刷新游戏画面
            time.sleep(0.2)
            for i in range(3):
                window.blit(image, (x + r * result[i][1], y + d * result[i][0]))
            pygame.display.update()  # 刷新游戏画面
            time.sleep(0.2)
        for i in range(3):  # 获胜后立即填满all_record，防止玩家在获胜后继续点击下棋（画叉叉）
            for j in range(3):
                add_all_record((i, j))
        if player == get_player_record():  # 如果胜利的是玩家
            incredible()  # 调用该函数处理玩家胜利的情况，incredible不可思议的，难以置信的
        elif player == get_AI_record():  # 如果胜利的是AI，加载获胜gif
            happy_gif(window)
    elif result == -1:  # 平局时处理
        daze_gif(window)


def log(pos, mark):
    '''
    游戏日志，记录游戏过程，万一玩家取胜了，就另存一份文件保存以供开发者调试
    :param pos: 传入坐标
    :param mark: 传入记号，如果是玩家则传'x'，如果是AI则传'o'
    :return: 无
    '''
    coord[pos[0]][pos[1]] = mark
    status = '  ' + coord[0][0] + ' ' + '|' + ' ' + coord[0][1] + ' ' + '|' + ' ' + coord[0][2] + ' \n' \
             + '  ' + coord[1][0] + ' ' + '|' + ' ' + coord[1][1] + ' ' + '|' + ' ' + coord[1][2] + ' \n' \
             + '  ' + coord[2][0] + ' ' + '|' + ' ' + coord[2][1] + ' ' + '|' + ' ' + coord[2][2] + ' \n'
    with open(log_file, mode='a', encoding='utf-8') as stream:  # 在日志上追加内容，打印当前棋局状态到日志中
        stream.write(status + '\n')


def incredible():
    '''
    玩家胜利后的处理函数，把游戏日志拷贝一份并以游戏胜利时的时间为名保存在同级目录中
    利用tkinter弹出窗口请求玩家将游戏过程（同级目录中以游戏胜利时的日期时间为名的文件）反馈给开发者
    :return: 无
    '''
    #
    player_win_log = os.path.join(pwd, datetime.datetime.now().strftime('%Y年%m月%d日%H时%M分%S秒') + '.txt')
    os.system('copy' + ' ' + log_file + ' ' + player_win_log)
    '''利用tkinter弹出窗口请求玩家将游戏过程反馈给开发者'''

    def update(idx):
        frame = frames[idx]
        idx += 1
        label.configure(image=frame)
        winner_window.after(duration, update, idx % numIdx)

    winner_window = Tk()  # 创建一个主窗口对象
    winner_window.geometry("800x525+300+150")
    winner_window.title('居然让你赢了，颁个奖给你吧！')
    winner_window.configure(bg='white')  # 设置背景色
    '''图片'''
    photo01 = PhotoImage(file="images/文字.gif")  # PhotoImage只能读取gif格式
    imLabel01 = Label(winner_window, image=photo01)
    imLabel01.pack()
    photo02 = PhotoImage(file="images/反馈.gif")  # PhotoImage只能读取gif格式
    imLabel02 = Label(winner_window, image=photo02)
    imLabel02.pack()
    '''gif'''
    im = Image.open('images/人才.gif')  # PIL库加载 gif文件名
    duration = im.info['duration']  # 帧速
    frames = [ImageTk.PhotoImage(m) for m in ImageSequence.Iterator(im)]  # 加载gif帧序列
    numIdx = len(frames)  # gif的帧数
    winner_window.after(0, update, 0)
    label = Label(winner_window)
    label.pack()

    winner_window.mainloop()
