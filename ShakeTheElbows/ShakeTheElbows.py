import random

goldCoin = 0
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
    Enter other content to exit
    Your choose:''')
    if choose == '1':
        topUp = input("Please enter the recharge amount: ")
        while (not topUp.isdigit()) or (int(topUp) % 10 != 0):
            topUp = input("Please enter the recharge amount (It has to be a multiple of ten): ")
        goldCoin += int(topUp) * 2
        print("Recharge successfully, thank you for your patronage")
        print("Your gold coin: %d" % goldCoin)
        print("-" * 100)
        continue
    elif choose == '2':
        if goldCoin >= 5:
            print("Gold -5\nPresented a gold coin")
            goldCoin -= 4
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
    else:
        break
print("Thanks for your playing")
