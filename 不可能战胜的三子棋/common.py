'''
专门存放各模块共用的全局变量
供其它模块调用
'''
player_record = set()  # 记录玩家已下棋子的位置
AI_record = set()  # 记录AI已下棋子的位置
all_record = set()  # 记录所有已下棋子的位置
sound_status = 1  # 背景音乐状态，1为满音量，0为静音
sound_button = None  # main中创建的sound_button对象，放在这里方便game.py调用
mouse = None  # main中创建的mouse对象，放在这里方便game.py调用


def init():
    '''
    初始化函数，让这里的全局变量全部初始化
    :return: 无
    '''
    global player_record, AI_record, all_record
    player_record = set()  # 记录玩家已下棋子的位置
    AI_record = set()  # 记录AI已下棋子的位置
    all_record = set()  # 记录所有已下棋子的位置


def add_player_record(value):
    global player_record
    player_record.add(value)


def pop_player_record(*args):
    global player_record
    return player_record.pop(*args)


def get_player_record():
    return player_record


def add_AI_record(value):
    global AI_record
    AI_record.add(value)


def get_AI_record():
    return AI_record


def add_all_record(value):
    global all_record
    all_record.add(value)


def union_all_record():
    global all_record
    if len(all_record) != 9:
        # 限制只有all_record没满才能合并，这里删掉会由于AI落子之后总会合并AI_record和player_record集合到all_record而出bug
        all_record = player_record.union(AI_record)


def get_all_record():
    return all_record


def set_sound_status(status):
    global sound_status
    sound_status = status


def get_sound_status():
    return sound_status


def set_sound_button(args):
    global sound_button
    sound_button = args


def get_sound_button():
    return sound_button


def set_mouse(args):
    global mouse
    mouse = args


def get_mouse():
    return mouse
