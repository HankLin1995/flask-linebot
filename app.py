from flask import Flask, render_template, request, jsonify
from database import create_table, insert_data,get_all_records
from myFunc import check_time_order,check_all_records

app = Flask(__name__)

# 设置装饰器以处理 CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'OPTIONS,HEAD,GET,POST,PUT,DELETE')
    return response

@app.route('/hello', methods=['GET'])
def download_excel():
    
    return 'hello'

# 首页路由
@app.route('/')
def index():
    return 'ok' #render_template('index.html')

# 提交表单的路由
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # 检查表是否存在，如果不存在就创建
    create_table()

    # 获取前端发送的 JSON 数据
    form_data = request.json

    f_event_date=form_data.get('event_date')
    f_start_time=form_data.get('startTime')
    f_end_time=form_data.get('endTime')

    #check if datetime pass
    if not check_time_order(f_start_time,f_end_time):
        return jsonify({'status': 'fail,time_order_error'})

    if not check_all_records(f_event_date,f_start_time,f_end_time):
        return jsonify({'status': 'check_all_records_error'})

    # 将数据插入到 SQLite 数据库
    insert_data(
        form_data.get('name'),
        form_data.get('event_date'), #申請日期
        form_data.get('startTime'),
        form_data.get('endTime'),
        form_data.get('location'),
        form_data.get('materialContent')
    )

    # 返回 JSON 响应
    return jsonify({'status': 'success'})

@app.route('/fetch_all')
def fetch_all():
    return jsonify(get_all_records())


if __name__ == '__main__':
    app.run(debug=True)