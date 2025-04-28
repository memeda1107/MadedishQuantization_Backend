import akshare as ak

import pandas as pd
from sqlalchemy import create_engine




stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600900", period="daily", start_date="20000101", end_date='20250327', adjust="qfq")
print(stock_zh_a_hist_df)

##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
yconnect = create_engine('mysql+pymysql://root:123456@localhost:3306/madedish_quantiza?charset=utf8')

stock_zh_a_hist_df.to_sql('history_market', yconnect, schema='madedish_quantiza', if_exists='replace', index=False)

# json_data=stock_zh_a_hist_df.to_json(orient = "records",force_ascii=False)

# print(json_data)
