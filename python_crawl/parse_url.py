# coding=utf-8
import requests
from retrying import retry

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Host": "movie.douban.com",
    "Referer": "https://movie.douban.com/explore",
    "Cookie": """bid=ritQLC6fjYo; gr_user_id=5918bd21-276d-4a80-9317-718689a1c95f; _vwo_uuid_v2=D9951E2C970B5B64B03F085111A475421|7a828f1c007f53618de9a6fbe511ea9b; __gads=ID=c0940d8498c73862:T=1566175932:S=ALNI_Mak2fzg33Gm17z5mOKN0-1DfstUIw; viewed="10546125_20432061"; ll="118297"; acw_tc=2760826215683820047082070ecbeb1d7604f8a889a38f76339bda1de33afb; __yadk_uid=SDytN8vqYzyGtITpzUOqBCuk97bpwjbV; _ga=GA1.2.930570486.1566136452; _gid=GA1.2.955509093.1568382446; UM_distinctid=16d2ae1bc7768-0a34bf851b571d-5373e62-151800-16d2ae1bc7836b; __utmc=30149280; __utmc=223695111; Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1568382500,1568420406; Hm_lpvt_19fc7b106453f97b6a84d64302f21a04=1568420406; __utma=30149280.930570486.1566136452.1568420138.1568435373.8; __utmz=30149280.1568435373.8.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1568435382%2C%22https%3A%2F%2Fwww.douban.com%2Fgroup%2Fexplore%22%5D; _pk_ses.100001.4cf6=*; __utmt_douban=1; __utma=223695111.7046039.1568382026.1568420033.1568435382.3; __utmb=223695111.0.10.1568435382; __utmz=223695111.1568435382.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/group/explore; _pk_id.100001.4cf6=94cac669206cab03.1568382026.3.1568435771.1568420253.; __utmb=30149280.7.10.1568435373"""
}


@retry(stop_max_attempt_number=3)
def _parse_url(url, method, data, proxies):
    # print("*" *20)
    if method == "POST":
        response = requests.post(
            url, data=data, headers=headers, proxies=proxies)
    else:
        response = requests.get(url, headers=headers,
                                timeout=3, proxies=proxies)
    assert response.status_code == 200
    return response.content.decode()


def parse_url(url, method="GET", data=None, proxies={}):
    try:
        html_str = _parse_url(url, method, data, proxies)
    except:
        html_str = None

    return html_str


if __name__ == "__main__":
    url = "www.baidu.com"
    # print(parse_url(url))
    # print(retrying)
