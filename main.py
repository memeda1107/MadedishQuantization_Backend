

from flask import Flask, jsonify,request
import akshare as ak
from flask_cors import cross_origin
import pandas as pd
import sqlalchemy_db



# stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em().head(20)
# print(stock_zh_a_spot_em_df)
#
# #dataframe转为json,指定 JSON 格式结构，支持 split、records、index、columns、values
#
# json_data=stock_zh_a_spot_em_df.to_json(orient = "records",force_ascii=False)

# print(json_data)

app = Flask(__name__)

# @app.route('/api/realTimeData', methods=['GET'])
# @cross_origin()
# def get_data():
#     return json_data

from sqlalchemy_db import engine
from model import ReviewDiary
# 导入创建会话的模块
from sqlalchemy.orm import sessionmaker

@app.route('/api/addDiary', methods=['post'])
@cross_origin()
def get_data():
    data = request.get_json()  # 获取JSON格式的数据，也可以通过request.form获取表单数据。确保前端Content-Type设置正确。
    # 使用 sessionmaker 创建一个会话类 Session，并绑定到数据库引擎（bind=engine）
    Session = sessionmaker(bind=engine)
    # 创建一个实例化的会话对象 session
    session = Session()
    # 创建一个新的 User 实例，即要插入到数据库中的新用户
    new_diary = ReviewDiary(income=data['income'], market_trend=data['marketTrend'],market_increase=data['marketIncrease'],
                            turnover=data['turnover'],number_of_rising=data['numberOfRising'],number_of_falling=data['numberOfFalling']
                            ,number_of_limit_up=data['NumberOfLimitUp'],number_of_limit_down=data['NumberOfLimitDown'],explosion_rate=data['explosionRate'],
                            yesterday_limit_up=data['yesterdayLimitUp'],yesterday_connecting_plate=data['yesterdayConnectingPlate'],short_term_funds=data['ShortTermFunds'],
                            overall_market_review=data['overallMarketReview'],any_differences_sectors=data['anyDifferencesSectors'],expected_leaders=data['expectedLeaders'],
                            today_best_solution=data['todayBestSolution'],mistakes_made_today=data['mistakesMadeToday'])
    # 将新用户添加到会话中，即将其添加到数据库操作队列中
    session.add(new_diary)
    # 提交会话，将所有在此会话中的数据库操作提交到数据库
    session.commit()
    return jsonify({'message': '用户创建成功！ID: {}'.format(new_diary.id)}), 201

if __name__ == '__main__':
    app.run()


