from datetime import datetime
import sqlite3
import json
import sys

def display_all_records():
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM event_schedule
    ''')

    records = cursor.fetchall()

    # 将结果转换为 JSON 格式
    records_json = json.dumps(records, default=str, indent=2)
    
    print(records_json)

    conn.close()

    return(records_json)

display_all_records()

sys.exit()

def convert_to_24_hour_format(time_str):
    dt = datetime.strptime(time_str, '%I:%M %p')
    return dt.strftime('%H:%M')

# # 测试
# time1 = '12:30 PM'
# time2 = '02:00 PM'

# time1_24_hour = convert_to_24_hour_format(time1)
# time2_24_hour = convert_to_24_hour_format(time2)

# print(f'Time 1 (24小时制): {time1_24_hour}')
# print(f'Time 2 (24小时制): {time2_24_hour}')

# if time1_24_hour < time2_24_hour:
#     print(f'{time1} 在 {time2} 之前')
# else:
#     print(f'{time1} 在 {time2} 之后')

def fetch_all_matching_records_by_date(event_date):
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM event_schedule
        WHERE event_date = ?
    ''', (event_date,))

    matching_records = cursor.fetchall()

    conn.close()

    return matching_records

# 使用示例
# event_date = '2024-01-26'

# matching_records = fetch_all_matching_records_by_date(event_date)

# print(matching_records)

# for record in matching_records:
#     print(record)

# sys.exit() #程式執行停止

def insert_fake_data():
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    # 插入假数据
    cursor.execute('''
        INSERT INTO event_schedule (name, event_date, start_time, end_time, location, material_content)
        VALUES
        ('Event1', '2024-01-26', '10:00 AM', '12:00 PM', 'Location1', 'Material1'),
        ('Event2', '2024-01-26', '02:00 PM', '04:00 PM', 'Location2', 'Material2'),
        ('Event3', '2024-01-27', '09:00 AM', '11:00 AM', 'Location3', 'Material3')
    ''')

    conn.commit()
    conn.close()

# # 插入假数据
# insert_fake_data()
    
def fetch_data_for_date(date):
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM event_schedule
        WHERE event_date = ?
    ''', (date,))

    rows = cursor.fetchall()

    conn.close()

    return rows

# # 检索 2024-01-26 的数据
# result = fetch_data_for_date('2024-01-26')

# # 以24小时制呈现时间
# for row in result:
#     formatted_start_time = datetime.strptime(row[3], '%I:%M %p').strftime('%H:%M')
#     formatted_end_time = datetime.strptime(row[4], '%I:%M %p').strftime('%H:%M')
#     print(f"Event: {row[1]}, Date: {row[2]}, Start Time: {formatted_start_time}, End Time: {formatted_end_time}, Location: {row[5]}, Material Content: {row[6]}")

def update_location_by_id(record_id, new_location):
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE event_schedule
        SET location = ?
        WHERE id = ?
    ''', (new_location, record_id))

    conn.commit()
    conn.close()

# # 要更新的记录的 id 和新的 location
# record_id_to_update = 1
# new_location_value = "ABCD"

# # 执行更新
# update_location_by_id(record_id_to_update, new_location_value)
    
def display_all_records():
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM event_schedule
    ''')

    records = cursor.fetchall()

    # 输出所有记录
    for record in records:
        print(record)

    conn.close()

# # 调用函数以显示所有记录
# display_all_records()

def check_all_records(my_event_date,new_start_time,new_end_time):
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM event_schedule
        WHERE event_date = ?
    ''', (my_event_date,))

    records = cursor.fetchall()

    is_pass=False

    # 遍历每一行记录
    for record in records:

        # 在这里，你可以处理时间判别的逻辑
        print(record)
        start_time = record[3]  # 第四列是start_time
        end_time = record[4]    # 第五列是end_time

        # 调用你的判别逻辑函数，例如 check_time_overlap
        is_time_between=check_is_time_between( start_time, end_time, new_start_time,new_end_time)
            
        if is_time_between:
            is_pass=True
            break
    
    print(is_pass)
        
    conn.close()

# 检查时间重叠的逻辑函数
def check_is_time_between( start_time, end_time, target_start, target_end):
    # 将时间格式转为24小时制
    formatted_start_time = convert_to_24_hour_format(start_time)
    formatted_end_time = convert_to_24_hour_format(end_time)
    target_start_time = convert_to_24_hour_format(target_start)
    target_end_time = convert_to_24_hour_format(target_end)

    # 在这里添加你的实际时间重叠判别逻辑
    # 例如，如果存在时间重叠，返回 True；否则，返回 False
    is_not_time_between = (
        (target_end_time<=formatted_start_time)or(target_start_time>=formatted_end_time) #True=不重疊
    )

    if not is_not_time_between: #False=重疊
        print("Formatted Start Time:", formatted_start_time)
        print("Formatted End Time:", formatted_end_time)
        print("Target Start Time:", target_start_time)
        print("Target End Time:", target_end_time)
        print("時間有重疊跡象!")
        return True

    return False

# # 执行显示符合条件的记录
# my_event_date='2024-01-26'
# new_start_time='11:00 AM'
# new_end_time='12:30 PM'
# # print([convert_to_24_hour_format(new_start_time),convert_to_24_hour_format(new_end_time)])
# check_all_records(my_event_date,new_start_time,new_end_time)

def check_time_order(start_time, end_time):
    # 将字符串转换为 datetime 对象
    start_datetime = datetime.strptime(start_time, '%I:%M %p')
    end_datetime = datetime.strptime(end_time, '%I:%M %p')

    # 检查时间顺序
    print(start_datetime < end_datetime)
    return start_datetime < end_datetime

# 测试
start_time = '3:00 PM'
end_time = '12:01 PM'

if check_time_order(start_time, end_time):
    print("时间顺序正确")
else:
    print("时间顺序错误")