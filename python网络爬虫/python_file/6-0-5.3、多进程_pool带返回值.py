import multiprocessing as mp


def job(x):
    return x**2


def main():
    pool = mp.Pool()
    ret = pool.map(job, range(10000)) # map适合处理多数据
    print(ret)


if __name__ == "__main__":
    main()


# -------------------------

def scrape(url):
    try:
        print requests.get(url)
    except ConnectionError:
        print 'Error Occured ', url
    finally:
        print 'URL ', url, ' Scraped'
 
 
if __name__ == '__main__':
    pool = Pool(processes=3)
    urls = [
        'https://www.baidu.com',
        'http://www.meituan.com/',
        'http://blog.csdn.net/',
        'http://xxxyxxx.net'
    ]
    pool.map(scrape, urls)