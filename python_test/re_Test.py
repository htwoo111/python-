
import re


txt = """<a  href="/29672425.html" class="truetit" target="_blank">孙子的女儿和外孙的儿子谁的地位比较高？</a>
"""

ret = re.search(r'(/\d+\.html)', txt).group()
print(ret)
# print(txt)
