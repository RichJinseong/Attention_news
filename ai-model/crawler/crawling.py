import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

data = list()


def crawling_bot():
    for hd_cate in ['news', 'sports', 'life', 'money', 'tech', 'travel', 'opinion']:
        url = f'https://www.usatoday.com/{hd_cate}'
        res = requests.get(url)
        soup = BeautifulSoup(
            res.text,
            'html.parser'
        )
        try:
            for td in soup.find('main', attrs={"class": "gnt_cw"}).find_all('a'):
                try:
                    news_url = td['href']
                    news_split = news_url.split('/')
                    if news_split[1] == 'story':
                        news_res = requests.get('https://www.usatoday.com' + news_url)
                        news_soup = BeautifulSoup(news_res.text, 'html.parser')
                        news = news_soup.find('article', attrs={'class': 'gnt_pr'})
                        head = news.find('h1').string
                        body = ''
                        for bd in news.find_all('p', attrs={'class': 'gnt_ar_b_p'}):
                            a = bd.string
                            if a is not None:
                                body += a
                        cate = ",".join(news_split[2:-6])
                        date = "-".join(news_split[-6:-3])
                        data.append(
                            {'platform': 'usatoday', 'category': cate, 'headline': head, 'content': body, 'date': date})
                        time.sleep(.5)
                except:
                    pass
        except:
            pass

    return data


if __name__ == '__main__':
    data = crawling_bot()
    print(len(data))

