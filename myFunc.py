from datetime import datetime
import sqlite3

def convert_to_24_hour_format(time_str):

    dt = datetime.strptime(time_str, '%I:%M %p')
    return dt.strftime('%H:%M')

# True=時間通過
def check_time_order(start_time, end_time):
   
    start_datetime = datetime.strptime(start_time, '%I:%M %p')
    end_datetime = datetime.strptime(end_time, '%I:%M %p')

    # print(start_datetime < end_datetime)
    return start_datetime < end_datetime 

# True=可以使用的時間
def check_is_time_not_between( start_time, end_time, target_start, target_end):
    
    formatted_start_time = convert_to_24_hour_format(start_time)
    formatted_end_time = convert_to_24_hour_format(end_time)
    target_start_time = convert_to_24_hour_format(target_start)
    target_end_time = convert_to_24_hour_format(target_end)

    # true=可以使用的時間
    is_not_time_between = ((target_end_time<=formatted_start_time)or(target_start_time>=formatted_end_time))

    return is_not_time_between

#確認是否紀錄都可以使用
def check_all_records(my_event_date,new_start_time,new_end_time):

    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM event_schedule
        WHERE event_date = ?
    ''', (my_event_date,))

    records = cursor.fetchall()

    is_pass=True

    # 遍历每一行记录
    for record in records:

        # 在这里，你可以处理时间判别的逻辑
        print(record)
        start_time = record[3]  # 第四列是start_time
        end_time = record[4]    # 第五列是end_time

        is_time_not_between=check_is_time_not_between( start_time, end_time, new_start_time,new_end_time)
            
        if not is_time_not_between:
            is_pass=False
            break
        
    conn.close()

    return is_pass

my_event_date='2024-01-25'
new_start_time='3:00 PM'
new_end_time='3:30 PM'
# print([convert_to_24_hour_format(new_start_time),convert_to_24_hour_format(new_end_time)])
# print(check_time_order(new_start_time,new_end_time))
check_all_records(my_event_date,new_start_time,new_end_time)

if not check_all_records(my_event_date,new_start_time,new_end_time):
    print({'status': 'check_all_records_error'})