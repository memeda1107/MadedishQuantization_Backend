
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/madedish_quantiza?charset=utf8')
db_session = scoped_session(sessionmaker(autoflush=False,bind=engine))

# import pymysql.cursors
# # 连接数据库
# connect = pymysql.Connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='madedish_quantiza',
#     charset='utf8'
# )
# cursor = connect.cursor()
# #新增
# def addData(data):
#   cursor.executemany("INSERT INTO review_diary (income, market_trend, market_increase,turnover,number_of_rising,number_of_falling,"
#                      "number_of_limit_up,number_of_limit_down,explosion_rate,yesterday_limit_up,yesterday_connecting_plate,short_term_funds,"
#                      "overall_market_review,any_differences_sectors,expected_leaders,today_best_solution,mistakes_made_today) VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)
#   connect.commit()
#   connect.close()






