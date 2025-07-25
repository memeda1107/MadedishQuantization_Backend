
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/madedish_quantiza?charset=utf8')


# 从环境变量读取配置，设置默认值（开发环境用）
MYSQL_USER = os.getenv('MYSQL_USER', 'root')          # 默认用户名为 'root'
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '123456') # 默认密码（仅限开发环境）
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')      # 默认本地主机
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')           # 默认端口
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'madedish_quantiza')  # 默认数据库名

# 动态生成连接字符串
connection_str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8"
engine = create_engine(connection_str)
db_session = scoped_session(sessionmaker(autoflush=False,bind=engine))






