from game_test import *

if __name__ == '__main__':
    pygame.init()  # 加载模块
    windows = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # 设置游戏窗口大小
    pygame.display.set_caption('不可能战胜的三子棋')  # 设置游戏标题
    background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
    background = pygame.transform.scale(background_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
    windows.blit(background, (0, 0))  # 渲染游戏背景图
    circle_image = pygame.image.load('images/圈圈.png')  # 加载圆圈图
    circle = pygame.transform.scale(circle_image, (180, 180))  # 拉伸圆圈图使其适应棋盘的方框

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (player(windows, event.pos)) and len(all_record) != 9:  # 保证玩家落子之后且棋盘还有空缺位置才到AI落子
                    # 注意：all_record是game.py中的参数
                    AI(windows)
