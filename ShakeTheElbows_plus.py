import random
import os

'''
本程序会将用户账号信息和每个用户的金币数数据都存储在txt文件上，以保存用户数据
'''
pwd = os.path.dirname(__file__)
login_file = os.path.join(pwd, 'login.txt')
with open(login_file, encoding='utf-8') as stream:  # 读取login登录文件，获取所有用户账号和密码
    user_data = stream.read()
user_data = user_data.split()
password = list()
for i in range(1, len(user_data), 2):
    password.append(user_data[i])
username_data = user_data[::2]
user_data = dict(zip(username_data, password))  # 把所有的账号密码存在user_data字典中


def registration():
    '''
    注册账号，先验证输入的账号是否已存在（不区分大小写），存在则重新输入，不存在则继续注册
    注册成功会以当前账号名命名创建一个金币记录文件
    :return: 返回注册用户名username
    '''
    new_username = input("请输入账号：")
    user_data_list = list(user_data.keys())
    for i in range(len(user_data_list)):
        user_data_list[i] = user_data_list[i].lower()
    if new_username.lower() in user_data_list:
        print("账号已存在！")
        return registration()
    else:
        password = input("请输入密码：")
        login_file = os.path.join(pwd, 'login.txt')
        with open(login_file, mode='a', encoding='utf-8') as stream:  # 往用户账号密码文件里追加写入
            stream.writelines("{} {}\n".format(new_username, password))
        user_goldCoin_file = os.path.join(pwd, '{}.txt'.format(new_username))
        with open(user_goldCoin_file, mode='x') as stream:  # 以当前账号名命名创建一个金币记录文件
            stream.write("0")
        username = new_username
        print("注册成功！")
        return username


def login():
    '''
    登录操作
    先验证账号是否存在，存在则输入密码，不存在则询问是否注册，注册则调用注册函数，不注册则重新登录
    密码输入正确返回True，错误则重新登录
    :return:返回登录或注册的账号名
    '''
    username = input("账号：")
    if username in user_data.keys():
        password = input("密码：")
        if password == user_data[username]:
            print("登录成功！")
            return username
        else:
            print("登录失败，账号或密码错误！")
            return login()
    else:
        choose = input("账号不存在！注册请输入”1“，输入其它则重新登录：")
        if choose == "1":
            return registration()  # 调用注册函数
        else:
            return login()


def change_password():
    '''
    修改密码
    先验证旧密码，输入正确后输入新密码即可自动修改用户登录文件中当前用户的密码数据
    :return: 无
    '''
    old_password = input("请输入旧密码：")
    with open(login_file, encoding='utf-8') as stream:  # 再次读取login登录文件，获取所有用户账号和密码，防止第一位用户注册后修改密码报错，及时更新登录文件
        user_data = stream.read()
    user_data = user_data.split()
    password = list()
    for i in range(1, len(user_data), 2):
        password.append(user_data[i])
    username_data = user_data[::2]
    user_data = dict(zip(username_data, password))  # 把所有的账号密码存在user_data字典中
    if old_password == user_data[username]:
        user_data[username] = input("请输入新密码：")
        user_data_list = list(user_data.items())
        with open(login_file, mode='w', encoding='utf-8') as stream:
            for i in range(len(user_data_list)):
                stream.write('{} {}\n'.format(user_data_list[i][0], user_data_list[i][1]))
        print("密码修改成功！")
    else:
        print("密码错误！")


def account_delete(username):
    '''
    删除账户
    从用户名单中删除当前用户的账号和密码并删除当前用户的金币记录文件
    :param username:用户名
    :return: 无
    '''
    with open(login_file, encoding='utf-8') as stream:  # 再次读取login登录文件，获取所有用户账号和密码，及时更新登录文件
        user_data = stream.read()
    user_data = user_data.split()
    password = list()
    for i in range(1, len(user_data), 2):
        password.append(user_data[i])
    username_data = user_data[::2]
    user_data = dict(zip(username_data, password))  # 把所有的账号密码存在user_data字典中
    confirm_password = input("please input your password：")
    if confirm_password == user_data[username]:
        user_data.pop(username)
        user_data_list = list(user_data.items())
        with open(login_file, mode='w', encoding='utf-8') as stream:
            for i in range(len(user_data_list)):
                stream.write('{} {}\n'.format(user_data_list[i][0], user_data_list[i][1]))
        user_goldCoin_file = os.path.join(pwd, '{}.txt'.format(username))
        os.remove(user_goldCoin_file)
        return True
    else:
        print("password error!")
        return False


