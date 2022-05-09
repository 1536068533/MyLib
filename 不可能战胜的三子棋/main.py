import pygame
from game import *


def first_choice(windows, pos):
    # 检测玩家选择自己先手还是AI先手
    if 87 <= pos[0] <= 686 and 264 <= pos[1] <= 344:
        background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
        background = pygame.transform.scale(background_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
        windows.blit(background, (0, 0))  # 渲染游戏背景图
        pygame.display.update()  # 刷新游戏画面
        return 'AI'
    if 142 <= pos[0] <= 606 and 446 <= pos[1] <= 523:
        background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
        background = pygame.transform.scale(background_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
        windows.blit(background, (0, 0))  # 渲染游戏背景图
        pygame.display.update()  # 刷新游戏画面
        return 'human'
    return 0


if __name__ == '__main__':
    pygame.init()  # 加载模块
    windows = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # 设置游戏窗口大小
    pygame.display.set_caption('不可能战胜的三子棋')  # 设置游戏标题

    xmb_image = pygame.image.load('images/主界面.png')  # 加载游戏背景图
    xmb = pygame.transform.scale(xmb_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
    windows.blit(xmb, (0, 0))  # 渲染游戏主界面
    pygame.display.flip()  # 首次刷新游戏画面

    '''先获取先手信息'''
    first = 0  # 先手信息（AI或human），初始为0
    while first == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:  # 鼠标键弹起时进来
                first = first_choice(windows, event.pos)  # 获取先手信息
                if first:
                    break  # 判断内容非0则说明获取到了先手信息，跳出循环
    limit_first = 1  # 限制次数为1的参数，初值为1

    '''如果玩家选择自己先手，则请求AI先手'''
    if first =='human':
        while True:
            for i in range(20):
                for event in pygame.event.get():#保证随时能退出
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                time.sleep(0.05)
                gif_image = pygame.image.load('gif/不要/' + str(i) + '.jpg')  # 加载'不要'gif图
                gif = pygame.transform.scale(gif_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
                windows.blit(gif, (0, 0))
                pygame.display.update()

    '''游戏开始'''
    while True:
        if first == 'AI' and limit_first:  # 当先手是AI并且第一颗棋子还没下的时候进来
            AI_aggressive(windows)
            limit_first = 0  # 第一颗棋子已下，赋值为0即上锁，下次循环不能进来了
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (player(windows, event.pos)) and len(all_record) != 9:  # 保证玩家落子之后且棋盘还有空缺位置才到AI落子
                    # 注意：all_record是game.py中的参数
                    if first == 'AI':  # 如果是AI先手，用进攻性算法下棋
                        AI_aggressive(windows)
                    else:  # 如果是玩家先手，用偏防守性下棋
                        AI(windows)
