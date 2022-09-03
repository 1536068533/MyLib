'''
由于下载OVERLORD的网站没有筛选高清视频功能，所以开发本程序
'''
from gevent import monkey

monkey.patch_all()  # 打上猴子补丁
import gevent
import requests
import re
import time


def https_address(url, page=1):
    '''
    接受网址参数并返回该网页的所有代码
    :param url: 网址
    :return: 该网址的代码
    '''
    stream = requests.get(url)
    print('第' + str(page) + '页的网页代码已获取！')
    return stream.text


def neaten(text):
    '''
    根据传入的网站代码，整理出有用信息，并整理成一个数组返回
    :param text: 网站的全部代码
    :return: 整理好有用信息的数组
    '''
    global all_data
    name = re.findall(r'<a href="/t/\d*">.*</a>', text)
    size = re.findall(r'<td class="size">.*</td>', text)
    for i in range(len(name)):
        correct_name = re.search(r'<a href="/t/\d*">.*(OVERLORD IV|不死者之王 第四季|Overlord S4).*</a>', name[i])
        if (correct_name):
            data = ['https://acg.rip/t/' + re.search(r'<a href="/t/(\d*)">.*</a>', name[i]).group(1),
                    re.search(r'<a href="/t/\d*">(.*)</a>', name[i]).group(1),
                    re.search(r'<td class="size">(.*)</td>', size[i]).group(1)]
            all_data.append(data)


def prepare_sort(size):
    '''
    排序前准备，判断大小单位是GB还是MB，如果是GB，换算成MB，最后再乘上100以去掉小数点
    :param size: 文件大小（字符串）
    :return: 如果文件大小是GB结尾，换算成MB并乘上100返回字符串，如果是MB则直接乘100返回字符串
    '''
    MB_size = float(re.search('(.*) (GB|MB)', size[2]).group(1))
    size_type = re.search('(.*) (GB|MB)', size[2]).group(2)
    if (size_type == 'GB'):
        return MB_size * 1024
    else:
        return MB_size


def coroutine(url, page):
    '''
    协程函数，协程要做的事都在这
    :param url: 网址
    :return: 无
    '''
    neaten(https_address(url, page))


if __name__ == '__main__':
    url = 'https://acg.rip/?term=OVERLORD'
    html_text = https_address(url)
    all_page = int(re.search(r'<li><a href="/page/(\d*)\?term=OVERLORD">(\d*)</a></li> <li class="next">'
                             , html_text).group(2))  # 求出一共有多少页
    print('总共'+str(all_page)+'页')
    all_data = []  # 用于整合最终结果
    coroutine_obj = dict()
    for i in range(1, all_page + 1):
        coroutine_obj['第' + str(i) + '页'] = gevent.spawn(coroutine,
                                                         "https://acg.rip/page/" + str(i) + "?term=OVERLORD", i)
        print('第' + str(i) + '页已请求……')
        coroutine_obj['第' + str(i) + '页'].join()
        time.sleep(9)

    result_data = sorted(all_data, key=prepare_sort, reverse=True)
    for i in range(len(result_data)):
        print(result_data[i])

    print("result_data列表长度：", len(result_data))
