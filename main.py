from flask import Flask, jsonify, request
# import akshare as ak
from flask_cors import cross_origin
# import pandas as pd
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
from sqlalchemy import and_


#新增复盘
@app.route('/addDiary', methods=['post'])
@cross_origin()
def add_diary():
    data = request.get_json()
    Session = sessionmaker(bind=engine)
    session = Session()
    new_diary = ReviewDiary(income=data['income'], market_trend=data['marketTrend'],
                            market_increase=data['marketIncrease'],
                            turnover=data['turnover'], number_of_rising=data['numberOfRising'],
                            number_of_falling=data['numberOfFalling']
                            , number_of_limit_up=data['numberOfLimitUp'],
                            number_of_limit_down=data['numberOfLimitDown'], explosion_rate=data['explosionRate'],
                            yesterday_limit_up=data['yesterdayLimitUp'],
                            yesterday_connecting_plate=data['yesterdayConnectingPlate'],
                            short_term_funds=data['shortTermFunds'],
                            overall_market_review=data['overallMarketReview'],
                            any_differences_sectors=data['anyDifferencesSectors'],
                            expected_leaders=data['expectedLeaders'],
                            record_date=datetime.strptime(data['recordDate'], "%Y-%m-%d"),
                            today_best_solution=data['todayBestSolution'],
                            mistakes_made_today=data['mistakesMadeToday'], user_id=data['userId'])
    diary = new_diary.to_dict()
    session.add(new_diary)
    session.commit()
    session.close()
    return jsonify(diary), 201


from model import Subject

#新增题材
@app.route('/addSubject', methods=['post'])
@cross_origin()
def get_subject_data():
    data = request.get_json()
    Session = sessionmaker(bind=engine)
    session = Session()
    new_Subject = Subject(core=data['core'], pioneer=data['pioneer'], middle_army=data['middleArmy'],
                          number_of_limit_up=data['numberOfLimitUp'], increase=data['increase'],
                          genre_trends=data['genreTrends']
                          , persistence=data['persistence'],
                          review_diary_id=data['reviewDiaryId'], subject_name=data['subjectName'])
    session.add(new_Subject)
    session.commit()
    subject = new_Subject.to_dict()
    session.close()
    return jsonify(subject), 201


from datetime import datetime


#获取所有复盘记录
@app.route('/get_diarys', methods=['post'])
@cross_origin()
def get_diarys():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        data = request.get_json()
        record = session.query(ReviewDiary).filter(ReviewDiary.user_id == data.get('userId')).all()
        events = []
        for r in record:
            events.append(r.to_dict())
        session.close()
        return jsonify(events)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


#获取单个复盘页面记录
@app.route('/get_diary', methods=['GET'])
@cross_origin()
def get_diary():
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            diary_id=request.args.get('id')
            record = session.query(ReviewDiary).get(diary_id)
            diary=record.to_dict()
            session.close()
            return jsonify(diary)
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500



#获取题材
@app.route('/get_subject', methods=['GET'])
@cross_origin()
def get_subject():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        review_diary_id = request.args.get('review_diary_id')

        if review_diary_id is not None:
            from sqlalchemy import cast, String
            query = session.query(Subject).filter(
                cast(Subject.review_diary_id, String) == review_diary_id).all()
        else:
            session.close()
            return jsonify({"error": str('查询id为空')}), 500
        subject=[]
        for r in query:
            subject.append(r.to_dict())
        session.close()
        return jsonify(subject)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

