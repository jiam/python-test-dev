import concurrent.futures
import urllib.request

URLS = ['https://www.baidu.com/',
        'https://www.qq.com/',
        'https://www.163.com/',
        'https://www.sina.com/',
        'https://www.jd.com/']

def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return url,conn.code

def get_url():
    for i in range(10):
        for url in URLS:
            yield url

rs = {}
for url in URLS:
    rs[url]={}

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    url_g = get_url()
    fs =[]
    for url in url_g:
        future = executor.submit(load_url,url,10)
        fs.append(future)
    for future in fs:
        url,code = future.result()
        rs[url][code] = rs[url].setdefault(code,0)+1

print(rs)
    


    