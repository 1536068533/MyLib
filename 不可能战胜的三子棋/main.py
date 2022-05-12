from game import *
from sprite import *


def start_game(window):
    '''
    游戏主界面，有play按钮，按钮背后播放gif动画，点中按钮则跳出本函数
    :param window: pygame的游戏窗口对象
    :return: None
    '''
    play_button = Button('images/play.png', (WINDOW_X / 2, WINDOW_Y * 0.75))  # 利用sprite.py中的类创建精灵对象
    while True:
        for n in range(249):
            clock.tick(20)  # 每秒运行20帧
            dance_image = pygame.image.load('gif/跳舞/' + str(n) + '.jpg')  # 加载'跳舞'gif图
            dance = pygame.transform.scale(dance_image, (WINDOW_X, WINDOW_Y))  # 拉伸该图使其适应游戏窗口
            window.blit(dance, (0, 0))
            play_button.update(window)  # 调用sprite.py中Button的update方法
            sound_button.update(window, get_sound_status())  # 刷新音量按钮
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 保证在gif循环里也能随时退出
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse.update()  # 调用sprite的Mouse类的update方法刷新鼠标精灵位置
                    if pygame.sprite.collide_mask(play_button, mouse):  # 检测play按钮和鼠标精灵中的像素是否碰撞
                        # 碰撞了（即鼠标点中了play按钮），直接跳出函数
                        return
                    elif pygame.sprite.collide_mask(sound_button, mouse):  # 判断是否在设置音量
                        if get_sound_status():
                            set_sound_status(0)
                        else:
                            set_sound_status(1)


