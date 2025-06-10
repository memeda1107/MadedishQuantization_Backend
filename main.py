

from flask import Flask, jsonify,request
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

@app.route('/addDiary', methods=['post'])
@cross_origin()
def add_diary():
    data = request.get_json()  # 获取JSON格式的数据，也可以通过request.form获取表单数据。确保前端Content-Type设置正确。
    # 使用 sessionmaker 创建一个会话类 Session，并绑定到数据库引擎（bind=engine）
    Session = sessionmaker(bind=engine)
    # 创建一个实例化的会话对象 session
    session = Session()
    # 创建一个新的实例，即要插入到数据库中
    new_diary = ReviewDiary(income=data['income'], market_trend=data['marketTrend'],market_increase=data['marketIncrease'],
                            turnover=data['turnover'],number_of_rising=data['numberOfRising'],number_of_falling=data['numberOfFalling']
                            ,number_of_limit_up=data['numberOfLimitUp'],number_of_limit_down=data['numberOfLimitDown'],explosion_rate=data['explosionRate'],
                            yesterday_limit_up=data['yesterdayLimitUp'],yesterday_connecting_plate=data['yesterdayConnectingPlate'],short_term_funds=data['shortTermFunds'],
                            overall_market_review=data['overallMarketReview'],any_differences_sectors=data['anyDifferencesSectors'],expected_leaders=data['expectedLeaders'],record_date=data['recordDate'],
                            today_best_solution=data['todayBestSolution'],mistakes_made_today=data['mistakesMadeToday'])
    # 将新用户添加到会话中，即将其添加到数据库操作队列中
    session.add(new_diary)
    # 提交会话，将所有在此会话中的数据库操作提交到数据库
    session.commit()
    # return jsonify({'message': '新增成功！','id': format(new_diary.id)}), 201
    return jsonify(new_diary.to_dict()), 201



from model import Subject
@app.route('/addSubject', methods=['post'])
@cross_origin()
def get_Subject_data():
    data = request.get_json()  # 获取JSON格式的数据，也可以通过request.form获取表单数据。确保前端Content-Type设置正确。
    # 使用 sessionmaker 创建一个会话类 Session，并绑定到数据库引擎（bind=engine）
    Session = sessionmaker(bind=engine)
    # 创建一个实例化的会话对象 session
    session = Session()
    # 创建一个新的实例，即要插入到数据库中
    new_Subject = Subject(core=data['core'], pioneer=data['pioneer'],middle_army=data['middleArmy'],
                            number_of_limit_up=data['numberOfLimitUp'],increase=data['increase'],genre_trends=data['genreTrends']
                            ,persistence=data['persistence'],
                            review_diary_id=data['reviewDiaryId'],subject_name=data['subjectName'])
    # 将新用户添加到会话中，即将其添加到数据库操作队列中
    session.add(new_Subject)
    # 提交会话，将所有在此会话中的数据库操作提交到数据库
    session.commit()
    return jsonify(new_Subject.to_dict()), 201


from datetime import datetime
@app.route('/get_events', methods=['GET'])
@cross_origin()
def get_events():
    try:
        Session = sessionmaker(bind=engine)
        # 创建一个实例化的会话对象 session
        session = Session()
        # 获取时间范围参数
        start_str = request.args.get('start')
        end_str = request.args.get('end')

        # 转换为 datetime 对象
        start = datetime.fromisoformat(start_str.replace('Z', '+00:00')) if start_str else None
        end = datetime.fromisoformat(end_str.replace('Z', '+00:00')) if end_str else None

        # 查询数据库
        # 动态构建查询
        query = session.query(ReviewDiary).order_by(ReviewDiary.record_date)
        if start is not None:
            query = query.filter(ReviewDiary.record_date >= start)
        if end is not None:
            query = query.filter(ReviewDiary.record_date <= end)

        events = query.all()
        # 转换为 FullCalendar 格式
        return jsonify([event.to_dict() for event in events])

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/get_diary', methods=['GET'])
@cross_origin()
def get_diary():
        try:
            Session = sessionmaker(bind=engine)
            # 创建一个实例化的会话对象 session
            session = Session()
            id=request.args.get('id')
            record = session.query(ReviewDiary).get(id)
            return jsonify([record.to_dict()])

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500




