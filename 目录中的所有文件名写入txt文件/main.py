import os
import re


def get_old_name(dir):
    '''
    根据所给的目录获取该目录下所有文件名（不包括子目录中的文件）
    :param dir: 目录的绝对路径
    :return: 返回该目录下所有文件名（列表）
    '''
    return os.listdir(dir)


def judge(name):
    '''
    筛选函数
    :param name: 传入的文件名参数
    :return: 根据正则表达式筛选，符合则返回False，不符合则返回True
    '''
    try:
        re.match(r'^[\w-]+.\w+$', name).group()  # 删除规则，可根据需要修改正则表达式
        return False
    except Exception:
        return True


if __name__ == "__main__":
    path = 'H:\数学\高等数学 天津大学 樊顺厚 视频'  # 目录，根据需要修改
    old_name_list = get_old_name(path)
    print(old_name_list)  # 筛选前的列表
    new_name_list = list(filter(judge, old_name_list))
    print(new_name_list)  # 筛选后的列表
    print(len(new_name_list))  # 剩下符合筛选条件的数量
    record = os.path.join(path, '高等数学樊顺厚视频名称索引.txt')
    '''开始写入txt文件'''
    with open(record, mode='w', encoding='utf-8') as stream:
        for i in range(len(new_name_list)):
            stream.write(new_name_list[i] + '\n')
