from sqlalchemy import Column, Integer, String, Sequence,Float,TEXT,Double,DateTime,Date
from sqlalchemy.ext.declarative import declarative_base

# 创建一个基类，用于定义数据模型的基本结构
Base = declarative_base()

# 定义一个数据模型类，对应数据库中的表
class ReviewDiary(Base):
    # 定义表名
    __tablename__ = 'review_diary'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    income=Column(Float(50))
    market_trend=Column(String(225))
    market_increase=Column(Float(50))
    turnover=Column(String(50))
    number_of_rising= Column(Integer)
    number_of_falling= Column(Integer)
    number_of_limit_up= Column(Integer)
    number_of_limit_down= Column(Integer)
    explosion_rate=Column(Float(50))
    yesterday_limit_up=Column(Float(50))
    yesterday_connecting_plate=Column(Float(50))
    short_term_funds=Column(Float(50))
    overall_market_review=Column(TEXT)
    any_differences_sectors=Column(TEXT)
    expected_leaders=Column(TEXT)
    today_best_solution=Column(TEXT)
    mistakes_made_today=Column(TEXT)
    record_date = Column(DateTime)

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": "收益："+str(self.income),
            # "title": "盈利" + self.income,
            "start": self.record_date.isoformat() if self.record_date else None,
            "end": self.record_date.isoformat() if self.record_date else None,
            # "description": self.market_trend
            "income":self.income,
            "marketTrend": self.market_trend,
            "marketIncrease": self.market_increase,
            "turnover": self.turnover,
            "numberOfRising": self.number_of_rising,
            "numberOfFalling": self.number_of_falling,
            "numberOfLimitUp": self.number_of_limit_up,
            "numberOfLimitDown": self.number_of_limit_down,
            "explosionRate": self.explosion_rate,
            "yesterdayLimitUp": self.yesterday_limit_up,
            "yesterdayConnectingPlate": self.yesterday_connecting_plate,
            "shortTermFunds": self.short_term_funds,
            "overallMarketReview": self.overall_market_review,
            "anyDifferencesSectors": self.any_differences_sectors,
            "expectedLeaders": self.expected_leaders,
            "todayBestSolution": self.today_best_solution,
            "mistakesMadeToday": self.mistakes_made_today,
            "recordDate":self.record_date,
        }


class Subject(Base):
    # 定义表名
    __tablename__ = 'subject_matter'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    core=Column(String(225))
    pioneer=Column(String(225))
    middle_army = Column(String(225))
    number_of_limit_up=Column(Double())
    increase=Column(Double())
    genre_trends=Column(String(225))
    persistence=Column(String(225))
    # date=Column(DateTime)
    review_diary_id=Column(Integer)
    subject_name=Column(String(225))

    def to_dict(self):
        return {
            "id": str(self.id),
            "core": self.core,
            "pioneer": self.pioneer,
            "middleArmy": self.middle_army,
            "numberOfLimitUp": self.number_of_limit_up,
            "increase": self.increase,
            "genreTrends": self.genre_trends,
            "persistence": self.persistence,
            "reviewDiaryId":self.review_diary_id,
            "subjectName":self.subject_name
        }

class OperatePlan(Base):
    # 定义表名
    __tablename__ = 'operate_plan'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    subject_name=Column(String(225))
    stock_name=Column(String(225))
    stock_code = Column(String(225))
    expect_open=Column(String(225))
    operate_plan=Column(String(225))
    # date=Column(DateTime)
    review_diary_id=Column(Integer)
    operate=Column(String(225))

    def to_dict(self):
        return {
            "id": str(self.id),
            "subjectName": self.subject_name,
            "stockName": self.stock_name,
            "stockCode": self.stock_code,
            "expectOpen": self.expect_open,
            "operatePlan": self.operate_plan,
            "reviewDiaryId":self.review_diary_id,
            "operate":self.operate
        }

