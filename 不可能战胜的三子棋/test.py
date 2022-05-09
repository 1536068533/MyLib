import pygame
import time


def gif(window, num, dir):
    for i in range(num):
        time.sleep(0.05)
        gif_image = pygame.image.load('gif/' + dir + '/' + str(i) + '.jpg')  # 加载叉叉图
        window.blit(gif_image, (0, 0))
        pygame.display.update()


pygame.init()
windows = pygame.display.set_mode((800, 800))  # 设置游戏窗口大小


while True:
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #         exit()
    # # gif(windows, 20, '不要')
    for i in range(20):
        for event in pygame.event.get():#保证随时能退出
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        time.sleep(0.05)
        gif_image = pygame.image.load('gif/' + '不要' + '/' + str(i) + '.jpg')  # 加载叉叉图
        windows.blit(gif_image, (0, 0))
        pygame.display.update()