def read_goldCoin():
    '''
    读取当前账号的金币文件
    :return: 返回金币文件中的内容
    '''
    user_goldCoin_file = os.path.join(pwd, '{}.txt'.format(username))
    with open(user_goldCoin_file) as stream:
        return int(stream.read())


def write_goldCoin(goldCoin):
    '''
    把金币数写入到当前账号的金币文件中
    :param goldCoin: 记录当前用户的金币数
    :return:无
    '''
    user_goldCoin_file = os.path.join(pwd, '{}.txt'.format(username))
    with open(user_goldCoin_file, mode='w') as stream:
        stream.write('{}'.format(goldCoin))


username = login()
goldCoin = read_goldCoin()
'''
每玩一局赠送一枚金币
充值可获取金币，但每次充值金额必须是十的倍数
每充值十元可获得20枚金币
每玩一局消耗5金币
游戏有两个骰子，开始游戏即猜大小，两个骰子点数合计大于6为大，否则为小
猜对可赢得两枚金币，猜错没有奖励
'''
print('''\
Welcome to shake the elbows game
%s
One gold coin per game
Recharge to get gold, but each recharge must be a multiple of ten
You get 20 gold coins for every 10 yuan you top up
Cost 5 gold per game
The game has two dice, start the game that guess the size, two dice number total is greater than 6 is large, otherwise is small
Two gold coins for guessing correctly, no prizes for guessing incorrectly
%s\
''' % ('-' * 100, '-' * 100))
print("Your gold coin: %d" % goldCoin)
while True:
    choose = input('''\
    If you want to top up, enter '1'
    If you want to start the game, enter '2'
    If you want to change your password, enter '9'
    If you want to delete your account, enter '0'
    Enter other content to exit
    Your choose:''')
    if choose == '1':
        topUp = input("Please enter the recharge amount: ")
        while (not topUp.isdigit()) or (int(topUp) % 10 != 0):
            topUp = input("Please enter the recharge amount (It has to be a multiple of ten): ")
        goldCoin += int(topUp) * 2
        write_goldCoin(goldCoin)
        print("Recharge successfully, thank you for your patronage")
        print("Your gold coin: %d" % goldCoin)
        print("-" * 100)
        continue
    elif choose == '2':
        if goldCoin >= 5:
            print("Gold -5\nPresented a gold coin")
            goldCoin -= 4
            write_goldCoin(goldCoin)
            print("Your gold coin: %d" % goldCoin)
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            totalPoint = dice1 + dice2
            if totalPoint > 6:
                size = "large"
            else:
                size = "small"
            guess = input("Please select large or small: ")
            while (not guess == "large") and (not guess == "small"):
                guess = input("Please select large or small: ")
            if guess == size:
                print("Congratulations on your guess! Gold + 2")
                goldCoin += 2
                write_goldCoin(goldCoin)
                print("Your gold coin: %d" % goldCoin)
            else:
                print("Sorry, wrong guess\nRight: " + size)
                print("Your gold coin: %d" % goldCoin)
            print("-" * 100)
            continue
        else:
            print("Your gold coin: %d" % goldCoin)
            print("Your gold coin is less than 5, please top it up")
            print("-" * 100)
            continue
    elif choose == '9':
        change_password()
        continue
    elif choose == '0':
        choose = input("Are you sure to delete the account?\nenter 'yes' to continue or enter other to back:")
        if choose == 'yes':
            if account_delete(username):
                break
            else:
                continue
        else:
            continue
    else:
        break
print("Thanks for your playing")
