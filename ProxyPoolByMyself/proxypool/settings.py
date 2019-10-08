"""
redis 数据库设置
"""
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 5
# redis地址
REDIS_HOST = 'localhost'
# redis 端口
REDIS_PORT = 6379
# redis密码
REDIS_PASSWORD = 'htwoo111'
# redis key
# REDIS_KEY = 'myProxies'
REDIS_KEY = 'proxies2'

# 设置代理池的代理最大数量
POOL_UPPER_THRESHOLD = 200

# 设置获取代理的轮询时间
GETTER_CYCLE = 200
# 设置验证代理的时间间隔
TESTER_CYCLE = 30



"""
开关
"""

GETTER_ENABLED = True
# GETTER_ENABLED = False
TESTER_ENABLED = True
# API_ENABLED = True
API_ENABLED = False

"""
Tester模块工具
"""
VAILD_STATUS_CODE = [200]
TEST_URL = 'https://weixin.sogou.com/'
# TEST_URL = 'https://bilibili.com'
BATCH_TEST_SIZE = 100

"""
API模块工具
"""
API_HOST = '0.0.0.0'
API_PORT = 5555