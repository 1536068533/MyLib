from game import *


def first_choice(windows, pos):
    '''
    检测玩家选择自己先手还是AI先手
    如果玩家选择自己先手，播放gif请求玩家让AI先手，玩家同意则表示开心gif，然后刷新棋局准备开始游戏
    :param windows: pygame的游戏窗口对象
    :param pos: 事件坐标，用于判定鼠标点中
    :return: 如果玩家最终选择自己先手返回'human'，选择AI返回'AI'，其它情况返回0
    '''
    if 87 <= pos[0] <= 686 and 264 <= pos[1] <= 344:
        background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
        background = pygame.transform.scale(background_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
        windows.blit(background, (0, 0))  # 渲染游戏背景图
        pygame.display.update()  # 刷新游戏画面
        return 'AI'
    if 142 <= pos[0] <= 606 and 446 <= pos[1] <= 523:
        '''当玩家选择自己先手时，AI请求先手'''
        while True:
            for i in range(21):
                for event in pygame.event.get():  # 保证随时能退出
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = event.pos
                        if 180 <= pos[0] <= 615 and 567 <= pos[1] <= 626:  # 判定是否点在同意请求的区域
                            '''因请求被同意而高兴，调用game.py的happ_gif函数'''
                            happy_gif(windows)
                            '''刷新棋局画面准备开始游戏'''
                            background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
                            background = pygame.transform.scale(background_image,
                                                                (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
                            windows.blit(background, (0, 0))  # 渲染游戏背景图
                            pygame.display.update()  # 刷新游戏画面
                            return 'AI'
                        elif 301 <= pos[0] <= 498 and 654 <= pos[1] <= 703:
                            background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
                            background = pygame.transform.scale(background_image,
                                                                (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
                            windows.blit(background, (0, 0))  # 渲染游戏背景图
                            pygame.display.update()  # 刷新游戏画面
                            return 'human'
                time.sleep(0.05)
                gif_image = pygame.image.load('gif/不要/' + str(i) + '.jpg')  # 加载'不要'gif图
                gif = pygame.transform.scale(gif_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
                windows.blit(gif, (0, 0))
                beg_txt = pygame.image.load('images/先手请求.PNG')  # 加载先手请求文字图片
                beg_image_size = beg_txt.get_size()  # 获取先手请求文字图片图片尺寸信息
                windows.blit(beg_txt, (WINDOW_X / 2 - beg_image_size[0] / 2, WINDOW_Y * 0.1))  # 先手请求文字位置
                agree_beg = pygame.image.load('images/同意请求.png')  # 加载同意请求文字图片
                agree_beg_size = agree_beg.get_size()  # 获取同意请求文字图片图片尺寸信息
                windows.blit(agree_beg, (WINDOW_X / 2 - agree_beg_size[0] / 2, WINDOW_Y * 0.7))  # 同意请求图片位置
                refuse_beg = pygame.image.load('images/拒绝请求.png')  # 加载拒绝请求文字图片
                refuse_size = refuse_beg.get_size()  # 获取拒绝请求文字图片图片尺寸信息
                windows.blit(refuse_beg, (WINDOW_X / 2 - refuse_size[0] / 2, WINDOW_Y * 0.8))  # 拒绝请求图片位置
                pygame.display.update()
    return 0


def main():
    '''
    游戏运行主函数，负责游戏过程
    :return:无
    '''
    xmb_image = pygame.image.load('images/主界面.png')  # 加载游戏背景图
    xmb = pygame.transform.scale(xmb_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
    windows.blit(xmb, (0, 0))  # 渲染游戏主界面
    pygame.display.flip()  # 刷新整个游戏画面
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

    '''游戏开始'''
    limit_first = 1  # 限制次数为1的参数，初值为1
    while True:
        if first == 'AI' and limit_first:  # 当先手是AI并且第一颗棋子还没下的时候进来
            AI_aggressive(windows)
            limit_first = 0  # 第一颗棋子已下，赋值为0即上锁，下次循环不能进来了
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (player(windows, event.pos)) and len(get_all_record()) != 9:  # 保证玩家落子之后且棋盘还有空缺位置才到AI落子
                    if first == 'AI':  # 如果是AI先手，用进攻性算法下棋
                        AI_aggressive(windows)
                    else:  # 如果是玩家先手，用偏防守性下棋
                        AI(windows)
        '''最后游戏结束跳出循环'''
        if len(get_all_record()) == 9:
            break


if __name__ == '__main__':
    '''游戏初始化'''
    pygame.init()  # 加载模块
    windows = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # 设置游戏窗口大小
    pygame.display.set_caption('不可能战胜的三子棋')  # 设置游戏标题

    '''游戏主体'''
    while True:
        main()  # 游戏运行函数，负责整个游戏过程
        initialization_log()  # 日志初始化
        init()  # 打完一把后游戏初始化，以便开始下一局游戏