def first_choice(window):
    '''
    检测玩家选择自己先手还是AI先手
    如果玩家选择自己先手，播放gif请求玩家让AI先手，玩家同意则表示开心gif，然后刷新棋局准备开始游戏
    :param window: pygame的游戏窗口对象
    :return: 如果玩家最终选择自己先手返回'human'，选择AI返回'AI'，其它情况返回0
    '''
    AI_first_Button = Button('images/AI很菜让AI先手.png', (WINDOW_X / 2, WINDOW_Y * 0.77))  # 通过sprite.py的Button类创建对象
    My_first_Button = Button('images/我要先手.png', (WINDOW_X / 2, WINDOW_Y * 0.87))  # 通过sprite.py的Button类创建对象
    while True:
        for i in range(22):
            clock.tick(24)  # 一秒24帧
            gif_image = pygame.image.load('gif/摇摆/' + str(i) + '.jpg')  # 加载'不要'gif图
            gif = pygame.transform.scale(gif_image, (WINDOW_X, WINDOW_Y))  # 拉伸该图使其适应游戏窗口
            window.blit(gif, (0, 0))
            AI_first_Button.update(window)
            My_first_Button.update(window)
            get_sound_button().update(window, get_sound_status())  # 刷新音量按钮
            pygame.display.update()  # 刷新游戏画面
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:  # 鼠标键弹起时进来
                    mouse.update()  # 刷新鼠标点击位置
                    if pygame.sprite.collide_mask(sound_button, mouse):  # 判断是否在设置音量
                        if get_sound_status():
                            set_sound_status(0)
                        else:
                            set_sound_status(1)
                    elif pygame.sprite.collide_mask(AI_first_Button, mouse):  # 玩家选择了AI先手
                        happy_gif(window)  # 加载表示开心的gif
                        background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
                        background = pygame.transform.scale(background_image, (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
                        window.blit(background, (0, 0))  # 渲染游戏背景图
                        pygame.display.update()  # 刷新游戏画面
                        return 'AI'
                    elif pygame.sprite.collide_mask(My_first_Button, mouse):  # 玩家选择自己先手
                        '''当玩家选择自己先手时，AI请求先手'''
                        agree_button = Button('images/同意请求.png',
                                              (WINDOW_X / 2, WINDOW_Y * 0.77))  # 通过sprite.py的Button类创建对象
                        refuse_button = Button('images/拒绝请求.png',
                                               (WINDOW_X / 2, WINDOW_Y * 0.87))  # 通过sprite.py的Button类创建对象
                        while True:
                            for i in range(21):
                                clock.tick(24)  # 一秒24帧
                                gif_image = pygame.image.load('gif/不要/' + str(i) + '.jpg')  # 加载'不要'gif图
                                gif = pygame.transform.scale(gif_image, (WINDOW_X, WINDOW_Y))  # 拉伸该图使其适应游戏窗口
                                window.blit(gif, (0, 0))
                                beg_txt = pygame.image.load('images/先手请求.PNG')  # 加载先手请求文字图片
                                beg_image_size = beg_txt.get_size()  # 获取先手请求文字图片图片尺寸信息
                                window.blit(beg_txt, (WINDOW_X / 2 - beg_image_size[0] / 2, WINDOW_Y * 0.1))  # 先手请求文字位置
                                agree_button.update(window)  # 调用sprite.py的Button类的update方法
                                refuse_button.update(window)  # 调用sprite.py的Button类的update方法
                                get_sound_button().update(window, get_sound_status())  # 刷新音量按钮
                                pygame.display.update()  # 刷新游戏画面
                                for event in pygame.event.get():  # 保证随时能退出
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if event.type == pygame.MOUSEBUTTONUP:
                                        pos = event.pos
                                        mouse.update()  # 刷新鼠标精灵位置
                                        if pygame.sprite.collide_mask(agree_button, mouse):  # 判定是否点在同意请求的区域
                                            '''因请求被同意而高兴，调用game.py的happy_gif函数'''
                                            happy_gif(window)
                                            '''刷新棋局画面准备开始游戏'''
                                            background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
                                            background = pygame.transform.scale(background_image,
                                                                                (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
                                            window.blit(background, (0, 0))  # 渲染游戏背景图
                                            pygame.display.update()  # 刷新游戏画面
                                            return 'AI'
                                        elif pygame.sprite.collide_mask(refuse_button, mouse):  # 判定拒绝请求是否和鼠标区域碰撞
                                            generalduty_gif(window, 'gif/下次不可以拒绝/', 20, cycle_index=1)  # 被拒绝后加载gif
                                            background_image = pygame.image.load('images/棋盘.jpg')  # 加载游戏背景图
                                            background = pygame.transform.scale(background_image,
                                                                                (WINDOW_X, WINDOW_Y))  # 拉伸游戏背景图使其适应游戏窗口
                                            window.blit(background, (0, 0))  # 渲染游戏背景图
                                            pygame.display.update()  # 刷新游戏画面
                                            return 'human'
                                        elif pygame.sprite.collide_mask(sound_button, mouse):  # 判断是否在设置音量
                                            if get_sound_status():
                                                set_sound_status(0)
                                            else:
                                                set_sound_status(1)


def main():
    '''
    游戏运行主函数，负责游戏过程
    :return:无
    '''
    '''调用主界面函数，点击play开始游戏'''
    start_game(window)

    '''调用先手选择函数获取先手信息'''
    first = first_choice(window)

    '''游戏开始'''
    limit_first = 1  # 限制次数为1的参数，初值为1
    while True:
        sound_button.update(window, get_sound_status())  # 刷新音量按钮
        pygame.display.update()  # 刷新游戏画面
        if first == 'AI' and limit_first:  # 当先手是AI并且第一颗棋子还没下的时候进来
            AI_aggressive(window)
            limit_first = 0  # 第一颗棋子已下，赋值为0即上锁，下次循环不能进来了
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse.update()  # 刷新鼠标精灵位置
                if pygame.sprite.collide_mask(sound_button, mouse):  # 判断是否在设置音量
                    if get_sound_status():
                        set_sound_status(0)
                    else:
                        set_sound_status(1)
                if player(window, event.pos) and len(get_all_record()) != 9:  # 保证玩家落子之后且棋盘还有空缺位置才到AI落子
                    if first == 'AI':  # 如果是AI先手，用进攻性算法下棋
                        AI_aggressive(window)
                    else:  # 如果是玩家先手，用偏防守性下棋
                        AI(window)
        '''最后游戏结束跳出循环'''
        if len(get_all_record()) == 9:
            break


if __name__ == '__main__':
    '''游戏初始化'''
    pygame.init()  # 加载模块
    pygame.mixer.init()  # 加载混音模块
    window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # 设置游戏窗口大小
    pygame.display.set_caption('不可能战胜的三子棋')  # 设置游戏标题
    clock = pygame.time.Clock()  # 游戏时钟对象
    music = pygame.mixer.music.load('sound/LUV2&Lino xd - Lost In The Night (Explicit) [mqms2].mp3')  # 加载音乐
    sound_button = SoundButton('images/音乐开.png', 'images/音乐关.png', (WINDOW_X, 0))  # 创建音乐按钮精灵对象
    set_sound_button(sound_button)  # 创建sound_button对象后，传到common.py方便game.py调用
    pygame.mixer.music.play(-1)  # -1 值告诉 Pygame 无限循环音乐文件
    mouse = Mouse()  # 调用sprite.py中的Mouse类创建鼠标精灵对象
    set_mouse(mouse)  # 创建mouse对象后，传到common.py方便game.py调用
    mouse.update()

    '''游戏主体'''
    while True:
        main()  # 游戏运行函数，负责整个游戏过程
        initialization_log()  # 日志初始化
        init()  # 打完一把后游戏初始化，以便开始下一局游戏
