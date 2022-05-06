import pygame

WINDOW_X = 800  # 游戏窗口宽度
WINDOW_Y = 800  # 游戏窗口高度
image_width = 180  # 圆圈和叉叉的宽度
image_high = 180  # 圆圈和叉叉的高度
x, y, r, d = 83, 73, 226, 233  # x，y分别是左上叉叉的初始横坐标和纵坐标，r是从左上到中上的叉叉的距离，d是从左上到左边的叉叉的距离
player_record = set()  # 记录玩家已下棋子的位置
AI_record = set()  # 记录AI已下棋子的位置
all_record = set()  # 记录所有已下棋子的位置

cross_image = pygame.image.load('images/叉叉.png')  # 加载圆圈图
cross = pygame.transform.scale(cross_image, (image_width, image_high))  # 拉伸圆圈图使其适应棋盘的方框
circle_image = pygame.image.load('images/圈圈.png')  # 加载圆圈图
circle = pygame.transform.scale(circle_image, (image_width, image_high))  # 拉伸圆圈图使其适应棋盘的方框


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
                all_record.update(player_record)
                pygame.display.update()  # 刷新游戏画面
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
                danger = i
        else:
            if count == 2 and (danger, danger) not in all_record:  # 当该斜线已有两个落子并且有空缺位置
                window.blit(circle, (x + r * danger, y + d * danger))
                AI_record.add((danger, danger))
                return 1;
        j = 2  # y坐标
        count = 0  # 初始化
        for i in range(3):  # 判断从右上连到左下是否将要连成一线，如果是，就把棋子下在空缺位置
            if (i, j) in record:
                count += 1
            else:
                danger = (i, j)
            j -= 1
        else:
            if count == 2 and danger not in all_record:  # 当该斜线已有两个落子并且有空缺位置
                window.blit(circle, (x + r * danger[1], y + d * danger[0]))
                AI_record.add(danger)
                return 1

        for i in range(3):  # 纵横检查判断
            if (i, 0) in record and (i, 1) in record and (i, 2) not in all_record:
                window.blit(circle, (x + r * 2, y + d * i))
                AI_record.add((i, 2))
                return 1
            elif (i, 0) in record and (i, 2) in record and (i, 1) not in all_record:
                window.blit(circle, (x + r * 1, y + d * i))
                AI_record.add((i, 1))
                return 1
            elif (i, 1) in record and (i, 2) in record and (i, 0) not in all_record:
                window.blit(circle, (x, y + d * i))
                AI_record.add((i, 0))
                return 1
            elif (0, i) in record and (1, i) in record and (2, i) not in all_record:
                window.blit(circle, (x + r * i, y + d * 2))
                AI_record.add((2, i))
                return 1
            elif (0, i) in record and (2, i) in record and (1, i) not in all_record:
                window.blit(circle, (x + r * i, y + d))
                AI_record.add((1, i))
                return 1
            elif (1, i) in record and (2, i) in record and (0, i) not in all_record:
                window.blit(circle, (x + r * i, y))
                AI_record.add((0, i))
                return 1
        return 0

    # 当玩家第一颗棋子没有下在中心时，下在中心处
    if len(player_record) == 1 and (1, 1) not in player_record:
        window.blit(circle, (x + r, y + d))
        AI_record.add((1, 1))

    choice = judge(AI_record)  # 当AI快要连成3子时，立即连成三子

    if choice != 1:
        judge(player_record)  # 当玩家快要连成3子时，及时阻止

    all_record.update(AI_record)
    pygame.display.update()  # 刷新游戏画面


def judge():  # 裁判函数，判断输赢
    pass
