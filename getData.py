

from flask import Flask, jsonify
import akshare as ak
from flask_cors import cross_origin
import pandas as pd



stock_zh_a_spot_em_df = ak.stock_zh_a_hist(symbol="399001", period="daily", start_date="20250301", end_date='20250412', adjust="")
print(stock_zh_a_spot_em_df)

#dataframe转为json,指定 JSON 格式结构，支持 split、records、index、columns、values

json_data=stock_zh_a_spot_em_df.to_json(orient = "records",force_ascii=False)

print(json_data)

app = Flask(__name__)

@app.route('/api/kline-data', methods=['GET'])
@cross_origin()
def get_data():
    return json_data




if __name__ == '__main__':
    app.run()
