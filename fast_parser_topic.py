import requests
from bs4 import BeautifulSoup
import re
# Парсер для поиска номеров телефонов обсуждениях в ВК, так же сохраняет имя, город, комментарий в отдельный файл
# _______________________________________________________________________________________________________________
def get_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36 '
    }
    r = requests.get(url, headers=headers)
    # print(r.status_code)
    return r.text


def get_write(data):
    with open('vk_out_topic.txt', 'a', encoding='UTF-8') as fw:
        fw.write(data)


def get_contact(link):
    soup2 = BeautifulSoup(link, 'lxml')
    town = soup2.find_all('div', class_='clear_fix profile_info_row')

    for i in town:
        try:
            dataa = i.find('a')
            if '[city]' in str(dataa):
                return dataa.text
            else:
                continue
        except Exception:
            pass


def get_write_phone(phone):
    with open('phone_from_topic.txt', 'a', encoding='UTF-8') as fw:
        fw.write(phone + '\n')


def get_data_html(html):
    global user_77
    soup = BeautifulSoup(html, 'lxml')

    links = soup.find_all('a', class_="bp_thumb")
    message_text = soup.find_all('div', class_='bp_text')
    for i, el in zip(links, message_text):

        message_user = el.text
        row_phone = re.findall(r"(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})", message_user)
        for row in row_phone:
            elem = list(row)
            user_77 = ''.join(elem)
            print(user_77)
            if user_77:
                get_write_phone(user_77)



        print(message_user)

        try:
            name = i.find('img').get('alt') + ' '
            print(name)
            get_write(name)
        except Exception:
            pass

        vk_link = ' https://vk.com' + i.get('href')

        town_ = get_contact(get_page(vk_link))
        get_write(vk_link + ' ')

        if town_ is None:
            get_write('Неизвестно  ')
            get_write(message_user + '\n')
        else:
            get_write(town_ + ' ')
            get_write(message_user + '\n')

        print(vk_link + '\n' + str(town_))


def main():
    with open(r'target_txt_file_with_topic_links', 'r', encoding='utf-8', errors='ignore') as fl:
        lists_topic = fl.readlines()
        s = 0
    for item_topic in lists_topic:
        s += 1
        if len(lists_topic) == s:
            break
        else:
            print(item_topic)
            print('Всего обсуждений  {}  из  {}'.format(s, len(lists_topic)))
            page = 10
# TODO: сделать определение количества страниц в топике
            while page != 3900:
                gen_url = 'https://' + item_topic.strip() + '?offset=' + str(page)
                print('Парсим страницу {}'.format(gen_url))
                get_data_html(get_page(gen_url))
                page += 10


if __name__ == '__main__':
    main()
