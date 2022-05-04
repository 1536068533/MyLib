'''
由于下载间谍过家家的网站没有筛选高清视频功能，所以开发本程序
'''
import requests
import re


def https_address(url):
    '''
    接受网址参数并返回该网页的所有代码
    :param url: 网址
    :return: 该网址的代码
    '''
    stream = requests.get(url)
    return stream.text


def neaten(text):
    '''
    根据传入的网站代码，整理出有用信息，并整理成一个数组返回
    :param text: 网站的全部代码
    :return: 整理好有用信息的数组
    '''
    name = re.findall(r'<a href="/t/\d*">.*</a>', text)
    size = re.findall(r'<td class="size">.*</td>', text)
    all_data = []
    for i in range(len(name)):
        data = ['https://acg.rip/t/' + re.search(r'<a href="/t/(\d*)">.*</a>', name[i]).group(1),
                re.search(r'<a href="/t/\d*">(.*)</a>', name[i]).group(1),
                re.search(r'<td class="size">(.*)</td>', size[i]).group(1)]
        all_data.append(data)
    return all_data


if __name__ == '__main__':
    https = 'https://acg.rip/page/1?term=%E9%97%B4%E8%B0%8D%E8%BF%87%E5%AE%B6%E5%AE%B6'
    next_page = https
    data = neaten(https_address(https))
    while True:
        try:
            next_page = 'https://acg.rip' + re.search(r'<li><a rel="next" href="(.*)">\d</a></li>',
                                                      https_address(next_page)).group(1)
            data += neaten(https_address(next_page))
        except Exception:
            break
    result_data = sorted(data, key=lambda x: x[2], reverse=True)
    for i in range(len(result_data)):
        print(result_data[i])
