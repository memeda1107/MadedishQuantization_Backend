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
            "id": self.id,
            "title": self.income,
            "start": self.record_date.isoformat()if self.record_date else None,
            "description": self.market_trend
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
    date=Column(DateTime)
    review_diary_id=Column(Integer)



