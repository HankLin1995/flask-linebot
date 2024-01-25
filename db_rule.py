import sqlite3
from datetime import datetime

def get_event_details(event_name):
    # 连接到 SQLite 数据库文件
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    # 执行 SQL 查询
    cursor.execute('''
        SELECT *
        FROM event_schedule
        WHERE name = ?
    ''', (event_name,))

    # 获取查询结果
    event_details = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 返回事件的详细信息
    return event_details


def convert_to_sql_time(time_str):
    # 将时间字符串转换为 SQLite 支持的格式
    dt_obj = datetime.strptime(time_str, '%I:%M %p')
    return dt_obj.strftime('%H:%M')

def check_overlap(event_date, new_start_time, new_end_time):
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    # 将输入的时间转换为 SQLite 支持的格式
    start_time_sql = convert_to_sql_time(new_start_time)
    end_time_sql = convert_to_sql_time(new_end_time)

    cursor.execute('''
        SELECT COUNT(*)
        FROM event_schedule
        WHERE event_date = ? 
            AND (
                (start_time <= ? AND end_time >= ?)
                OR (start_time <= ? AND end_time >= ?)
                OR (start_time >= ? AND end_time <= ?)
            )
    ''', (event_date, start_time_sql, end_time_sql, start_time_sql, end_time_sql, start_time_sql, end_time_sql))

    overlap_count = cursor.fetchone()[0]

    conn.close()

    return overlap_count > 0

event_date = '2024-01-26'
new_start_time = '2:00 PM'
new_end_time = '4:00 PM'

overlap_result = check_overlap(event_date, new_start_time, new_end_time)

print(f'是否存在时间重叠: {overlap_result}')

event_name_to_print = 'Event3'
event3_details = get_event_details(event_name_to_print)
print(f'{event_name_to_print} 的详细信息: {event3_details}')
