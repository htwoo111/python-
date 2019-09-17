import requests
from lxml import etree
import json

class TiebaSpider(object):
    def __init__(self):
        self.url = "https://tieba.baidu.com/f?kw=%E4%B8%AD%E7%A7%8B%E8%8A%82&pn={}&"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Referer": "https://tieba.baidu.com/",
            "Cookie": "BAIDUID=433DB4AAED0290A1196E65E26551F041:FG=1; BIDUPSID=433DB4AAED0290A1196E65E26551F041; PSTM=1560467964; BDUSS=dnfn5zZnE3eHNlMkMwdjlLR3dUVH56WDR1OHhVQWY1UTBZZjFrSUhhMm9WM3RkRVFBQUFBJCQAAAAAAAAAAAEAAADTpYnPaHR3b28yMjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKjKU12oylNdVT; H_WISE_SIDS=133994_124610_100805_135462_135311_134551_128065_133680_120155_135322_132909_131246_132439_130763_132378_131518_118882_118865_118855_118830_118798_107312_132783_134391_133352_132553_129655_132250_127025_134854_128967_133838_133847_132551_133287_134463_134320_129643_131423_135336_135552_134600_134489_110085_127969_131754_131951_135672_135458_127417_135045_135036_134383_135503_134353; TIEBAUID=8def7439658107cd1106f38b; STOKEN=ffce0822077b028660923867c7aec6d035e7a63adf151b67759a76671085058f; TIEBA_USERTYPE=744b29c1d10868fb821f4b1b; locale=zh; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=a27501ef9cdf21a57df86398c6685bdc89b800a4_1568592847_js; H_PS_PSSID=29654_1423_21087_29523_29521_29720_29567_29220_26350_22158; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=7; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1568117660,1568605001,1568605020,1568605215; 3481904595_FRSVideoUploadTip=1; wise_device=0; SEENKW=%E4%B8%AD%E7%A7%8B%E8%8A%82; IS_NEW_USER=13f77af84c1af1678ec28563; BAIDU_WISE_UID=wapp_1568616371161_183; USER_JUMP=-1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1568616372; CLIENTWIDTH=375; CLIENTHEIGHT=812; LASW=375"
        }

        self.proxies = {
            "https": "https://182.116.234.216:9999"
            #             "https":"https://115.210.82.231:8118",
            #             "https":"https://222.240.184.126:8086"
        }

    def parse_url(self, url):
        """获取网站信息"""
        print(url)
        r = requests.get(url, headers=self.headers)  # , proxies=self.proxies)
        return r.content.decode()

    def data_analysis(self, html_str):
        """对获取到的数据，进行xpath解析"""
        html = etree.HTML(html_str)
        authors = html.xpath(
            '//li[@class="tl_shadow tl_shadow_new "]//span[contains(@class,"ti_author")]/text()[1]')
        contents = html.xpath(
            '//li[@class="tl_shadow tl_shadow_new "]//div[@class="ti_title"]/span//text()')
        hrefs = html.xpath(
            '//li[@class="tl_shadow tl_shadow_new "]//a[@class="j_common ti_item "]/@href')
        info = []
        for content in contents:
            item = {}
            item['author'] = authors[contents.index(content)] if len(
                authors[contents.index(content)]) else None
            item['href'] = "https://tieba.baidu.com" + \
                hrefs[contents.index(content)] if len(
                    hrefs[contents.index(content)]) else None
            info.append(item)
        return info

    def save(self, info):
        """对获取到的info(list)进行保存"""
        with open("crawl_file/018.tieba.txt", 'a+', encoding='utf-8') as f:
            for i in info:  # 遍历info列表，获取每一条信息
                content = json.dumps(i, ensure_ascii=False)  # 转换成str
                f.write(content)
                f.write('\n')
            print('保存成功')

    def run(self):
        """实现主程序"""
        current_page = 0
        # 0.获取url
        while True:
            url = self.url.format(current_page)
            # 1.发送请求，获取数据
            html_str = self.parse_url(url)
            # 2.数据处理，lxml解析
            info = self.data_analysis(html_str)
            # 3.保存
            self.save(info)
            if current_page >= 3000:
                break
            current_page += 30


if __name__ == "__main__":
    tieba_spider = TiebaSpider()
    html_str = tieba_spider.run()
