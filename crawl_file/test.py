import requests
import re
import json


class TiebaSpider(object):
    def __init__(self):
        self.url = "https://tieba.baidu.com/f?kw=%E4%B8%AD%E7%A7%8B%E8%8A%82&pn=0"
        self.headers = {
            "Cookie": "BAIDUID=433DB4AAED0290A1196E65E26551F041:FG=1; BIDUPSID=433DB4AAED0290A1196E65E26551F041; PSTM=1560467964; BDUSS=dnfn5zZnE3eHNlMkMwdjlLR3dUVH56WDR1OHhVQWY1UTBZZjFrSUhhMm9WM3RkRVFBQUFBJCQAAAAAAAAAAAEAAADTpYnPaHR3b28yMjIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKjKU12oylNdVT; H_WISE_SIDS=133994_124610_100805_135462_135311_134551_128065_133680_120155_135322_132909_131246_132439_130763_132378_131518_118882_118865_118855_118830_118798_107312_132783_134391_133352_132553_129655_132250_127025_134854_128967_133838_133847_132551_133287_134463_134320_129643_131423_135336_135552_134600_134489_110085_127969_131754_131951_135672_135458_127417_135045_135036_134383_135503_134353; TIEBAUID=8def7439658107cd1106f38b; STOKEN=ffce0822077b028660923867c7aec6d035e7a63adf151b67759a76671085058f; TIEBA_USERTYPE=744b29c1d10868fb821f4b1b; locale=zh; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; yjs_js_security_passport=a27501ef9cdf21a57df86398c6685bdc89b800a4_1568592847_js; H_PS_PSSID=29654_1423_21087_29523_29521_29720_29567_29220_26350_22158; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=7; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1568117660,1568605001,1568605020,1568605215; 3481904595_FRSVideoUploadTip=1; wise_device=0; SEENKW=%E4%B8%AD%E7%A7%8B%E8%8A%82; IS_NEW_USER=13f77af84c1af1678ec28563; BAIDU_WISE_UID=wapp_1568616371161_183; USER_JUMP=-1; CLIENTWIDTH=375; CLIENTHEIGHT=812; pb_prompt=1; SET_PB_IMAGE_WIDTH=355; mo_originid=2; LASW=1440; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1568622446",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Host": "tieba.baidu.com"
        }

    def parse_url(self):
        print(self.url)
        r = requests.get(self.url, headers=self.headers)
        return r.content.decode()

    def run(self):
        html_str = self.parse_url()
        with open("crawl_file/000test.html", "w", encoding="utf-8") as f:
            f.write(json.dumps(html_str, ensure_ascii=False))
        print("保存成功")

if __name__ == "__main__":
    tieba_spider = TiebaSpider()
    tieba_spider.run()
