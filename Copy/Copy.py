import os


def copy(src, target):
    '''
    要求输入原文件和目标路径的绝对路径，把原文件的所有内容拷贝到目标路径中
    会判断src和target是绝对路径，是否存在，不存在则拷贝失败
    判断src和target都是目录的情况，src是文件而target是目录的情况，然后拷贝文件
    如果target是文件的绝对路径，会print说明target不是目录路径，拷贝失败
    如果target是不存在的目录路径，会先询问是否创建目录，包括多层目录，并调用自身继续拷贝
    如果复制的文件在目标路径中已存在，会询问是否覆盖
    复制的目录中有目录且目标路径已有同名目录时，自动合并文件夹
    :param src: 原文件的绝对路径
    :param target:目标的绝对路径
    :return:无
    '''
    if os.path.isabs(src) and os.path.isabs(target):  # 判断绝对路径
        if os.path.exists(src) and os.path.exists(target):  # 判断存在
            if os.path.isdir(src) and os.path.isdir(target):
                # src和target都是目录
                files = os.listdir(src)
                for i in files:
                    if os.path.exists(os.path.join(target, i)) and not os.path.isdir(os.path.join(target, i)):
                        # 复制的某文件在目标路径中已存在并且这个文件不是一个目录，询问是否覆盖
                        choose = input("文件 {} 已存在，如覆盖请输入'yes'，否则输入其它：".format(i))
                        if choose == 'yes':
                            with open(os.path.join(src, i), mode='rb') as stream:
                                file_data = stream.read()
                            with open(os.path.join(target, i), mode='wb') as stream:
                                stream.write(file_data)
                            print("文件", i, "已拷贝 -------------------------", os.path.getsize(os.path.join(target, i)),
                                  "字节")
                        else:
                            continue
                    elif os.path.isdir(os.path.join(src, i)) and os.path.exists(os.path.join(target, i)):
                        # 复制的目录中有目录且目标路径已有同名目录时，直接再次调用自己
                        print("文件夹", i, "已存在，正在合并文件夹……")
                        copy(os.path.join(src, i), os.path.join(target, i))
                    elif os.path.isdir(os.path.join(src, i)) and not os.path.exists(os.path.join(target, i)):
                        # 复制的目录中有目录且目标路径没有同名目录时，先创建文件夹再调用自己
                        os.mkdir(os.path.join(target, i))
                        print("文件夹", i, "已拷贝 -------------------------", os.path.getsize(os.path.join(target, i)), "字节")
                        copy(os.path.join(src, i), os.path.join(target, i))  # 拷贝的目录中有目录时，再次调用自己
                    else:
                        with open(os.path.join(src, i), mode='rb') as stream:
                            file_data = stream.read()
                        with open(os.path.join(target, i), mode='wb') as stream:
                            stream.write(file_data)
                        print("文件", i, "已拷贝 -------------------------", os.path.getsize(os.path.join(target, i)), "字节")
            elif os.path.isfile(src) and os.path.isdir(target):
                # src是文件，target是目录
                with open(src, mode='rb') as stream:
                    file_data = stream.read()
                with open(os.path.join(target, os.path.split(src)[1]), mode='wb') as stream:
                    stream.write(file_data)
                print("文件", os.path.split(src)[1], "已拷贝到目标文件夹 -------------------------",
                      os.path.getsize(os.path.join(target, os.path.split(src)[1])), "字节")
            else:
                # target是文件
                print("目标路径输入的不是一个目录，而是一个已存在的文件！")
        elif os.path.exists(src) == False:  # 判断原文件还是目标文件问题
            print("输入的原文件路径不存在！")
        else:
            print("输入的目标路径不存在！")
            choose = input("输入'yes'创建目录（包括多层目录）以继续拷贝，输入其它则退出：")
            if choose == 'yes':
                os.makedirs(target)
                copy(src, target)  # 调用自己以继续拷贝
    elif os.path.isabs(src) == False:  # 判断原文件还是目标文件问题
        print("输入的原文件路径不是绝对路径！")
    else:
        print("输入的目标路径不是绝对路径！")


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    src_path = input("请输入原文件的绝对路径：")
    target_path = input("请输入目标文件夹的绝对路径：")
    copy(src_path, target_path)