@app.route('/get_subject', methods=['GET'])
@cross_origin()
def get_subject():
    try:
        Session = sessionmaker(bind=engine)
        # 创建一个实例化的会话对象 session
        session = Session()
        review_diary_id = request.args.get('review_diary_id')

        if review_diary_id is not None:
            from sqlalchemy import cast, String
            query = session.query(Subject).filter(
                cast(Subject.review_diary_id, String) == review_diary_id)
        else:
            return jsonify({"error": str('查询id为空')}), 500


        results = query.all()
        return jsonify([result.to_dict() for result in results])

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/edit_diary', methods=['post'])
@cross_origin()
def edit_diary():
    try:
        Session = sessionmaker(bind=engine)
        # 创建一个实例化的会话对象 session
        session = Session()
        # id = request.data.get('id')
        data = request.get_json()
        id=data['id']

        if id is not None:
            from sqlalchemy import cast, String
            diary = session.query(ReviewDiary).filter(
                cast(ReviewDiary.id, String) == id).first()
        else:
            return jsonify({"error": str('查询id为空')}), 500

        diary.income=data['income']
        diary.market_trend=data['marketTrend']
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
        # 执行更新操作
        session.commit()

        # 返回成功响应
        return jsonify({
            "message": "更新成功",
            "data": {
                "id": diary.id,
            }
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/edit_subject', methods=['post'])
@cross_origin()
def edit_subject():
        try:
            Session = sessionmaker(bind=engine)
            # 创建一个实例化的会话对象 session
            session = Session()
            # id = request.data.get('id')
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
            subject.subject_name=data['subjectName']

            # 执行更新操作
            session.commit()

            # 返回成功响应
            return jsonify({
                "message": "更新成功",
                "data": {
                    "id": subject.id,
                }
            }), 200

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500


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

        # 返回成功响应
        return jsonify({
            "message": "已删除",
            "data": {
                "id": subject.id,
            }
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

from model import OperatePlan
@app.route('/getStockPlan', methods=['GET'])
@cross_origin()
def get_stock_plan():
    try:
        Session = sessionmaker(bind=engine)
        # 创建一个实例化的会话对象 session
        session = Session()
        review_diary_id = request.args.get('review_diary_id')

        if review_diary_id is not None:
            from sqlalchemy import cast, String
            query = session.query(OperatePlan).filter(
                cast(OperatePlan.review_diary_id, String) == review_diary_id)
        else:
            return jsonify({"error": str('查询id为空')}), 500
        results = query.all()
        return jsonify([result.to_dict() for result in results])
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/addStockPlan', methods=['post'])
@cross_origin()
def add_stock_plan():
    data = request.get_json()  # 获取JSON格式的数据，也可以通过request.form获取表单数据。确保前端Content-Type设置正确。
    # 使用 sessionmaker 创建一个会话类 Session，并绑定到数据库引擎（bind=engine）
    Session = sessionmaker(bind=engine)
    # 创建一个实例化的会话对象 session
    session = Session()
    # 创建一个新的实例，即要插入到数据库中
    new_operatePlan = OperatePlan(stock_name=data['stockName'], expect_open=data['expectOpen'],operate_plan=data['operatePlan'],
                            operate=data['operate'],review_diary_id=data['reviewDiaryId'],subject_name=data['subjectName'])
    # 将新用户添加到会话中，即将其添加到数据库操作队列中
    session.add(new_operatePlan)
    # 提交会话，将所有在此会话中的数据库操作提交到数据库
    session.commit()
    return jsonify(new_operatePlan.to_dict()), 201


@app.route('/editStockPlan', methods=['post'])
@cross_origin()
def edit_stock_plan():
        try:
            Session = sessionmaker(bind=engine)
            # 创建一个实例化的会话对象 session
            session = Session()
            # id = request.data.get('id')
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
            operatePlan.subject_name=data['subjectName']

            # 执行更新操作
            session.commit()

            # 返回成功响应
            return jsonify({
                "message": "更新成功",
                "data": {
                    "id": operatePlan.id,
                }
            }), 200

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 500

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

        # 返回成功响应
        return jsonify({
            "message": "已删除",
            "data": {
                "id": operatePlan.id,
            }
        }), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run()


