import pygame
import random
import os
import time
import datetime

WINDOW_X = 800  # 游戏窗口宽度
WINDOW_Y = 800  # 游戏窗口高度
image_width = 180  # 圆圈和叉叉的宽度
image_high = 180  # 圆圈和叉叉的高度
x, y, r, d = 83, 73, 226, 233  # x，y分别是左上叉叉的初始横坐标和纵坐标，r是从左上到中上的叉叉的距离，d是从左上到左边的叉叉的距离
player_record = set()  # 记录玩家已下棋子的位置
AI_record = set()  # 记录AI已下棋子的位置
all_record = set()  # 记录所有已下棋子的位置

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
                    y + image_high) + d * i and (i, j) not in all_record:
                window.blit(cross, (x + r * j, y + d * i))
                player_record.add((i, j))
                log((i, j), 'x')
                all_record.update(player_record)
                pygame.display.update()  # 刷新游戏画面
                '''
                获胜处理！！！！！！！！！！！！
                '''
                return 1
    return 0


def AI(window):
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
            if count == 2 and choice not in all_record:  # 当该斜线已有两个落子并且有空缺位置
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
            if count == 2 and choice not in all_record:  # 当该斜线已有两个落子并且有空缺位置
                return choice

        for i in range(3):  # 纵横检查判断
            if (i, 0) in record and (i, 1) in record and (i, 2) not in all_record:
                return (i, 2)
            elif (i, 0) in record and (i, 2) in record and (i, 1) not in all_record:
                return (i, 1)
            elif (i, 1) in record and (i, 2) in record and (i, 0) not in all_record:
                return (i, 0)
            elif (0, i) in record and (1, i) in record and (2, i) not in all_record:
                return (2, i)
            elif (0, i) in record and (2, i) in record and (1, i) not in all_record:
                return (1, i)
            elif (1, i) in record and (2, i) in record and (0, i) not in all_record:
                return (0, i)
        return 0

    choice = judge(AI_record)
    if len(player_record) == 1 and (1, 1) not in player_record:  # 当玩家第一颗棋子没有下在中心时，下在中心处
        window.blit(circle, (x + r, y + d))
        AI_record.add((1, 1))
        log((1, 1), 'o')
    elif len(player_record) <= 2 and (1, 1) in player_record:
        # 当玩家第一颗棋子下在中心位置时，AI第一次下随机下在四角中的一个，第二次下检查玩家是否将要连成三子，及时阻止，否则随机下在角落处
        danger = judge(player_record)
        if danger:  # 检查危险，玩家是否将要连成三子，及时阻止
            window.blit(circle, (x + r * danger[1], y + d * danger[0]))
            AI_record.add(danger)
            log(danger, 'o')
        else:
            while True:
                corner = (2 if random.randint(0, 1) == 1 else 0, 2 if random.randint(0, 1) == 1 else 0)
                if corner not in all_record:
                    window.blit(circle, (x + r * corner[1], y + d * corner[0]))
                    AI_record.add(corner)
                    log(danger, 'o')
                    break
    elif choice:  # 当AI快要连成3子时，立即连成三子
        window.blit(circle, (x + r * choice[1], y + d * choice[0]))
        AI_record.add(choice)
        log(choice, 'o')
    elif choice == 0:
        try:
            defend = judge(player_record)  # 当玩家快要连成3子时，及时阻止
            window.blit(circle, (x + r * defend[1], y + d * defend[0]))
            AI_record.add(defend)
            log(defend, 'o')
        except Exception:
            # 利用随机数选择空缺位置落子，假设下一步下这个地方，是否能促进AI将要连成三子
            hypothesis = set()
            hypothesis.update(all_record)
            # hypothesis猜想，随机出来的位置都填入这个集合中
            break_out = 0  # 用于跳出多层循环
            while True:
                m = random.randint(0, 2)
                n = random.randint(0, 2)
                if (m, n) not in hypothesis:
                    hypothesis.add((m, n))
                    if judge(AI_record.union({(m, n)})):  # 假设下一步下这个地方，能促进AI将要连成三子，就下这个地方
                        window.blit(circle, (x + r * n, y + d * m))
                        AI_record.add((m, n))
                        log((m, n), 'o')
                        break
                if len(hypothesis) == 9:
                    # 如果hypothesis集合长度为9
                    # 说明每个可能都试过了，下一步找不到能促进AI将要连成三子的地方，就随机下一个空位置
                    while True:
                        m = random.randint(0, 2)
                        n = random.randint(0, 2)
                        if (m, n) not in all_record:
                            window.blit(circle, (x + r * n, y + d * m))
                            AI_record.add((m, n))
                            log((m, n), 'o')
                            break_out = 1
                            break
                        if len(all_record) == 9:  # 如果all_record集合长度为9说明棋盘已经满了，直接跳出循环
                            break_out = 1
                            break
                if break_out == 1:  # 跳出多层循环
                    break
    all_record.update(AI_record)
    pygame.display.update()  # 刷新游戏画面
    cheer(window, AI_record)  # 调用cheer函数判断是否已获胜


def referee(player_record):
    '''
    裁判函数，判断输赢
    :param player_record: 传入对应的玩家记录集合，判断该玩家是否获胜
    :return: 如果判断出已获胜，返回获胜列表，对应三棋子坐标，如果没有获胜且棋盘还有空缺位置则返回0，如果平局返回-1
    '''
    winner = list()
    for i in range(3):  # 横向扫描判断是否连成三子
        for j in range(3):
            if (i, j) in player_record:
                winner.append((i, j))
            else:
                winner = []
                break
        else:
            return winner

    for i in range(3):
        for j in range(3):
            if (j, i) in player_record:
                winner.append((j, i))
            else:
                winner = []
                break
        else:
            return winner

    for i in range(3):
        if (i, i) in player_record:
            winner.append((i, i))
        else:
            winner = []
            break
    else:
        return winner

    if (2, 0) in player_record and (1, 1) in player_record and (0, 2) in player_record:
        return [(0, 2), (1, 1), (2, 0)]
    if len(all_record) == 9:
        return -1
    return 0


def cheer(window, player_record):
    '''
    通过判断referee返回的类型，如果是列表说明获胜了
    获胜则让连成3子的地方闪烁
    :param window: pygame的游戏窗口对象
    :param player_record: 传入玩家数据，player_record或AI_record集合
    :return: 无
    '''
    result = referee(player_record)
    if type(result) is list:  # 获胜时让连成3子的地方闪烁
        for i in range(3):
            for i in range(3):
                window.blit(circle_disappear, (x + r * result[i][1], y + d * result[i][0]))
            pygame.display.update()  # 刷新游戏画面
            time.sleep(0.2)
            for i in range(3):
                window.blit(circle, (x + r * result[i][1], y + d * result[i][0]))
            pygame.display.update()  # 刷新游戏画面
            time.sleep(0.2)
        for i in range(3):  # 获胜后立即填满all_record集合，防止玩家在获胜后继续点击下棋（画叉叉）
            for j in range(3):
                all_record.add((i, j))


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
