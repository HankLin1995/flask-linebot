import sqlite3
import json

# 创建 SQLite 数据库表的函数
def create_table():
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            event_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            location TEXT NOT NULL,
            material_content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    

# 插入数据到 SQLite 数据库的函数
def insert_data(name, event_date, start_time, end_time, location, material_content):
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO event_schedule (name, event_date, start_time, end_time, location, material_content)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, event_date, start_time, end_time, location, material_content))

    conn.commit()
    conn.close()

def get_all_records():
    
    conn = sqlite3.connect('eng.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT *
        FROM event_schedule
    ''')

    records = cursor.fetchall()

    conn.close()

    # 将结果转换为 JSON 格式
    records_json = json.dumps(records, default=str, indent=2)

    # 返回 JSON 响应
    return records_json

