from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(executable_path = 'D:\Documents\Downloads\chromedriver_win32\chromedriver.exe', options=chrome_options)

browser.get("https://www.zhihu.com/signin")
browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("用户名")
import time
time.sleep(3)
browser.find_element_by_css_selector(".SignFlow-password input").send_keys("密码")
browser.find_element_by_css_selector(
    ".Button.SignFlow-submitButton").click()
