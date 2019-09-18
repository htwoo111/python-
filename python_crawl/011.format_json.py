# 选择元素
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'lxml')
print(type(soup.title))  # 返回bs4类：元素标签
print(soup.title)
print(soup.head)
print(soup.p)
soup.
