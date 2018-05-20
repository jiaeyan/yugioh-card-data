import json
import urllib.request
from itertools import product
from bs4 import BeautifulSoup
# url = 'https://www.ourocg.cn/card/EasMO0'
# url = 'https://www.ourocg.cn/card/9vsw3'
# url1 = 'https://www.ourocg.cn/card/wvsWz'
# url2 = 'https://www.ourocg.cn/card/Qbsg4'
# url3 = 'https://www.ourocg.cn/card/vasZW5'
# url4 = 'https://www.ourocg.cn/card/wvsbDJ'
# url5 = 'https://www.ourocg.cn/card/EasrQw'
# url6 = 'https://www.ourocg.cn/card/lNsg6N'
#
# url7 = 'https://www.ourocg.cn/card/list-5/1'
# url8 = 'https://www.ourocg.cn/card/77s2RX'
# url9 = 'https://ocg.xpg.jp/deck/deck.fcgi'
#
# data = urllib.request.urlopen(url).read().decode('UTF-8')
# soup = BeautifulSoup(data, "lxml")
# info = soup.article.div.stripped_strings
# for string in info:
#     print(string)
#     print()


def collect_data(digit_list):
    num = 0
    l = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    l = set(list(l))
    print('正在收集卡片...')
    with open('valid_urls.txt', 'w') as f:
        for digit in digit_list:
            for rand in product(*[l for _ in range(digit)]):
                url = 'https://www.ourocg.cn/card/' + ''.join(rand)
                if generate_card_file(url, ''.join(rand)):
                    num += 1
                    f.write(url + '\n')
                    print('已收集到 {} 张卡片...'.format(num))
                    if num == 9012:
                        print('恭喜，卡片收集结束！')
                        break



# for pat in permutations(l, 5):
#     count += 1
# print(count)

# l = [1,2,3]
# res = list(product(*[l for _ in range(5)]))
# print(len(res))
# print(len(set(res)))

# for child in soup.article.div.children:
#     # content = child.string
#     # if content:
#     print(child)
#     print(type(child))
#     print(child.string)
    # print(child.stripped_strings)
    # print()


def generate_card_file(url, rand):
    try:
        data = urllib.request.urlopen(url).read().decode('UTF-8')
        soup = BeautifulSoup(data, "lxml")
        info = list(soup.article.div.stripped_strings)
        write_file(info)

        return True

    except:
        print('尝试 {} 失败，更换随机数...'.format(rand))
        return False

# 未收录灵摆刻度
def write_file(info):
    card = dict()
    card[info[0]] = info[1]
    card[info[2]] = info[3]
    card[info[4]] = info[5]
    type_index = info.index('卡片种类') + 1
    code_index = info.index('卡片密码') + 1
    code = info[code_index]
    type = info[type_index]
    card['卡片种类'] = type
    card['卡片密码'] = code
    card['卡片子种类'] = info[type_index + 1: code_index - 1]
    if '效果' in card['卡片子种类']:  # two 效果s in text lists， one as sub type and one as effect description
        info[type_index + 1] = '效果1'
    card['使用限制'] = info[info.index('使用限制') + 1]
    card['效果'] = info[(info.index('效果') + 1): info.index('收录详情')]
    if type == '怪兽':
        card['种族'] = info[info.index('种族') + 1]
        card['属性'] = info[info.index('属性') + 1]
        card['攻击力'] = info[info.index('攻击力') + 1]  # ?
        if '连接' not in card['卡片子种类']:
            card['防御力'] = info[info.index('防御力') + 1]  # ?
            size = '阶级' if 'XYZ' in card['卡片子种类'] else '星级'
            card[size] = int(info[info.index(size) + 1])
        else:
            card['LINK'] = int(info[info.index('LINK') + 1])

    with open('scrape_cards/' + code + '.json', 'w') as f:
        json.dump(card, f, sort_keys=True)


# d = {2:True, 1:{'g':[1,2,3], 'c':('你好', '喜欢')}}
# with open('test.json', 'w') as f:
#     json.dump(d, f, sort_keys=True)
#
# with open('test.json') as data_file:
#     data = json.load(data_file)
#     print(list(data.keys()))


collect_data([6])
# generate_card_file(url8)

# with open('cards/74997493.json') as data_file:
#     data = json.load(data_file)
#     print(data)
