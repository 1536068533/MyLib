from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import time, os


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
