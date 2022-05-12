import pygame
from common import *


class Mouse(pygame.sprite.Sprite):
    '''
    鼠标类精灵，用于判定鼠标是否点击中其它精灵
    '''

    def __init__(self):
        super().__init__()  # 调用父类构造
        self.image = pygame.Surface((1, 1))  # 创建新的长和宽都为1像素的图像对象
        self.image.fill('red')  # 用红色填满这个对象
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()  # 初始位置，图像中心正好是鼠标指针位置

    def update(self):
        self.rect.center = pygame.mouse.get_pos()  # 调用本函数时移到鼠标指针位置


class Button(pygame.sprite.Sprite):
    '''
    按钮类精灵
    '''

    def __init__(self, filename, location):
        super().__init__()  # 调用父类构造
        self.image = pygame.image.load(filename)  # 加载图片
        self.rect = self.image.get_rect()  # 获取图片矩形区域
        self.rect.center = location  # 设置图中心点初始位置

    def update(self, window):
        '''
        刷新对象画面
        :param window_object: pygame的游戏窗口对象
        :return: 无
        '''
        window.blit(self.image, self.rect)  # 在window对象（pygame的游戏窗口对象）上刷新图片和区域


class SoundButton(pygame.sprite.Sprite):
    '''
    音量按钮精灵，实现一个按钮，两张图片，互斥显示
    '''
    filename_one = None
    filename_two = None

    def __init__(self, filename_one, filename_two, location):
        super().__init__()
        self.image = pygame.image.load(filename_one)  # 加载图片
        self.filename_one = filename_one
        self.filename_two = filename_two
        self.rect = self.image.get_rect()  # 获取图片矩形区域
        self.rect.topright = location  # 设置图右上角初始位置

    def update(self, window, status):
        '''
        根据status传入的int决定是刷新filename_one还是filename_two的图
        status传参1或0
        status参数会和common.py的sound_status同步
        :param window: pygame的游戏窗口对象
        :param status: 等于1时刷新filename_one的图，等于0时刷新filename_two的图
        :return: 无
        '''
        if status:  # 为1时音量开
            self.image = pygame.image.load(self.filename_one)
            pygame.mixer.music.set_volume(status)
            set_sound_status(status)  # 让common.py的sound_status同步为1
        else:  # 为0时音量关
            self.image = pygame.image.load(self.filename_two)
            pygame.mixer.music.set_volume(status)
            set_sound_status(status)  # 让common.py的sound_status同步为0
        window.blit(self.image, self.rect)
