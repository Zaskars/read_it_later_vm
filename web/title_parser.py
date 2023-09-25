import urllib.request as urllib
from bs4 import BeautifulSoup
import re


def get_title(url):
    try:
        soup = BeautifulSoup(urllib.urlopen(url), "lxml")
        safestring = soup.title.string.replace('/', ' ')  # название без "опасных" слешей
        return re.sub(' +', ' ', safestring)  # название без кучи пробелов (на всякий)
    except Exception as e:
        print(e)
        return url


if __name__ == '__main__':
    print(get_title('https://habr.com/ru/article/721338/'))
