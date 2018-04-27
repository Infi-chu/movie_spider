import requests,json,re,time
from requests.exceptions import RequestException


def get_page(url):
    try:
        header = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        }
        res = requests.get(url,headers=header)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for i in items:
        yield {
            'index': i[0],
            'image': i[1],
            'title': i[2],
            'actor': i[3].strip()[3:],
            'time': i[4].strip()[5:],
            'score': i[5] + i[6],
        }

def w_file(content):
    with open('list.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_page(url)
    for i in parse_page(html):
        print(i)
        w_file(i)

if __name__ == '__main__':
    for i in range(10):
        main(offset= i * 10)
        time.sleep(1)