#编辑复盘
@app.route('/edit_diary', methods=['post'])
@cross_origin()
def edit_diary():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        data = request.get_json()
        id = data['id']
        if id is not None:
            from sqlalchemy import cast, String
            diary = session.query(ReviewDiary).filter(
                cast(ReviewDiary.id, String) == id).first()
        else:
            return jsonify({"error": str('查询id为空')}), 500

        diary.income = data['income']
        diary.market_trend = data['marketTrend']
        diary.market_increase = data['marketIncrease']
        diary.turnover = data['turnover']
        diary.number_of_rising = data['numberOfRising']
        diary.number_of_falling = data['numberOfFalling']
        diary.number_of_limit_up = data['numberOfLimitUp']
        diary.number_of_limit_down = data['numberOfLimitDown']
        diary.explosion_rate = data['explosionRate']
        diary.yesterday_limit_up = data['yesterdayLimitUp']
        diary.yesterday_connecting_plate = data['yesterdayConnectingPlate']
        diary.short_term_funds = data['shortTermFunds']
        diary.overall_market_review = data['overallMarketReview']
        diary.any_differences_sectors = data['anyDifferencesSectors']
        diary.expected_leaders = data['expectedLeaders']
        diary.today_best_solution = data['todayBestSolution']
        diary.mistakes_made_today = data['mistakesMadeToday']
        session.commit()
        diaryId = data['id']
        session.close()
        return jsonify({
            "message": "更新成功",
            "data": {
                "id": diaryId,
            }
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

#编辑题材
@app.route('/edit_subject', methods=['post'])
@cross_origin()
def edit_subject():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        data = request.get_json()
        id = data['id']

        if id is not None:
            from sqlalchemy import cast, String
            subject = session.query(Subject).filter(
                cast(Subject.id, String) == id).first()
        else:
            return jsonify({"error": str('查询id为空')}), 500

        subject.core = data['core']
        subject.pioneer = data['pioneer']
        subject.middle_army = data['middleArmy']
        subject.number_of_limit_up = data['numberOfLimitUp']
        subject.increase = data['increase']
        subject.genre_trends = data['genreTrends']
        subject.persistence = data['persistence']
        subject.pioneer = data['pioneer']
        subject.review_diary_id = data['reviewDiaryId']
        subject.subject_name = data['subjectName']
        session.commit()
        subjectId = subject.id
        session.close()
        return jsonify({
            "message": "更新成功",
            "data": {
                "id": subjectId
            }
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

#删除题材
@app.route('/delete_subject', methods=['delete'])
@cross_origin()
def delete_subject():
    id = request.json.get('id')
    if not id:
        return jsonify({"error": "缺少ID参数"}), 400
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        subject = session.query(Subject).get(id)
        if not subject:
            return jsonify({"error": f"ID {id} 不存在"}), 404
        session.delete(subject)
        session.commit()
        subjectId = subject.id
        session.close()
        return jsonify({
            "message": "已删除",
            "data": {
                "id": subjectId,
            }
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


from model import OperatePlan

#获取交易计划
@app.route('/getStockPlan', methods=['GET'])
@cross_origin()
def get_stock_plan():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        review_diary_id = request.args.get('review_diary_id')
        if review_diary_id is not None:
            from sqlalchemy import cast, String
            query = session.query(OperatePlan).filter(
                cast(OperatePlan.review_diary_id, String) == review_diary_id).all()
        else:
            session.close()
            return jsonify({"error": str('查询id为空')}), 500
        plan=[]
        for r in query:
            plan.append(r.to_dict())

        session.close()
        return jsonify(plan)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

#新增交易计划
@app.route('/addStockPlan', methods=['post'])
@cross_origin()
def add_stock_plan():
    data = request.get_json()
    Session = sessionmaker(bind=engine)
    session = Session()
    new_operatePlan = OperatePlan(stock_name=data['stockName'], expect_open=data['expectOpen'],
                                  operate_plan=data['operatePlan'],
                                  operate=data['operate'], review_diary_id=data['reviewDiaryId'],
                                  subject_name=data['subjectName'])

    session.add(new_operatePlan)
    session.commit()
    plan=new_operatePlan.to_dict()
    session.close()
    return jsonify(plan), 201

#编辑交易计划
@app.route('/editStockPlan', methods=['post'])
@cross_origin()
def edit_stock_plan():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        data = request.get_json()
        id = data['id']

        if id is not None:
            from sqlalchemy import cast, String
            operatePlan = session.query(OperatePlan).filter(
                cast(OperatePlan.id, String) == id).first()
        else:
            return jsonify({"error": str('查询id为空')}), 500
        operatePlan.stock_name = data['stockName']
        operatePlan.expect_open = data['expectOpen']
        operatePlan.operate_plan = data['operatePlan']
        operatePlan.operate = data['operate']
        operatePlan.review_diary_id = data['reviewDiaryId']
        operatePlan.subject_name = data['subjectName']
        session.commit()
        operatePlanId = operatePlan.id
        session.close()
        return jsonify({
            "message": "更新成功",
            "data": {
                "id": operatePlanId,
            }
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

#删除交易计划
@app.route('/deleteStockPlan', methods=['delete'])
@cross_origin()
def delete_stock_plan():
    id = request.json.get('id')
    if not id:
        return jsonify({"error": "缺少ID参数"}), 400
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        operatePlan = session.query(OperatePlan).get(id)
        if not operatePlan:
            return jsonify({"error": f"ID {id} 不存在"}), 404
        session.delete(operatePlan)
        session.commit()
        operatePlanId = operatePlan.id
        session.close()
        return jsonify({
            "message": "已删除",
            "data": {
                "id": operatePlanId,
            }
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


from model import User

#注册用户
import bcrypt
@app.route('/addUser', methods=['post'])
@cross_origin()
def add_user():
    data = request.get_json()
    Session = sessionmaker(bind=engine)
    session = Session()
    #检验是否已存在该用户名
    user = session.query(User).filter(
        data.get('userName') == User.user_name).all()
    if user:
        session.close()
        return jsonify({"message": "已存在该用户名！"}), 401

    frontend_hashed_pwd = data['password'].encode('utf-8')
    # 二次哈希（加盐）
    salt=bcrypt.gensalt(10)
    backend_hashed_pwd = bcrypt.hashpw(frontend_hashed_pwd,salt)
    new_user = User(user_name=data['userName'], password=backend_hashed_pwd,salt=salt)
    session.add(new_user)
    session.commit()
    user=new_user.to_dict()
    session.close()
    return jsonify(user), 201

#用户登录
@app.route('/login', methods=['post'])
@cross_origin()
def login():
    data = request.get_json()
    frontend_hashed_pwd = data['password'].encode('utf-8')  # 前端已加密的密码
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(
        User.user_name == data.get('userName')).first()
    if not user:
        session.close()
        return jsonify({"message": "用户不存在！"}), 401

    backend_hashed_pwd=user.password.encode('utf-8')
    # 验证哈希格式
    if not backend_hashed_pwd.startswith((b"$2a$", b"$2b$")):
        return "无效的哈希格式", 500
    # 验证密码
    backend_hashed_pwd = bcrypt.hashpw(frontend_hashed_pwd, user.salt.encode('utf-8'))
    checkPassword=bcrypt.checkpw(frontend_hashed_pwd, backend_hashed_pwd)
    if not checkPassword:
        session.close()
        return jsonify({"message": "密码错误"}), 401
    from jwt_token import generate_jwt_token
    token = generate_jwt_token(user.id)
    loginUser=user.to_dict()
    return jsonify({
        "message": "登录成功",
        "token": token,
        "userData": loginUser,
    })


if __name__ == '__main__':
    app.run()
